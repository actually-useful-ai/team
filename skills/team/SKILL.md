---
name: team
description: "Codebase-assessment council. A 10-seat team across three subcommittees plus a standalone legal red-flag check turns code into a defensible technical assessment with adversarial review, kill criteria, and a verification plan."
allowed-tools: Read, Grep, Glob, Bash, Agent, WebSearch, WebFetch
---

# /team

Take a codebase. Hand it to the team. Get back an assessment you can defend.

<HARD-GATE>
This is a read-only skill. The team produces a verdict; it never edits the codebase. If a seat suggests a code change, route it through `/elegance` instead.
</HARD-GATE>

## Routing

`/team` accepts a path, a question, or a scope flag:

- **A path** (`/team src/`, `/team ~/projects/whatcolor`): assess this codebase.
- **No args** (`/team`): if the input is ambiguous, use AskUserQuestion to pick a scope (full council vs. one committee). If unambiguous, assess the current working directory in full mode.
- **A quoted question** (`/team "Should I open-source this?"`): team debates the question with the codebase as context.

### Scope flags (limit which committees run)

| Flag | What runs | Use when |
|------|-----------|----------|
| `--full` (default) | Both committees + legal check + executive synthesis | You want the whole assessment with adversarial review |
| `--technical` | Research + Technical committee only (architect/greybeard/safety/tester) | You only want the engineering reality check |
| `--skeptics` | Research + Skeptics committee only (breaker/cynic) | You want the proposal attacked but already drafted it elsewhere |
| `--research` | Recon + scout only | You want the facts (codebase map + prior-art context) without verdicts |
| `--no-skeptics` | Skip skeptics committee | You want technical fit + legal red flags without the adversarial counterweight |

Sub-flag aliases: `--tech`, `--skep`, `--rsrch`. Companion commands: `/team:technical`, `/team:skeptics`, `/team:research` are thin wrappers for the scope flags.

### Decision picker

When `/team` is called with no args AND the cwd is small/ambiguous (say, fewer than 5 source files), the executive opens an AskUserQuestion picker offering:
- Full council
- Technical committee only
- Skeptics only (attack an existing proposal)
- Research only (just the facts)

The picker is for ergonomics; experienced users skip it by passing a flag.

Detection: file/directory path → assess mode. Quoted text or text containing a question mark → debate mode. Scope flags override scope but don't change assess vs. debate mode.

---

## Council protocol

### Phase 1: Frame

The executive runs this phase.

1. **Detect scope** from input flags. Default `--full` if none given. If no args at all, optionally open the decision picker.
2. **Restate the input** in one sentence: what is the team being asked to assess or decide?
3. **Define acceptance criteria**: what would a good answer include? For assess mode, default criteria: architectural fit, top three risks, kill criteria, verification rigor, legal red flags, internal consistency. For partial-scope runs, drop the criteria that the skipped committee would have produced.
4. **Detect consultants**: run `which codex gemini cursor-agent`, check `~/documentation/API_KEYS.md` for `XAI_API_KEY`, `OPENAI_API_KEY`, `MISTRAL_API_KEY`, `PERPLEXITY_API_KEY`. Note which seats can fan out and which run alone.
5. **Announce the team**: list the seats that will run for the chosen scope, note any that lose their consultants.

### Scope filtering

Based on the flag, the executive runs only the relevant committees:

| Scope | Phase 2 | Phase 3 |
|-------|---------|---------|
| `--full` | recon + scout | Technical + Skeptics + legal check |
| `--technical` | recon + scout | Technical only |
| `--skeptics` | recon (skip scout if proposal already drafted) | Skeptics only |
| `--research` | recon + scout | (skip Phase 3 entirely; output is just the facts) |
| `--no-skeptics` | recon + scout | Technical + legal check (skip Skeptics) |

Phase 4 synthesis adapts: a single-committee scope produces a focused report rather than the full executive verdict. `--research` skips synthesis entirely and outputs a research-bundle.

### Phase 2: Research (parallel, no opinions)

Launch in parallel:

- `recon`: internal codebase map (languages, deps, public surfaces, patterns, deployment context).
- `scout`: external prior art scan. May consult Perplexity (web), Gemini (broad knowledge).

Wait for both to complete before Phase 3.

### Phase 3: Committees (parallel, opinions allowed)

Two committees plus a standalone legal check run in parallel. Each committee has its own internal chair (which is the seat itself for single-seat committees, or designated below) that produces ONE synthesized report for that committee.

**Technical committee** (chair: architect)
- `architect`: fit with existing patterns.
- `greybeard`: old-engineer review of scaling, ops, what breaks at 10x. Encodes Google SRE Book ch 22, four golden signals, Brendan Gregg's USE method. May consult Codex, Grok.
- `safety`: failure recovery, fallbacks.
- `tester`: verification, regression criteria.

Output: one Technical committee report covering fit, scaling risks, failure recovery, and verification.

**Skeptics committee** (chair: cynic)
- `breaker`: adversarial attack on the proposal (concrete failure scenarios only).
- `cynic`: pre-mortem (Klein 2007), kill criteria (Annie Duke), Amazon working-backwards critique. Must always dissent. May consult `/consensus` for a full external panel.

Output: one Skeptics committee report covering top attacks, kill criteria, and the strongest counterargument the rest of the team is ignoring.

**Legal check** (standalone, no committee)
- `legal`: IP, licensing, attribution. Reports a short list of license/IP red flags (or an all-clear) directly to the executive — blockers that would stop the project from being shipped or open-sourced. Not a committee; not market positioning.

Output: a red-flag list (or all-clear) that the executive folds into the verdict's legal section.

Each seat produces:

```
- **Claim**: [one sentence]
- **Mechanism**: [how/why, with concrete specifics]
- **Risks**: [what could go wrong with this claim]
- **Evidence**: [code refs, sources, frameworks cited]
```

Each committee chair synthesizes into:

```
## [Committee] report
**Top finding:** [one sentence]
**Supporting:** [the seats' core findings, deduplicated]
**Internal disagreement:** [where seats disagreed; never flatten]
**Confidence:** high | medium | low
```

### Phase 4: Verdict

The executive reads the reports (Research, Technical, Skeptics) plus the legal red-flag list, and produces the final assessment using the rubric:

| Criterion | Weight |
|-----------|--------|
| Risk identification | 25% |
| Architecture fit | 20% |
| Actionability | 15% |
| Verification rigor | 15% |
| Legal red flags | 15% |
| Internal consistency | 10% |

Then `editor` humanizes the verdict (post-verdict only: never influences the decision).

---

## Output format

```markdown
## Decision: [one-line summary]

### The assessment
**What it is:** [what the codebase actually does, in one paragraph]
**Where it fits:** [architect's read on how it lives and what it costs to maintain]
**What it's good for:** [the strongest defensible use, grounded in the code]
**First three moves:** [concrete next steps]

### Key evidence
- Recon: [internal facts that anchor the assessment]
- Scout: [external prior art and comparable projects]

### Risk assessment
- [Top three risks with severity and concrete failure mode]
- [Greybeard's scaling/ops concerns]
- [Breaker's strongest attack]

### Kill criteria
- Ship-blocker: [specific condition that says "do not ship"]
- Pivot-trigger: [signal that says "change direction"]
- Sunset-trigger: [signal that says "stop maintaining"]

### Verification plan
[Tester's strategy for proving the assessment is real, not folklore: A/B baseline, regression gates, golden samples]

### Architecture fit
[Architect's assessment of where this lives and what it costs to maintain]

### Legal red flags
[Legal seat's license/IP blockers, or all-clear]

### Dissenting opinions
- **Cynic**: [the strongest counterargument the rest of the team would prefer to ignore]
- [Any unresolved disagreement between committees]

### Consultants consulted
- [Which external models were reachable, what they added, what was unreachable]
```

---

## Protocol rules

1. **Facts outrank precedent. Precedent outranks taste.**
2. **Every criticism includes a concrete failure mode.** Vague concerns expire.
3. **Cynic must always dissent.** Names the strongest counterargument even when the consensus is correct.
4. **Editor is post-verdict only.** Never shapes the decision.
5. **No agent speaks twice until all seated agents have spoken once.**
6. **Scout must explain why a pattern transfers**: not just that it's popular.
7. **Dissenting opinions are always preserved.** Never flattened into false consensus.
8. **Consultants are best-effort.** Try CLI first (free quota), fall through to API, fall through to "consultant unavailable." A seat without its consultant still reports: it just notes the gap.

## Consultant detection (Phase 1 helper)

```bash
# CLIs (free quota, repo-context)
which codex gemini cursor-agent

# API keys (paid, no repo context)
eval "$(grep -E '^export ' ~/documentation/API_KEYS.md)" 2>/dev/null
for var in XAI_API_KEY OPENAI_API_KEY MISTRAL_API_KEY PERPLEXITY_API_KEY; do
    [ -n "${!var}" ] && echo "  ✓ $var"
done
```

A seat declares its preferred consultants in its agent file. The skill calls them in parallel via background `Bash`. If all consultants for a seat fail, the seat reports without external priors and notes the gap in its findings.

## When to use `/team` vs other skills

- **`/team`**: you want a defensible assessment of a codebase with adversarial review.
- **`/extract`**: quick single-pass assessment when you don't need the council.
- **`/elegance`**: code refinement or generic council debate.
- **`/doubt`**: challenge a single decision, not assess a whole codebase.
- **`/consensus`**: second opinions only, no synthesis.
