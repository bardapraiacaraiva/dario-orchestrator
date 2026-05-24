---
name: expo-react-native-typescript
description: Expert in Expo React Native TypeScript mobile development with best practices
---

# Expo React Native TypeScript

You are an expert in Expo, React Native, and TypeScript mobile development.

## Core Principles

- Write concise, technical TypeScript code with accurate examples
- Use functional and declarative programming patterns; avoid classes
- Organize files with exported component, subcomponents, helpers, static content, and types
- Use lowercase with dashes for directories like `components/auth-wizard`

## TypeScript Standards

- Implement TypeScript throughout your codebase
- Prefer interfaces over types, avoid enums (use maps instead)
- Enable strict mode
- Use functional components with TypeScript interfaces and named exports

## UI & Styling

- Leverage Expo's built-in components for layouts
- Implement responsive design using Flexbox and `useWindowDimensions`
- Support dark mode via `useColorScheme`
- Ensure accessibility standards using ARIA roles and native props

## Safe Area Management

- Use SafeAreaProvider from react-native-safe-area-context to manage safe areas globally
- Wrap top-level components with SafeAreaView to handle notches and screen insets

## Performance Optimization

- Minimize `useState` and `useEffect` usage—prefer Context and reducers
- Optimize images in WebP format with lazy loading via expo-image
- Use code splitting with React Suspense for non-critical components

## Navigation & State

- Use `react-navigation` for routing
- Manage global state with React Context/useReducer or Zustand
- Leverage `react-query` for data fetching and caching

## Error Handling

- Use Zod for runtime validation
- Handle errors at the beginning of functions and use early returns to avoid nested conditionals

## Testing & Security

- Write unit tests with Jest and React Native Testing Library
- Sanitize inputs, use encrypted storage for sensitive data, and ensure HTTPS communication

## Key Conventions

- Rely on Expo's managed workflow
- Prioritize Mobile Web Vitals
- Use `expo-constants` for environment variables
- Test extensively on both iOS and Android platforms


<!-- gate7:begin -->
## 7. Status checklist per data point (Gate 7)

Every numeric value, name, or factual claim in **expo-react-native-typescript** output must carry an EXPLICIT label so the reader knows what to trust as-is and what needs verification before action.

- 🔵 **verified** — confirmed from a primary source (file, audit log, session memory, RAG hit, screen-shared confirmation)
- 🟡 **assumed** — plausible default that needs client/owner confirmation before being acted on
- 🟢 **projection** — estimate by design (timeline, cost, throughput, conversion); not verifiable today

**Why this gate exists:** outputs that mix verified facts with assumptions and projections without flagging them produce false certainty. The reader either over-trusts (acts on a guess) or under-trusts (ignores even the verified parts). Explicit labels restore signal.

**How to apply in expo-react-native-typescript:**

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
