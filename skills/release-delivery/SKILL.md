---
name: release-delivery
description: Validate and publish an explicitly authorized release with traceable artifacts and verification.
---

# Release Delivery

## Inputs

Version, repository, release scope, publish authorization, and release conventions.

## Workflow

1. Inspect branch, working tree, release conventions, and existing tags. Preserve unrelated changes and never move an existing release tag silently.
2. Run required checks and inspect the exact staged diff. Align version metadata, changelog, and distributable contents.
3. Commit only intended files. Push and publish only within the authorized target; use an exact commit for the tag and release.
4. Verify remote commit, tag, CI, and artifact availability. If any step fails, report which parts succeeded and the precise remaining work.

## Output

Commit SHA, version/tag, release URL, test results, and publication status.

## Example

Publish v0.1.0 with a verified archive and SHA-256 checksum.
