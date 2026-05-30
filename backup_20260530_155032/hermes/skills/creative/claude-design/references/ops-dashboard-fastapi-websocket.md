# Ops Dashboard Patterns: FastAPI + WebSocket + Local JS

When using this skill to create functional dashboards:

### 1. Backend Integration (FastAPI)
- **FastAPI + WebSocket + SQL + psutil**: 
  - Define `DB_PATH = Path(...)` and `VAULT_ROOT = Path(...)`.
  - Use `sqlite3.Row` for dict-like row access.
  - For system monitoring, install `psutil` via `uv pip`.
  - CORS middleware (`allow_origins=["*"]`) is REQUIRED for browser-to-local-server fetch.

### 2. Frontend Integration (Vanilla JS)
- **Event-safe tab switching**:
  ```javascript
  // HTML
  <div onclick="switchTab(event, 'fleet')">...</div>

  // JS
  function switchTab(evt, name) {
      // evt.currentTarget safely identifies which button was clicked
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.add('hidden'));
      document.getElementById('tab-' + name).classList.remove('hidden');
      evt.currentTarget.classList.add('active');
  }
  ```
- **Real-time pipeline**:
  - `ws.onmessage` handler needs to re-render the view completely from state.
  - Always have a fallback for closed/errored states.

### 3. File Security
- **Path Traversal Guard**:
  ```python
  resolved = (ROOT / path).resolve()
  if not str(resolved).startswith(str(ROOT.resolve())):
      raise HTTPException(status_code=403, detail="Forbidden")
  ```
- Never trust the `path` param from user input without resolution and prefix check.
