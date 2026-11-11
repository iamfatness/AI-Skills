---
name: scoped-implementation
description: Implement a feature or refactor within an existing codebase while preserving unrelated work.
---

# Scoped Implementation

## Inputs

Requested behavior, repository context, and acceptance criteria.

## Workflow

1. Inspect repository instructions, working-tree changes, affected callers, and existing abstractions.
2. Choose the smallest coherent change that satisfies the behavior. Preserve public contracts unless the task requires changing them.
3. Implement error paths and recovery alongside the main action. Avoid unrelated rewrites or new dependencies without a concrete benefit.
4. Exercise changed behavior and relevant regressions. Review the final diff for accidental edits and disclose untested environments.

## Output

The implemented change, relevant checks, and known limitations.

## Example

Add a validated optional query parameter without changing existing callers.
