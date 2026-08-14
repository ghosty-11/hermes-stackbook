# Guide for AI contributors

This repository is public-safe architecture and operations documentation for a self-hosted Hermes Agent + Oh My Pi stack. Preserve that boundary: document reproducible decisions and verification, not one operator's deployment.

## Start here

1. Read `README.md` and follow its reading order.
2. Read `SUPPORT.md` before preparing issue evidence.
3. Read the complete target document and its linked source documents.
4. For behavior claims, check the current installed CLI help where available, then official documentation or source. Date claims whose truth can change.

## Repository map

- `README.md` — scope, requirements, assisted setup, architecture, and navigation.
- `docs/` — planning, implementation, security, operations, and verification guidance.
- `templates/` — reusable public-safe records and deployment worksheets; copy before filling.
- `docs/sources.md` — primary references and community discovery catalogs.
- `docs/compatibility.md` — pinned upstream references and evidence level.
- `SUPPORT.md` — issue-reporting, evidence, and public-safety requirements.
- `SECURITY.md` — vulnerability reporting and disclosure boundary.

## Content contracts

- Keep the optional public bot explicitly optional. The private stack must stand without it.
- Keep the core private path visibly separate from optional extension modules.
- Keep planned and deferred work explicit; do not imply a planned component ships here.
- Keep recommendations separate from upstream behavior and deployment-specific policy.
- Prefer stable role, boundary, and verification guidance over copied version-specific configuration.
- Label free tiers, experimental endpoints, model examples, quotas, and provider terms as changeable; link the primary source.
- Never add credentials, private hostnames or paths, account or bot IDs, personal data, private repository names, or production logs.
- Use fictional identifiers and `example.invalid` when an example needs a non-resolving domain.
- Preserve relative Markdown links and GitHub-compatible Mermaid syntax.
- Do not add an installer. Readers and their assistants must adapt upstream installation commands to the live OS and CLI.
- Do not describe prose, a persona, or a model prompt as a security boundary. Name the capability, credential, process, or network control.
- One active writer per shared checkout. Preserve unrelated changes.

## Change method

1. State the observable reader outcome.
2. Update every affected document, template, and cross-reference in the same change.
3. Cite current primary sources for new behavior claims.
4. Update the executable documentation contract when observable validation behavior changes; otherwise validate the rendered documentation directly.
5. Review the final diff as a reader following the guide from a clean host.

## Verification

Before committing an owner change or preparing issue evidence:

- run `npm ci --ignore-scripts`;
- run `npm audit --audit-level=high`;
- run `python3 -m unittest discover -s tests -v`;
- run `python3 scripts/check_docs.py --max-age-days 120 --extract-mermaid /tmp/hermes-stack-mermaid`;
- run `npm run lint:markdown`;
- render every extracted Mermaid block with `./node_modules/.bin/mmdc`;
- run the checksum-verified Gitleaks and Lychee binaries through the workflow or install them with `scripts/install-ci-tools.sh`;
- scan the working tree and full Git history for private identifiers and secrets;
- report which checks ran and any runtime surface that was not exercised.
