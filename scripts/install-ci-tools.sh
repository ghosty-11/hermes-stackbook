#!/usr/bin/env bash
set -euo pipefail

readonly BIN_DIR="${1:?usage: install-ci-tools.sh BIN_DIR}"
readonly DOWNLOAD_DIR="${RUNNER_TEMP:-/tmp}/hermes-stackbook-ci-downloads"
readonly GITLEAKS_VERSION="8.24.3"
readonly GITLEAKS_ARCHIVE="gitleaks_${GITLEAKS_VERSION}_linux_x64.tar.gz"
readonly GITLEAKS_SHA256="9991e0b2903da4c8f6122b5c3186448b927a5da4deef1fe45271c3793f4ee29c"
readonly LYCHEE_VERSION="0.24.2"
readonly LYCHEE_ARCHIVE="lychee-x86_64-unknown-linux-gnu.tar.gz"
readonly LYCHEE_SHA256="1f4e0ef7f6554a6ed33dd7ac144fb2e1bbed98598e7af973042fc5cd43951c9a"

rm -rf -- "$DOWNLOAD_DIR"
mkdir -p -- "$BIN_DIR" "$DOWNLOAD_DIR/gitleaks" "$DOWNLOAD_DIR/lychee"

curl --fail --location --silent --show-error \
  "https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/${GITLEAKS_ARCHIVE}" \
  --output "$DOWNLOAD_DIR/$GITLEAKS_ARCHIVE"
printf '%s  %s\n' "$GITLEAKS_SHA256" "$DOWNLOAD_DIR/$GITLEAKS_ARCHIVE" | sha256sum --check --status
tar --extract --gzip --file "$DOWNLOAD_DIR/$GITLEAKS_ARCHIVE" --directory "$DOWNLOAD_DIR/gitleaks" gitleaks
install -m 0755 "$DOWNLOAD_DIR/gitleaks/gitleaks" "$BIN_DIR/gitleaks"

curl --fail --location --silent --show-error \
  "https://github.com/lycheeverse/lychee/releases/download/lychee-v${LYCHEE_VERSION}/${LYCHEE_ARCHIVE}" \
  --output "$DOWNLOAD_DIR/$LYCHEE_ARCHIVE"
printf '%s  %s\n' "$LYCHEE_SHA256" "$DOWNLOAD_DIR/$LYCHEE_ARCHIVE" | sha256sum --check --status
tar --extract --gzip --file "$DOWNLOAD_DIR/$LYCHEE_ARCHIVE" --directory "$DOWNLOAD_DIR/lychee" \
  --strip-components=1 lychee-x86_64-unknown-linux-gnu/lychee
install -m 0755 "$DOWNLOAD_DIR/lychee/lychee" "$BIN_DIR/lychee"

rm -rf -- "$DOWNLOAD_DIR"
