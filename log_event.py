import sys
import sqlite3
import uuid
from datetime import datetime, timezone

def main():
    if len(sys.argv) < 5:
        sys.exit(1)
    
    agent_name = sys.argv[1]
    task_summary = sys.argv[2][:150]
    status = sys.argv[3]
    validation_status = sys.argv[4]
    artifact_path = sys.argv[5] if len(sys.argv) > 5 else None
    
    db_path = '/home/hiryu/.hermes/agent-logs.db'
    log_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO activity_logs (id, timestamp, agent_name, task_summary, status, validation_status, artifact_path) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (log_id, timestamp, agent_name, task_summary, status, validation_status, artifact_path)
    )
    conn.commit()
    conn.close()
    print(log_id)

if __name__ == '__main__':
    main()
