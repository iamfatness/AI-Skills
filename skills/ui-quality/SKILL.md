---
name: ui-quality
description: Implement or audit visible UI against an established design system and actual rendered behavior.
---

# Ui Quality

## Inputs

Target screen, user journeys, accepted design references, and rendering tools.

## Workflow

1. Read the existing design system and reuse accepted patterns. If missing, define only the decisions necessary for this screen.
2. Check hierarchy, alignment, control dimensions, readable labels, responsive density, contrast, and keyboard operation. Use semantic controls before adding ARIA.
3. Inspect populated and selected-record states at desktop and phone widths after the last edit. Check loading, empty, error, and recovery states relevant to the change.
4. Exercise the main action, filters, return navigation, and focus after refresh. Review actual screenshots; creating screenshots alone is not acceptance.
5. For React or similar apps, investigate measured waterfalls, excessive rerenders, and unnecessary client work before optimizing. Record unavailable visual checks as unverified.

## Output

Implemented or reviewed scope, visual evidence, interaction results, and remaining gaps.

## Example

Verify a record list and detail panel on desktop and phone using real populated fixtures.
