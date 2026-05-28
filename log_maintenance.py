#!/usr/bin/env python3
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path('/home/hiryu/.hermes/agent-logs.db')
ARCHIVE_PATH = Path('/home/hiryu/.hermes/vault/dev/telemetry_archive.md')
LIMIT = 500

def main():
    ARCHIVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM activity_logs')
    count = cur.fetchone()[0]
    if count <= LIMIT:
        conn.close()
        print(f'OK: {count} rows; no pruning needed')
        return

    prune_count = count - LIMIT
    cur.execute('SELECT id, timestamp, agent_name, task_summary, status, validation_status, artifact_path FROM activity_logs ORDER BY timestamp ASC, id ASC LIMIT ?', (prune_count,))
    rows = cur.fetchall()

    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    with ARCHIVE_PATH.open('a', encoding='utf-8') as f:
        if ARCHIVE_PATH.stat().st_size == 0:
            f.write('---\nauthor: Dev\nstatus: active\ntimestamp: ' + now + '\ntags: [telemetry, archive, audit]\n---\n\n# Telemetry Archive\n\n')
        f.write(f'\n## Pruned at {now}\n')
        for row in rows:
            log_id, ts, agent, summary, status, validation, artifact = row
            artifact_text = artifact or ''
            f.write(f'- `{ts}` | `{agent}` | {status}/{validation} | {summary} | `{artifact_text}` | id `{log_id}`\n')

    ids = [(r[0],) for r in rows]
    cur.executemany('DELETE FROM activity_logs WHERE id = ?', ids)
    conn.commit()
    cur.execute('SELECT COUNT(*) FROM activity_logs')
    remaining = cur.fetchone()[0]
    conn.close()
    print(f'PRUNED: archived {len(rows)} rows to {ARCHIVE_PATH}; remaining {remaining}')

if __name__ == '__main__':
    main()
