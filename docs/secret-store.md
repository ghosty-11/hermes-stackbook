# Central secret store

Two harnesses, several profiles, scheduled jobs and supporting services each need credentials.
Left alone, they accumulate copies: a profile `.env` per seat, a key file beside a model config,
an inline password in a service unit, a token read directly by a helper script. Every copy is a
place to forget during rotation and a place to leak during a backup.

This page describes a store that removes the copies. Read
[Security](security.md) first for what a store cannot do.

## What a store does and does not buy

State this plainly before adopting one, because the common failure is claiming the wrong benefit.

**It buys:** one rotation point, one revocation point, no plaintext at rest, one thing to back up,
and — if the store is a Git repository — a reviewable change history.

**It does not buy a security boundary.** Every design ends with the harness process holding a
usable credential. Whatever key or token unlocks the store must be readable by the identity the
harness runs as, so an agent running as that identity can read it too, or simply invoke the store
CLI itself. A store is credential *hygiene*; the boundary is a separate control — an absent tool,
a container without the mount, a different OS user, a network rule. See
[Core concepts](core-concepts.md).

The practical gain is narrower than "secrets are safe" and still worth having: with plaintext
credential files, an accidental copy — `cp .env .env.bak`, an editor backup, a stray archive —
exposes every secret it contains. With an encrypted store, the same accident produces ciphertext.

## Requirements before choosing

A store is only adoptable if it satisfies the delivery contracts the harnesses already impose.
Establish these against your own installation rather than assuming them.

1. **Per-identity isolation, for reads *and* writes.** If two harnesses run as different OS users
   that cannot currently read each other's credentials, the store must preserve that. One shared
   encrypted blob readable by both is a *regression* in blast radius, not a neutral
   simplification. Separate files are only half of it: each identity also needs a directory only
   it can write, because write access to another's file is enough to substitute credentials
   (see [Encryption controls reading; ownership controls writing](#encryption-controls-reading-ownership-controls-writing)).
2. **Native seams, no code changes.** Both harnesses can already shell out for a secret. Hermes has
   a command secret source; OMP resolves configuration values prefixed with `!` by running a
   command and using its stdout. Prefer a store whose CLI fits those seams directly.
3. **Two output shapes.** The Hermes command source expects a **complete `KEY=VALUE` map from one
   invocation**; OMP expects **one value per configured field**. A store that only does per-key
   reads needs a wrapper for Hermes; a store that only dumps everything needs one for OMP.
4. **A hard timeout budget.** These seams have fixed timeouts measured in seconds. Measure the real
   command against the real file size; do not assume.
5. **Non-interactive after reboot.** Scheduled jobs run with no human present. Any store needing a
   passphrase, PIN, agent priming or desktop session at unlock time is disqualified unless it has a
   documented unattended path.
6. **Recovery must not be circular.** The material that opens the store cannot live only inside the
   store, and must not live only inside a backup the store's own credential is needed to open.
7. **Backups must be extended deliberately.** Backup source lists are usually allowlists. A new
   store path is unprotected until explicitly added and a restore is tested.

## A design that satisfies them

Encrypted files in one repository, one file per consuming identity, each encrypted only to that
identity's key — and each in a directory only that identity can write.

```mermaid
graph LR
  subgraph Repo["one repository — parent NOT group-writable"]
    subgraph DA["dir A — writable by identity A only"]
      F1["agent-a.env<br/>encrypted to key A"]
    end
    subgraph DB["dir B — writable by identity B only"]
      F2["agent-b.env<br/>encrypted to key B"]
    end
  end
  F1 -->|"decrypt whole file"| C1["Agent A<br/>bulk KEY=VALUE seam"]
  F2 -->|"extract one key"| C2["Agent B<br/>per-field seam"]
  K1["key A<br/>readable only by A"] -.-> C1
  K2["key B<br/>readable only by B"] -.-> C2
```

The separation is the point. "Central" means one repository, one rotation procedure and one backup
— **not** one ciphertext that every consumer can open.

### Encryption controls reading; ownership controls writing

Splitting the files is necessary and not sufficient. A store configuration lists the **public**
recipient for every file, because that is how encryption is targeted. So a principal that can
*write* another principal's file can encrypt values of its own choosing to that file's legitimate
recipient — and the victim will decrypt them cleanly, because they are correctly encrypted. That
is credential substitution, and it needs no private key at all.

A shared, group-writable store directory therefore leaves one principal able to feed another
arbitrary credentials: an API key pointing at an attacker-controlled endpoint, or simply a value
that breaks the service. Give each identity its own directory, owned by that identity, and keep
the parent directory non-group-writable so nobody can add or replace files beside another's.

Reading another principal's ciphertext is harmless — they cannot decrypt it — so a directory may
stay readable if something legitimately needs it, such as committing the repository. Writing is
the privilege to withhold.

**Verify both properties rather than trusting them.** Decrypting each file with the other
identity's key must exit non-zero with no plaintext; creating, replacing or deleting a file in
another identity's directory must be refused. Test the refusals as the other user, and be
suspicious of a check that passes for a reason you have not confirmed — a command that fails for
the wrong reason reads exactly like a boundary that holds.

File-based stores fit this shape well. A daemon-based secret manager also works, but for a small
static credential set it adds a service, a bootstrap secret to unlock that service, a bearer token
per client, and a stateful volume with its own restore drill — while landing in exactly the same
place on the boundary question. Choose a daemon when you actually need its distinguishing
features: dynamic short-lived credentials, leases, policy tenancy or a read audit trail. Note that
some open-core products gate audit logging and rotation behind a paid tier; check the licence of
the specific features you are adopting, not the repository's headline licence.

## Worked example

One concrete implementation of the design above, using [SOPS](https://github.com/getsops/sops)
with [age](https://github.com/FiloSottile/age) recipients. Adapt the paths and identity names;
these are illustrative, not a script to paste. Check current upstream installation instructions
for your OS — at the time of writing `age` is commonly packaged while `sops` is often a single
binary from its releases page, so verify the published checksum before installing it.

**One identity per consuming principal.** Generate each as the user that will own it, mode `0600`,
and keep it out of the store directory:

```bash
age-keygen -o "$IDENTITY"          # prints the public recipient to stderr
chmod 600 "$IDENTITY"
```

**One encrypted file per identity**, encrypted only to that identity's recipient. Use the dotenv
input/output type so the decrypted form is directly the `KEY=VALUE` map a bulk seam expects:

```bash
sops encrypt --age "$RECIPIENT_A" --input-type dotenv --output-type dotenv \
  plain-a.env > store/agent-a.env
```

**Wire each consumer to its own file.** A bulk seam decrypts the whole file; a per-field seam
extracts one key:

```bash
# bulk: complete KEY=VALUE map, one invocation
SOPS_AGE_KEY_FILE="$IDENTITY_A" sops decrypt store/agent-a.env

# per-field: one value
SOPS_AGE_KEY_FILE="$IDENTITY_B" sops decrypt --extract '["SOME_KEY"]' store/agent-b.env
```

**Rotate one value without exposing it in the process list.** `sops set` takes a JSON-encoded
value, so a bare string is rejected — encode it first:

```bash
printf '%s' "$NEW_VALUE" | jq -Rs . \
  | sops set --value-stdin store/agent-b.env '["SOME_KEY"]'
```

**Change who can decrypt** by editing the recipients in `.sops.yaml`, then re-wrapping the
existing data key. Add and test the new recipient before removing the old one:

```bash
sops updatekeys --yes store/agent-b.env
```

Commit only the encrypted files. The identities never enter the repository, and they must not sit
inside a backup alongside the ciphertext they open — treat them exactly as you treat the backup
repository's own password.

## Migration

Move one credential class at a time and keep the old path working until the new one is proven.

1. **Inventory every reader first.** The harness seams are the visible consumers; they are rarely
   the only ones. Expect service units with an environment-file directive, helper scripts that
   parse a credential file directly, inline passwords in container definitions, and tooling
   credentials in their own config. A migration that covers only the harnesses leaves live copies
   behind, and "rotate once" becomes false.
2. **Do not widen access.** A credential currently readable only by a privileged system identity
   should stay there. Moving it into a store that agent identities can read is a downgrade, even
   though it looks like consolidation.
3. **Prove the seam with a throwaway value.** Populate a test entry, point one configuration field
   at the store, measure the command against its timeout, and confirm the consumer works — before
   any real credential moves.
4. **Migrate, verify, then revoke.** Only after the new path is proven for a given credential
   should the old copy be removed and the upstream credential rotated.
5. **Remove the old plaintext.** Command-resolved values are typically held in memory only, but the
   previous files, database rows and backup copies persist until deleted.
6. **Know which seams are additive and which replace.** They are not equivalent, and the
   difference decides your rollback. A source that merges into an existing environment without
   overriding it is *additive*: the old file still wins, a store outage changes nothing, and
   backing out is disabling the source. A configuration field whose value you rewrite to call the
   store is a *hard cutover*: the old path no longer executes, an unreachable store breaks
   credential resolution for that consumer, and backing out means editing configuration. Write
   down which of your consumers is which **before** you rely on "we can always roll back" — and
   note that a consumer failing closed is correct behaviour, not evidence the store is fine.

## Rotation

Rotation is not finished when the stored value changes. Long-running consumers commonly cache a
resolved secret for the life of the process, so plan the restarts as part of the procedure.

1. Update the value at the single authoritative point, using a command form that does not put the
   secret in a command line — the process list is world-readable on most systems.
2. Restart or reload each long-running consumer; note which ones share a process, because
   restarting a multiplexed service restarts every profile it serves.
3. Let short-lived consumers — scheduled jobs, socket-activated helpers, new sessions — pick the
   value up on their next run, and verify one of them actually did.
4. Verify every consumer's health check before revoking the previous credential upstream.
5. Revoke upstream last.

Rotating the *store's own* key is a separate operation: add the new recipient, re-encrypt, deploy
and test the new key, then remove the old recipient and re-encrypt again.

Removing a recipient stops it decrypting the *current* revision. It does not reach historical
revisions in version control or backups, and it cannot un-read a secret already read. When a
credential has actually been exposed, rotate the credential itself at the provider; changing store
keys is not a substitute.

## Verification

Prove each of these against the live installation, not the documentation:

- each identity can read its own file and **cannot** read the other's;
- each identity **cannot create, replace or delete** a file in another identity's directory, and
   the parent directory does not let it add one alongside;
- the bulk command emits a complete, correctly parsed map within its timeout;
- the per-key command returns one value within its timeout;
- values containing `=`, quotes, spaces and escaped newlines survive a round trip unchanged;
- rotation changes the intended key and leaves the others untouched;
- a scheduled job reads the store successfully after an unattended reboot;
- a restore from backup, using only material available after host loss, yields a usable store.

Related: [Security](security.md) · [Supporting services](supporting-services.md) ·
[Operations](operations.md) · [Verification](verification.md)
