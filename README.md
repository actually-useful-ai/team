# team

Council-style codebase-assessment plugin for Claude Code.

Point it at a codebase. A 10-seat team across three subcommittees (research, technical, skeptics) plus a standalone legal red-flag check decides what it is, where it fits, what breaks it, what kills it, and how to know whether the assessment is any good.

## Install

This plugin lives in `~/.claude/plugins/marketplaces/lukeslp-team/`. Add the marketplace and install via the Claude Code plugin tooling, or symlink directly into your local plugin tree.

## Usage

```bash
/team                            # assess the current directory
/team src/                       # assess a specific path
/team ~/projects/whatcolor       # assess a project elsewhere on disk
/team "Should I open-source this?"   # team debate on a question
```

## What you get back

A short verdict from the executive chair, structured as:

- **Decision**: one line.
- **The assessment**: what it is, where it fits, what it's good for.
- **What kills it**: kill criteria, top three risks, the strongest attack.
- **Verification plan**: how to know if the assessment is right.
- **Legal red flags**: license/IP blockers, or all-clear.
- **Dissenting opinions**: preserved, not flattened.
- **Consultant notes**: what external models said when they could be reached.

## The seats

**Research (facts, not opinions)**
- `recon`: maps the codebase. Languages, dependencies, public surfaces, internal patterns.
- `scout`: external prior art. Comparable projects, technical approaches. Optional consult: Perplexity, Gemini.

**Technical**
- `architect`: fit with the existing codebase patterns. Chairs the committee.
- `greybeard`: old-engineer review of what breaks at 10x. Encodes the Google SRE Book (chapter 22, four golden signals), Brendan Gregg's USE method. Optional consult: Codex, Grok.
- `safety`: failure recovery, fallbacks, graceful degradation.
- `tester`: verification strategy, regression criteria.

**Skeptics**
- `breaker`: adversarial attack on the assessment. Concrete failure scenarios only.
- `cynic`: pre-mortem (Klein 2007), kill criteria (Annie Duke), Amazon working-backwards critique. Must always disagree. Optional consult: full `/consensus` fan-out.

**Legal check (standalone)**
- `legal`: IP, licensing, attribution. A red-flag list of license/IP blockers that would stop the project from being shipped or open-sourced. Looks at every dep's license and the project's own.

**Chair and polish**
- `executive`: reads the committee reports plus the legal list, synthesizes the verdict, preserves dissent.
- `editor`: strips machine-generated writing indicators. Post-verdict only.

## Consultants

Several seats can call external models for diverse priors. All consultant calls are best-effort: try CLI first (free quota: Codex, Gemini, Cursor agent), fall through to direct API (xAI, OpenAI, Mistral, Perplexity), fall through to "consultant unavailable." The skill works fine without any external auth, consultants only sharpen the verdict when they're reachable.

The full fan-out lives at `skills/consensus/` and is invoked by the cynic seat as the panel of last resort.

## Why a council and not a single pass

A single LLM pass will produce an assessment that sounds confident regardless of merit. Adversarial review: especially from seats anchored to canonical frameworks (SRE Book, USE method, Klein pre-mortem, Annie Duke kill criteria), catches the failure modes a confident single pass misses. The subcommittee structure prevents the executive from drowning in ten voices.

The design is sympathetic to the parallel-critics + single-synthesis pattern that holds up better in recent multi-agent research (arxiv 2509.05396, 2025) than round-table debate.

## Author

Luke Steuber · luke@lukesteuber.com · https://lukesteuber.com
