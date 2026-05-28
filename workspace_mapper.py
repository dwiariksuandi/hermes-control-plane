#!/usr/bin/env python3
import os
import sqlite3
from pathlib import Path

HERMES_HOME = Path("/home/hiryu/.hermes")
DEFAULT_TARGETS = [HERMES_HOME, HERMES_HOME / "vault"]
DB_PATH = HERMES_HOME / "agent-logs.db"


def get_file_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".py", ".sh", ".bash"}:
        return "script"
    if suffix in {".md", ".txt", ".rst"}:
        return "document"
    if suffix in {".json", ".yaml", ".yml", ".toml", ".ini", ".cfg"}:
        return "config"
    if suffix in {".db", ".sqlite"}:
        return "database"
    if suffix in {".html", ".css", ".js"}:
        return "web"
    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}:
        return "asset"
    if suffix in {".log"}:
        return "log"
    return "other"


def get_brief_summary(path: Path, max_lines: int = 5) -> str:
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            lines = []
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                line = line.strip()
                if line:
                    lines.append(line)
        return " ".join(lines)[:600]
    except Exception:
        return ""


def ensure_schema(cur: sqlite3.Cursor) -> None:
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS workspace_graph (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT UNIQUE NOT NULL,
            file_type TEXT,
            brief_summary TEXT,
            last_modified REAL
        )
        """
    )


def map_workspace(targets=None) -> int:
    targets = targets or DEFAULT_TARGETS
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    ensure_schema(cur)
    cur.execute("DELETE FROM workspace_graph")

    indexed = 0
    seen = set()
    for root in targets:
        root = Path(root)
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [
                d for d in dirnames
                if not d.startswith('.') and d not in {"__pycache__", "node_modules", "dist", "build", ".git"}
            ]
            for name in filenames:
                if name.startswith('.'):
                    continue
                full_path = Path(dirpath) / name
                if full_path in seen:
                    continue
                seen.add(full_path)

                try:
                    rel = str(full_path.relative_to(HERMES_HOME))
                except ValueError:
                    rel = str(full_path)

                cur.execute(
                    """
                    INSERT OR REPLACE INTO workspace_graph (file_path, file_type, brief_summary, last_modified)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        rel,
                        get_file_type(full_path),
                        get_brief_summary(full_path),
                        full_path.stat().st_mtime,
                    ),
                )
                indexed += 1

    conn.commit()
    conn.close()
    return indexed


def query_workspace(pattern: str = "%", file_type: str = None, limit: int = 50):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if file_type:
        cur.execute(
            """
            SELECT file_path, file_type, brief_summary, last_modified
            FROM workspace_graph
            WHERE file_path LIKE ? AND file_type = ?
            ORDER BY last_modified DESC
            LIMIT ?
            """,
            (pattern, file_type, limit),
        )
    else:
        cur.execute(
            """
            SELECT file_path, file_type, brief_summary, last_modified
            FROM workspace_graph
            WHERE file_path LIKE ?
            ORDER BY last_modified DESC
            LIMIT ?
            """,
            (pattern, limit),
        )
    rows = cur.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    count = map_workspace()
    print(f"workspace_graph indexed: {count}")
    sample = query_workspace(limit=5)
    for row in sample:
        print(row[0], row[1])
