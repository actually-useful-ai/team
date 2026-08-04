#!/usr/bin/env python3
"""Package and Craft Ask integration regressions for Team."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TeamPackageTests(unittest.TestCase):
    def test_manifest_versions_match(self) -> None:
        plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        marketplace = json.loads(
            (ROOT / ".claude-plugin/marketplace.json").read_text()
        )["plugins"][0]
        self.assertEqual(plugin["version"], "0.1.3")
        self.assertEqual(marketplace["version"], "0.1.3")

    def test_consensus_discovers_craft_without_private_dependency(self) -> None:
        consensus = (ROOT / "skills/consensus/SKILL.md").read_text()
        for expected in ("craft-ask --list", "craft-ask --status", "native read-only agents"):
            self.assertIn(expected, consensus)
        for stale in (
            "~/.claude/bin/ask.sh",
            "ask.sh --health",
            "deepseek/deepseek-v4-pro",
            "grok-4.3",
            "gpt-5.4",
        ):
            self.assertNotIn(stale, consensus)

    def test_outside_calls_require_explicit_authorization(self) -> None:
        team = (ROOT / "skills/team/SKILL.md").read_text()
        executive = (ROOT / "agents/executive.md").read_text()
        for content in (team, executive):
            self.assertIn("explicitly authorizes external", content)
            self.assertIn("craft-ask --list", content)
        self.assertIn("`/team` alone does not", team)

    def test_consensus_keeps_provenance_dissent_and_fallback(self) -> None:
        consensus = (ROOT / "skills/consensus/SKILL.md").read_text()
        for expected in (
            "actual provider/model provenance",
            "Never flatten",
            "native read-only agents rather than failing",
        ):
            self.assertIn(expected, consensus)

    def test_every_skill_description_has_trigger_context(self) -> None:
        for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
            frontmatter = skill.read_text().split("---", 2)[1]
            self.assertIn("Use ", frontmatter, skill.as_posix())


if __name__ == "__main__":
    unittest.main()
