---
name: hermes-dashboard-integration
description: Build Hermes Mission Control dashboard with system health endpoint and cyberpunk UI.
version: 1.0.0
author: Hermes Agent
platforms: [linux]
metadata:
  hermes:
    tags: [dashboard, api, ui, cyberpunk, psutil, chartjs]
    related_skills: [claude-design, python-debugpy]
---
# Hermes Dashboard Integration Skill

This skill captures the end-to-end process of building the Hermes Mission Control dashboard, including:
- Installing psutil for hardware telemetry
- Adding a `/api/system-health` endpoint to the FastAPI backend
- Creating a cyberpunk-themed HTML frontend with Chart.js radar and Tailwind CSS
- Launching the dashboard as a background daemon

## When to Use
Use this skill when you need to provision or update the Hermes local dashboard with real-time system metrics and a sci-fi command center interface.

## Prerequisites
- Hermes environment with `uv` package manager available
- Existing FastAPI backend at `/home/hiryu/.hermes/dashboard_api.py`
- Existing frontend directory at `/home/hiryu/.hermes/dashboard/`
- Python 3.8+

## Step-by-Step Procedure

### 1. Install psutil via UV
```bash
/home/hiryu/.local/bin/uv pip install psutil
```

### 2. Update Backend (`dashboard_api.py`)
- Ensure `import psutil` is present (add if missing)
- Add the following endpoint:
```python
@app.get("/api/system-health")
async def get_system_health():
    return {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }
```
- Verify existing endpoints (`/api/status`, `/api/logs`) remain intact.

### 3. Overwrite Frontend (`dashboard/index.html`)
Replace the file with a cyberpunk-themed HTML that includes:
- Tailwind CSS via CDN
- FontAwesome icons via CDN
- Chart.js via CDN
- Dark space background (`#0a0a1a`) with neon cyan (`#00f0ff`) and neon purple (`#b026ff`) accents
- Layout structure:
  - Left sidebar with vertical navigation (icons: satellite, tachometer, users-cog, tasks, cogs)
  - Top header with glowing "HERMES AGENT MISSION CONTROL" title and neon badge
  - Top row panels:
    * Mission Radar (Chart.js hexagon radar)
    * Current Directive (context window progress bar)
    * VPS Health (horizontal progress bars for CPU, RAM, Disk from `/api/system-health`)
  - Middle row: Gateway status badge area
  - Bottom row: Activity log table styled with dark rows and neon status text
- All panels use glassmorphism: `bg-white/5`, `backdrop-blur-md`, thin glowing border (`border border-[#00f0ff]/30`)
- Include JavaScript to:
  - Poll `/api/system-health` every 5 seconds to update progress bars
  - Poll `/api/logs` every 5 seconds to populate the activity log table
  - Initialize Chart.js radar with sample data

### 4. Launch Dashboard Daemon
Use the provided launcher script (`launch_dashboard.py`) or execute:
```bash
/home/hiryu/.local/bin/uv run --with fastapi --with uvicorn uvicorn dashboard_api:app --host 0.0.0.0 --port 8000 &
```
Ensure the server logs to `/home/hiryu/.hermes/vault/dev/dashboard.log`.

### 5. Verification
- Check that `http://localhost:8000/api/system-health` returns JSON with CPU, RAM, Disk percentages.
- Confirm the dashboard loads at `http://localhost:8000` (or via frontend proxy) and displays:
  - Radar chart with six axes
  - Progress bars for context window and system health
  - Activity log table with recent entries
  - Neon cyberpunk aesthetic with glowing text and blurred panels

## Pitfalls & Troubleshooting
- **Missing psutil after install**: Ensure UV is using the correct Python environment; try `uv pip list` to verify.
- **CORS blocking frontend**: Verify `dashboard_api.py` includes `CORSMiddleware` with `allow_origins=["*"]`.
- **Port already in use**: Kill existing uvicorn processes (`pkill -f uvicorn`) before relaunching.
- **Chart not rendering**: Ensure Chart.js script loads successfully; check browser console for errors.
- **Logs table empty**: Confirm `/api/logs` endpoint returns JSON array; check SQLite database for rows.

## Artifacts Produced
- Updated `/home/hiryu/.hermes/dashboard_api.py` (with psutil import and `/api/system-health` endpoint)
- Updated `/home/hiryu/.hermes/dashboard/index.html` (cyberpunk dashboard)
- Launcher script `/home/hiryu/.hermes/launch_dashboard.py` (optional)
- Log file `/home/hiryu/.hermes/vault/dev/dashboard.log`

## References
- [psutil documentation](https://psutil.readthedocs.io/)
- [Chart.js documentation](https://www.chartjs.org/docs/latest/)
- [Tailwind CSS playground](https://play.tailwindcss.com/)
- [FontAwesome icons](https://fontawesome.com/icons)

---