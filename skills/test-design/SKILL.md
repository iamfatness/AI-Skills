---
name: test-design
description: Design and run behavior-focused tests for changed contracts and meaningful failure modes.
---

# Test Design

## Inputs

Behavior under test, risk, existing test conventions, and available runtime.

## Workflow

1. Identify externally observable invariants, boundary cases, and failure recovery rather than mirroring private implementation.
2. Use the smallest suitable test level. Keep test data deterministic and isolate filesystem, network, and clock dependencies.
3. Include a regression that fails for the demonstrated defect where practical. Verify that a negative case cannot pass accidentally.
4. Run the relevant suite and report actual results, skipped cases, and environmental limits. Avoid brittle wording or snapshot checks without a behavioral reason.

## Output

Focused tests, execution results, and remaining coverage gaps.

## Example

Test an installer for idempotency, conflicting files, and path containment.
