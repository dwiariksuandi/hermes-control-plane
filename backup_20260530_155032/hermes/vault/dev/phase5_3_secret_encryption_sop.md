# Phase 5.3 — Secret Encryption Hardening SOP

Tanggal: 2026-05-30
Owner: Hermes Orchestrator
Status: PASS

## Tujuan
Melindungi rahasia Hermes at-rest dan di backup repo.

## Scope Rahasia
- /home/hiryu/.hermes/.env
- /home/hiryu/.hermes/auth.json
- /home/hiryu/.hermes/state.db

## Arsitektur Keamanan
1. Key utama disimpan lokal saja:
   - /home/hiryu/.hermes/hermes_keys/hermes-backup.key
   - Permission: 600
2. Artefak backup menyimpan hanya file terenkripsi:
   - hermes/encrypted_secrets/.env.age
   - hermes/encrypted_secrets/auth.json.age
   - hermes/encrypted_secrets/state.db.age
3. Key directory tidak ikut backup:
   - EXCLUDE_PATTERNS memuat `hermes_keys/`

## Eksekusi yang sudah diverifikasi
1. Generate key age
2. Encrypt .env + auth.json
3. Encrypt state.db via SQLite snapshot (bukan live DB)
4. Set permission 600 untuk setiap *.age
5. Integrasi ke backup pipeline:
   - /home/hiryu/.hermes/scripts/hermes_backup_master.py
6. Jalankan backup real dan verifikasi hasil di repo backup

## Bukti
- Backup ID: 20260530_135025
- Manifest: /home/hiryu/.hermes/vault/dev/backup-manifests/manifest_20260530_135025.json
- Git commit: aa57fd2
- Encrypted files present + mode 600:
  - /home/hiryu/hermes-control-plane-backup/backup_20260530_135025/hermes/encrypted_secrets/.env.age
  - /home/hiryu/hermes-control-plane-backup/backup_20260530_135025/hermes/encrypted_secrets/auth.json.age
  - /home/hiryu/hermes-control-plane-backup/backup_20260530_135025/hermes/encrypted_secrets/state.db.age

## Restore SOP (ringkas)
1. Siapkan hermes-backup.key di host target (permission 600)
2. Decrypt file:
   - age -d -i hermes-backup.key -o .env .env.age
   - age -d -i hermes-backup.key -o auth.json auth.json.age
   - age -d -i hermes-backup.key -o state.db state.db.age
3. Validasi checksum bila tersedia
4. Start Hermes dan uji healthcheck

## Catatan Cerdas
- state.db live berubah cepat (WAL churn), verifikasi harus berbasis snapshot konsisten.
- Jangan pernah commit private key ke repo.
- Untuk rotasi key: re-encrypt semua artefak backup aktif.

## Next Gate
Lanjut Phase 5.4: Multi-cloud replication + integrity check matrix.