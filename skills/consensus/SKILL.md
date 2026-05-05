---
name: consensus
description: "Read-only second opinions from external models. Tries installed CLI agents first; falls back to direct API calls (xAI Grok, OpenAI GPT-5, Mistral) when CLI auth fails. Use when the user explicitly asks for `/consensus` or when the request clearly matches this command."
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
| Codex | `codex exec --skip-git-repo-check -c 'sandbox_mode="read-only"' "$PROMPT"` | `which codex` |
| Gemini | `gemini -m gemini-2.5-pro -p "$PROMPT"` | `which gemini` |
| Cursor | `cursor-agent --print --output-format text "$PROMPT"` | `which cursor-agent` |

CLI agents see the project's CLAUDE.md and can grep the codebase, so their answers carry context the API path can't replicate. Worth the first attempt even when auth is flaky.

**Common failure modes** (skip and fall through to API path):
- `Authentication required` / `token expired` / `refresh token already used`: the OAuth-style CLIs lose state regularly. Don't try to re-auth from inside the skill; just fall through.
- `Quota exceeded` / HTTP 429: Gemini's free tier is 0/day in many configurations. Fall through.
- Process exits with a non-zero code and no useful stdout.

### 2. Direct API calls (the reliable fallback)

Source `~/documentation/API_KEYS.md` to populate the env vars, then `curl` directly. The file is markdown with prose plus `export X="..."` lines, so `source` chokes on the prose; extract just the exports:

```bash
eval "$(grep -E '^export ' ~/documentation/API_KEYS.md)" 2>/dev/null
```

(The `2>/dev/null` swallows harmless warnings from any multi-line PEM-key blocks; valid `export FOO="bar"` lines populate cleanly.)

Pick a diverse 2–3 from the table below. Diversity matters more than model size for consensus: one OpenAI + one xAI + one Mistral catches more disagreement than three OpenAI variants.

| Provider | Env var | Model recommendation (early 2026) | Endpoint |
|----------|---------|-----------------------------------|----------|
| xAI | `XAI_API_KEY` | `grok-4-fast` (fast, terse, good critic) | `https://api.x.ai/v1/chat/completions` |
| OpenAI | `OPENAI_API_KEY` | `gpt-5-mini` or `o3-mini` | `https://api.openai.com/v1/chat/completions` |
| Mistral | `MISTRAL_API_KEY` | `mistral-large-latest` | `https://api.mistral.ai/v1/chat/completions` |
| DeepSeek | `DEEPSEEK_API_KEY` | `deepseek-chat` | `https://api.deepseek.com/v1/chat/completions` |
| Perplexity | `PERPLEXITY_API_KEY` | `llama-3.1-sonar-large-128k-online` (when web context helps) | `https://api.perplexity.ai/chat/completions` |
| Anthropic | `ANTHROPIC_API_KEY` | `claude-sonnet-4-6` | `https://api.anthropic.com/v1/messages` |

**Skip Anthropic in self-consensus by default.** You're Claude: asking another Claude is the weakest signal. Reach for it only when the user explicitly wants a Claude family check, or when it's the only key available.

**Standard request shape** (OpenAI-compatible providers; xAI / Mistral / DeepSeek / Perplexity all accept this):

```bash
curl -s https://api.x.ai/v1/chat/completions \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-4-fast",
    "messages": [{"role": "user", "content": "<PROMPT>"}],
    "temperature": 0.2
  }' | python3 -c "import json,sys; print(json.load(sys.stdin)['choices'][0]['message']['content'])"
```

Anthropic uses a different shape:

```bash
curl -s https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4-6",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "<PROMPT>"}]
  }' | python3 -c "import json,sys; print(json.load(sys.stdin)['content'][0]['text'])"
```

Run all chosen providers in parallel via background `Bash` calls. Wait for completion notifications, then aggregate.

### 3. Local API gateway (low-priority backstop)

If `~/servers/api-gateway/` is reachable on `localhost:5200`, it offers a unified `/v1/llm` endpoint that proxies to multiple providers behind one rate limit. Useful when:

- The user wants the call accounted against the gateway's quota instead of personal API spend
- Multiple downstream agents need a single rate-limited shared budget

Detection:

```bash
curl -sf http://localhost:5200/health | grep -q healthy && echo "gateway up"
```

Endpoint discovery is at `http://localhost:5200/` (returns a JSON manifest of routes). Use only when transport 1 and 2 are both unavailable, or when the user explicitly asks for `--via-gateway`.

## Procedure

1. **Frame the question once.** Write a single compact prompt that asks for verdicts in a tight format ("number, AGREE/DISAGREE/WAIT, one-line reason"). Save to `/tmp/consensus-<topic>.txt` so each transport gets identical input.

2. **Detect transports.** Run `which codex gemini cursor-agent` plus `[ -f ~/documentation/API_KEYS.md ]`. Note what's available.

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

- **Don't paste API keys into log messages or commits.** The keys file is private; treat it as such.
- **Don't retry on auth failure.** The CLIs keep state across sessions; if they're stale, they'll keep being stale until the user re-auths.
- **Don't fan out to 5+ voices.** The aggregation cost outgrows the signal. Pick 2–4 with diverse provenance.
- **Don't ask the same model twice in different costumes** (e.g. GPT-5 via OpenAI and GPT-5 via OpenRouter). Diversity is the point.
- **Don't reach for the local gateway by default.** It rate-limits across the whole server's traffic; reserve for genuine need.

## Notes

- This skill is read-only. Never let an external model's reply trigger an edit. Synthesize, present, and let the user decide.
- The user's `~/documentation/API_KEYS.md` is the single source of API credentials. Source it; never hand-copy values.
- Knowledge cutoff drift: model names age fast. If a model name returns a 404 or "model not found", check the provider's models endpoint (`/v1/models`) before assuming the key is bad.
