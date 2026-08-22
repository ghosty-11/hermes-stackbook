# Try it safely, then throw it away

**Read this first if you want to evaluate the stack without risking anything you care about.**
It describes a disposable environment, a bounded 30-minute trial, and how to destroy the
result. It is deliberately *not* a secure production blueprint — it is a way to look at the
software before you decide whether to plan a real deployment.

The reason this page exists is in the [personal-machine warning](../README.md#personal-machine-privacy-warning):
an agent can reach whatever its operating-system identity can reach. The safest way to
evaluate one is to give it an identity that owns nothing.

## Recommended default: a local throwaway virtual machine

A fresh Linux VM on hardware you already have, created for this and deleted afterwards.

- **Why this one:** destruction is unambiguous — you delete the disk image and the experiment
  is gone. It cannot read your daily-user home directory by construction, not by policy.
- **What to allocate:** 2–4 CPU cores, 8 GiB RAM, 40 GiB disk. (The bands in the README's
  [system requirements](../README.md#system-requirements) are *planning* figures for a real
  deployment; this is only for a look.)
- **Guest:** a current long-term-support Linux release you are comfortable with.
- **Networking:** default NAT is fine and preferable. You do not need inbound access.

### Alternatives, and when each makes sense

| Option | Good for | Cost | Watch out for |
|---|---|---|---|
| Local throwaway VM *(recommended)* | Most evaluators | Free if you have the hardware | Do not add shared folders |
| Low-cost cloud VM | No spare local capacity; keeps the experiment off your home network | Hourly/monthly host cost | Needs a provider account; remember to destroy the volume too |
| Spare physical machine | Strongest practical local separation | Hardware you already own, or its purchase | Still on your LAN; treat it as untrusted |
| Separate OS user or container on your daily machine | Constrained advanced experiments | Free | **Not recommended for a first look** — shared home directories, forwarded credentials, and mounted sockets are easy to get wrong, and each one quietly removes the isolation you think you have |

## Before you install anything: five things that must be true

An environment is only disposable if nothing valuable is reachable *from inside it*. Check,
from inside the VM:

1. **No host filesystem is mounted.** No shared folders, no passed-through drives.
2. **No credentials were forwarded.** No SSH agent, no Git credential helper, no cloud CLI
   configuration, no password-manager export, no browser profile, no private-network keys.
3. **The working directory is empty and new** — create one, e.g. `~/stackbook-test`, and keep
   everything inside it.
4. **The model credential is disposable.** Use a free tier or a throwaway key with a hard
   spending limit. Do not paste a key you use elsewhere.
5. **Nothing listens publicly.** Keep services on loopback. Do not create a public chat bot
   for a trial.

If you cannot make all five true, you do not yet have a disposable environment — fix that
before continuing, because a VM with your home directory mounted is not meaningfully safer
than running on the host.

## The 30-minute trial

Deliberately small. One assistant, one model, no automation.

1. **Install Hermes inside the VM** following [Installation](installation.md) and the current
   upstream instructions it points to.
2. **Configure one model provider.** One is enough. See the README's
   [free and low-cost starting points](../README.md#free-and-low-cost-starting-points).
3. **Run the built-in diagnostic** (`hermes doctor`) and read it. Fix anything it calls
   blocking; ignore optional-feature notices for now.
4. **Ask one harmless question from the command line** and get an answer. That is the whole
   milestone: a private assistant that replies.
5. **Optional, if coding is your interest:** install OMP, create a disposable Git repository
   containing one small file and one test, and ask it to make a trivial change. See
   [Installation](installation.md).
6. **Optional:** export a Hermes backup and confirm the archive exists, so you have seen the
   recovery path referenced later.

**Success looks like:** a reply to your question; a diagnostic with no blocking problem; and,
if you tried OMP, a small change in a repository you do not care about.

**Stop here.** Do not add scheduled jobs, a public chat bot, a knowledge base, plugins,
research services, a local model, or a second profile during a trial. Each is covered later
in the guide with the boundaries it needs, and none of it is required to judge whether this is
for you.

## Destroy it

- **Local VM:** shut it down, then delete the machine *and* its virtual disk and snapshots.
- **Cloud VM:** terminate the instance, then delete its attached volume and any firewall or
  network rules you created. Check the bill the next day.
- **Either way:** revoke the model API key you used, and delete any bot token you created.

## Residual risk, stated plainly

A VM reduces blast radius; it does not make an agent safe. Inside it, an agent can still spend
your model credit, send whatever it is given to a provider, and act on any credential you
placed there. Prompts and personas are not permissions. The controls that actually constrain
an agent — resolved tool surfaces, credential separation, network limits, process identity —
are the subject of [Security](security.md) and [Profiles and models](profiles-and-models.md),
and none of them are relaxed by running in a VM.

When you are ready to build something you intend to keep, start over from
[Planning](planning.md) on a host you have chosen deliberately. Do not promote this sandbox
into a real deployment: it was built to be thrown away, and it has none of the boundaries a
kept system needs.
