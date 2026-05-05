---
name: team
description: "Codebase-to-pitch council. A 12-seat team across four subcommittees turns code into a product pitch with adversarial review, kill criteria, and a verification plan."
allowed-tools: Read, Grep, Glob, Bash, Agent, WebSearch, WebFetch
---

# /team

Take a codebase. Hand it to the team. Get back a pitch you can defend.

<HARD-GATE>
This is a read-only skill. The team produces a verdict; it never edits the codebase. If a seat suggests a code change, route it through `/elegance` instead.
</HARD-GATE>

## Routing

`/team` accepts:

- **A path** (`/team src/`, `/team ~/projects/whatcolor`): pitch this codebase.
- **No args** (`/team`): pitch the current working directory.
- **A quoted question** (`/team "Should I open-source this?"`): team debates the question with the codebase as context.

Detection: file/directory path → pitch mode. Quoted text or text containing a question mark → debate mode.

---

## Council protocol

### Phase 1: Frame

The executive runs this phase.

1. **Restate the input** in one sentence: what is the team being asked to pitch or decide?
2. **Define acceptance criteria**: what would a good answer include? For pitch mode, default criteria: audience specificity, monetization plausibility, top three risks, kill criteria, internal consistency, legal coherence, novelty over the obvious-pitch baseline.
3. **Detect consultants**: run `which codex gemini cursor-agent`, check `~/documentation/API_KEYS.md` for `XAI_API_KEY`, `OPENAI_API_KEY`, `MISTRAL_API_KEY`, `PERPLEXITY_API_KEY`. Note which seats can fan out and which run alone.
4. **Announce the team**: list the seats, note any that lose their consultants.

### Phase 2: Research (parallel, no opinions)

Launch in parallel:

- `recon`: internal codebase map (languages, deps, public surfaces, patterns, deployment context).
- `scout`: external prior art and market scan. May consult Perplexity (web), Gemini (broad knowledge).

Wait for both to complete before Phase 3.

### Phase 3: Committees (parallel, opinions allowed)

Three committees run in parallel. Each committee has its own internal chair (which is the seat itself for single-seat committees, or designated below) that produces ONE synthesized report for that committee.

**Business committee** (chair: marketing)
- `marketing`: audience, positioning, GTM, pricing. Encodes Moore (*Crossing the Chasm*), Dunford (*Obviously Awesome*), Jobs-to-be-Done, Bullseye. May consult Gemini, Grok.
- `legal`: IP, licensing, can-this-actually-be-sold.
- `manager`: maintenance cost, debt, runway. Encodes SQALE method, Cunningham/Fowler quadrant.

Output: one Business committee report covering audience, monetization, legal posture, and runway cost.

**Technical committee** (chair: architect)
- `architect`: fit with existing patterns.
- `greybeard`: old-engineer review of scaling, ops, what breaks at 10x. Encodes Google SRE Book ch 22, four golden signals, Brendan Gregg's USE method. May consult Codex, Grok.
- `safety`: failure recovery, fallbacks.
- `tester`: verification, regression criteria.

Output: one Technical committee report covering fit, scaling risks, failure recovery, and verification.

**Skeptics committee** (chair: cynic)
- `breaker`: adversarial attack on the pitch (concrete failure scenarios only).
- `cynic`: pre-mortem (Klein 2007), kill criteria (Annie Duke), Amazon working-backwards critique. Must always dissent. May consult `/consensus` for a full external panel.

Output: one Skeptics committee report covering top attacks, kill criteria, and the strongest counterargument the rest of the team is ignoring.

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

The executive reads the four reports (Research, Business, Technical, Skeptics) and produces the final pitch using the rubric:

| Criterion | Weight |
|-----------|--------|
| Audience specificity | 20% |
| Monetization plausibility | 15% |
| Risk identification | 20% |
| Actionability | 15% |
| Novelty vs. obvious-pitch baseline | 10% |
| Internal consistency | 10% |
| Legal coherence | 10% |

Then `editor` humanizes the verdict (post-verdict only: never influences the decision).

---

## Output format

```markdown
## Decision: [one-line summary]

### The pitch
**Product:** [what it is]
**Audience:** [specific buyer persona: role, budget, pain]
**Positioning:** [the obviously-awesome paragraph]
**Monetization:** [pricing model, comparable references]
**First three moves:** [concrete next steps]

### Key evidence
- Recon: [internal facts that anchor the pitch]
- Scout: [external prior art and market context]

### Risk assessment
- [Top three risks with severity and concrete failure mode]
- [Greybeard's scaling/ops concerns]
- [Breaker's strongest attack]

### Kill criteria
- Ship-blocker: [specific condition that says "do not launch"]
- Pivot-trigger: [signal that says "change positioning"]
- Sunset-trigger: [signal that says "stop maintaining"]

### Verification plan
[Tester's strategy for proving the pitch is real, not folklore: A/B baseline, regression gates, golden samples]

### Architecture fit
[Architect's assessment of where this lives and what it costs to maintain]

### Legal and IP
[Legal seat's licensing posture and any blockers]

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

- **`/team`**: codebase has product potential, you want a pitch with adversarial review.
- **`/extract`**: quick single-pass pitch when you don't need the council.
- **`/elegance`**: code refinement or generic council debate (not pitch-flavored).
- **`/doubt`**: challenge a single decision, not pitch a whole codebase.
- **`/consensus`**: second opinions only, no synthesis or pitch shape.
