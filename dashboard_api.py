import asyncio
from pathlib import Path
import sqlite3
import psutil
import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import HTTPException

# Configure rotating logs
log_path = Path("/home/hiryu/.hermes/vault/dev/dashboard.log")
log_path.parent.mkdir(parents=True, exist_ok=True)
handler = RotatingFileHandler(log_path, maxBytes=5*1024*1024, backupCount=3)
logging.basicConfig(level=logging.INFO, handlers=[handler], format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("dashboard")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "/home/hiryu/.hermes/agent-logs.db"


@app.get("/api/status")
async def get_status():
    return {"status": "online", "agents": ["Scout", "Scribe", "Reach", "Dev"]}


@app.get("/api/logs")
async def get_logs():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM activity_logs ORDER BY rowid DESC LIMIT 50")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except sqlite3.Error as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}")

@app.get("/api/system-health")
async def get_system_health():
    return {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }


@app.websocket("/ws/telemetry")
async def ws_telemetry(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT timestamp, agent_name, task_summary, status
                    FROM activity_logs
                    ORDER BY timestamp DESC
                    LIMIT 50
                """)
                rows = cursor.fetchall()
                conn.close()

                logs = [
                    {
                        "timestamp": r[0],
                        "agent_name": r[1],
                        "task_summary": r[2],
                        "status": r[3],
                    }
                    for r in rows
                ]

                payload = {
                    "system_health": {
                        "cpu": psutil.cpu_percent(),
                        "ram": psutil.virtual_memory().percent,
                        "disk": psutil.disk_usage('/').percent,
                    },
                    "logs": logs,
                }
                await websocket.send_json(payload)
                # Heartbeat: expect ping or close within 2s
                try:
                    await asyncio.wait_for(websocket.receive(), timeout=30)
                except asyncio.TimeoutError:
                    pass  # No client message = normal, keep looping
            except WebSocketDisconnect:
                break
            except Exception:
                await asyncio.sleep(2)
                continue
    except WebSocketDisconnect:
        return
    except Exception:
        return

@app.get("/api/fleet")
async def get_fleet():
    agents = [
        {
            "id": "scout",
            "name": "Scout",
            "role": "Deep web research, source validation",
            "status": "active",
            "last_task": "Research & validation",
        },
        {
            "id": "scribe",
            "name": "Scribe",
            "role": "Knowledge compilation, Markdown docs, Obsidian",
            "status": "active",
            "last_task": "Documentation & SOPs",
        },
        {
            "id": "reach",
            "name": "Reach",
            "role": "Audience mechanics, growth strategies, distribution",
            "status": "active",
            "last_task": "Campaign analytics",
        },
        {
            "id": "dev",
            "name": "Dev",
            "role": "Systems automation, shell integrations, telemetry",
            "status": "active",
            "last_task": "Backend & dashboard engineering",
        },
    ]
    return {"agents": agents}


VAULT_ROOT = Path("/home/hiryu/.hermes/vault")

def build_tree(p: Path) -> dict:
    items = {}
    for entry in p.iterdir():
        if entry.is_dir():
            items[entry.name] = build_tree(entry)
        else:
            items[entry.name] = str(entry)
    return items

@app.get("/api/vault/tree")
async def vault_tree():
    return build_tree(VAULT_ROOT)

@app.get("/api/vault/file")
async def vault_file(path: str):
    # Security: resolve absolute path
    resolved = (VAULT_ROOT / path).resolve()
    # Check if inside vault
    if not str(resolved).startswith(str(VAULT_ROOT.resolve())):
        raise HTTPException(status_code=403, detail="Forbidden")
    if not resolved.is_file():
        raise HTTPException(status_code=404, detail="Not found")
    content = resolved.read_text(encoding="utf-8", errors="replace")
    return {"content": content}
