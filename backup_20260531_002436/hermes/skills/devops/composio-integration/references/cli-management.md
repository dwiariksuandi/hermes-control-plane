# Composio CLI Management

## Clean Reinstallation
When the global Composio CLI (`~/.composio/composio`) is corrupted, failing to update, or missing from PATH, perform a clean reinstall. 

1. **Extract existing API Key** (to avoid losing auth state):
   ```bash
   grep -o 'uak_[^"]*' ~/.composio/user_data.json
   ```

2. **Wipe existing installation**:
   ```bash
   rm -rf ~/.composio
   ```

3. **Run the current official install script**:
   *Pitfall: The old `install.sh` endpoint and `npm install -g @composio/cli` return 404s. Use the extensionless `/install` endpoint.*
   ```bash
   curl -fsSL https://composio.dev/install | bash
   ```

4. **Verify/Fix PATH**:
   ```bash
   grep -q 'export PATH="$HOME/.composio:$PATH"' ~/.bashrc || echo 'export PATH="$HOME/.composio:$PATH"' >> ~/.bashrc
   ```

## Known Pitfalls
* **Version String Mismatch**: The installer may fetch a newer tag (e.g., `0.2.28`), but the binary internally reports an older version (e.g., `0.2.27`) when running `composio --version`. `composio upgrade` will not resolve this. This is an upstream packaging artifact; if the CLI executes properly, it can be safely ignored.