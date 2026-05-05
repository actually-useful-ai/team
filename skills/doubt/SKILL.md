---
name: doubt
description: "Targeted challenge to the current approach with explicit alternatives. Use when the user explicitly asks for `/doubt` or when the request clearly matches this command."
allowed-tools: Read, Grep, Glob
---

# /doubt

Targeted challenge to the current approach with explicit alternatives.

## Contract

- Primary route: `inspect -> parallel-challenge -> compare -> synthesize`
- Suggested handoffs: /thinkagain, /team, /consensus
- Category: `reconsideration`
- Read only: `yes`
- Uses parallelism: `yes`
- Uses external agents: `no`
- First principles: `no`

## Guidance

- Focuses on the current frame rather than rebuilding from scratch.
- Should compare the active direction against at least one viable alternative.
- Output should be terse: a one-paragraph statement of the active direction, a one-paragraph alternative, a side-by-side risk comparison, a recommendation with confidence.
- Do not pretend to reconsider from first principles; that is `/thinkagain`'s job. `/doubt` accepts the current frame and challenges within it.
