#!/usr/bin/env python3
"""Package and Craft Ask integration regressions for Team."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_MANIFESTS = (
    ROOT / ".claude-plugin/plugin.json",
    ROOT / ".codex-plugin/plugin.json",
    ROOT / ".cursor-plugin/plugin.json",
)
EXPECTED_SKILLS = {
    "consensus",
    "doubt",
    "research",
    "skeptics",
    "team",
    "technical",
}
EXPECTED_AGENTS = {
    "architect",
    "breaker",
    "cynic",
    "editor",
    "executive",
    "greybeard",
    "legal",
    "recon",
    "safety",
    "scout",
    "tester",
}


class TeamPackageTests(unittest.TestCase):
    def test_runtime_manifests_match(self) -> None:
        manifests = [json.loads(path.read_text()) for path in PACKAGE_MANIFESTS]
        marketplace = json.loads(
            (ROOT / ".claude-plugin/marketplace.json").read_text()
        )["plugins"][0]
        cursor_marketplace = json.loads(
            (ROOT / ".cursor-plugin/marketplace.json").read_text()
        )

        shared_fields = (
            "name",
            "version",
            "description",
            "homepage",
            "repository",
            "license",
            "keywords",
            "skills",
        )
        for manifest in manifests:
            self.assertEqual(manifest["name"], "team")
            self.assertEqual(manifest["version"], "0.1.4")
            self.assertEqual(manifest["skills"], "./skills/")
            self.assertEqual(manifest["author"]["name"], "Luke Steuber")
            for field in shared_fields:
                self.assertEqual(manifest[field], manifests[0][field])
        self.assertEqual(manifests[1]["interface"]["displayName"], "Team")
        self.assertEqual(manifests[2]["agents"], "./agents/")
        self.assertEqual(marketplace["name"], manifests[0]["name"])
        self.assertEqual(marketplace["version"], manifests[0]["version"])
        self.assertEqual(cursor_marketplace["name"], "lukeslp-team")
        self.assertEqual(cursor_marketplace["metadata"]["version"], "0.1.4")
        self.assertEqual(cursor_marketplace["plugins"][0]["name"], "team")
        self.assertEqual(cursor_marketplace["plugins"][0]["source"], ".")

    def test_skill_and_agent_inventory_is_authoritative(self) -> None:
        skill_paths = sorted((ROOT / "skills").glob("*/SKILL.md"))
        agent_paths = sorted((ROOT / "agents").glob("*.md"))
        skill_names = {path.parent.name for path in skill_paths}
        agent_names = {path.stem for path in agent_paths}

        self.assertEqual(skill_names, EXPECTED_SKILLS)
        self.assertEqual(agent_names, EXPECTED_AGENTS)
        for path in skill_paths:
            self.assertIn(f"name: {path.parent.name}", path.read_text())
        for path in agent_paths:
            self.assertIn(f"name: {path.stem}", path.read_text())

        for documentation in (ROOT / "README.md", ROOT / "CLAUDE.md"):
            content = documentation.read_text()
            self.assertIn(f"{len(skill_names)} skill", content)
            self.assertIn(f"{len(agent_names)} agent", content)
            self.assertIn(f"{len(agent_names)}-seat", content)

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
