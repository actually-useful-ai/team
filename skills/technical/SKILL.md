---
name: technical
description: "Just the technical committee of /team: architect + greybeard + safety + tester. Skips the skeptics committee and the legal check. Use when you only want the engineering reality check."
allowed-tools: Read, Grep, Glob, Bash, Agent
---

# /team:technical

Routes to the `team` skill with `--technical` scope. Runs research (recon + scout) plus the Technical committee only:

- `architect` — fit with existing patterns
- `greybeard` — old-engineer scaling/ops review (Google SRE Book ch 22, four golden signals, Brendan Gregg's USE method)
- `safety` — failure recovery, fallbacks, graceful degradation
- `tester` — verification, regression criteria

Skips the Skeptics committee and the legal check. Output is a focused Technical report.

See `skills/team/SKILL.md` for the full council protocol. This skill is a scope shortcut.

## Procedure

1. Treat input as a path or question per `/team:team` routing.
2. Skip the Skeptics committee and the legal check.
3. Run Research (recon + scout) and Technical committee in parallel.
4. Produce a Technical report (not a full executive verdict):
   - Architectural fit (architect's verdict, migration cost)
   - Scaling and ops (greybeard's verdict, what breaks at 10x)
   - Failure recovery (safety's verdict, recovery paths)
   - Verification (tester's strategy)
   - Internal disagreement among the four Technical seats

## Handoffs

`/team:team` for the full council. `/team:skeptics` to attack the resulting technical plan.
