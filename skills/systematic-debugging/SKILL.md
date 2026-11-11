---
name: systematic-debugging
description: Diagnose reproducible failures and verify a targeted fix using evidence.
---

# Systematic Debugging

## Inputs

Observed failure, expected behavior, logs or reproduction steps, and environment.

## Workflow

1. Reproduce the failure or capture the strongest available evidence; distinguish symptoms from suspected causes.
2. Trace the boundary where behavior diverges. Form a falsifiable hypothesis and run a focused experiment.
3. Fix the demonstrated cause while preserving supported behavior. Avoid stacking speculative fixes.
4. Re-run the original reproduction and nearby regression checks. Record remaining uncertainty if the environment prevents reproduction.

## Output

Cause, fix, reproduction result, and relevant regression evidence.

## Example

Investigate an intermittent duplicate submission using request IDs and persistence logs.
