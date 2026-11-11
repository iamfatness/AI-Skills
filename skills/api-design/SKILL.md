---
name: api-design
description: Design or review API contracts for compatibility, validation, errors, and reliable retries.
---

# Api Design

## Inputs

Consumers, resource model, existing contract, and operational constraints.

## Workflow

1. Model consumer workflows and resource identities before endpoints. Reuse existing naming, versioning, and pagination conventions.
2. Specify request and response shapes, validation, authorization boundaries, and stable error semantics. Distinguish missing, null, and empty values.
3. Define idempotency and retry behavior for mutations, pagination consistency for collections, and concurrency semantics where data can change.
4. Provide concrete success and failure examples and contract tests. Review compatibility and migration needs before changing a published API.

## Output

A reviewable contract or implementation with examples and compatibility notes.

## Example

Design a retry-safe create endpoint that handles duplicate client requests.
