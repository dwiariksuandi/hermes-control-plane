---
name: local-ops-dashboard
description: Build and operate a local FastAPI-based mission control dashboard with telemetry, vault browsing, and agent fleet status. Single-file vanilla JS frontend, detached daemon backend.
version: 1.0.0
platforms: [linux]
metadata:
  hermes:
    tags: [dashboard, fastapi, websocket, telemetry, ops, monitoring, vault]
    related_skills: [claude-design, hermes-agent]
---

# Local Ops Dashboard Stack

Build a self-contained local operations dashboard for orchestrating agents, viewing telemetry, and browsing a file-based vault. Backend is FastAPI; frontend is a single `index.html` with vanilla JS and Tailwind CDN.

## Trigger Conditions

Use this skill when the user asks to:
- Build a local dashboard / mission control / telemetry UI
- Create an agent fleet status page
- Browse a local vault directory from a web UI
- Stream SQLite logs or system metrics to a frontend
- Launch a background FastAPI server that persists after the agent session ends

## Architecture

```
Backend:  FastAPI + SQLite + psutil + WebSocket (/ws/telemetry)
Frontend: Single index.html (Tailwind CDN, vanilla JS, Chart.js optional)
Launcher: Python script using subprocess.Popen detached mode
```

## Backend Patterns

### 1. FastAPI Scaffolding

Always include CORS middleware with `allow_origins=["*"]` so the local `index.html` can fetch without browser blocking:

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2. WebSocket Telemetry Stream

Push both system health (psutil) and recent logs (SQLite) on a 1-second loop:

```python
@app.websocket("/ws/telemetry")
async def ws_telemetry(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # ... query SQLite logs ...
            payload = {
                "system_health": {
                    "cpu": psutil.cpu_percent(),
                    "ram": psutil.virtual_memory().percent,
                    "disk": psutil.disk_usage('/').percent,
                },
                "logs": logs,
            }
            await websocket.send_json(payload)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        return
```

### 3. Vault File Serving (Path Traversal Guard)

Use `pathlib.Path.resolve()` and a prefix check. Never serve files outside the vault root:

```python
from pathlib import Path
VAULT_ROOT = Path("/home/hiryu/.hermes/vault")

@app.get("/api/vault/file")
async def vault_file(path: str):
    resolved = (VAULT_ROOT / path).resolve()
    if not str(resolved).startswith(str(VAULT_ROOT.resolve())):
        raise HTTPException(status_code=403, detail="Forbidden")
    if not resolved.is_file():
        raise HTTPException(status_code=404, detail="Not found")
    content = resolved.read_text(encoding="utf-8", errors="replace")
    return {"content": content}
```

### 4. Fleet Endpoint

Return a static or dynamic list of agents with role, status, and last_task fields:

```python
@app.get("/api/fleet")
async def get_fleet():
    return {"agents": [{"id": "scout", "name": "Scout", "role": "...", "status": "active", "last_task": "..."}]}
```

## Frontend Patterns

### 1. Single-File Structure

Use one `index.html` with embedded `<style>` and `<script>`. Load Tailwind via CDN:

```html
<script src="https://cdn.tailwindcss.com"></script>
```

### 2. Tab Switching

Use `hidden` class toggling, not multiple HTML files:

```javascript
function switchTab(name) {
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.add('hidden'));
    document.querySelectorAll('.nav-link').forEach(n => n.classList.remove('active'));
    document.getElementById('tab-' + name).classList.remove('hidden');
    event.currentTarget.classList.add('active');
}
```

### 3. WebSocket Client

Connect once, update multiple DOM regions from a single `onmessage` handler:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/telemetry');
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    // update health bars, log table, status badge
};
```

### 4. Sci-Fi Aesthetic (Optional)

If the user requests a cyberpunk/mission-control look:
- Background: `#0a0a1a`
- Primary neon: `#00f0ff` (cyan)
- Accent neon: `#b026ff` (magenta)
- Panels: `rgba(255,255,255,0.05)` + `backdrop-filter: blur(10px)` + `border: 1px solid rgba(0,240,255,0.3)`
- Fonts: `'Orbitron'` for headers, `'Roboto Mono'` for body
- Progress bars: gradient from `#b026ff` to `#00f0ff` with `box-shadow` glow

## Detached Daemon Launcher

The launcher script MUST use `subprocess.Popen` with `stdout=subprocess.DEVNULL`, `stderr=subprocess.DEVNULL`, `start_new_session=True`, and `close_fds=True` so the server survives the agent session:

```python
proc = subprocess.Popen(
    cmd,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    cwd="/home/hiryu/.hermes",
    start_new_session=True,
    close_fds=True,
)
```

Store PID in a log file for later inspection.

## Verification Checklist

After each backend change:
1. Kill old uvicorn (`pkill -f uvicorn`)
2. Relaunch via launcher script
3. Test endpoints physically:
   - `curl http://localhost:8000/api/status`
   - `curl http://localhost:8000/api/system-health`
   - `curl http://localhost:8000/api/vault/tree`
   - `curl "http://localhost:8000/api/vault/file?path=SOUL.md"`
   - `curl http://localhost:8000/api/fleet`
   - Path traversal guard: expect 403 for `?path=../../etc/passwd`
4. Confirm WebSocket accepts connections
5. Check frontend file size > 0 and contains expected tab IDs

## Pitfalls

- **DO NOT use `delegate_task` for writing HTML/JS files.** Delegated subagents often return incomplete or fail to write. Use direct `write_file` or `execute_code` instead.
- **DO NOT use `uvicorn.run()` inside `execute_code`.** It blocks the execution thread. Always use a detached subprocess launcher.
- **DO NOT forget CORS.** Without it, the local `file://` or `localhost` frontend will be blocked by browser security.
- **DO NOT trust conversation memory for file contents.** Always `cat` or `read_file` before editing.
- **Avoid multiple `<script src="...">` tags with inline JS inside them.** Browsers may execute inline code before the CDN loads. Keep CDN scripts closed (`</script>`) and place inline JS in a separate `<script>` block below.

## File Layout

```
~/.hermes/
  dashboard_api.py          # FastAPI backend
  dashboard/
    index.html               # Single-page frontend
  launch_dashboard.py        # Detached daemon launcher
  agent-logs.db              # SQLite telemetry DB
  vault/                     # File tree served by /api/vault/*
```
