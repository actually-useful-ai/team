# team

Council-style codebase-to-pitch plugin for Claude Code.

Point it at a codebase. A 12-seat team across four subcommittees (research, business, technical, skeptics) decides what it is, who buys it, what kills it, and how to know whether the pitch is any good.

## Install

This plugin lives in `~/.claude/plugins/marketplaces/lukeslp-team/`. Add the marketplace and install via the Claude Code plugin tooling, or symlink directly into your local plugin tree.

## Usage

```bash
/team                            # pitch the current directory
/team src/                       # pitch a specific path
/team ~/projects/whatcolor       # pitch a project elsewhere on disk
/team "Should I open-source this?"   # team debate on a question
```

## What you get back

A short verdict from the executive chair, structured as:

- **Decision**: one line.
- **The pitch**: product, audience, positioning, monetization.
- **What kills it**: kill criteria, top three risks, who would say no.
- **Verification plan**: how to know if the pitch is right.
- **Dissenting opinions**: preserved, not flattened.
- **Consultant notes**: what external models said when they could be reached.

## The seats

**Research (facts, not opinions)**
- `recon`: maps the codebase. Languages, dependencies, public surfaces, internal patterns.
- `scout`: external prior art. Comparable products, market context. Optional consult: Perplexity, Gemini.

**Business**
- `marketing`: audience, positioning, GTM. Encodes Geoffrey Moore (*Crossing the Chasm*), April Dunford (*Obviously Awesome*), Jobs-to-be-Done, the Bullseye framework. Optional consult: Gemini, Grok.
- `legal`: IP, licensing, can-this-actually-be-sold. Looks at every dep's license and the project's own.
- `manager`: maintenance cost, debt, runway. Encodes the SQALE method, Cunningham/Fowler's debt quadrant.

**Technical**
- `architect`: fit with the existing codebase patterns.
- `greybeard`: old-engineer review of what breaks at 10x. Encodes the Google SRE Book (chapter 22, four golden signals), Brendan Gregg's USE method. Optional consult: Codex, Grok.
- `safety`: failure recovery, fallbacks, graceful degradation.
- `tester`: verification strategy, regression criteria.

**Skeptics**
- `breaker`: adversarial attack on the pitch. Concrete failure scenarios only.
- `cynic`: pre-mortem (Klein 2007), kill criteria (Annie Duke), Amazon working-backwards critique. Must always disagree. Optional consult: full `/consensus` fan-out.

**Chair and polish**
- `executive`: reads four committee reports, synthesizes the verdict, preserves dissent.
- `editor`: strips machine-generated writing indicators. Post-verdict only.

## Consultants

Several seats can call external models for diverse priors. All consultant calls are best-effort: try CLI first (free quota: Codex, Gemini, Cursor agent), fall through to direct API (xAI, OpenAI, Mistral, Perplexity), fall through to "consultant unavailable." The skill works fine without any external auth, consultants only sharpen the verdict when they're reachable.

The full fan-out lives at `skills/consensus/` and is invoked by the cynic seat as the panel of last resort.

## Why a council and not a single pass

A single LLM pass will produce a pitch that sounds confident regardless of merit. Adversarial review: especially from seats anchored to canonical frameworks (Moore, Dunford, SRE Book, SQALE, Klein), catches the failure modes a confident single pass misses. The subcommittee structure prevents the executive from drowning in twelve voices.

The design is sympathetic to the parallel-critics + single-synthesis pattern that holds up better in recent multi-agent research (arxiv 2509.05396, 2025) than round-table debate.

## Author

Luke Steuber · luke@lukesteuber.com · https://lukesteuber.com
