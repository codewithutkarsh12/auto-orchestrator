# AUTO UI/UX Reference Intelligence

Status: design specification + initial source inventory
Branch: feat/ui-ux-reference-library
Source reviewed: DailyFlutterUI Payhip storefront, 2026-11-17

## Goal

Give AUTO a reusable, searchable UI/UX reference library for future mobile apps, websites, dashboards, SaaS products, and prototypes. AUTO should discover reference sources, capture permitted visual evidence, analyse design patterns, retrieve relevant examples for a task, and implement an original design that fits the product brief.

This subsystem is a reference and design-pattern engine, not a code-copying engine.

## Non-goals and safety boundaries

- Do not scrape behind authentication, bypass anti-bot controls, or download paid files without a valid purchase and permission.
- Do not copy a paid template's source code, proprietary assets, branding, or distinctive screen-by-screen expression unless the user has the appropriate licence and explicitly asks to use those licensed materials.
- Prefer extracting general design knowledge: information hierarchy, layout patterns, navigation, spacing scale, typography roles, color relationships, component behaviour, responsive rules, accessibility, and motion principles.
- Preserve source attribution, source URL, capture date, licence/usage terms, and provenance for every reference.
- Treat downloaded archives, scripts, and dependencies as untrusted. Never execute them during discovery.
- Discovery must not install anything. Installation or external side effects require user approval.
- Never claim a screenshot, source archive, or UI flow was inspected unless the artifact was actually captured and reviewed.

## Resource types

Support these source types through adapters:
1. Public web pages and product pages.
2. Screenshots and user-uploaded images.
3. Figma files/frames where access is granted.
4. User-owned local projects and code.
5. Downloadable UI kits/templates where the user has legal access.
6. Design systems, component libraries, icon packs, fonts, motion references, and documentation.

## Pipeline

1. **Discover** — find candidate URLs, kits, repositories, skills, tools, plugins, and libraries.
2. **Classify** — platform (Flutter, native, React, web, etc.), product domain, resource type, source/license status.
3. **Capture** — take full-page and viewport screenshots at defined viewport sizes; record page URL, dimensions, timestamp, and capture tool. Capture only pages the user is allowed to access.
4. **Inspect** — enumerate screens, states, navigation, repeated components, responsive breakpoints, empty/loading/error states, and interaction cues.
5. **Analyse** — extract design tokens and patterns: color roles, type scale, spacing, radii, elevation, grid, component anatomy, motion, accessibility, content density, and usability strengths/weaknesses.
6. **Normalize** — store structured metadata and references in a common schema.
7. **Score** — rate relevance, visual quality, usability, accessibility, implementation feasibility, freshness, licence clarity, and source confidence. Keep factual evidence separate from subjective scores.
8. **Retrieve** — select a small number of relevant references based on the current task, platform, domain, audience, and constraints.
9. **Implement** — generate original code and assets, using the references as guidance rather than blindly cloning.
10. **Verify** — compare the implementation against the brief and extracted design principles; run responsive and accessibility checks.
11. **Maintain** — detect source changes and stale references; refresh only with approval where capture or access has side effects.

## Proposed reference record

Each record should include:
- `id`, `title`, `source_url`, `source_owner`, `source_type`, `platform`, `product_domain`
- `discovered_at`, `captured_at`, `last_verified_at`
- `access_status`, `license_status`, `usage_constraints`, `attribution`
- `screenshots[]`: local/remote artifact pointer, viewport, page/state, hash, capture method
- `screens[]`: screen name, purpose, hierarchy, layout, components, states, navigation
- `design_tokens`: color roles, typography, spacing, radii, shadows, breakpoints, motion
- `patterns[]`: pattern, context, rationale, evidence, caveats
- `quality_scores`: relevance, usability, accessibility, visual_quality, feasibility, confidence
- `analysis_status`: discovered | metadata_reviewed | screenshots_captured | analysed | verified
- `provenance`: reviewer/tool/version and evidence links

Do not store large binaries in the Git repository by default. Keep screenshots in a local artifact cache or approved object storage; commit only lightweight metadata and optional small previews. Avoid storing purchased ZIPs or copied commercial source code in this repository.

## AUTO integration

- Add a `ui_ux_reference` capability to the universal resource registry.
- Add adapters rather than coupling the core orchestrator to Playwright, Figma, or a specific design platform.
- Use a local SQLite index for searchable runtime metadata; export/import portable JSON manifests.
- Add a task router rule: when a task involves UI, UX, frontend, mobile, web, dashboard, or design recreation, retrieve relevant references before implementation.
- Keep retrieval bounded: normally 2–4 high-confidence references per task, not the entire catalogue.
- Add a dedicated `ui-reference-analysis` skill/workflow that accepts a URL, screenshots, Figma frame, or permitted local template and produces a structured analysis.
- Add a `design-implementation` workflow that converts selected patterns into original responsive code and verifies the result.
- Use optional Playwright/browser and Figma adapters. They must remain optional so AUTO's Python core stays lightweight and usable without heavy dependencies.
- Provide commands conceptually equivalent to `auto ui discover <url>`, `auto ui capture <url>`, `auto ui analyse <reference-id>`, and `auto ui search <task>`; final CLI names are subject to implementation review.

## DailyFlutterUI initial inventory

The Payhip storefront currently displayed 16 product listings. The initial scan recorded listing metadata and opened several detail pages. This is not a completed visual audit.

| Product | Product page | Listing price | Initial evidence status |
|---|---|---:|---|
| Ride-Hailing App UI | https://payhip.com/b/ihtrF | $18.88 | Detail text reviewed; screenshot capture blocked |
| Food Delivery App UI | https://payhip.com/b/0ZL2M | $16.00 | Detail text reviewed; screenshot capture blocked |
| Flight Booking App UI | https://payhip.com/b/cwCBv | $16.00 | Detail text reviewed; screenshot capture blocked |
| Airbnb Clone App UI | https://payhip.com/b/n4ZFb | $16.00 | Detail text reviewed; screenshot capture blocked |
| Fintech App UI | https://payhip.com/b/cD0Rg | $16.00 | Detail text reviewed; screenshot capture blocked |
| Parcel Delivery App UI | https://payhip.com/b/XcZhz | $16.00 | Detail text reviewed; screenshot capture blocked |
| EV Charging App UI | https://payhip.com/b/Ojm1n | $16.00 | Listing + partial detail page; full inspection pending |
| Pizza App UI | https://payhip.com/b/bVFmT | $16.00 | Listing only; detail inspection pending |
| Farm App UI | https://payhip.com/b/afcOr | $16.00 | Listing only; detail inspection pending |
| Sneaker Shopping App UI | https://payhip.com/b/l2TdZ | $16.00 | Listing only; detail inspection pending |
| Fitness App UI Kit | https://payhip.com/b/Z0vx9 | $16.00 | Listing only; detail inspection pending |
| Fashion App UI | https://payhip.com/b/cxXGj | $16.00 | Listing only; detail inspection pending |
| Fintech App UI (second listing) | https://payhip.com/b/LVOHC | $16.00 | Listing only; detail inspection pending |
| Digital Wallet App UI | https://payhip.com/b/SKqhL | $16.00 | Listing only; detail inspection pending |
| Liquid Glass Effect | https://payhip.com/b/kN3ga | $8.88 | Listing only; detail inspection pending |
| Lightning App UI Kit | https://payhip.com/b/LKd4i | $8.88 | Listing only; detail inspection pending |

### Findings from accessible product descriptions

- Ride-hailing: booking, destination search, maps, driver location/tracking, fare estimate, ride status, driver details, dark mode, reusable widgets. Seller listing says ZIP is 226 MB.
- Food delivery: restaurant browsing, menus, order tracking, real-time map updates, reusable widgets. Seller listing says ZIP is 466 MB.
- Flight booking: search/filtering, destination discovery, seat selection, booking details, digital boarding pass, reusable widgets. Seller listing says ZIP is 142 MB.
- Vacation rental: property discovery, search/filtering, accommodation detail, photo galleries, booking screens. Seller listing says ZIP is 62 MB.
- Fintech: account balances, transaction history, transfers, payment screens, financial dashboards, wallet/transaction UI. Seller listing says ZIP is 35 MB.
- Parcel delivery: parcel booking, tracking maps, status updates/timeline, shipment history. Seller listing says ZIP is 324 MB.

These are seller-provided descriptions, not independently verified feature tests. Several accessible product pages displayed no customer reviews. Do not infer quality or production readiness from the marketing copy.

### Capture limitation and next evidence required

The page parser exposed image links, but direct image retrieval through the current web inspection path failed. Therefore no actual screenshot has been captured or visually analysed in this pass. The remaining product detail pages also need a reliable browser session for full review.

For a complete audit, use an authorized browser on the user's machine or ChatGPT Work cloud browser to:
- capture the storefront and each product detail page at desktop and mobile widths;
- capture every gallery image and all publicly visible screen previews;
- record the actual number and names of screens shown;
- inspect navigation, forms, overlays, animations, and responsive behaviour where demonstrable;
- avoid checkout, purchase, login, or access-restricted content unless the user explicitly authorizes it.

If the user provides purchased ZIPs, inspect their file trees and source code in an isolated, non-executing review workflow. Confirm licence terms before using code/assets in another project.

## Acceptance criteria

- A new reference can be added from a URL, screenshot, Figma frame, or permitted local kit.
- Captures include source URL, viewport, timestamp, and content hash.
- Analysis output is structured and searchable, with evidence links.
- Retrieval returns a bounded shortlist relevant to a project brief.
- The implementation workflow produces original code and records which references influenced it.
- Licence/access restrictions are enforced before assets or code are reused.
- No external resource is installed or executed without explicit approval.
- Tests cover schema validation, deduplication, retrieval ranking, stale references, provenance, and permission checks.
- The existing orchestrator remains backward-compatible; this subsystem is an additive module.

## Source

DailyFlutterUI storefront: https://payhip.com/DailyFlutterUI
Initial inspection date: 2026-11-17


## Live audit update — 2026-11-17

The connected browser exposed the DailyFlutterUI storefront's extracted page content. The catalogue now records 16 product listings and 32 observed image-element source tokens (two per listing). These are not screenshot artifacts: no image pixels were captured or visually analysed in this session.

A secondary DailyFlutterUI-branded portfolio page was found through search indexing. It lists six UI categories with screen-image labels (Airbnb, Pizza, Parcel Delivery, Food Delivery, Fashion, Fintech). The relationship to the Payhip seller is plausible from the shared brand/handle, but exact product mapping is unverified. The portfolio's additional-screen markers are preserved as raw observations, not interpreted totals.

Detailed evidence, per-product inspection checklists, unknowns, limitations, and the next capture steps are documented in:
- `docs/reports/DAILYFLUTTERUI_VISUAL_AUDIT_2026-11-17.md`
- `references/ui-ux/catalog/dailyflutterui.json`

Current evidence coverage:
- E1 storefront metadata: 16/16 products
- Storefront image element references: 32/32 observed
- E2 seller descriptions: six products plus partial EV Charging
- E3 secondary portfolio index: six categories
- E4 pixel-level screenshot analysis: 0 products
- E5 permitted source-code inspection: 0 products

Do not mark this source visually verified or quality-certified until actual screenshot artifacts have been captured and inspected. Chat-mode browser text extraction is not screenshot capture.


## Additional web UI source catalogue

A separate catalogue was added at `references/ui-ux/catalog/web-ui-libraries.json` for four React/web-focused sources: NeoBrutalism, SmoothUI, Magic UI, and Unlumen UI. The metadata audit is in `docs/reports/WEB_UI_REFERENCE_SOURCES_2026-11-17.md`.

Keep these records separate from Flutter template records. They are primarily React/Next.js and Tailwind sources; Flutter tasks may use their general design/interaction principles as inspiration but must implement Flutter-native components. The catalogue explicitly tracks free/Pro distinctions, platform, motion technology, evidence status, and approval-before-installation.

These sources are currently metadata-reviewed only. Screenshot capture, pixel-level analysis, source review, licence clearance, and runtime integration remain pending.
