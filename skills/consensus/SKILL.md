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

1. Detect native Claude Code, Grok, Ollama, and Claude Code configured for Z.ai.
   Treat command presence as a lead, not proof of working authentication.
   These four native CLI routes are the consultation providers; do not use
   direct API requests, a gateway, or OpenAI/Luna as a substitute.
2. If `craft-ask` is available, run `craft-ask --list` and
   `craft-ask --status`. These commands make no inference calls. The versioned
   Craft route table is authoritative; do not copy its model IDs here.
3. When Craft is unavailable, use native read-only agents only and state the
   limitation. Use each installed CLI's documented noninteractive mode with
   tools disabled, a scratch working directory, stdin prompts, and a timeout.
   Keep Z.ai credentials/config separate from the ordinary Claude login. If
   these constraints cannot be enforced, report that route unavailable. Team
   remains independently usable and must not depend on a private Craft path.

Use `craft-ask --probe PROVIDER` only for explicit single-route diagnosis; it
makes a paid call. There is no all-provider health sweep.

## Procedure

1. Frame one compact prompt asking each voice for the same numbered verdicts,
   confidence, one-line reason, and strongest objection.
2. Choose two or three genuinely diverse voices among `claude`, `grok`, `zai`,
   and `ollama`. In Claude, prefer Grok and Z.ai; in Codex/OpenAI, prefer Claude
   and Grok. Respect explicitly named routes. `anthropic`/`claude` and
   `xai`/`grok` are aliases, never separate votes. Z.ai uses GLM through the
   Claude executable; executable name does not establish model family. Check
   Ollama's selected model family and remote/cloud status before disclosure.
   Two aliases or hosts running the same underlying model do not add diversity.
3. Launch independent calls in parallel. For Craft routes, pass the prompt on
   stdin with `craft-ask --json PROVIDER -` so prompt text is not shell-interpolated.
4. Record the actual provider/model provenance reported by each response.
   Keep `requested_model` separate from `model`; `requested-only` answers have
   unverified identity and cannot count as verified independent model votes.
   Present those answers separately as advisory material. Failed or mismatched
   routes stay failed; do not relabel or silently replace them.
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
authority over their evidence. Missing Craft degrades
to native read-only agents rather than failing the council. Missing credentials
leave that voice unavailable; they do not authorize a different transport.

## Anti-patterns

- More than four voices; aggregation cost overtakes new signal.
- Retrying authentication or quota failures inside the skill.
- Copying provider model IDs or hand-rolling provider requests.
- Passing raw `$ARGUMENTS`, secrets, or repository contents through a shell
  command line.
- Treating an outside answer as measured evidence without verification.
