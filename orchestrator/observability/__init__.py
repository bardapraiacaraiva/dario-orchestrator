"""DARIO observability — dashboards, telemetry, tracing.

generate_dashboard.py: builds dashboard.html (auto-gen)
cognitive_dashboard.py: dashboard widget aggregator
weekly_summary.py: weekly rollup to Obsidian
otel_setup.py: OpenTelemetry config
span_tracer.py, tracer.py: lightweight tracing
token_meter.py: per-task token accounting

Most are CLI/subprocess-driven (called by cron, hook, or run_engine), so
direct python imports of these are rare. Moving here keeps top-level clean.
"""
