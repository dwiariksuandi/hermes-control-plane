# Secret Encryption Hardening SOP

**Purpose:** Secure sensitive backup files at-rest using `age` (X25519-ChaCha20-Poly1305) to ensure zero plaintext leakage, even in private storage/multicloud.

## 1. Asset Inventory

The following files contain sensitive credentials and must be encrypted before backup:
- `~/.hermes/.env` (API keys, secrets)
- `~/.hermes/auth.json` (OAuth tokens, pooled credentials)
- `~/.hermes/state.db` (Session transcripts, may contain leaked secrets)

## 2. Key Generation & Storage

- Keys must be generated once and stored in a highly restrictive directory.
- Keys are **never** included in backups. The user provides the private key manually during disaster recovery.

```bash
# Install age (if not available)
curl -sLo /tmp/age.tar.gz https://github.com/FiloSottile/age/releases/download/v1.2.1/age-v1.2.1-linux-amd64.tar.gz
tar -xzf /tmp/age.tar.gz -C /tmp
mv /tmp/age/age /home/hiryu/.local/bin/age
mv /tmp/age/age-keygen /home/hiryu/.local/bin/age-keygen
chmod +x /home/hiryu/.local/bin/age /home/hiryu/.local/bin/age-keygen

# Setup restrictive directory
mkdir -p ~/.hermes/hermes_keys && chmod 700 ~/.hermes/hermes_keys

# Generate keypair
age-keygen -o ~/.hermes/hermes_keys/hermes-backup.key
chmod 600 ~/.hermes/hermes_keys/hermes-backup.key
```

## 3. Encryption Pipeline

Before archival/backup, encrypt target files to a staging directory.

**Critical: Live Database Handling**
`state.db` is a live SQLite database with active WAL writes. Directly encrypting a live DB file causes checksum mismatches because the file changes between encryption and verification.

**Solution: Create a consistent snapshot first using SQLite `.backup` API:**

```python
import sqlite3

def snapshot_db(live_path, snapshot_path):
    """Create a consistent snapshot of a live SQLite database."""
    con = sqlite3.connect(live_path)
    bck = sqlite3.connect(snapshot_path)
    with bck:
        con.backup(bck)
    bck.close()
    con.close()
```

Then encrypt the snapshot, not the live file.

**Extracting Public Key from Private Key:**
```bash
age-keygen -y ~/.hermes/hermes_keys/hermes-backup.key
```

**Encryption Commands:**
```bash
PUBKEY="age1..." # Extracted above
ENCDIR=~/.hermes/hermes_keys/encrypted
mkdir -p "$ENCDIR" && chmod 700 "$ENCDIR"

# Static files — encrypt directly
age -r "$PUBKEY" -o "$ENCDIR/.env.age" ~/.hermes/.env
age -r "$PUBKEY" -o "$ENCDIR/auth.json.age" ~/.hermes/auth.json

# Live DB — snapshot first, then encrypt
python3 -c "
import sqlite3
con = sqlite3.connect('/home/hiryu/.hermes/state.db')
bck = sqlite3.connect('/tmp/state.db.snap')
with bck: con.backup(bck)
bck.close(); con.close()
"
age -r "$PUBKEY" -o "$ENCDIR/state.db.age" /tmp/state.db.snap
rm /tmp/state.db.snap
```

## 4. Verification Scripts

See `references/phase5_3_4_verify_v2.py` for the full snapshot-based roundtrip verification script.

Quick roundtrip proof:
```bash
# Decrypt
age -d -i ~/.hermes/hermes_keys/hermes-backup.key -o /tmp/test.env ~/.hermes/hermes_keys/encrypted/.env.age

# Checksum validation
sha256sum ~/.hermes/.env /tmp/test.env
```

**For state.db snapshot roundtrip proof:**
```bash
# Create fresh snapshot
python3 -c "
import sqlite3
con = sqlite3.connect('/home/hiryu/.hermes/state.db')
bck = sqlite3.connect('/tmp/state.db.snap')
with bck: con.backup(bck)
bck.close(); con.close()
"

# Encrypt snapshot
age -r "$PUBKEY" -o /tmp/state.db.age /tmp/state.db.snap

# Decrypt
age -d -i ~/.hermes/hermes_keys/hermes-backup.key -o /tmp/state.db.dec /tmp/state.db.age

# Compare
sha256sum /tmp/state.db.snap /tmp/state.db.dec
```

## 5. Backup Pipeline Integration

When integrating into `hermes_backup_master.py`:

1. After the copy loop, add an encryption step (Step 1.5)
2. Encrypt secrets before manifest writing
3. **Remove plaintext secrets from staging after encryption** (secure `unlink`)
4. Exclude `hermes_keys/` from the backup items list (keys must not leak into archives)
5. Set `chmod 600` on all `.age` files and `chmod 700` on the encrypted directory
6. For `state.db`: snapshot → encrypt → delete snapshot from staging
7. The staging directory containing plaintext is cleaned up naturally at end of script

**Anti-patterns:**
- ✗ Encrypting live `state.db` without snapshot
- ✗ Including `hermes_keys/` directory in backup archives
- ✗ Leaving plaintext copies in staging after encryption
- ✗ Setting permissive permissions (>600) on encrypted files

## 6. Disaster Recovery Considerations

- Private key is **not** in backups — it must be provided by the user during recovery
- Recovery procedure: obtain key → place in `~/.hermes/hermes_keys/hermes-backup.key` → decrypt → restore
- Document key storage location (e.g., separate encrypted USB, password manager export)
- Key rotation: generate new key periodically or after any suspected compromise

## 7. Security Invariants

- **Law 6 (Preservation):** Never encrypt-in-place destructively. Always encrypt to a separate staging path (`*.age`).
- **Law 12 (Secrets):** Never echo private keys or file contents to stdout.
- **Verification:** Always prove the encryption roundtrip (encrypt → decrypt → sha256 match) before relying on it in production.
- **Permissions:** Private key `600`, key directory `700`, encrypted files `600`.
- **Key exclusion:** `hermes_keys/` must be in `EXCLUDE_PATTERNS` for all backup scripts.