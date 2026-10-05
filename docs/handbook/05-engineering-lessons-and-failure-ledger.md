# Alpha Linux Engineering Lessons & Failure Knowledge Base

**Status:** Maintained  
**Baseline:** v0.3.0a → v0.4.0  
**Purpose:** Prevent recurrence of project failures and preserve engineering knowledge.

## Incident method
**Symptom → Evidence → Root Cause → Fix → Verification → Preventive Rule → Permanent Gate**

## L001 — A2 oversized artifact transport
Large ISO artifacts were unreliable to transfer. Fixed by splitting into chunks of at most 900 MiB plus provider digest, Alpha SHA-256 and reassembly verification. Permanent rule: release transport stays bounded and independently verifiable.

## L002 — Cross-run publication dependency
Indirect workflow-run discovery created publication risk. Fixed by publishing from the exact validated OS-image workspace/run. Permanent rule: publisher never rebuilds, substitutes or guesses the source image.

## L003 — Branding only part of the Live product
Desktop identity could be correct while boot/media metadata still identified Ubuntu. Fixed by validating all Alpha identity surfaces. Permanent rule: boot metadata, OS identity, hostname, installer entries and boot labels must agree.

## L004 — Stale Live user in greetd
Graphical startup could fail before COSMIC despite valid packages. Root cause was a stale Ubuntu username. Fixed by one canonical Live UID 1000 identity. Permanent rule: Live identity is a single validated contract.

## L005 — Unprivileged SquashFS extraction
Extraction failed when filesystem objects required privileges. Fixed by running extraction with required root privileges. Permanent rule: distinguish validator defects from image defects.

## L006 — Live/QEMU evidence overstated as installation evidence
Boot/QEMU success cannot prove physical installation readiness. Permanent rule: keep Live, QEMU, installer, physical hardware, Secure Boot and Windows-coexistence gates separate.

## L007 — A4 retired as active baseline
A4 became a historical release-candidate context even though v0.3.0a is the last validated product experience we want to carry forward. Decision: retain A4 for traceability, retire it as the development baseline, and build v0.4.0 from v0.3.0a.

## L008 — CI status must be terminal
Running, queued, skipped or unknown workflows are not release evidence. Permanent rule: release gates close only on terminal successful jobs and actual logs are inspected on failure.

## L009 — Merge proof
A merge SHA alone is insufficient. Permanent rule: verify merged=true, state=closed, merge commit, then target main and current CI.

## L010 — Lightweight product boundary
Bundling every domain application into the ISO makes the base product large and harder to validate. Decision: Core + COSMIC in the ISO; optional capabilities installed later.

## Archival policy
Historical candidates such as v0.1.0a4 remain available for traceability and lessons. They are labeled historical/superseded and do not define current architecture or release readiness.

## Release review checklist
1. Baseline commit
2. Version metadata
3. Build workflow
4. Validation workflow
5. Artifact/provenance
6. Runtime evidence
7. Physical evidence where required
8. Release assets
9. Documentation synchronization
10. Lessons from the release cycle
