# Security policy

This repository contains documentation and example contracts, not a deployed service. Security issues still matter when the guidance could expose credentials, broaden agent capabilities, enable unsafe ingress/egress, or recommend a vulnerable supply-chain path.

## Report privately

Use GitHub's private vulnerability reporting for this repository when available. If it is not enabled, open a minimal issue that says a private security report is needed; do not include exploit details, credentials, private deployment data, or third-party personal information in a public issue.

## Include

- affected document and section;
- the unsafe behavior or boundary;
- current Hermes/OMP or dependency version;
- reproducible evidence using fictional/non-sensitive data;
- the narrowest safe correction;
- whether the issue affects already-published Git history.

## Deployment incidents

Do not report a private deployment incident by pasting logs into this repository. Revoke or rotate exposed credentials first, preserve evidence privately, and contact the affected upstream project through its security channel when the defect is upstream.

Upstream reports:

- Hermes Agent: follow the security process in [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent).
- OMP: follow [can1357/oh-my-pi security guidance](https://github.com/can1357/oh-my-pi/blob/main/.github/SECURITY.md).

## Supported documentation

Only the current default branch is maintained. Historical commits remain available for audit but may describe older product behavior.
