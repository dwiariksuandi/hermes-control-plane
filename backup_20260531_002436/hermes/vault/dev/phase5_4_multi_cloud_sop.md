# SOP Phase 5.4: Multi-Cloud Replication with Rclone (Google Drive)

**Tanggal:** 2026-05-30
**Versi:** 1.0
**Status:** Final
**Penulis:** Hermes Orchestrator
**Reviewer:** dwiariksuandi

## 1. Tujuan
Membangun pipeline replikasi backup Hermes Control Plane ke Google Drive menggunakan `rclone`, memastikan data terenkripsi (`.age`) direplikasi secara andal dan terverifikasi, sebagai bagian dari strategi hardening Phase 5.

## 2. Lingkup
Meliputi instalasi `rclone`, konfigurasi remote Google Drive, integrasi ke script backup master (`hermes_backup_master.py`), dan verifikasi end-to-end. Fokus pada replikasi data terenkripsi dan manifest backup.

## 3. Prasyarat
- `age` dan `age-keygen` terinstal di `/home/hiryu/.local/bin/`.
- Private key `hermes-backup.key` tersedia di `/home/hiryu/.hermes/hermes_keys/`.
- Akun Google Drive aktif dan terotorisasi untuk `rclone`.
- Script `hermes_backup_master.py` sudah di-patch dengan fitur enkripsi dan `--sync-rclone` flag.
- Direktori backup lokal: `/home/hiryu/hermes-control-plane-backup/`.
- Google Drive folder ID target: `1pWdcLhq0h7GHXQPrUFxPSwN8S_AuPXxY` (`Hermes-Backup`).

## 4. Prosedur

### 4.1. Instalasi Rclone (Non-root)
1. **Unduh Rclone:**
   ```bash
   curl -sL https://downloads.rclone.org/rclone-current-linux-amd64.zip -o /tmp/rclone.zip
   ```
2. **Ekstrak & Pindahkan:**
   ```bash
   cd /tmp && unzip -q rclone.zip
   find /tmp -name 'rclone' -type f -executable -exec cp {} /home/hiryu/.local/bin/rclone \;
   ```
3. **Set Izin Eksekusi:**
   ```bash
   chmod +x /home/hiryu/.local/bin/rclone
   ```
4. **Verifikasi Instalasi:**
   ```bash
   /home/hiryu/.local/bin/rclone version
   ```
   (Output harus menampilkan versi `rclone`.)

### 4.2. Konfigurasi Rclone Google Drive Remote (Interaktif)
1. Jalankan konfigurasi interaktif:
   ```bash
   /home/hiryu/.local/bin/rclone config
   ```
   - Pilih `n` untuk `New remote`.
   - Beri nama remote, contoh: `gdrive2`.
   - Pilih tipe storage `drive` (biasanya opsi `15` atau sesuai daftar).
   - Biarkan `client_id` dan `client_secret` kosong (tekan Enter).
   - Pilih `N` untuk `Auto config`.
   - Di prompt browser: `y` (jika OS VM memiliki browser) atau `n` (jika headless).
     - Jika `n`, akan diberikan link untuk otorisasi di browser lokal Anda.
   - Setelah otorisasi, token akan tersimpan di `~/.config/rclone/rclone.conf`.

### 4.3. Integrasi ke Script Backup Master (`hermes_backup_master.py`)
1. **Backup script asli:**
   ```bash
   cp /home/hiryu/.hermes/scripts/hermes_backup_master.py /home/hiryu/.hermes/scripts/hermes_backup_master.py.bak.pre_rclone_integrate
   ```
2. **Patch script:** (sudah dilakukan otomatis oleh Hermes)
   - Menambahkan flag `--sync-rclone` untuk mengaktifkan sinkronisasi.
   - Menambahkan blok kode `rclone copy` ke Google Drive remote `gdrive2` setelah proses git commit.
   - Memastikan `drive-root-folder-id` disetel ke `1pWdcLhq0h7GHXQPrUFxPSwN8S_AuPXxY`.
   - Konfigurasi `rclone` menggunakan `drive-chunk-size`, `transfers`, `checkers`, `retries` untuk optimasi dan ketahanan.
   - Logging detail ke `/home/hiryu/.hermes/vault/dev/logs/rclone_sync_full_<TIMESTAMP>.log`.

### 4.4. Eksekusi & Verifikasi Pipeline End-to-End
1. **Jalankan backup dengan sinkronisasi:**
   ```bash
   python3 /home/hiryu/.hermes/scripts/hermes_backup_master.py --sync-rclone [--push]
   ```
   - Opsional `--push` jika ingin langsung push ke GitHub.
   - Proses ini akan melakukan backup lokal, enkripsi secret, git commit, dan replikasi rclone.

2. **Verifikasi Log Rclone:**
   Cek file log `/home/hiryu/.hermes/vault/dev/logs/rclone_sync_full_<TIMESTAMP>.log` untuk memastikan status `Transferred: 100%`.
   ```bash
   tail -n 20 /home/hiryu/.hermes/vault/dev/logs/rclone_sync_full_<TIMESTAMP>.log
   ```

3. **Verifikasi Integritas Remote (jumlah & ukuran file):**
   - Dapatkan jumlah dan ukuran file lokal:
     ```bash
     find /home/hiryu/hermes-control-plane-backup/backup_<TIMESTAMP> -type f | wc -l
     du -bhs /home/hiryu/hermes-control-plane-backup/backup_<TIMESTAMP> | awk '{print $1}'
     ```
   - Dapatkan jumlah dan ukuran file remote:
     ```bash
     /home/hiryu/.local/bin/rclone ls gdrive2:backup_<TIMESTAMP> --drive-root-folder-id 1pWdcLhq0h7GHXQPrUFxPSwN8S_AuPXxY | awk '{s+=$1} END{print NR " files, " s " bytes"}'
     ```
   - Pastikan angka file dan total bytes sama antara lokal dan remote.

## 5. Pemeliharaan
- Secara berkala cek file `rclone_sync_full_<TIMESTAMP>.log` untuk setiap backup.
- Pastikan token OAuth `rclone` tetap valid. Jika ada masalah otorisasi, jalankan `rclone config reconnect gdrive2:` lagi.

## 6. Risko & Mitigasi
- **Risiko:** Gagal sinkronisasi karena timeout/rate limit Google Drive.
  - **Mitigasi:** `rclone` dikonfigurasi dengan `retries` dan `retries-sleep` yang agresif. Log file menyediakan jejak audit.
- **Risiko:** Token OAuth kadaluarsa.
  - **Mitigasi:** Jalankan ulang proses `rclone config reconnect` secara manual jika terjadi. Dapat diotomasi lebih lanjut dengan flow refresh token.
- **Risiko:** Kebocoran secret.
  - **Mitigasi:** Semua secret sensitif dienkripsi dengan `age` sebelum replikasi. Private key `age` tidak ikut direplikasi.

## 7. Catatan
- `--drive-root-folder-id` sangat penting untuk memastikan replikasi di dalam folder yang benar, bukan root Drive.
- `rclone copy` akan menyalin hanya file yang berubah atau belum ada, sehingga efisien untuk incremental backup.
