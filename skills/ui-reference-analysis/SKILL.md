---
name: ui-reference-analysis
description: Inspect a permitted UI/UX source and turn it into reusable, evidence-backed design patterns for future app and web projects.
version: 1.0.0
capabilities:
  - ui-reference-inspection
  - screenshot-analysis
  - design-token-extraction
  - ux-pattern-analysis
inputs:
  - url
  - screenshots
  - figma-frame
  - permitted-local-template
outputs:
  - reference-record
  - design-pattern-report
  - evidence-gaps
permissions:
  network: optional
  filesystem_read: optional
  filesystem_write: approval-required
  shell: prohibited-by-default
---

# UI Reference Analysis

## Objective

Convert a user-authorized website, screenshot, Figma frame, or legally accessible UI kit into a reusable reference record. The output must explain *why* a design works and how its general principles can inform a different product.

## Required workflow

1. Confirm the exact source and the user's access/permission.
2. Record source URL, owner, date, platform, product domain, and licence/usage status. If licence terms are unknown, mark them unknown.
3. Capture screenshots only with an authorized browser/capture adapter. Record viewport size, page/state, timestamp, and artifact hash. Never claim capture succeeded if no image artifact exists.
4. Enumerate visible screens and states. Separate observed facts from inferred interactions.
5. Analyse:
   - information architecture and navigation;
   - visual hierarchy and content density;
   - color roles and contrast;
   - typography roles and scale;
   - spacing, grid, alignment, radii, elevation;
   - component anatomy and reusable patterns;
   - forms, feedback, empty/loading/error states;
   - responsive behaviour;
   - motion/animation cues;
   - accessibility and usability risks.
6. Produce a structured reference record and concise human-readable report.
7. Add evidence links for each major observation. Mark unavailable evidence and confidence explicitly.
8. Deduplicate against existing references before adding a new record.

## Output format

Return:
- Source metadata and access/licence status.
- Capture inventory with viewport and screenshot artifact paths.
- Screen inventory and flow map.
- Extracted design tokens.
- Reusable patterns with context, rationale, and caveats.
- UX/accessibility strengths and weaknesses.
- Confidence and unresolved evidence gaps.
- Suggested use cases and search tags.

## Safety and quality rules

- Do not bypass logins, paywalls, anti-bot controls, or access restrictions.
- Do not download or execute unknown archives/scripts during discovery.
- Do not copy paid source code, proprietary images, logos, text, or distinctive branded layouts unless the user has confirmed a valid licence and requested their use.
- Prefer abstracting general principles and creating original implementations.
- Keep source attribution and provenance with every record.
- Never invent screens, interactions, animations, or technical details not visible in evidence.
- Treat marketing copy as seller claims, not verified product functionality.
- Do not install dependencies or plugins. Recommend them separately for user approval.
