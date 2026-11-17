---
name: ui-reference-implementation
description: Use selected UI/UX references to build an original, responsive, accessible app or web interface and verify it against the product brief.
version: 1.0.0
capabilities:
  - reference_retrieval
  - ui_implementation
  - responsive_design
  - design_qa
inputs:
  - product_brief
  - target_platform
  - selected_reference_records
  - existing_codebase
outputs:
  - implementation_plan
  - original_ui_code
  - design_qa_report
permissions:
  filesystem_write: approval-required
  shell: approval-required
  network: optional
---

# UI Reference Implementation

## Objective

Build an original interface informed by relevant UI/UX references. References guide design decisions; they are not permission to copy a commercial template.

## Workflow

1. Read the product brief, target users, primary tasks, platform, technical constraints, and accessibility needs.
2. Retrieve only 2–4 relevant, high-confidence reference records.
3. Explain which patterns are being reused conceptually and why they fit the product.
4. Establish a product-specific visual direction and design tokens. Do not copy a reference's branding, logos, text, proprietary assets, or exact distinctive composition.
5. Inspect the existing codebase and preserve its architecture, conventions, dependencies, and working behaviour.
6. Implement semantic, reusable components and responsive layouts.
7. Include relevant states: loading, empty, error, success, disabled, validation, and navigation.
8. Verify at mobile, tablet, and desktop sizes as applicable.
9. Run available tests, lint, type checks, and accessibility checks. Do not claim a check passed unless it was run.
10. Compare the rendered result against the brief and selected design principles; record gaps and fixes.

## Output

- Selected references and relevance rationale.
- Design tokens and component plan.
- Implementation changes.
- Commands/tests actually executed and results.
- Responsive and accessibility review.
- Known gaps and next steps.

## Guardrails

- Preserve existing user code and data; inspect before modifying.
- Ask before destructive changes, adding paid dependencies, external services, or installing tools.
- Do not add heavy UI dependencies when native framework capabilities are sufficient.
- Respect licence and attribution requirements for any assets or code used.
- Do not represent mock data or placeholder integrations as production functionality.
- Never report success without evidence from the actual build/test/browser result.
