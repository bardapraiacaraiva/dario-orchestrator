"""Execution timeline — data collector + live page (Next-Gen N3, 2026-06-12).

The runtime had SSE streaming since #15, but nothing consumed it, and the
in-process EventBus cannot see work done by subprocess engines or other
sessions anyway. The N2 task_steps journal is the durable, cross-process
record of every execution — this module turns it into:

  - get_timeline(db): JSON feed of recent task activity with per-step
    timestamps (served at GET /api/timeline)
  - TIMELINE_HTML: a zero-dependency live page (served at GET /timeline)
    that polls the feed every 3s and subscribes to /events SSE for the
    live ticker when available.

Read-only by design: this module never mutates orchestrator state.
"""

from datetime import UTC, datetime, timedelta


def _parse_iso(value):
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def get_timeline(db, hours: int = 24, limit: int = 60) -> dict:
    """Recent execution activity, newest first.

    A task appears if it is currently in flight (in_progress / in_review /
    blocked) or had journal/update activity within the window. Each entry
    carries its journal steps (checked_out -> executed -> finalized) so the
    page can render the at-risk window and crash-recovery state precisely.
    """
    now = datetime.now(UTC)
    cutoff = (now - timedelta(hours=hours)).isoformat()

    with db._conn() as conn:
        rows = conn.execute(
            """SELECT id, title, project, skill, assignee, status, priority,
                      execution_policy, quality_score, actual_tokens,
                      checked_out_at, completed_at, updated_at
               FROM tasks
               WHERE status IN ('in_progress', 'in_review', 'blocked')
                  OR updated_at >= ?
               ORDER BY updated_at DESC LIMIT ?""",
            (cutoff, limit)).fetchall()
        tasks = [dict(r) for r in rows]

        step_rows = conn.execute(
            """SELECT task_id, step, status, created_at FROM task_steps
               WHERE created_at >= ? ORDER BY id""", (cutoff,)).fetchall()

    steps_by_task: dict[str, list] = {}
    for s in step_rows:
        steps_by_task.setdefault(s["task_id"], []).append(
            {"step": s["step"], "status": s["status"], "at": s["created_at"]})

    items = []
    for t in tasks:
        steps = steps_by_task.get(t["id"], [])
        executed = any(s["step"] == "executed" for s in steps)
        finalized = any(s["step"] == "finalized" for s in steps)
        items.append({
            **t,
            "steps": steps,
            # resumable = paid-for output exists but finalize never ran (N2)
            "resumable": (t["status"] == "in_progress" and executed and not finalized),
        })

    counts: dict[str, int] = {}
    for t in items:
        counts[t["status"]] = counts.get(t["status"], 0) + 1

    return {
        "generated_at": now.isoformat(),
        "window_hours": hours,
        "counts": counts,
        "tasks": items,
    }


TIMELINE_HTML = """<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DARIO — Execution Timeline</title>
<style>
  :root {
    --bg: #0b0e14; --panel: #11151f; --line: #1d2433; --text: #d8dee9;
    --dim: #7b8496; --accent: #5ccfe6; --ok: #5fd068; --warn: #f2c14e;
    --bad: #ef6b73; --violet: #b18cff;
  }
  * { box-sizing: border-box; margin: 0; }
  body { background: var(--bg); color: var(--text);
         font: 14px/1.5 "Segoe UI", system-ui, sans-serif; padding: 28px; }
  header { display: flex; align-items: baseline; gap: 14px; margin-bottom: 6px; }
  h1 { font-size: 19px; font-weight: 600; letter-spacing: .4px; }
  .live { font-size: 11px; color: var(--ok); }
  .live::before { content: "●"; margin-right: 5px; animation: blink 2s infinite; }
  @keyframes blink { 50% { opacity: .25; } }
  .meta { color: var(--dim); font-size: 12px; margin-bottom: 18px; }
  .counts { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
  .pill { background: var(--panel); border: 1px solid var(--line);
          border-radius: 20px; padding: 4px 14px; font-size: 12px; }
  .pill b { color: var(--accent); }
  .task { background: var(--panel); border: 1px solid var(--line);
          border-radius: 10px; padding: 14px 18px; margin-bottom: 10px; }
  .row1 { display: flex; gap: 12px; align-items: baseline; flex-wrap: wrap; }
  .tid { font-family: Consolas, monospace; color: var(--accent); font-size: 13px; }
  .title { font-weight: 600; }
  .badge { font-size: 11px; border-radius: 4px; padding: 1px 8px; margin-left: auto; }
  .st-done { background: #14331c; color: var(--ok); }
  .st-in_progress { background: #1d2c40; color: var(--accent); }
  .st-in_review { background: #3a2f14; color: var(--warn); }
  .st-blocked, .st-failed { background: #3a1a1d; color: var(--bad); }
  .st-todo, .st-backlog { background: #20242e; color: var(--dim); }
  .row2 { color: var(--dim); font-size: 12px; margin-top: 3px; }
  .row2 b { color: var(--text); font-weight: 500; }
  .steps { display: flex; gap: 6px; margin-top: 10px; flex-wrap: wrap; }
  .chip { font-size: 11px; font-family: Consolas, monospace;
          border: 1px solid var(--line); border-radius: 4px; padding: 2px 8px;
          color: var(--dim); }
  .chip.done, .chip.pass { border-color: #2c5237; color: var(--ok); }
  .chip.tripwire, .chip.failed { border-color: #5b2a2e; color: var(--bad); }
  .chip.flag { border-color: #5b4a1e; color: var(--warn); }
  .resume { color: var(--violet); font-size: 11px; margin-top: 8px; }
  #ticker { background: var(--panel); border: 1px solid var(--line);
            border-radius: 10px; padding: 10px 16px; margin-bottom: 18px;
            font-family: Consolas, monospace; font-size: 12px; color: var(--dim);
            max-height: 96px; overflow-y: auto; }
  #ticker div { padding: 1px 0; }
  .empty { color: var(--dim); padding: 30px; text-align: center; }
</style>
</head>
<body>
<header><h1>DARIO · Execution Timeline</h1><span class="live" id="live">live</span></header>
<div class="meta" id="meta">a carregar…</div>
<div class="counts" id="counts"></div>
<div id="ticker"><div>· live events (SSE) aparecem aqui</div></div>
<div id="tasks"></div>

<script>
const fmtAgo = iso => {
  if (!iso) return "—";
  const s = (Date.now() - new Date(iso)) / 1000;
  if (s < 60) return Math.floor(s) + "s";
  if (s < 3600) return Math.floor(s / 60) + "m";
  if (s < 86400) return Math.floor(s / 3600) + "h";
  return Math.floor(s / 86400) + "d";
};
const esc = t => (t || "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

async function refresh() {
  try {
    const r = await fetch("/api/timeline");
    const d = await r.json();
    document.getElementById("meta").textContent =
      `janela ${d.window_hours}h · ${d.tasks.length} tasks · atualizado ${new Date(d.generated_at).toLocaleTimeString("pt-PT")}`;
    document.getElementById("counts").innerHTML = Object.entries(d.counts)
      .map(([k, v]) => `<span class="pill">${esc(k)} <b>${v}</b></span>`).join("");
    const wrap = document.getElementById("tasks");
    if (!d.tasks.length) { wrap.innerHTML = '<div class="empty">sem atividade na janela</div>'; return; }
    wrap.innerHTML = d.tasks.map(t => `
      <div class="task">
        <div class="row1">
          <span class="tid">${esc(t.id)}</span>
          <span class="title">${esc(t.title)}</span>
          <span class="badge st-${esc(t.status)}">${esc(t.status)}</span>
        </div>
        <div class="row2">
          ${esc(t.project || "—")} · <b>${esc(t.skill || "—")}</b> · ${esc(t.assignee || "—")}
          ${t.quality_score != null ? ` · score <b>${t.quality_score}</b>` : ""}
          ${t.actual_tokens ? ` · ${Number(t.actual_tokens).toLocaleString()} tok` : ""}
          · ${fmtAgo(t.updated_at)} atrás
        </div>
        ${t.steps.length ? `<div class="steps">` + t.steps.map(s =>
            `<span class="chip ${esc(s.status)}">${esc(s.step)} · ${fmtAgo(s.at)}</span>`
          ).join("") + `</div>` : ""}
        ${t.resumable ? `<div class="resume">⟳ output pago no journal — finalize será replayed no próximo pulse (N2)</div>` : ""}
      </div>`).join("");
  } catch (e) {
    document.getElementById("live").style.color = "var(--bad)";
    document.getElementById("meta").textContent = "runtime inacessível — retry em 3s";
  }
}
refresh();
setInterval(refresh, 3000);

// SSE live ticker (best-effort enhancement; polling above is the source of truth)
try {
  const es = new EventSource("/events");
  es.onmessage = ev => {
    const box = document.getElementById("ticker");
    const line = document.createElement("div");
    line.textContent = new Date().toLocaleTimeString("pt-PT") + "  " + ev.data;
    box.prepend(line);
    while (box.children.length > 6) box.removeChild(box.lastChild);
  };
} catch (e) { /* SSE indisponível — polling continua */ }
</script>
</body>
</html>
"""
