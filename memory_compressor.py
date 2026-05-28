#!/usr/bin/env python3
import sqlite3
import datetime
import json
import uuid
import os

DB_PATH = "/home/hiryu/.hermes/agent-logs.db"


def ensure_table(conn):
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS long_term_memory (
            id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            source_window_start TEXT,
            source_window_end TEXT,
            source_count INTEGER NOT NULL,
            summary TEXT NOT NULL,
            source_agents TEXT,
            source_rowids TEXT
        )
        """
    )
    conn.commit()


def bucket_key(ts: str):
    # Group by date-hour for dense batches
    # expects ISO-ish timestamp
    try:
        dt = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        try:
            dt = datetime.datetime.strptime(ts[:19], "%Y-%m-%d %H:%M:%S")
        except Exception:
            return "unknown"
    return dt.strftime("%Y-%m-%d %H")


def compress_group(rows):
    # rows: (rowid, timestamp, agent_name, task_summary, status, artifact_path)
    by_agent = {}
    artifacts = []
    statuses = {"success": 0, "other": 0}
    for r in rows:
        _, ts, agent, summary, status, artifact = r
        agent = agent or "Unknown"
        summary = (summary or "").strip()
        by_agent.setdefault(agent, [])
        if summary:
            by_agent[agent].append(summary)
        if artifact:
            artifacts.append(artifact)
        if status and str(status).lower() == "success":
            statuses["success"] += 1
        else:
            statuses["other"] += 1

    # Dense semantic-ish summary (rule-based local compressor)
    parts = []
    for agent, items in by_agent.items():
        uniq = []
        seen = set()
        for it in items:
            k = it.lower()
            if k not in seen:
                seen.add(k)
                uniq.append(it)
        snippet = "; ".join(uniq[:3])
        if len(uniq) > 3:
            snippet += f"; +{len(uniq)-3} more"
        parts.append(f"{agent}: {snippet}" if snippet else f"{agent}: activity recorded")

    artifacts_short = []
    for a in artifacts[:5]:
        artifacts_short.append(a)
    art_text = ", ".join(artifacts_short)
    if len(artifacts) > 5:
        art_text += f", +{len(artifacts)-5} more"

    summary = (
        f"Compressed batch. Agents -> " + " | ".join(parts) + 
        f". Status counts: success={statuses['success']}, other={statuses['other']}." +
        (f" Artifacts: {art_text}." if art_text else "")
    )
    return summary


def main(hours_old=0):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    ensure_table(conn)

    cur.execute("SELECT COUNT(*) FROM activity_logs")
    before_count = cur.fetchone()[0]

    # select rows eligible for compression
    cur.execute(
        """
        SELECT rowid, timestamp, agent_name, task_summary, status, artifact_path
        FROM activity_logs
        ORDER BY timestamp ASC, rowid ASC
        """
    )
    all_rows = cur.fetchall()

    if not all_rows:
        print(json.dumps({"result": "no_data", "before": before_count, "after": before_count}))
        conn.close()
        return

    # If hours_old > 0, keep recent rows
    eligible = []
    if hours_old > 0:
        threshold = datetime.datetime.utcnow() - datetime.timedelta(hours=hours_old)
        for r in all_rows:
            ts = r[1]
            try:
                dt = datetime.datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
                dt_naive = dt.replace(tzinfo=None)
            except Exception:
                dt_naive = datetime.datetime.min
            if dt_naive < threshold:
                eligible.append(r)
    else:
        eligible = all_rows[:]  # batch test now

    if not eligible:
        print(json.dumps({"result": "no_eligible_rows", "before": before_count, "after": before_count}))
        conn.close()
        return

    # group by hour-bucket
    groups = {}
    for r in eligible:
        k = bucket_key(str(r[1]))
        groups.setdefault(k, []).append(r)

    compressed_batches = 0
    pruned_rows = 0

    for k, rows in groups.items():
        rowids = [str(r[0]) for r in rows]
        agents = sorted(list({(r[2] or "Unknown") for r in rows}))
        summary = compress_group(rows)
        window_start = str(rows[0][1])
        window_end = str(rows[-1][1])

        cur.execute(
            """
            INSERT INTO long_term_memory
            (id, created_at, source_window_start, source_window_end, source_count, summary, source_agents, source_rowids)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(uuid.uuid4()),
                datetime.datetime.utcnow().isoformat(),
                window_start,
                window_end,
                len(rows),
                summary,
                json.dumps(agents),
                json.dumps(rowids),
            ),
        )

        # prune raw rows
        placeholders = ",".join(["?"] * len(rowids))
        cur.execute(f"DELETE FROM activity_logs WHERE rowid IN ({placeholders})", rowids)
        pruned_rows += len(rowids)
        compressed_batches += 1

    conn.commit()

    cur.execute("SELECT COUNT(*) FROM activity_logs")
    after_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM long_term_memory")
    ltm_count = cur.fetchone()[0]

    conn.close()

    print(json.dumps({
        "result": "ok",
        "compressed_batches": compressed_batches,
        "pruned_rows": pruned_rows,
        "activity_logs_before": before_count,
        "activity_logs_after": after_count,
        "long_term_memory_rows": ltm_count
    }, indent=2))


if __name__ == "__main__":
    # default batch test now (compress all existing rows)
    main(hours_old=0)
