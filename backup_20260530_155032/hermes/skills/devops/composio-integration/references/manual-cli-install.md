# Composio CLI: Manual Install & Version Mismatch Fix

This document outlines the robust, manual process for installing or fixing a specific version of the Composio CLI, bypassing the official installer which can sometimes serve stale binaries.

## The Problem: Version Mismatch

You may encounter a situation where:
1. You run the official installer (`curl -fsSL https://composio.dev/install | bash`).
2. The installer claims to fetch version `0.2.28` (or newer).
3. The installed binary at `~/.composio/composio --version` reports an older version (e.g., `0.2.27`).
4. `composio upgrade` does nothing.

This indicates the installer's download source is pointing to a cached or outdated binary, even though newer release tags exist on GitHub.

## The Solution: Manual Asset Download

The fix is to find the direct `browser_download_url` for the desired version from the GitHub releases API and replace the binary manually.

### Step 1: Find the Correct Release URL

The `latest` release endpoint can be misleading. You must scan the full list of releases to find the correct `@composio/cli` package with assets.

Use this Python script to list all available CLI versions and their download URLs:

```python
import json
import urllib.request

url = 'https://api.github.com/repos/ComposioHQ/composio/releases?per_page=100'

try:
    with urllib.request.urlopen(url) as r:
        data = json.load(r)
    
    print("Found the following CLI releases with 'linux-x64' assets:\n")
    found = False
    for rel in data:
        tag = rel.get('tag_name', '')
        if tag.startswith('@composio/cli@'):
            for asset in rel.get('assets', []):
                if 'linux-x64.zip' in asset.get('name', ''):
                    found = True
                    print(f"Version: {tag}")
                    print(f"  Asset URL: {asset.get('browser_download_url')}")
                    print(f"  Published: {rel.get('published_at')}\n")
                    break # Move to next release once we found the asset
    if not found:
        print("No recent stable CLI releases with linux-x64 assets found.")

except Exception as e:
    print(f"An error occurred: {e}")

```

### Step 2: Download, Unzip, and Replace

Once you have the URL for the desired version (e.g., from `@composio/cli@0.2.28`), use these commands to perform the manual update.

```bash
# Set the URL from the script output
ASSET_URL="https://github.com/ComposioHQ/composio/releases/download/%40composio/cli%400.2.28/composio-linux-x64.zip"

# Download to a temporary file
curl -L -o /tmp/composio-linux-x64.zip "$ASSET_URL"

# Backup the old binary (optional but recommended)
cp -a /home/hiryu/.composio/composio /home/hiryu/.composio/composio.bak

# Unzip and overwrite the existing binary
# The -o flag forces overwrite. The zip may contain a sub-directory.
unzip -o /tmp/composio-linux-x64.zip -d /home/hiryu/.composio/

# The binary might be in a subdirectory, e.g., 'composio-linux-x64/composio'
# This command moves it to the correct location, overwriting the old one.
if [ -f /home/hiryu/.composio/composio-linux-x64/composio ]; then
    mv -f /home/hiryu/.composio/composio-linux-x64/composio /home/hiryu/.composio/composio
    rm -rf /home/hiryu/.composio/composio-linux-x64 # cleanup empty dir
fi

# Ensure it's executable
chmod +x /home/hiryu/.composio/composio

# Verify the new version
/home/hiryu/.composio/composio --version
```

This procedure guarantees you are running the exact version corresponding to the GitHub release tag.
