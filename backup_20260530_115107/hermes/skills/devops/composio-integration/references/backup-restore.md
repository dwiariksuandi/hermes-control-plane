---
name: hermes-control-plane-backup
description: "One-click backup and restore pattern for Hermes Agent + Composio integration"
category: devops
---

# Hermes Control Plane Backup & Restore

This skill provides a comprehensive backup and restore system for the entire Hermes Agent + Composio MCP integration, ensuring disaster recovery capability and easy migration.

## When to Use This Skill

Use this skill when you need to:
- Backup the entire Hermes Agent configuration and Composio integration
- Restore from backup on a new server or after catastrophic failure
- Ensure disaster recovery capability for production deployments
- Migrate to new infrastructure without losing configuration state
- Document infrastructure state for reproducibility

## Key Benefits

- **One-Click Restore**: Single script restores entire environment
- **Disaster Recovery**: Complete system state preserved in GitHub
- **Security**: API keys are never stored in backup; restored from environment
- **Isolation**: Backup includes only configuration, not runtime state
- **Reproducibility**: Identical system state across deployments

## Architecture

```
hermes-control-plane/
├── configs/hermes/                    # Configuration files
│   ├── config.yaml                    # Main Hermes config (sanitized)
│   └── mcp_servers/composio/run_server.py  # Composio MCP launcher
├── dependencies/                      # System dependencies
│   ├── apt-packages.txt              # System packages (apt)
│   └── hermes-pip-requirements.txt  # Python packages (pip)
├── scripts/                          # Automation scripts
│   ├── 00_install_deps.sh           # Install dependencies
│   ├── 01_restore_configs.sh        # Restore configuration
│   └── restore.sh                   # Master restore script
└── README.md                         # Documentation
```

## Installation & Setup

### 1. Create Backup Structure

```bash
# Create backup directory
mkdir -p /home/hiryu/hermes-control-plane-backup/{configs/hermes/mcp_servers/composio,dependencies,scripts,configs/shell}

# Copy current configuration (sanitized)
cp ~/.hermes/config.yaml /home/hiryu/hermes-control-plane-backup/configs/hermes/config.yaml
cp ~/.hermes/mcp_servers/composio/run_server.py /home/hiryu/hermes-control-plane-backup/configs/hermes/mcp_servers/composio/run_server.py

# Copy dependency lists
cp /home/hiryu/hermes-control-plane-backup/dependencies/apt-packages.txt /home/hiryu/hermes-control-plane-backup/dependencies/apt-packages.txt
cp /home/hiryu/hermes-control-plane-backup/dependencies/hermes-pip-requirements.txt /home/hiryu/hermes-control-plane-backup/dependencies/hermes-pip-requirements.txt
```

### 2. Create Restore Scripts

**`scripts/restore.sh`** (Master script):
```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "====================================================================="
echo "   🚀 HERMES CONTROL PLANE - RESTORE SEQUENCE"
echo "====================================================================="

if [ -z "${COMPOSIO_API_KEY:-}" ]; then
    echo "❌ ERROR: COMPOSIO_API_KEY environment variable is not set."
    echo "Please set it before running this script:"
    echo "  export COMPOSIO_API_KEY=\"yo..."
    exit 1
fi

echo ""
bash "${REPO_ROOT}/scripts/00_install_deps.sh"

echo ""
echo "🤖 [2/3] Installing Hermes Agent core …"
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

echo ""
bash "${REPO_ROOT}/scripts/01_restore_configs.sh"

echo ""
echo "====================================================================="
echo " 🎉 RESTORE COMPLETE!"
echo "====================================================================="
echo "Your Hermes Agent is now identical to the target state, including:"
echo " - Custom 'Smart_Agent' personality & config"
echo " - Composio MCP server integration"
echo " - All necessary dependencies"
echo ""
echo "👉 NEXT STEPS:"
echo "1. Restart your terminal (or run: source ~/.bashrc)"
echo "2. Run 'hermes' to start the agent."
echo "====================================================================="
```

**`scripts/00_install_deps.sh`** (Dependencies):
```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "📦 [1/3] Updating system and installing OS packages …"
if command -v apt-get &>/dev/null; then
    sudo apt-get update
    sudo xargs -a "${REPO_ROOT}/dependencies/apt-packages.txt" sudo apt-get install -y
else
    echo "⚠️  apt-get not found. Skipping system package installation."
fi

echo "📦 [2/3] Setting up Python virtual environment for Composio MCP …"
COMPOSIO_VENV_DIR="${HOME}/.hermes/mcp_servers/composio/venv"
mkdir -p "$(dirname "$COMPOSIO_VENV_DIR")"

if command -v uv &>/dev/null; then
    echo "🚀 Using 'uv' for fast installation …"
    uv venv "$COMPOSIO_VENV_DIR"
    uv pip install -r "${REPO_ROOT}/dependencies/hermes-pip-requirements.txt" --python "$COMPOSIO_VENV_DIR/bin/python"
else
    echo "🐍 Using standard 'venv' …"
    python3 -m venv "$COMPOSIO_VENV_DIR"
    "$COMPOSIO_VENV_DIR/bin/pip" install --upgrade pip
    "$COMPOSIO_VENV_DIR/bin/pip" install -r "${REPO_ROOT}/dependencies/hermes-pip-requirements.txt"
fi

echo "📦 [3/3] Ensuring Node.js environment is ready …"
if command -v npm &>/dev/null; then
    echo "✅ Node.js $(node --version) and npm $(npm --version) found."
else
    echo "❌ Node.js/npm not found. Some MCP servers may fail to start."
fi

echo "✅ Dependencies installation complete."
```

**`scripts/01_restore_configs.sh`** (Configuration):
```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HERMES_HOME="${HOME}/.hermes"

echo "⚙️  [1/2] Restoring Hermes Agent configuration …"
mkdir -p "$(dirname "${HERMES_HOME}/mcp_servers/composio")"

cp "${REPO_ROOT}/configs/hermes/config.yaml" "${HERMES_HOME}/config.yaml"
echo "  ✅ ${HERMES_HOME}/config.yaml"

mkdir -p "${HERMES_HOME}/mcp_servers/composio"
cp "${REPO_ROOT}/configs/hermes/mcp_servers/composio/run_server.py" \
   "${HERMES_HOME}/mcp_servers/composio/run_server.py"
echo "  ✅ ${HERMES_HOME}/mcp_servers/composio/run_server.py"

echo "⚙️  [2/2] Restoring shell configuration …"
for f in .bashrc .profile; do
    if [ -f "${HOME}/${f}" ] && ! cmp -s "${REPO_ROOT}/configs/shell/${f}" "${HOME}/${f}"; then
        cp "${HOME}/${f}" "${HOME}/${f}.backup-$(date +%Y%m%d-%H%M%S)"
        echo "  💾 Backed up existing ${f}"
    fi
done
cp "${REPO_ROOT}/configs/shell/.bashrc" "${HOME}/.bashrc"
cp "${REPO_ROOT}/configs/shell/.profile" "${HOME}/.profile"
echo "  ✅ ${HOME}/.bashrc"
echo "  ✅ ${HOME}/.profile"

echo "✅ Configuration restore complete."
```

## Usage

### First-Time Backup

```bash
# 1. Create backup structure (if not exists)
mkdir -p /home/hiryu/hermes-control-plane-backup

# 2. Navigate to backup directory
cd /home/hiryu/hermes-control-plane-backup

# 3. Initialize git (if needed)
git init
git remote add origin git@github.com:dwiariksuandi/hermes-control-plane.git

# 4. Copy configuration (as shown above)

# 5. Commit and push
git add .
git commit -m "feat: add robust restore-ready control plane structure"
git push -u origin main
```

### One-Click Restore

```bash
# 1. Clone the backup repository
git clone git@github.com:dwiariksuandi/hermes-control-plane.git
cd hermes-control-plane

# 2. Set API key (required)
export COMPOSIO_API_KEY="your_actual_api_key"

# 3. Run the master restore script
./scripts/restore.sh

# 4. Restart terminal
source ~/.bashrc

# 5. Start Hermes
hermes
```

## Verification (VBC)

After restore, verify the system is identical:

```bash
# 1. Check Hermes version
hermes --version

# 2. Check Composio MCP server is configured
cat ~/.hermes/config.yaml | grep -A10 "composio:"

# 3. Test tool availability
hermes chat -q "List tools that start with mcp_composio_"

# 4. Test GitHub integration (example)
hermes chat -q "Use mcp_composio_github_get_user to get your GitHub profile"

# 5. Verify configuration files exist
ls -la ~/.hermes/config.yaml ~/.hermes/mcp_servers/composio/run_server.py
```

## Security & Best Practices

### API Key Management
- **Never** store `COMPOSIO_API_KEY` in the backup repository
- Always export the key in the environment before restore:
  ```bash
  export COMPOSIO_API_KEY="your_key_here"
  ```
- Enable secret redaction: `hermes config set security.redact_secrets true`

### Backup Maintenance
- Push updates after any configuration change:
  ```bash
  cd /home/hiryu/hermes-control-plane-backup
  git add .
  git commit -m "Update configuration: [describe change]"
  git push origin main
  ```

### Disaster Recovery Steps
1. Identify target server requirements (Ubuntu/Debian, Python 3.11, Node.js)
2. Install minimal system dependencies (git, curl, build-essential)
3. Set environment variables (`COMPOSIO_API_KEY`)
4. Clone backup repository
5. Run `./scripts/restore.sh`
6. Verify with VBC checks above

## Troubleshooting

**"COMPOSIO_API_KEY not set" Error**
- Ensure the key is exported in the current shell
- Check for typos in the key
- Verify the key is valid at composio.dev

**MCP Server Fails to Start**
- Test manually: `~/.hermes/mcp_servers/composio/venv/bin/python ~/.hermes/mcp_servers/composio/run_server.py`
- Check composio service status at status.composio.dev
- Verify network connectivity

**Tools Not Appearing**
- Restart Hermes Agent after restore
- Check logs for MCP connection messages
- Verify tool naming: `mcp_composio_<toolkit>_<action>`

**Configuration Not Restored**
- Verify paths in restore scripts match your environment
- Check file permissions (scripts must be executable)
- Ensure all directories exist in backup structure

## Related Skills

- `composio-integration`: Core Composio setup and management
- `native-mcp`: MCP client functionality in Hermes
- `secure-agent-ops-lifecycle`: Secure lifecycle operations
- `github-pr-workflow`: GitHub operations for backup management

## Maintenance

### Updating Backup
After any configuration change:
```bash
cd /home/hiryu/hermes-control-plane-backup
git add .
git commit -m "Update configuration: [describe change]"
git push origin main
```

### Checking Backup Status
```bash
cd /home/hiryu/hermes-control-plane-backup
git status
git log --oneline -5
```

### Backup to Another Repository
```bash
# Add new remote
git remote add backup git@github.com:other-user/other-repo.git

# Push to backup
git push backup main
```

---

*This skill ensures complete disaster recovery capability for the Hermes Agent + Composio integration, following the principle of "infrastructure as code" and maintaining security through secret-redaction and environment-based key management.*
