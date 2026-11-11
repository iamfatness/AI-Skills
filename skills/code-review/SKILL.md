---
name: code-review
description: Review a concrete patch for actionable correctness, security, and regression defects.
---

# Code Review

## Inputs

A patch or commit range, expected behavior, and relevant surrounding code.

## Workflow

1. Read the patch and changed callers, contracts, and tests. Evaluate only defects introduced or exposed by the change.
2. Trace each suspected issue to a concrete trigger and user-visible impact. Verify the claim against surrounding safeguards.
3. Prioritize findings by impact; include file locations and a minimal reproduction or reasoning chain. Separate optional style suggestions.
4. Report no findings when evidence does not support a defect, and list important coverage limits. Do not modify code unless asked.

## Output

Prioritized evidence-backed findings and review scope.

## Example

Review a pagination change for skipped records and incorrect boundary handling.
