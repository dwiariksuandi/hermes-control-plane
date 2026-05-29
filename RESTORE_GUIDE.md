# 🔄 HERMES CONTROL PLANE - PANDUAN RESTORE LENGKAP

> **Tujuan:** Dokumen ini adalah panduan definitive untuk merestore sistem Hermes Agent ke kondisi 100% identik dengan setup terakhir yang telah dibangun.
> 
> **Versi:** 1.0.0  
> **Terakhir Update:** 2026-05-29  
> **Target State:** Hermes Agent v0.15.0 + Composio MCP + Custom Config

---

## 📋 DAFTAR ISI

1. [Prerequisites (Persiapan Awal)](#1-prerequisites)
2. [Pre-Restore Checklist](#2-pre-restore-checklist)
3. [Proses Restore (Step-by-Step)](#3-proses-restore)
4. [Post-Restore Verification](#4-post-restore-verification)
5. [Troubleshooting](#5-troubleshooting)
6. [Referensi Cepat](#6-referensi-cepat)

---

## 1. PREREQUISITES

### 1.1 Hardware Requirements
```
OS:        Linux (Debian/Ubuntu preferred) atau WSL2
RAM:       Minimum 4GB (8GB+ direkomendasikan)
Disk:      Minimum 10GB free space
Network:   Koneksi internet stabil
```

### 1.2 Software yang Harus Diinstall SEBELUM Restore

| Software | Versi Min | Cara Install | Kegunaan |
|----------|-----------|--------------|----------|
| **Git** | 2.30+ | `sudo apt install git` | Clone repo backup |
| **curl** | 7.68+ | `sudo apt install curl` | Download Hermes installer |
| **Node.js** | 18+ | `sudo apt install nodejs npm` | MCP servers (filesystem, github) |
| **Python** | 3.10+ | `sudo apt install python3 python3-pip python3-venv` | Composio venv & Hermes core |
| **uv** | 0.11+ | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | Fast Python package manager (alternatif pip) |
| **sudo** | any | Pre-installed | Install system packages |

**Install semua prerequisites:**
```bash
sudo apt-get update
sudo apt-get install -y git curl unzip nodejs npm python3-pip python3-venv build-essential

# Install uv (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # atau restart terminal
```

### 1.3 Credentials yang Harus Disiapkan

| Credential | Format | Dapatkan Dari |
|------------|--------|---------------|
| **COMPOSIO_API_KEY** | `ak_...` | Dashboard Composio (https://app.composio.dev) |
| **GITHUB_TOKEN** | `ghp_...` | GitHub Settings > Developer Settings > Personal Access Tokens |

> ⚠️ **PENTING:** Simpan credential ini di tempat aman (password manager). JANGAN simpan di file teks biasa.

---

## 2. PRE-RESTORE CHECKLIST

Sebelum menjalankan restore, pastikan:

- [ ] **OS baru/fresh install** (atau VPS baru)
- [ ] **User account sudah dibuat** (contoh: `hiryu`)
- [ ] **Internet connectivity OK** (`ping google.com`)
- [ ] **Prerequisites terinstall** (lihat bagian 1.2)
- [ ] **Credentials tersedia** (COMPOSIO_API_KEY & GITHUB_TOKEN)
- [ ] **Repo backup sudah dikloning** (atau tersedia di media transfer)

---

## 3. PROSES RESTORE

### 3.1 Clone Repository Backup

```bash
# Buat direktori kerja
mkdir -p ~/projects && cd ~/projects

# Clone repo backup
git clone https://github.com/dwiariksuandi/hermes-control-plane.git
cd hermes-control-plane

# Atau jika repo sudah di-rename:
# git clone https://github.com/dwiariksuandi/hermes-control-plane-backup.git
```

### 3.2 Set Environment Variables

```bash
# Export credential sebagai environment variable
export COMPOSIO_API_KEY="ak_Cz6JevAJUymAxsi70CEk"  # GANTI dengan key Anda
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"       # GANTI dengan token Anda

# Verifikasi
echo "Composio key set: ${COMPOSIO_API_KEY:0:10}..."
echo "GitHub token set: ${GITHUB_TOKEN:0:10}..."
```

> 💡 **Tips:** Agar tidak perlu export setiap kali, tambahkan ke `~/.bashrc` atau `~/.profile`.

### 3.3 Jalankan Restore Script

```bash
# Berikan permission execute
chmod +x scripts/*.sh

# Jalankan restore utama
bash scripts/restore.sh
```

**Apa yang dilakukan `restore.sh`:**
1. **Install system packages** (dari `dependencies/apt-packages.txt`)
2. **Install Hermes Agent** (via official installer)
3. **Install Composio SDK** ke venv terisolasi
4. **Restore config files** ke `~/.hermes/`
5. **Setup shell configs** (`.bashrc`, `.profile`)

### 3.4 Restart Terminal Session

```bash
# Reload environment
source ~/.bashrc

# Verifikasi Hermes tersedia
which hermes
hermes --version
```

---

## 4. POST-RESTORE VERIFICATION

### 4.1 Verifikasi Hermes Agent

```bash
# 1. Check Hermes version
hermes --version
# Expected: Hermes Agent v0.15.0+

# 2. Check MCP servers
hermes mcp list
# Expected: time, filesystem, github, composio (all enabled)

# 3. Check config loaded
grep "composio:" ~/.hermes/config.yaml
# Expected: Shows composio MCP server entry
```

### 4.2 Verifikasi Composio Integration

```bash
# 1. Check Composio venv exists
ls -la ~/.hermes/mcp_servers/composio/venv/bin/python

# 2. Test Composio MCP server directly
~/.hermes/mcp_servers/composio/venv/bin/python \
  ~/.hermes/mcp_servers/composio/run_server.py --help
# Expected: Shows server startup (or usage info)

# 3. Verify tools available in Hermes
# Start interactive session dan coba panggil:
# "/tools" untuk melihat semua tools yang terdaftar
```

### 4.3 Verifikasi Toolsets

| Toolset | Status | Command Test |
|---------|--------|--------------|
| `terminal` | ✅ Required | `hermes chat -q "run ls -la"` |
| `file` | ✅ Required | `hermes chat -q "read ~/.hermes/config.yaml"` |
| `mcp_time_*` | ✅ Native MCP | `hermes chat -q "what time is it"` |
| `mcp_filesystem_*` | ✅ Native MCP | `hermes chat -q "list vault directory"` |
| `mcp_github_*` | ✅ Native MCP | `hermes chat -q "list my github repos"` |
| `mcp_composio_*` | ✅ Composio MCP | `hermes chat -q "list available composio tools"` |

### 4.4 Verifikasi Security Config

```bash
# Check redaction enabled
grep "redact_secrets" ~/.hermes/config.yaml
# Expected: redact_secrets: true

# Check approval mode
grep "mode:" ~/.hermes/config.yaml | head -1
# Expected: mode: smart (or manual)
```

---

## 5. TROUBLESHOOTING

### 5.1 Common Issues

#### Issue: `hermes: command not found`
**Cause:** PATH belum terupdate  
**Fix:**
```bash
source ~/.bashrc
# atau
export PATH="$HOME/.local/bin:$PATH"
```

#### Issue: `COMPOSIO_API_KEY not provided`
**Cause:** Environment variable belum di-export  
**Fix:**
```bash
export COMPOSIO_API_KEY="ak_Cz6JevAJUymAxsi70CEk"
# Tambahkan ke ~/.bashrc untuk persistensi
```

#### Issue: MCP server `composio` not found
**Cause:** Config belum reload atau server belum start  
**Fix:**
```bash
# Restart Hermes atau reload MCP
hermes mcp reload
# atau
hermes chat -q "/reload-mcp"
```

#### Issue: Permission denied saat install
**Cause:** User tidak punya sudo access  
**Fix:**
```bash
# Tambahkan user ke sudoers
sudo usermod -aG sudo $USER
# Logout dan login ulang
```

### 5.2 Recovery Commands

```bash
# Reset Hermes config ke default (HATI-HATI!)
mv ~/.hermes/config.yaml ~/.hermes/config.yaml.bak.$(date +%Y%m%d)
cp configs/hermes/config.yaml ~/.hermes/config.yaml

# Rebuild Composio venv (jika corrupt)
rm -rf ~/.hermes/mcp_servers/composio/venv
bash scripts/00_install_deps.sh

# Full reset (ulang dari awal)
rm -rf ~/.hermes
bash scripts/restore.sh
```

---

## 6. REFERENSI CEPAT

### 6.1 Struktur File Pasca-Restore

```
~/.hermes/
├── config.yaml              # Config utama (sanitized)
├── mcp_servers/
│   └── composio/
│       ├── venv/            # Python venv untuk Composio
│       └── run_server.py    # Launcher script
├── skills/                  # Skills yang terinstall
├── sessions/                # Session history
└── logs/                    # Log files

~/hermes-control-plane-backup/  (atau nama repo yang di-clone)
├── configs/
│   ├── hermes/
│   │   ├── config.yaml
│   │   └── mcp_servers/composio/run_server.py
│   └── shell/
│       ├── .bashrc
│       └── .profile
├── dependencies/
│   ├── apt-packages.txt
│   └── hermes-pip-requirements.txt
├── scripts/
│   ├── 00_install_deps.sh
│   ├── 01_restore_configs.sh
│   └── restore.sh
├── README.md
└── RESTORE_GUIDE.md         # File ini
```

### 6.2 Key Environment Variables

| Variable | Value | Diset Di |
|----------|-------|----------|
| `COMPOSIO_API_KEY` | `ak_Cz6JevAJUymAxsi70CEk` | `~/.bashrc` atau inline |
| `GITHUB_TOKEN` | `ghp_...` | `~/.bashrc` atau inline |
| `HERMES_HOME` | `~/.hermes` | Auto-set |
| `PATH` | Include `~/.local/bin` | `~/.bashrc` |

### 6.3 One-Liner Commands

```bash
# Full restore (setelah clone repo)
export COMPOSIO_API_KEY="ak_..." && export GITHUB_TOKEN="ghp_..." && bash scripts/restore.sh

# Quick Hermes start
hermes chat -q "status check"

# Update Hermes
hermes update

# Check all MCP servers
hermes mcp list

# View logs
tail -f ~/.hermes/logs/agent.log
```

---

## 7. KONTAK & SUPPORT

Jika mengalami masalah:
1. Cek log: `~/.hermes/logs/agent.log`
2. Restart Hermes: `hermes chat -q "/restart"`
3. Referensi docs: https://hermes-agent.nousresearch.com/docs/
4. Composio docs: https://docs.composio.dev

---

> **Catatan:** Simpan panduan ini bersama repo backup. Update jika ada perubahan konfigurasi signifikan.

*Dokumen ini digenerate otomatis oleh Hermes Agent pada 2026-05-29.*
