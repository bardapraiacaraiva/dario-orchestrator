"""Hook adapter — called by Claude Code hooks to notify the DARIO Runtime.
Fails silently if service is down (non-blocking).
"""
import json
import sys
import urllib.request
import urllib.error

ORCH_URL = "http://localhost:8421"


def notify(endpoint: str, data: dict = None):
    """POST to orchestrator service. Silent on failure."""
    try:
        payload = json.dumps(data or {}).encode("utf-8")
        req = urllib.request.Request(
            f"{ORCH_URL}{endpoint}",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=3)
    except (urllib.error.URLError, OSError):
        pass  # Service down — fail silently


if __name__ == "__main__":
    event = sys.argv[1] if len(sys.argv) > 1 else "session-start"

    if event == "session-start":
        notify("/hooks/session-start", {"session_id": "cli", "timestamp": ""})
    elif event == "session-end":
        notify("/hooks/session-end", {"session_id": "cli", "timestamp": ""})
    elif event == "task-complete":
        # Usage: hook_adapter.py task-complete <task_id> <skill> <score> [tokens]
        task_id = sys.argv[2] if len(sys.argv) > 2 else None
        skill = sys.argv[3] if len(sys.argv) > 3 else None
        score = float(sys.argv[4]) if len(sys.argv) > 4 else None
        tokens = int(sys.argv[5]) if len(sys.argv) > 5 else None
        notify("/hooks/task-complete", {
            "task_id": task_id,
            "skill": skill,
            "quality_score": score,
            "tokens_used": tokens,
        })
