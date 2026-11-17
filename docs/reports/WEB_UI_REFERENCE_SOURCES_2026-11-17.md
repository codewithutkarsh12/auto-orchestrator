# Web UI Reference Sources — Initial Metadata Audit

Date: 2026-11-17  
Branch: `feat/ui-ux-reference-library`  
Sources: NeoBrutalism, SmoothUI, Magic UI, Unlumen UI

## Executive summary

Four public web UI sources have been added to AUTO's reference catalogue. They are primarily React/Next.js and Tailwind-oriented component ecosystems. Their strongest use is as web component, visual-pattern, and motion references.

They are **not Flutter UI kits**. AUTO may extract platform-neutral design and interaction principles from them, but must implement Flutter-native equivalents rather than treating React components as directly portable.

No screenshots have been captured or visually inspected in this pass. This is a metadata review from public documentation and indexed content, not a pixel-level visual audit or a licence review.

## Source-by-source notes

### NeoBrutalism — https://neobrutalism.com/

- Type: neobrutalist design system, React component registry, blocks and templates.
- Stack described by docs: React/Next.js, TypeScript, Tailwind CSS, shadcn CLI.
- Component primitives: Radix UI, Base UI, React Aria variants are documented.
- Homepage advertises 50+ components and 158+ blocks; current component gallery lists 57 components.
- Style traits described by its documentation: thick borders, hard offset shadows, bold/high-contrast fills, heavy type and tactile button feedback.
- MCP server and Figma kit are advertised.
- Evidence: https://neobrutalism.com/ ; https://neobrutalism.com/components ; https://neobrutalism.com/docs ; https://neobrutalism.com/docs/installation
- Audit status: metadata reviewed; screenshots pending.
- Licence/access: check the selected component/block/template terms individually. Do not assume Pro blocks or templates are free.

### SmoothUI — https://smoothui.dev/

- Type: animated React component library.
- Stack described by docs: React, TypeScript, Tailwind CSS, Motion (formerly Framer Motion) and GSAP.
- Docs advertise 181 animated components.
- Categories/examples include text effects, interactive cards, buttons, animated inputs, notifications and dynamic-island-style components.
- Docs describe reduced-motion support and shadcn CLI-compatible installation.
- Evidence: https://smoothui.dev/docs/components ; https://smoothui.dev/docs/guides/animated-components ; https://smoothui.dev/docs/guides
- Audit status: metadata reviewed; screenshots pending.
- Validation required: test actual performance, accessibility and reduced-motion behaviour; marketing claims are not independently benchmarked.

### Magic UI — https://magicui.design/

- Type: animated React components and landing-page visual patterns.
- Stack: React/Next.js ecosystem; component docs expose shadcn-style installation patterns.
- Public docs list components such as Animated Beam, Bento Grid, Magic Card, Marquee, Meteors, Orbiting Circles, Shimmer Button, Safari, animated text and background patterns.
- Evidence: https://magicui.design/ ; https://magicui.design/docs/components
- Audit status: metadata reviewed; screenshots pending.
- Validation required: inspect each selected component's current install instructions, dependency requirements, licence/access tier, responsive behaviour and reduced-motion handling.

### Unlumen UI — https://ui.unlumen.com/

- Type: animated React components/primitives for shadcn projects.
- Stack described by site: React, shadcn conventions, Tailwind CSS, Motion; some image/background examples use Canvas or WebGL.
- Gallery groups: animations, image effects, marketing, navigation, backgrounds/shaders and icons.
- Gallery visibly distinguishes Free and Pro components.
- Examples include hover feature cards, motion FAQ accordion, cursor image trail, tilt cards, animated lists, docks, floating navbars, pixel backgrounds and animated SVG icons.
- Evidence: https://ui.unlumen.com/ ; https://ui.unlumen.com/components
- Audit status: metadata reviewed; screenshots pending.
- Validation required: preserve Free/Pro distinction, inspect WebGL/canvas performance and fallbacks, keyboard access and reduced-motion behaviour.

## Cross-source design insights (metadata-level only)

These are categories to inspect in Chrome, not conclusions about visual quality:
1. Component anatomy and variants.
2. Hover, focus, pressed, loading and disabled states.
3. Motion triggers, spring/timing choices and reduced-motion fallbacks.
4. Responsive behaviour and touch interaction.
5. Accessibility: keyboard navigation, focus visibility, semantic markup and contrast.
6. Dependency footprint and implementation complexity.
7. Free/Pro access and component-level licence clarity.

## AUTO classification and routing

Keep the sources as four distinct source records. Do not merge them into one generic "UI kit".

- NeoBrutalism: design-system/style reference + component registry + blocks/templates.
- SmoothUI: motion-heavy component library.
- Magic UI: animated components + landing-page/background patterns.
- Unlumen UI: motion, image effects, navigation, marketing and shader references.

For Web tasks, route to React/Next.js adapters after checking the actual stack. For Flutter tasks, use these as visual/interaction inspiration only and generate original Dart/Flutter implementations.

Return a bounded set of 2–4 relevant references per task. Do not install any component, MCP server, package, font, or dependency without explicit user approval.

## Chrome inspection checklist for next session

When the user grants browser access:
1. Capture each homepage at desktop and mobile viewport sizes.
2. Open every relevant component gallery and inspect category navigation.
3. Capture each component preview, including hover/focus/pressed states where demonstrable.
4. Open documentation and inspect code examples, install commands, dependencies and variants.
5. Record exact Free/Pro status and licence terms for each candidate component.
6. Test responsive behaviour and reduced-motion controls.
7. Record accessibility evidence; do not assume "accessible" from marketing copy.
8. Save screenshot artifacts outside Git by default, with source URL, viewport, capture time and SHA-256.
9. Update each source record with observed design tokens and interaction patterns.
10. Do not install anything or execute downloaded code during reference capture.

## Current evidence boundary

- Public documentation metadata: reviewed for all four sources.
- Screenshot capture: 0.
- Pixel-level visual audit: not started.
- Source code review: not started.
- Licence clearance: not started.
- Runtime integration: not implemented.

Keep the catalogue status at `metadata_reviewed_not_visually_verified` until the Chrome session produces real screenshot evidence.
