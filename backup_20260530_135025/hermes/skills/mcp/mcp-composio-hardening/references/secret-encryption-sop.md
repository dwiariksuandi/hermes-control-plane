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
# Setup restrictive directory
mkdir -p ~/.hermes/hermes_keys && chmod 700 ~/.hermes/hermes_keys

# Generate keypair
age-keygen -o ~/.hermes/hermes_keys/hermes-backup.key
chmod 600 ~/.hermes/hermes_keys/hermes-backup.key
```

## 3. Encryption Pipeline
Before archival/backup, encrypt target files to a staging directory.

```bash
PUBKEY="age1..." # Extract from hermes-backup.key
mkdir -p ~/.hermes/hermes_keys/encrypted && chmod 700 ~/.hermes/hermes_keys/encrypted

# Example encryption loop
for src in ".env" "auth.json" "state.db"; do
    age -r "$PUBKEY" -o "~/.hermes/hermes_keys/encrypted/${src}.age" "~/.hermes/${src}"
done
```

## 4. Decryption Verification (Roundtrip Proof)
To ensure backups are viable, verify decryption and checksums locally:

```bash
# Decrypt
age -d -i ~/.hermes/hermes_keys/hermes-backup.key -o /tmp/test.env ~/.hermes/hermes_keys/encrypted/.env.age

# Checksum validation
sha256sum ~/.hermes/.env /tmp/test.env
```

## 5. Security Invariants
- **Law 6 (Preservation):** Never encrypt-in-place destructively. Always encrypt to a separate staging path (`*.age`).
- **Law 12 (Secrets):** Never echo private keys or file contents to stdout.
- **Verification:** Always prove the encryption roundtrip (encrypt -> decrypt -> diff checksum) before relying on it in production backup scripts.