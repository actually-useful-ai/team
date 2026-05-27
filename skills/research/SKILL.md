---
name: research
description: "Just the research phase of /team: recon (internal codebase map) + scout (external prior art, ecosystem context). No verdicts, no opinions."
allowed-tools: Read, Grep, Glob, Bash, Agent, WebSearch, WebFetch
---

# /team:research

Routes to the `team` skill with `--research` scope. Runs Phase 2 only:

- `recon` — internal codebase map (languages, deps, public surfaces, patterns, deployment context)
- `scout` — external prior art scan (comparable projects, technical approaches, transfer test)

No committee debate. No executive synthesis. Output is the facts the rest of the team would have used.

See `skills/team/SKILL.md` for the full council protocol. This skill is a scope shortcut.

## When to use

- You want a clean codebase map and prior-art scan without a verdict.
- You're going to write the assessment yourself and want raw inputs.
- You're about to launch a full `/team:team` and want to inspect the research first.
- Quick "what's out there" reconnaissance for a side question.

## Procedure

1. Treat input as a path or topic.
2. Run recon and scout in parallel.
3. Output:
   - Recon's claim/mechanism/evidence (codebase facts)
   - Scout's claim/mechanism/evidence (comparables, ecosystem context, transfer-test reasoning)
   - Gaps either flagged in their mapping
4. No synthesis, no committee.

## Handoffs

`/team:team` for the full council using these facts. `/team:technical` or `/team:skeptics` for a single-committee follow-up.
