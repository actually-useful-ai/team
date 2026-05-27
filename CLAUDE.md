# team v0.1

Council-style codebase-assessment plugin for Claude Code. Takes a codebase, returns a technical assessment reviewed by a 10-seat team.

## Architecture

**One command, one mode (for now):**

- `/team src/` → council assesses the codebase
- `/team` (no args) → council assesses the current directory
- `/team "Should we open-source this?"` → council debate on a question

## The team

| Committee | Seats |
|-----------|-------|
| **Research** | recon, scout |
| **Technical** | architect, greybeard, safety, tester |
| **Skeptics** | breaker, cynic |
| **Legal check** | legal (standalone) |
| **Chair** | executive |
| **Polish** | editor |

10 seats total. The committees run in parallel, with the legal check alongside them. Each committee chair synthesizes its seats. The executive sees the committee reports plus the legal list, not ten voices.

## Plugin Structure

```
.claude-plugin/          Plugin metadata (marketplace.json, plugin.json)
agents/                  10 agent definitions
  executive.md           Chair, synthesis
  editor.md              Post-verdict humanize
  recon.md               Internal codebase map
  scout.md               External prior art scan
  legal.md               IP, licensing, red-flag check (standalone)
  architect.md           Codebase fit
  greybeard.md           Old-engineer review of scaling and ops
  safety.md              Failure recovery, fallbacks
  tester.md              Verification, regression
  breaker.md             Adversarial attack on the assessment
  cynic.md               Pre-mortem, kill criteria, devil's advocate
skills/team/SKILL.md     Council protocol
skills/consensus/        Read-only second opinions from external models
skills/doubt/            Targeted challenge to a current approach
commands/team.md         /team entry point
scripts/banner.sh        ASCII banners
```

## Council protocol rules

1. Facts outrank precedent. Precedent outranks taste.
2. Every criticism must include a concrete failure mode.
3. Cynic must always dissent (absorbs the catfish role).
4. Editor is post-verdict only.
5. Dissenting opinions are always preserved.
6. Consultants are best-effort. Skill works fine when external models are unreachable.

## Development

Pure-markdown plugin. No build step. Edit the `.md` files directly. Banner script requires `pyfiglet`, `toilet`, or `figlet` (falls back to plain text).
