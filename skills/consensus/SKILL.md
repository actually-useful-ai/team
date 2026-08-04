---
name: consensus
description: "Collect and compare bounded read-only opinions from external models. Use when Luke explicitly asks for consensus, multiple outside-model views, or external fan-out on a question."
allowed-tools: Read, Grep, Glob, Bash, Agent
---

# /consensus

Collect a small, diverse set of outside opinions, preserve disagreement, and
return advisory evidence. This skill never edits the target and never lets an
outside response trigger an action on its own.

## Authorization and disclosure

Explicit `/consensus`, outside-model, or external fan-out wording authorizes the
bounded calls needed for this skill. A normal `/team` run does not. Before a
call, reduce repository context to the smallest useful brief. Never send
credentials, private keys, broad directory contents, or an entire repository.

Provider calls may incur usage charges. Do not run broad liveness sweeps or
silently replace a failed provider with another one.

## Transport discovery

1. Detect useful installed read-only CLI agents for repository-aware opinions.
   Treat command presence as a lead, not proof of working authentication.
2. If `craft-ask` is available, run `craft-ask --list` and
   `craft-ask --status`. These commands make no inference calls. The versioned
   Craft route table is authoritative; do not copy its model IDs here.
3. When Craft is unavailable, use native read-only agents only and state the
   limitation. Team remains independently usable and must not depend on a
   private Craft filesystem path.

Use `craft-ask --probe PROVIDER` only for explicit single-route diagnosis; it
makes a paid call. There is no all-provider health sweep.

## Procedure

1. Frame one compact prompt asking each voice for the same numbered verdicts,
   confidence, one-line reason, and strongest objection.
2. Choose two or three genuinely diverse voices. In Claude, prefer Grok and
   OpenAI routes; in Codex/OpenAI, prefer Anthropic and Grok routes. Do not ask
   the current model family twice in different costumes.
3. Launch independent calls in parallel. For Craft routes, pass the prompt on
   stdin with `craft-ask PROVIDER -` so prompt text is not shell-interpolated.
4. Record the actual provider/model provenance reported by each response.
   Failed or mismatched routes stay failed; do not relabel them.
5. Group answers by question. Distinguish unanimous agreement, splits, and
   unresolved objections. Never flatten a majority into false consensus.
6. Verify any load-bearing factual claim before presenting it as established.

## Output

```markdown
## Consensus on <topic>

**Voices:** <actual provider/model labels>
**Unavailable:** <route and classified reason>

| # | Question | Voice A | Voice B | Voice C | Result |
|---|---|---|---|---|---|
| 1 | ... | AGREE | DISAGREE | WAIT | split |

### Notable objections
- **<voice> on #1:** <concrete failure mode and whether it changes the decision>
```

## Composition

Consensus is an advisory evidence provider for `/team`; the executive retains
the verdict and preserves dissent. Craft's Ask owns provider routing and model
truth when installed. Domain, accessibility, legal, and security skills retain
authority over their evidence. Missing Craft or provider credentials degrades
to native read-only agents rather than failing the council.

## Anti-patterns

- More than four voices; aggregation cost overtakes new signal.
- Retrying authentication or quota failures inside the skill.
- Copying provider model IDs or hand-rolling provider requests.
- Passing raw `$ARGUMENTS`, secrets, or repository contents through a shell
  command line.
- Treating an outside answer as measured evidence without verification.
