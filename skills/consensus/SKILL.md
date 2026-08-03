---
name: consensus
description: "Read-only second opinions from external models. Tries installed CLI agents first; falls back to `~/.claude/bin/ask.sh` (DeepSeek, Kimi, Grok, GPT, Gemini, Mistral, Perplexity) when CLI auth fails. Use when the user explicitly asks for `/consensus` or when the request clearly matches this command."
allowed-tools: Read, Grep, Glob, Bash
---

# /consensus

Read-only second opinions from external models. Three transports, in order of preference.

## Contract

- Primary route: `detect-transports -> fan-out -> compare -> synthesize`
- Suggested handoffs: /doubt, /team, /thinkagain
- Category: `consensus`
- Read only: `yes`
- Uses parallelism: `yes`
- Uses external agents: `yes`
- First principles: `no`

## Transport priority

Try in this order; skip silently on failure and fall through.

### 1. Installed CLI agents (preferred: they have repo context)

| Agent | Command | Detect with |
|-------|---------|-------------|
| Codex | `codex exec --skip-git-repo-check -c 'sandbox_mode="read-only"' "$PROMPT"` | `which codex` (slow — allow 300s+) |
| ~~Gemini~~ | **DEAD on beast (2026-06-22): `IneligibleTierError`, Google retired the free individual tier. Route Gemini via `ask.sh gemini` (transport 2) — the gateway's gemini is also broken, see below.** | — |
| Cursor | `cursor-agent --print --trust --output-format text "$PROMPT"` | `which cursor-agent` |

CLI agents see the project's CLAUDE.md and can grep the codebase, so their answers carry context the API path can't replicate. Worth the first attempt even when auth is flaky. **Cursor headless needs `--trust`** (or `-f`/`--yolo`) or it aborts with "Workspace Trust Required."

**Common failure modes** (skip and fall through to API path):
- `Authentication required` / `token expired` / `refresh token already used`: the OAuth-style CLIs lose state regularly. Don't try to re-auth from inside the skill; just fall through.
- `IneligibleTierError` / "no longer supported for Gemini Code Assist for individuals": the **gemini CLI is permanently dead on beast** (Antigravity migration, 2026-06-22) — not transient. Don't detect it at all; use `ask.sh gemini` instead.
- `Quota exceeded` / HTTP 429: free tiers can be 0/day. Fall through.
- Process exits with a non-zero code and no useful stdout.

### 2. `ask.sh` — the shared provider table (the reliable fallback)

`~/.claude/bin/ask.sh` owns the routing. It maps a provider name to a transport (gateway,
OpenRouter, or direct) plus a current model id, and prints plain text on stdout. Use it instead of
hand-rolled `curl`: it is the same table behind `/deepseek`, `/kimi`, `/grok` and friends, so a
rotted model id gets fixed in one place for every caller.

```bash
~/.claude/bin/ask.sh deepseek "<PROMPT>"
~/.claude/bin/ask.sh --list      # the provider table
~/.claude/bin/ask.sh --health    # auth + balances for every route
```

Pick a diverse 2–3. Diversity matters more than model size for consensus: one OpenAI + one xAI +
one DeepSeek catches more disagreement than three OpenAI variants.

| Provider arg | Routes via | Model (verified 2026-08-03) |
|---|---|---|
| `deepseek` | OpenRouter | `deepseek/deepseek-v4-pro` |
| `deepseek-flash` | OpenRouter | `deepseek/deepseek-v4-flash` — pennies, good for bulk verdicts |
| `kimi` | OpenRouter | `moonshotai/kimi-k3` |
| `grok` | gateway | `grok-4.3` |
| `gpt` | gateway | `gpt-5.4` |
| `mistral` | gateway | `mistral-large-latest` |
| `cohere` | gateway | gateway picks |
| `gemini` | direct | `gemini-3-flash-preview` |
| `perplexity` | direct | `sonar-pro` — web-grounded; **flat $0.005/request** on top of tokens |
| `claude` | gateway | `claude-sonnet-4-6` |

**Skip `claude` in self-consensus by default.** You're Claude: asking another Claude is the weakest
signal. Reach for it only when the user explicitly wants a Claude-family check.

Run the chosen providers in parallel via background `Bash` calls, then aggregate.

### 3. dr.eamer.dev gateway via the `dreamer` CLI (reliable, server-keyed)

The gateway holds server-side keys for seven providers, and `ask.sh` already routes `grok`, `gpt`,
`mistral`, `cohere` and `claude` through it — so transport 2 covers the gateway for you. Reach for
the `dreamer` CLI directly only when you want a raw route or gateway-quota accounting.

```bash
dreamer ask "<PROMPT>" -p xai      # or: openai | mistral | anthropic | cohere
```

**Verified against the live gateway 2026-08-03 — do not trust the older provider list:**

- **Working:** `xai`, `openai`, `mistral`, `anthropic`, `cohere`.
- **`groq` is gone.** No server key (`GROQ_API_KEY is required`); the local var was removed too.
  Any older advice to use `-p groq` for cheap throwaway checks is dead — use `ask.sh deepseek-flash`.
- **`gemini` is broken** at the gateway (returns no valid `Part`). Use `ask.sh gemini`, which goes direct.
- **`perplexity` and `ollama` 500** at the gateway. Use `ask.sh perplexity`, which goes direct.

Rate limit 10,000 requests/day. It spends real money on the server's keys, and exposes **no balance
endpoint** — `ask.sh --health` can prove liveness but never remaining credit. Detect with
`which dreamer` (or `dreamer health`).

## Procedure

1. **Frame the question once.** Write a single compact prompt that asks for verdicts in a tight format ("number, AGREE/DISAGREE/WAIT, one-line reason"). Save to `/tmp/consensus-<topic>.txt` so each transport gets identical input.

2. **Detect transports.** Run `which codex cursor-agent dreamer` plus `[ -x ~/.claude/bin/ask.sh ]`. Note what's available. Don't probe `gemini` — the CLI is dead; reach Gemini via `ask.sh gemini`.

3. **Fan out in parallel.** Pick 2–4 voices favouring CLI agents first. Launch each as a background `Bash` task so the skill returns control while they work.

4. **Wait for completions.** Background-task notifications arrive as system events. Don't poll.

5. **Compare results.** For each finding/question, group verdicts. Note unanimous agreement, splits, and any unique objections. **Preserve dissent**: never collapse a 2-1 split into "the consensus is X."

6. **Report.** Short summary with one row per question, columns for each respondent. Add a "Notable" section for any objection that named a concrete failure mode.

## Output format

```markdown
## Consensus on <topic>

**Voices:** <list with model name and transport>
**Skipped:** <auth-failed agents, with reason>

| # | Question | Codex | Grok-4-fast | GPT-5-mini | Verdict |
|---|----------|-------|-------------|------------|---------|
| 1 | … | AGREE | AGREE | AGREE | unanimous AGREE |
| 2 | … | AGREE | DISAGREE (…) | WAIT | split: see below |

### Notable objections
- **Grok on #2**: <reason>. <Whether to act on it>.
```

## Anti-patterns

- **Don't paste API keys into log messages or commits.** Never read a key value at all — `ask.sh` reads them from the environment so you never have to handle one.
- **Don't retry on auth failure.** The CLIs keep state across sessions; if they're stale, they'll keep being stale until the user re-auths.
- **Don't fan out to 5+ voices.** The aggregation cost outgrows the signal. Pick 2–4 with diverse provenance.
- **Don't ask the same model twice in different costumes** (e.g. GPT-5 via OpenAI and GPT-5 via OpenRouter). Diversity is the point.
- **Don't hand-roll `curl` against a provider.** `ask.sh` is the one routing table; a second copy of a model id somewhere else is how the table rots. Add a row there instead.
- **Don't burn a flagship on a throwaway check.** `ask.sh deepseek-flash` costs ~$0.09 per million input tokens. Reserve `gpt`/`gemini`/`claude` for verdicts that earn it, and remember `perplexity` bills a flat $0.005 per request regardless of size.

## Notes

- This skill is read-only. Never let an external model's reply trigger an edit. Synthesize, present, and let the user decide.
- **Credentials live in the environment**, exported from `~/.zshenv` locally and `/etc/dreamer/secrets.env` on the server. `ask.sh` reads them; you never touch a key value. (An older version of this skill named `~/documentation/API_KEYS.md` as the source — **that file does not exist**, on any host.)
- Knowledge cutoff drift: model names age fast. If a model name returns a 404 or "model not found", run `ask.sh --health` — it exercises every route and surfaces retired ids — then fix the table in `~/.claude/bin/ask.sh`.
