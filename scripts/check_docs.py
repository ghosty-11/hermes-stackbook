from __future__ import annotations

import argparse
import ipaddress
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path
from urllib.parse import unquote, urlsplit

LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.+?)\s*$")
FENCE_PATTERN = re.compile(r"^\s{0,3}(`{3,}|~{3,})([^`]*)$")
DATE_REQUIREMENTS = (
    (
        "README.md",
        re.compile(r"Compatibility baseline:.*?reviewed (\d{4}-\d{2}-\d{2})", re.IGNORECASE),
        "compatibility baseline",
    ),
    (
        "docs/sources.md",
        re.compile(r"Reviewed (\d{4}-\d{2}-\d{2})\.", re.IGNORECASE),
        "source review",
    ),
)

IGNORED_PARTS = {".git", "node_modules"}


def repository_files(root: Path, pattern: str) -> list[Path]:
    return sorted(
        path
        for path in root.rglob(pattern)
        if not any(part in IGNORED_PARTS for part in path.relative_to(root).parts)
    )


def markdown_prose(text: str) -> str:
    output: list[str] = []
    active_fence: str | None = None
    for line in text.splitlines():
        match = FENCE_PATTERN.match(line)
        if match:
            marker = match.group(1)
            if active_fence is None:
                active_fence = marker[0]
            elif marker[0] == active_fence:
                active_fence = None
            output.append("")
            continue
        output.append(line if active_fence is None else "")
    return re.sub(r"`[^`\n]*`", "", "\n".join(output))


def github_slug(text: str) -> str:
    text = re.sub(r"`([^`]*)`", r"\1", text.strip().lower())
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    return re.sub(r"\s+", "-", text)


def markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    seen: dict[str, int] = {}
    prose = markdown_prose(path.read_text())
    for line in prose.splitlines():
        match = HEADING_PATTERN.match(line)
        if not match:
            continue
        base = github_slug(match.group(1))
        count = seen.get(base, 0)
        seen[base] = count + 1
        anchors.add(base if count == 0 else f"{base}-{count}")
    return anchors


def unclosed_fence(path: Path) -> bool:
    active_fence: str | None = None
    for line in path.read_text().splitlines():
        match = FENCE_PATTERN.match(line)
        if not match:
            continue
        marker = match.group(1)
        if active_fence is None:
            active_fence = marker[0]
        elif marker[0] == active_fence:
            active_fence = None
    return active_fence is not None


def validate_repository(
    root: Path,
    *,
    today: date | None = None,
    max_age_days: int = 120,
) -> list[str]:
    root = root.resolve()
    today = today or date.today()
    failures: list[str] = []
    markdown_files = repository_files(root, "*.md")

    for path in markdown_files:
        relative = path.relative_to(root)
        text = path.read_text()
        prose = markdown_prose(text)
        if unclosed_fence(path):
            failures.append(f"{relative}: unclosed code fence")
        if "[[" in prose or "]]" in prose:
            failures.append(f"{relative}: contains an Obsidian wikilink")

        for raw_target in LINK_PATTERN.findall(prose):
            target = raw_target.strip().split()[0].strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme:
                if parsed.scheme == "mailto":
                    continue
                if parsed.scheme != "https":
                    failures.append(f"{relative}: {target}: external link must use HTTPS")
                    continue
                if parsed.username is not None or parsed.password is not None:
                    failures.append(f"{relative}: {target}: external link contains user information")
                    continue
                host = parsed.hostname or ""
                target_is_public = True
                try:
                    target_is_public = ipaddress.ip_address(host).is_global
                except ValueError:
                    target_is_public = not (
                        host == "localhost"
                        or host.endswith((".local", ".internal", ".lan", ".home", ".corp"))
                    )
                if not target_is_public:
                    failures.append(f"{relative}: {target}: external link target is not public")
                continue
            path_part, _, fragment = target.partition("#")
            resolved = path if not path_part else (path.parent / unquote(path_part)).resolve()
            if not resolved.exists():
                failures.append(f"{relative}: {target}: missing target")
                continue
            if fragment and resolved.suffix.lower() == ".md":
                if unquote(fragment).lower() not in markdown_anchors(resolved):
                    failures.append(f"{relative}: {target}: missing anchor")

    for relative_name, pattern, label in DATE_REQUIREMENTS:
        path = root / relative_name
        if not path.exists():
            continue
        match = pattern.search(path.read_text())
        if not match:
            failures.append(f"{relative_name}: missing {label} date")
            continue
        checked = datetime.strptime(match.group(1), "%Y-%m-%d").date()
        age = (today - checked).days
        if age < 0:
            failures.append(f"{relative_name}: {label} date is in the future")
        elif age > max_age_days:
            failures.append(
                f"{relative_name}: {label} is stale ({age} days; maximum {max_age_days})"
            )

    for path in repository_files(root, "*.json"):
        try:
            json.loads(path.read_text())
        except json.JSONDecodeError as error:
            failures.append(f"{path.relative_to(root)}: invalid JSON: {error}")

    return failures


def extract_mermaid_blocks(root: Path, output: Path) -> list[Path]:
    root = root.resolve()
    output.mkdir(parents=True, exist_ok=True)
    for existing in output.glob("*.mmd"):
        existing.unlink()

    diagrams: list[Path] = []
    pattern = re.compile(r"```mermaid\s*\n(.*?)\n```", re.DOTALL)
    for path in repository_files(root, "*.md"):
        relative_stem = str(path.relative_to(root).with_suffix("")).replace("/", "__")
        for index, block in enumerate(pattern.findall(path.read_text()), 1):
            destination = output / f"{relative_stem}-{index}.mmd"
            destination.write_text(block + "\n")
            diagrams.append(destination)
    return diagrams


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate repository documentation contracts.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root (default: script parent repository).",
    )
    parser.add_argument("--max-age-days", type=int, default=120)
    parser.add_argument("--extract-mermaid", type=Path)
    arguments = parser.parse_args()

    failures = validate_repository(
        arguments.root,
        max_age_days=arguments.max_age_days,
    )
    if arguments.extract_mermaid:
        diagrams = extract_mermaid_blocks(arguments.root, arguments.extract_mermaid)
        print(f"Extracted {len(diagrams)} Mermaid diagram(s).")

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1

    print("Documentation contracts passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
