---
name: business
description: "Just the business committee of /team: marketing + legal + manager. Skips technical and skeptics. Use when you only want the audience + positioning + monetization + IP picture."
allowed-tools: Read, Grep, Glob, Bash, Agent, WebSearch, WebFetch
---

# /team:business

Routes to the `team` skill with `--business` scope. Runs research (recon + scout) plus the Business committee only:

- `marketing` — audience, positioning, GTM, pricing (Moore + Dunford + JTBD + Bullseye)
- `legal` — IP, licensing, can-this-actually-be-sold
- `manager` — maintenance cost, debt, runway (SQALE, Cunningham/Fowler)

Skips Technical and Skeptics committees. Output is a focused Business report rather than a full pitch with adversarial review.

See `skills/team/SKILL.md` for the full council protocol. This skill is a scope shortcut.

## Procedure

1. Treat input as a path or question per `/team:team` routing.
2. Skip the Technical and Skeptics committees.
3. Run Research (recon + scout) and Business committee in parallel.
4. Produce a Business report (not a full executive verdict):
   - Audience and positioning
   - Monetization plausibility with comparable references
   - Legal posture (license-compatible monetization)
   - Maintenance cost (SQALE-style breakdown)
   - Internal disagreement among the three Business seats

## Handoffs

`/team:team` for the full council. `/team:technical` for the engineering reality check. `/team:skeptics` to attack the resulting business case.
