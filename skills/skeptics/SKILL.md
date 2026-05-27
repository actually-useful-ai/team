---
name: skeptics
description: "Just the skeptics committee of /team: breaker + cynic. Use when you have a draft assessment and want it stress-tested with attacks, kill criteria, and a pre-mortem."
allowed-tools: Read, Grep, Glob, Bash, Agent
---

# /team:skeptics

Routes to the `team` skill with `--skeptics` scope. Runs research (recon, optionally scout) plus the Skeptics committee only:

- `breaker` — adversarial attack on the assessment with concrete failure scenarios
- `cynic` — Klein pre-mortem, Annie Duke kill criteria, Amazon working-backwards critique. Must always dissent.

Skips the Technical committee and the legal check. Best for stress-testing a draft assessment you already wrote (yourself or via `/team:technical`).

See `skills/team/SKILL.md` for the full council protocol. This skill is a scope shortcut.

## Procedure

1. Treat input as a path, draft assessment, or question per `/team:team` routing.
2. Skip the Technical committee and the legal check.
3. Run minimal Research (recon; skip scout if the assessment is already drafted) and the Skeptics committee.
4. Produce a Skeptics report:
   - Pre-mortem narrative (the failure story)
   - Kill criteria: ship-blocker, pivot-trigger, sunset-trigger
   - Top three attacks (breaker's strongest, with severity)
   - Strongest counterargument the rest of the team would prefer to ignore (cynic's required dissent)
   - README / 6-pager critique if applicable

## Handoffs

`/team:team` for full council with synthesis. `/team:technical` to redraft the assessment addressing the attacks.
