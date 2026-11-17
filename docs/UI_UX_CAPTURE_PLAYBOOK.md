# AUTO UI/UX Capture Playbook

## Purpose

Capture permitted visual evidence for a reference and preserve reproducible provenance. This playbook is intentionally tool-agnostic; use an approved browser-control or screenshot tool available in the current environment.

## Standard capture matrix

For responsive mobile UI:
- Mobile viewport: 390 × 844 CSS px (or nearest supported device preset).
- Tablet viewport: 768 × 1024 CSS px.
- Desktop viewport: 1440 × 900 CSS px.

For app UI kits shown as device mockups:
- Capture the original preview image at native resolution.
- Also capture the full gallery page and any individual enlarged preview.
- Do not crop out labels, status bars, device edges, or annotations unless a separate crop is explicitly recorded.

## Capture procedure

1. Confirm the page is public or the user has authorized access.
2. Record the canonical URL and page title.
3. Dismiss only non-essential cookie banners if permitted; record if the banner obscured content.
4. Capture the full page and each visible gallery preview.
5. Open gallery/detail views only through ordinary visible controls; do not bypass authentication, paywalls, or anti-bot measures.
6. For interactive demos, capture representative states: initial, navigation, selection, loading, empty, error, and success where publicly accessible.
7. Record viewport, browser, timestamp, scroll position, and source URL.
8. Hash each artifact (SHA-256) and store outside Git by default.
9. Add artifact pointers and hashes to the reference JSON record.
10. Analyse only the pixels actually captured.

## Naming convention

`<source-id>/<product-id>/<viewport>/<sequence>-<screen-name>.<ext>`

Example:
`dailyflutterui-payhip/food-delivery-app-ui/mobile-390x844/001-home.png`

## Analysis checklist

For each screen, record:
- Screen purpose and primary user task.
- Information hierarchy and reading order.
- Navigation model and back/close affordances.
- Layout grid, spacing, alignment, and content density.
- Color roles, typography roles, radii, elevation, and borders.
- Components, variants, and interaction states.
- Responsive behaviour and overflow.
- Accessibility: contrast, touch targets, labels, semantics, focus order.
- Motion: trigger, direction, duration (only if measurable), and reduced-motion fallback.
- Strengths, usability issues, and context-specific caveats.

## Evidence discipline

Use separate fields for:
- `observed`: directly visible in screenshot or page content.
- `seller_claim`: marketing copy from the seller.
- `inferred`: plausible interpretation, clearly labelled.
- `unknown`: not evidenced.

Do not create a visual-quality score from listing titles or seller marketing text. A screenshot source URL is not itself a screenshot artifact. A page-relative image filename is not an image file.

## Copyright and security

- Respect the seller's licence and access terms.
- Do not redistribute paid source code or proprietary assets.
- Store only screenshots and excerpts needed for the user's reference purpose, with attribution and access controls.
- Never execute scripts from a purchased or downloaded archive during discovery.
- Review dependencies and build scripts in an isolated environment before any execution.
