from __future__ import annotations

import tempfile
import unittest
from datetime import date
from pathlib import Path

from scripts.check_docs import extract_mermaid_blocks, validate_repository


TODAY = date(2026, 8, 14)


class DocumentationChecksTest(unittest.TestCase):
    def make_repository(self) -> Path:
        root = Path(self.enterContext(tempfile.TemporaryDirectory()))
        (root / "docs").mkdir()
        (root / "README.md").write_text(
            "# Guide\n\n"
            "**Compatibility baseline:** documentation and public sources reviewed 2026-08-14.\n\n"
            "[Details](docs/details.md#known-boundary)\n\n"
            "Use the literal syntax `[[wikilinks]]` only when documenting it.\n"
        )
        (root / "docs" / "details.md").write_text(
            "# Details\n\n## Known boundary\n\n```text\nclosed fence\n```\n"
        )
        (root / "docs" / "sources.md").write_text(
            "# Sources\n\nReviewed 2026-08-14.\n"
        )
        return root

    def test_clean_repository_passes(self) -> None:
        root = self.make_repository()

        self.assertEqual(
            validate_repository(root, today=TODAY, max_age_days=120),
            [],
        )

    def test_missing_relative_link_fails(self) -> None:
        root = self.make_repository()
        (root / "README.md").write_text("# Guide\n\n[Missing](docs/missing.md)\n")

        failures = validate_repository(root, today=TODAY, max_age_days=120)

        self.assertTrue(any("missing target" in failure for failure in failures), failures)

    def test_missing_heading_anchor_fails(self) -> None:
        root = self.make_repository()
        (root / "README.md").write_text("# Guide\n\n[Bad anchor](docs/details.md#absent)\n")

        failures = validate_repository(root, today=TODAY, max_age_days=120)

        self.assertTrue(any("missing anchor" in failure for failure in failures), failures)

    def test_unclosed_fence_fails(self) -> None:
        root = self.make_repository()
        (root / "docs" / "details.md").write_text("# Details\n\n```text\nunclosed\n")

        failures = validate_repository(root, today=TODAY, max_age_days=120)

        self.assertTrue(any("unclosed code fence" in failure for failure in failures), failures)

    def test_stale_compatibility_date_fails(self) -> None:
        root = self.make_repository()
        (root / "README.md").write_text(
            "# Guide\n\n"
            "**Compatibility baseline:** documentation and public sources reviewed 2025-01-01.\n"
        )

        failures = validate_repository(root, today=TODAY, max_age_days=120)

        self.assertTrue(any("compatibility baseline is stale" in failure for failure in failures), failures)

    def test_non_https_external_link_fails(self) -> None:
        root = self.make_repository()
        (root / "README.md").write_text("# Guide\n\n[Insecure](http://example.com)\n")

        failures = validate_repository(root, today=TODAY, max_age_days=120)

        self.assertTrue(any("external link must use HTTPS" in failure for failure in failures), failures)

    def test_external_link_with_credentials_fails(self) -> None:
        root = self.make_repository()
        (root / "README.md").write_text("# Guide\n\n[Credential](https://user:pass@example.com)\n")

        failures = validate_repository(root, today=TODAY, max_age_days=120)

        self.assertTrue(any("external link contains user information" in failure for failure in failures), failures)

    def test_external_link_with_private_target_fails(self) -> None:
        root = self.make_repository()
        (root / "README.md").write_text("# Guide\n\n[Internal](https://127.0.0.1/status)\n")

        failures = validate_repository(root, today=TODAY, max_age_days=120)

        self.assertTrue(any("external link target is not public" in failure for failure in failures), failures)

    def test_dependency_markdown_is_not_repository_content(self) -> None:
        root = self.make_repository()
        dependency = root / "node_modules" / "dependency"
        dependency.mkdir(parents=True)
        (dependency / "README.md").write_text(
            "# Dependency\n\n[Internal](http://127.0.0.1/status)\n"
        )

        self.assertEqual(
            validate_repository(root, today=TODAY, max_age_days=120),
            [],
        )

    def test_mermaid_blocks_are_extracted_for_real_rendering(self) -> None:
        root = self.make_repository()
        (root / "docs" / "details.md").write_text(
            "# Details\n\n```mermaid\nflowchart LR\n    A --> B\n```\n"
        )
        output = root / "render"

        diagrams = extract_mermaid_blocks(root, output)

        self.assertEqual(len(diagrams), 1)
        self.assertEqual(diagrams[0].read_text(), "flowchart LR\n    A --> B\n")

    def test_readme_leads_with_portable_personal_agent_use_case(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text()

        self.assertTrue(readme.startswith("# Hermes Stackbook\n"))
        uses = readme.split("## What you can use this setup for", 1)[1]
        first_bullet = next(line for line in uses.splitlines() if line.startswith("- "))
        for required in (
            "personal AI agent",
            "grows and learns with you",
            "on your machine",
            "review",
            "model provider",
            "switch",
            "skills and memories",
        ):
            self.assertIn(required, first_bullet)

    def test_copy_paste_prompt_separates_planning_from_implementation(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text()
        prompt = readme.split("Copy-paste prompt:", 1)[1].split("```text", 1)[1].split("```", 1)[0]

        for required in (
            "first plan, then—only after I approve an implementation phase—help me implement",
            "Phase 1 is read-only.",
            "Do not install packages, write configuration, create credentials, start or restart services, or alter network or firewall state.",
            "Wait for my approval before beginning implementation.",
        ):
            self.assertIn(required, prompt)

    def test_readme_warns_personal_machine_users_about_private_data(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text()
        heading = "### Personal-machine privacy warning"

        self.assertIn(heading, readme)
        warning = readme.split(heading, 1)[1].split("\n## ", 1)[0]
        for required in (
            "private files",
            "dedicated OS identity",
            "least-privilege filesystem permissions",
            "separate public or web-facing agents",
            "sandbox",
            "outbound provider",
        ):
            self.assertIn(required, warning)

    def test_stackbook_does_not_duplicate_package_contracts(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertFalse((root / "templates" / "coding-job.schema.json").exists())
        self.assertFalse((root / "docs" / "hermes-omp-integration.md").exists())
        package = (root / "package.json").read_text()
        self.assertNotIn("coding-job.schema.json", package)
        self.assertNotIn("validate:schema", package)

    def test_publication_checks_match_the_shipped_repository(self) -> None:
        root = Path(__file__).resolve().parents[1]
        agents = (root / "AGENTS.md").read_text()
        package = (root / "package.json").read_text()
        workflow = (root / ".github" / "workflows" / "documentation.yml").read_text()
        security = (root / "docs" / "security.md").read_text()

        self.assertNotIn("validate:schema", agents)
        self.assertNotIn("ajv-cli", package)
        self.assertIn("npm audit --audit-level=high", workflow)
        self.assertIn(
            "Choose a license for the repository you are preparing to publish.",
            security,
        )

    def test_optional_modules_are_documented_as_selected_scope(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text()
        checklist = (root / "templates" / "deployment-checklist.md").read_text()
        sequence = (root / "docs" / "build-sequence.md").read_text()

        self.assertIn("https://github.com/ghosty-11/hermes-omp-broker", readme)
        self.assertIn("https://github.com/ghosty-11/hermes-mailbox", readme)
        self.assertNotIn("planned for a future release", readme.lower())
        for heading in (
            "## Optional: OMP",
            "## Optional: research",
            "## Optional: knowledge base",
            "## Optional: coding broker",
        ):
            self.assertIn(heading, checklist)
        self.assertIn("selected and enabled modules", sequence)

    def test_every_released_package_is_indexed_and_reviewable(self) -> None:
        """A released package the guide never names is a coverage gap, not a secret.

        One package was public for a day before any document mentioned it, because the
        package list lived in prose that nobody had to update. The index and the review
        section are both asserted so provenance and procedure cannot drift apart.
        """
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text()
        plugins = (root / "docs" / "skills-and-plugins.md").read_text()
        sources = (root / "docs" / "sources.md").read_text()
        packages = (
            "hermes-omp-broker",
            "hermes-mailbox",
            "hermes-optmem-tools",
            "hermes-discord-ambient",
            "hermes-trace",
            "hermes-web-research",
        )
        self.assertIn("## Released packages", readme)
        for package in packages:
            url = f"https://github.com/ghosty-11/{package}"
            self.assertIn(url, readme, f"{package} is absent from the README index")
            self.assertIn(url, plugins, f"{package} escapes the plugin review section")
            self.assertIn(url, sources, f"{package} has no recorded provenance")

        # First-party provenance must be stated, not implied by the account name.
        self.assertIn("First-party packages from this project", sources)
        self.assertIn("being first-party is provenance, not an exemption", plugins)
        self.assertNotIn("is one public implementation to review", readme)

    def test_self_improvement_is_evidence_backed_and_operator_gated(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text()
        architecture = (root / "docs" / "architecture.md").read_text()
        verification = (root / "docs" / "verification.md").read_text()
        sequence = (root / "docs" / "build-sequence.md").read_text()

        self.assertIn("self-evaluation through deterministic guards and behavioral evals", readme)
        self.assertIn("cannot approve, install, restart, or publish its own recommendation", architecture)
        self.assertIn("operator-gated self-improvement loop, not autonomous self-modification", verification)
        self.assertIn("clean state stays silent, and no proposal can apply itself", sequence)

    def test_change_drift_template_reconciles_authoritative_and_resolved_state(self) -> None:
        root = Path(__file__).resolve().parents[1]
        guide = (root / "templates" / "README.md").read_text()
        template = (root / "templates" / "change-drift-runbook.md").read_text()

        self.assertIn("[Change-drift runbook](change-drift-runbook.md)", guide)
        for required in (
            "## Authoritative and observed state",
            "Source artifact",
            "Deployed artifact",
            "Resolved runtime state",
            "## Drift classification",
            "False positive",
            "Reconciliation direction",
            "## Detection contract",
            "A healthy check is silent",
            "## Reconciliation procedure",
            "## Independent verification",
        ):
            self.assertIn(required, template)

    def test_runbooks_and_templates_are_installed_into_operator_knowledge_base(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = " ".join((root / "README.md").read_text().split())
        guide = " ".join((root / "templates" / "README.md").read_text().split())
        operations = " ".join((root / "docs" / "operations.md").read_text().split())
        sequence = " ".join((root / "docs" / "build-sequence.md").read_text().split())

        self.assertIn(
            "copy and adapt the selected runbooks and templates into it",
            readme,
        )
        self.assertIn("## Install into your operational knowledge base", guide)
        for required in (
            "Do not bulk-import",
            "source URL or revision",
            "owners",
            "approval gates",
            "verification commands",
            "field use",
        ):
            self.assertIn(required, guide)
        for required in (
            "private operational copy",
            "normal knowledge-base search",
            "public versions are starting points",
        ):
            self.assertIn(required, operations)
        self.assertIn(
            "adapted copies of the selected runbooks and templates",
            sequence,
        )

    def test_proposed_wiki_structure_is_complete_and_linked(self) -> None:
        root = Path(__file__).resolve().parents[1]
        proposal_path = root / "docs" / "knowledge-base-structure.md"

        self.assertTrue(proposal_path.is_file())
        proposal = proposal_path.read_text()
        for required in (
            "Home.md",
            "README.md",
            "log.md",
            "agents/",
            "projects/",
            "services/",
            "runbooks/",
            "reviews/",
            "reference/",
            "meta/",
            "templates/",
            "inbox/",
            "inbox/processed/",
            "concepts/",
            "raw/",
            "_archive/",
            "_meta/",
            ".obsidian/",
            ".stversions/",
            ".stfolder/",
        ):
            self.assertIn(required, proposal)

        self.assertIn(
            "(docs/knowledge-base-structure.md)",
            (root / "README.md").read_text(),
        )
        for path in (
            root / "docs" / "build-sequence.md",
            root / "docs" / "supporting-services.md",
        ):
            self.assertIn("(knowledge-base-structure.md)", path.read_text())
        self.assertIn(
            "(../docs/knowledge-base-structure.md)",
            (root / "templates" / "README.md").read_text(),
        )

    def test_proposed_wiki_structure_plans_information_lifecycle(self) -> None:
        root = Path(__file__).resolve().parents[1]
        proposal = (root / "docs" / "knowledge-base-structure.md").read_text().lower()

        for required in (
            "plan the information lifecycle",
            "canonical owner",
            "intake",
            "distillation",
            "review dates",
            "retention",
            "sensitive",
            "restore",
        ):
            self.assertIn(required, proposal)

    def test_omp_engineering_guidance_recommends_advisor_with_cost_tradeoff(self) -> None:
        root = Path(__file__).resolve().parents[1]
        installation = " ".join(
            (root / "docs" / "installation.md").read_text().split()
        )
        for required in (
            "`/advisor on`",
            "second-model reviewer",
            "verify assumptions",
            "correct likely mistakes",
            "steer the primary agent",
            "raises result quality",
            "increases token usage and cost",
            "`/advisor status`",
            "`/advisor off`",
        ):
            self.assertIn(required, installation)

        compatibility = (root / "docs" / "compatibility.md").read_text()
        self.assertIn("448632b8190e", compatibility)
        self.assertNotIn("404695b", compatibility)

    def test_compatibility_evidence_is_current_for_publication_candidate(self) -> None:
        root = Path(__file__).resolve().parents[1]
        current_date = "2026-08-14"
        previous_date = "2026-08-13"
        paths = (
            root / "README.md",
            root / "docs" / "compatibility.md",
            root / "docs" / "profiles-and-models.md",
            root / "docs" / "sources.md",
        )

        for path in paths:
            content = path.read_text()
            self.assertIn(current_date, content, path)
            self.assertNotIn(previous_date, content, path)

        compatibility = (root / "docs" / "compatibility.md").read_text()
        self.assertIn("Current private candidate", compatibility)
        self.assertIn("No clean-host golden path claimed", compatibility)

    def test_suggested_custom_skills_are_public_safe_and_release_gated(self) -> None:
        root = Path(__file__).resolve().parents[1]
        guide = (root / "docs" / "skills-and-plugins.md").read_text()

        section = guide.split("## Suggested custom skills to develop", 1)[1].split(
            "\n## ", 1
        )[0]
        self.assertIn("| Suggested skill | General purpose | Release gate |", section)
        normalized = section.lower()
        for required in (
            "design and architecture decisions",
            "shared knowledge bases",
            "scheduled-job authoring",
            "systematic debugging",
            "test-driven implementation",
            "verification before completion",
            "honest outcome reporting",
            "operator decisions and escalation",
            "agent-to-agent handoffs",
            "runbook operations",
            "long-running stateful jobs",
            "skill authoring and maintenance",
            "domain modeling and requirements grilling",
            "repository audits and change review",
            "does not publish or copy private skill bodies",
            "reviewed public skill releases are planned",
            "no promised release dates",
        ):
            self.assertIn(required, normalized)

    def test_public_drift_runbooks_cover_skills_and_loaded_artifacts(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text()
        operations = (root / "docs" / "operations.md").read_text()
        skills = (root / "docs" / "skill-drift.md").read_text()
        artifacts = (root / "docs" / "extension-and-file-drift.md").read_text()

        for link in (
            "[Skill drift runbook](docs/skill-drift.md)",
            "[Extension and file drift runbook](docs/extension-and-file-drift.md)",
        ):
            self.assertIn(link, readme)
        self.assertIn("[Skill drift](skill-drift.md)", operations)
        self.assertIn("[Extension and file drift](extension-and-file-drift.md)", operations)

        for required in (
            "## Source, discovered, and exercised state",
            "name collisions",
            "fresh harness process",
            "positive and nearby negative selection",
            "A healthy drift check is silent",
        ):
            self.assertIn(required, skills)

        for required in (
            "## Source, deployed, loaded, and exercised state",
            "normal installer or deployment path",
            "Reload only when required",
            "consumer-visible behavior",
            "A healthy drift check is silent",
        ):
            self.assertIn(required, artifacts)


if __name__ == "__main__":
    unittest.main()
