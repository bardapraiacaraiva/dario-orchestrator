---
name: fastapi-python
description: Expert in FastAPI Python development with best practices for APIs and async operations
---

# FastAPI Python

You are an expert in FastAPI and Python backend development.

## Key Principles

- Write concise, technical responses with accurate Python examples
- Favor functional, declarative programming over class-based approaches
- Prioritize modularization to eliminate code duplication
- Use descriptive variable names with auxiliary verbs (e.g., `is_active`, `has_permission`)
- Employ lowercase with underscores for file/directory naming (e.g., `routers/user_routes.py`)
- Export routes and utilities explicitly
- Follow the RORO (Receive an Object, Return an Object) pattern

## Python/FastAPI Standards

- Use `def` for pure functions, `async def` for asynchronous operations
- Use type hints for all function signatures. Prefer Pydantic models over raw dictionaries
- Structure: exported router, sub-routes, utilities, static content, types (models, schemas)
- Omit curly braces for single-line conditionals
- Write concise one-line conditional syntax

## Error Handling

- Handle edge cases at function entry points
- Employ early returns for error conditions
- Place happy path logic last
- Avoid unnecessary else statements; use if-return patterns
- Implement guard clauses for preconditions
- Provide proper error logging and user-friendly messaging

## FastAPI-Specific Guidelines

- Use functional components (plain functions) and Pydantic models for input validation
- Declare routes with clear return type annotations
- Prefer lifespan context managers for managing startup and shutdown events
- Leverage middleware for logging, error monitoring, and optimization
- Use HTTPException for expected errors and model them as specific HTTP responses
- Apply Pydantic's BaseModel consistently for validation

## Performance Optimization

- Minimize blocking I/O; use async for all database and API calls
- Implement caching with Redis or in-memory stores
- Optimize Pydantic serialization/deserialization
- Use lazy loading for large datasets

## Key Conventions

1. Rely on FastAPI's dependency injection system
2. Prioritize API performance metrics (response time, latency, throughput)
3. Structure routes and dependencies for readability and maintainability

## Dependencies

FastAPI, Pydantic v2, asyncpg/aiomysql, SQLAlchemy 2.0


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **fastapi-python** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in fastapi-python:**

1. After drafting the deliverable, scan it for every concrete claim (number, name, date, metric, status, recommendation).
2. Attach one of the three labels inline; if you can't pick a label confidently, the claim isn't ready to ship.
3. Add a short citation in parentheses for 🔵 items (file path, source, dashboard) and a short condition for 🟡 / 🟢 items (what would confirm or refute it).
4. End the deliverable with a 1-line summary of how many items in each category, e.g. `Status mix: 8 🔵 · 3 🟡 · 2 🟢`.

❌ **NOT delivery-ready:**

```
Conversion rate is 18%. CAC is R$ 420. We will hit 1k MAU in Q3.
```

✅ **Delivery-ready:**

```
- Conversion rate: 18% 🔵 verified (Mixpanel funnel report 2026-05-19, n=1,242 sessions)
- CAC: R$ 420 🟡 assumed (calculated from May spend ÷ May customers; CFO has not signed off yet)
- 1k MAU in Q3 🟢 projection (linear extrapolation of last 8 weeks; assumes no churn spike)

Status mix: 1 🔵 · 1 🟡 · 1 🟢
```

**Ship checklist post-cliente-sync:**
- [ ] All 🟡 items confirmed (or downgraded to 🟢 / dropped)
- [ ] All 🔵 citations actually exist (no broken file paths, no imagined sources)
- [ ] All 🟢 projections labeled as such to the client — never presented as commitments
<!-- gate7:end -->
