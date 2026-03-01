---
name: mobile-audit
description: Audit mobile optimization — Core Web Vitals, responsive design, touch targets, performance, navigation, and content layout
---

# Mobile Audit — Mobile Optimization & Core Web Vitals

This skill audits a project's mobile experience — Core Web Vitals compliance, responsive design, touch interaction, performance, content layout, and navigation patterns. It identifies issues that hurt mobile usability and SEO ranking, and fixes them directly in the codebase.

No arguments needed. Just run `/mobile-audit` and the skill scans the project automatically.

**Difference from other audits:**
- `/ui-audit` checks **visual polish** — spacing, typography, color, consistency (desktop + mobile)
- `/ux-audit` checks **behavioral outcomes** — cognitive load, decision-making, system feedback
- `/a11y-audit` checks **accessibility** — WCAG compliance, keyboard nav, screen readers
- `/mobile-audit` checks **mobile-specific optimization** — Core Web Vitals, responsive CSS, touch targets, mobile performance, mobile navigation

Reference sources:
- Google Core Web Vitals: https://web.dev/vitals/
- Google Mobile-Friendly Guidelines: https://developers.google.com/search/docs/appearance/mobile
- Apple Human Interface Guidelines (Touch Targets)
- Material Design Touch Target Guidelines

---

## Step 0: Understand the project

Before auditing, read:
- `CLAUDE.md` / `README.md` for project context and stack
- Build configuration (Vite, webpack, etc.) for optimization settings
- CSS architecture (Tailwind, CSS modules, styled-components)
- Image handling (formats, sizes, lazy loading)
- Third-party scripts and their loading strategy
- Navigation component (mobile menu implementation)
- All page components at mobile viewport (320px-414px)

Identify:
- **Build tool** — Vite, webpack, Next.js, etc. (affects optimization approach)
- **CSS framework** — Tailwind, vanilla CSS, etc. (affects responsive strategy)
- **Image pipeline** — manual, Vite plugin, CDN, etc.
- **Critical path** — what must load for first meaningful paint?
- **Third-party script count** — how many external scripts load?

---

## Step 1: Audit across 6 categories

Go through **each category** below. For every issue found, note the file, the specific rule violated, and the recommended fix. Rate severity as:
- **🔴 Critical** — fails Core Web Vitals, broken on mobile, blocks SEO ranking
- **🟠 Major** — noticeably degraded mobile experience
- **🟡 Minor** — optimization opportunity, polish

---

### Category 1: Core Web Vitals

#### LCP — Largest Contentful Paint (≤2.5s)
> The largest visible element (hero image, headline, video) must render within 2.5 seconds on mobile.

**Check for:**
- Hero image not optimized (>100KB, wrong format, no srcset)
- Hero image not preloaded (`<link rel="preload">`)
- Web fonts blocking render (no `font-display: swap`)
- Large above-fold components importing heavy dependencies
- Server response time (TTFB) > 600ms
- Render-blocking CSS or JS in `<head>`
- LCP element hidden behind JavaScript (client-side rendered)

**Fix pattern:**
- Preload LCP image: `<link rel="preload" as="image" href="...">`
- Use WebP/AVIF with fallback: `<picture><source>` or Vite plugin
- Hero images ≤100KB, width ≤1200px for mobile
- Add `font-display: swap` to all `@font-face` declarations
- Inline critical CSS, defer the rest
- Preconnect to critical origins: `<link rel="preconnect" href="...">`

---

#### INP — Interaction to Next Paint (≤200ms)
> Every tap, click, or keypress must produce visible feedback within 200ms.

**Check for:**
- Heavy JavaScript running on the main thread during interaction
- Click handlers with synchronous expensive operations
- No visual feedback on tap (no `:active` state, no loading indicator)
- Third-party scripts blocking the main thread (analytics, chat widgets)
- Large component re-renders on state change
- Event handlers without `passive: true` on scroll/touch listeners

**Fix pattern:**
- Defer non-critical JS: `<script defer>` or dynamic `import()`
- Break long tasks with `requestIdleCallback` or `setTimeout(fn, 0)`
- Add `:active` states to all interactive elements
- Use `will-change` sparingly for animated elements
- Passive event listeners for scroll/touch: `{ passive: true }`
- Code-split heavy components with lazy loading

---

#### CLS — Cumulative Layout Shift (≤0.1)
> No unexpected layout jumps. Every element must have reserved space before it loads.

**Check for:**
- Images without `width` and `height` attributes (or CSS aspect-ratio)
- Web fonts causing text reflow (FOUT without size adjustment)
- Dynamically injected content above the fold (banners, cookie bars pushing content)
- Ads or embeds without reserved space
- CSS animations that change layout properties (`height`, `width`, `top`, `left`)
- Lazy-loaded components that shift content when they appear

**Fix pattern:**
- Always set `width` and `height` on `<img>` and `<video>` elements
- Use `aspect-ratio` CSS for responsive containers
- Use `font-display: swap` + `size-adjust` for font fallbacks
- Reserve space for dynamic content with min-height or skeleton placeholders
- Animate only `transform` and `opacity` (composited properties)
- Cookie banners: overlay, don't push content down

---

### Category 2: Responsive Design

#### Mobile-First CSS
> CSS should be written for 320px first, then scaled up with `min-width` breakpoints.

**Check for:**
- Desktop-first CSS with `max-width` media queries scaling down
- Base styles that assume desktop layout
- Mobile styles overriding desktop with excessive specificity
- Components that look broken at 320px (smallest common viewport)
- Tailwind: using non-prefixed classes for desktop, `sm:` for mobile (inverted)

**Fix pattern:** Base styles = mobile. Add complexity upward:
```css
/* Base = mobile */
.container { padding: 1rem; }
/* Tablet+ */
@media (min-width: 768px) { .container { padding: 2rem; } }
/* Desktop+ */
@media (min-width: 1024px) { .container { padding: 3rem; } }
```

---

#### Fluid Layout
> No fixed pixel widths that break on narrow screens. Use relative units.

**Check for:**
- Fixed `width` values in px on containers or content elements
- Elements wider than viewport causing horizontal scroll
- Fixed-width columns that don't stack on mobile
- `min-width` values that exceed 320px on content elements
- Images or videos with fixed dimensions that overflow

**Fix pattern:**
- Use `%`, `vw`, `rem`, `clamp()` instead of fixed `px` for widths
- `max-width: 100%` on all images and media
- `overflow-x: hidden` on `<body>` as safety net (but fix the cause)
- Use CSS Grid or Flexbox with `flex-wrap: wrap` for adaptive layouts

---

#### No Horizontal Scroll
> The page must never scroll horizontally on any mobile viewport.

**Check for:**
- Elements with `width` > 100vw
- Negative margins pulling content outside viewport
- Absolute/fixed positioned elements outside viewport bounds
- Tables without responsive handling (horizontal overflow)
- Code blocks or pre-formatted text without `overflow-x: auto`
- Hidden overflow on parent but child still causes scrollbar

**Test at:** 320px, 375px, 390px, 414px viewports.

**Fix pattern:** Identify the element causing overflow (DevTools → inspect body width). Fix with `max-width: 100%`, `overflow-x: auto` on tables/code, or responsive restructuring.

---

#### Viewport Meta Tag
> The viewport meta tag must be present and correctly configured.

**Check for:**
- Missing `<meta name="viewport" content="width=device-width, initial-scale=1">`
- `maximum-scale=1` or `user-scalable=no` present (blocks pinch-to-zoom, a11y violation)
- Viewport tag inside `<body>` instead of `<head>`

**Fix pattern:** Add to `<head>`:
```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```
Never add `maximum-scale=1` or `user-scalable=no` — these fail WCAG 1.4.4.

---

### Category 3: Touch & Interaction

#### Tap Target Size (≥48x48px)
> All interactive elements must be at least 48x48px for comfortable thumb tapping.

**Check for:**
- Buttons or links with height/width < 48px on mobile
- Icon buttons without sufficient padding (icon is 24px but no padding to 48px)
- Navigation links that are text-only without padding
- Close buttons (X) that are too small
- Checkbox/radio inputs without enlarged tap areas
- Footer links crammed together without sufficient tap area

**Fix pattern:** Minimum tap target: 48x48px. If the visual element is smaller, expand the tap area with padding:
```css
.icon-button { padding: 12px; /* 24px icon + 24px padding = 48px */ }
```

---

#### Touch Target Spacing (≥8px)
> Adjacent interactive elements must have at least 8px gap to prevent mis-taps.

**Check for:**
- Buttons directly adjacent with no gap
- Inline links too close together
- Form inputs with labels that overlap touch areas
- Navigation items without sufficient spacing
- Social media icon rows without gaps

**Fix pattern:** Add `gap: 8px` or `margin: 4px` between adjacent interactive elements. Audit all button groups, nav items, and link clusters.

---

#### Minimum Font Size (≥16px)
> Body text must be at least 16px on mobile. Smaller text triggers iOS auto-zoom on input focus.

**Check for:**
- Body font-size < 16px
- Input fields with font-size < 16px (iOS zooms on focus)
- Caption/label text below 12px (unreadable on mobile)
- Text that requires pinch-to-zoom to read
- `font-size` set in `px` without responsive scaling

**Fix pattern:**
- Base `font-size: 16px` minimum on body
- All `<input>`, `<select>`, `<textarea>`: `font-size: 16px` minimum (prevents iOS zoom)
- Use `clamp()` for fluid typography: `font-size: clamp(1rem, 2.5vw, 1.25rem)`

---

#### Thumb Zone Placement
> Primary CTAs and frequent actions should be in the bottom 2/3 of the screen (easy thumb reach).

**Check for:**
- Primary CTA only at the top of the page (unreachable after scroll)
- Important actions in top corners (hardest to reach)
- No sticky/fixed CTA for long scroll pages
- Mobile navigation only at the top (consider bottom nav for apps)
- Modal action buttons at the top of the modal

**Fix pattern:**
- Sticky CTA bar at bottom for long pages
- Place primary actions in bottom 66% of viewport
- Bottom sheet patterns for mobile modals (actions at bottom)
- Consider bottom navigation for app-like experiences

---

### Category 4: Performance

#### Image Optimization
> Images are the #1 cause of slow mobile pages. Optimize aggressively.

**Check for:**
- Images served as JPEG/PNG instead of WebP/AVIF
- Hero images > 100KB
- Images without `srcset` for different screen sizes
- Images above fold without `loading="eager"` (or missing explicit loading)
- Images below fold without `loading="lazy"`
- Images without `width` and `height` attributes (causes CLS)
- Images without `decoding="async"`
- SVGs not optimized (unnecessary metadata, excessive precision)
- No image CDN or optimization pipeline

**Fix pattern:**
```html
<!-- Above fold: eager, preloaded -->
<img src="hero.webp" width="800" height="600"
     srcset="hero-400.webp 400w, hero-800.webp 800w"
     sizes="100vw" loading="eager" decoding="async" alt="...">

<!-- Below fold: lazy loaded -->
<img src="card.webp" width="400" height="300"
     loading="lazy" decoding="async" alt="...">
```

---

#### JavaScript Optimization
> Every KB of JS blocks the main thread. Minimize, defer, and split.

**Check for:**
- Bundle size > 200KB (compressed) for initial load
- No code splitting (entire app loads on first page)
- Third-party scripts loaded synchronously (`<script src="...">` without `defer`/`async`)
- Unused JavaScript (tree-shaking not working)
- Polyfills loaded for all browsers (not conditional)
- Heavy libraries imported for small features (e.g., full Lodash for one function)
- No dynamic imports for below-fold components

**Fix pattern:**
- `<script defer>` for all non-critical JS
- Dynamic `import()` for below-fold components and routes
- Analyze bundle: `npx vite-bundle-visualizer` or `webpack-bundle-analyzer`
- Replace heavy libraries with lighter alternatives or native APIs
- Tree-shake: use named imports (`import { debounce } from 'lodash-es'`)

---

#### CSS Optimization
> CSS blocks rendering. Minimize render-blocking CSS.

**Check for:**
- Large CSS bundle loaded entirely in `<head>` (blocks first paint)
- Unused CSS rules (check with Coverage tab in DevTools)
- CSS `@import` chains (each one is a network request)
- Heavy animations using layout properties (`width`, `height`, `top`, `left`)
- No critical CSS inlining for above-fold content

**Fix pattern:**
- Inline critical CSS for above-fold content
- Load non-critical CSS with `media="print" onload="this.media='all'"`
- Purge unused CSS (Tailwind does this by default in production)
- Animate only `transform` and `opacity`

---

#### Font Loading
> Web fonts block text rendering. Load them without blocking.

**Check for:**
- Fonts loaded from Google Fonts CDN (render-blocking + third-party transfer)
- Missing `font-display: swap` or `font-display: optional`
- Too many font weights loaded (each is a separate file)
- Font files > 50KB per weight
- No `preload` for critical fonts
- No font subsetting (loading full Unicode range for Latin text)

**Fix pattern:**
- Self-host fonts (avoid third-party CDN)
- `font-display: swap` on all `@font-face`
- Preload critical fonts: `<link rel="preload" as="font" type="font/woff2" href="..." crossorigin>`
- Subset fonts to Latin characters only
- Limit to 2-3 weights maximum
- Use `size-adjust` on fallback fonts to reduce CLS

---

#### Compression & Caching
> Assets must be compressed and cached.

**Check for:**
- No Gzip/Brotli compression on text assets (HTML, CSS, JS, SVG)
- Missing cache headers (`Cache-Control`) on static assets
- No content hashing in filenames (breaks cache busting)
- Large uncompressed SVGs
- No `preconnect` to critical third-party origins

**Fix pattern:**
- Enable Brotli (preferred) or Gzip on server/CDN
- Static assets: `Cache-Control: public, max-age=31536000, immutable`
- HTML: `Cache-Control: no-cache` (always revalidate)
- Vite/webpack: content hashing enabled by default in production builds
- `<link rel="preconnect" href="https://fonts.googleapis.com">`

---

### Category 5: Content & Layout

#### Above-Fold Content (≤1s)
> Value proposition + primary CTA must be visible within 1 second on mobile, without scrolling.

**Check for:**
- Hero section requires scroll to see CTA
- Large hero image/video delays content visibility
- Above-fold content depends on JavaScript to render
- Cookie banner covers the entire above-fold area
- Navigation pushes content below the fold on mobile

**Fix pattern:** On 375px viewport, the headline + subline + CTA must all be visible without scrolling. Reduce hero image size, move CTA up, ensure no overlay blocks it.

---

#### Content Parity
> Mobile and desktop users should see the same content. No `display: none` hiding.

**Check for:**
- Content hidden on mobile with `display: none` or `hidden` that's visible on desktop
- Simplified mobile version missing key information
- Different text content for mobile vs. desktop (except layout adaptations)
- Features disabled on mobile without explanation
- Links/CTAs present on desktop but missing on mobile

**Fix pattern:** Same content, different layout. Use responsive CSS to reflow, not to hide. If content must differ, ensure mobile has equivalent information.

---

#### No Intrusive Interstitials
> Pop-ups must not block content on mobile (Google penalizes this).

**Check for:**
- Full-screen pop-ups on page load
- Interstitials that cover >30% of the viewport
- Pop-ups without easy, visible dismiss button
- Cookie banners that block all content (should overlay, not block)
- Newsletter modals on first visit before user engagement
- Interstitials that can't be dismissed on mobile (X button too small or missing)

**Exceptions (allowed):**
- Legal requirement interstitials (age verification, cookie consent)
- Login dialogs for gated content
- App install banners that use a small portion of the screen

**Fix pattern:** Use non-intrusive alternatives: inline banners, slide-ups, bottom sheets. Delay pop-ups until engagement signal (scroll depth, time on page).

---

#### Mobile Typography
> Text must be readable on mobile without zooming.

**Check for:**
- Line length > 80 characters on mobile (too wide to scan)
- Line-height < 1.5 for body text on mobile
- Paragraphs > 3 lines on mobile without visual break
- Text overlapping or clipping at narrow viewports
- Contrast issues on mobile (glare-prone screens need higher contrast)

**Fix pattern:** Line length: 45-75 characters on mobile. Line-height: 1.5-1.7 for body. Short paragraphs. Test on actual device in sunlight.

---

### Category 6: Mobile Navigation

#### Mobile Menu Pattern
> Navigation must be accessible, simple, and predictable on mobile.

**Check for:**
- No hamburger menu (all nav items crammed in header)
- Hamburger menu with > 7 items (too many)
- Deep flyout/mega menus on mobile (unusable)
- Menu doesn't close on link click (SPA issue)
- Menu doesn't close on outside tap
- Menu doesn't close on Escape key
- No visual indicator of current page in menu
- Menu animation janky or missing

**Fix pattern:** Hamburger menu with 5-7 items max. Full-screen or slide-in overlay. Close on: link click, outside tap, Escape key. Animate with `transform` (smooth).

---

#### Sticky Navigation
> Navigation should remain accessible during scroll on long pages.

**Check for:**
- Navigation scrolls away on long pages (no sticky header)
- Sticky header too tall on mobile (wastes viewport space)
- Sticky header without hide-on-scroll-down / show-on-scroll-up behavior
- Sticky CTA bar overlapping with sticky header
- Sticky elements causing content clipping

**Fix pattern:** Sticky header: max 56-64px height on mobile. Consider hide on scroll down, show on scroll up. Ensure no content is hidden behind sticky elements (`scroll-padding-top`).

---

#### Back Button & History
> The browser back button must always work as expected.

**Check for:**
- SPA navigation that breaks browser back button
- Modals/overlays that don't push history state (back button goes to previous page instead of closing)
- Multi-step flows (surveys, checkout) where back goes to wrong step
- Hash-based navigation that confuses history
- Infinite scroll that loses scroll position on back

**Fix pattern:** Use `history.pushState` for significant view changes. Modals should push state so back closes them. Multi-step flows should support back navigation per step.

---

#### Scroll & Gesture Behavior
> Scrolling must feel native. Custom gestures must be intuitive.

**Check for:**
- Custom scroll hijacking (parallax, scroll snapping that feels broken)
- Scroll snapping without `-webkit-overflow-scrolling: touch` on iOS
- Pull-to-refresh interference with custom scroll areas
- Horizontal scroll areas without visual indicator (no scrollbar, no peek)
- Swipe gestures that conflict with browser back/forward (edge swipe)
- `overflow: hidden` on body that prevents scrolling (common modal bug)

**Fix pattern:** Use native scrolling. If using scroll snap, test on real iOS/Android devices. Horizontal scroll areas: show partial next item (closure principle). Never hijack native gestures.

---

## Step 2: Report findings

Present findings grouped by severity:

```
## Mobile Audit Results

### Core Web Vitals Estimate
| Metric | Target | Estimated Status | Notes |
|--------|--------|-----------------|-------|
| LCP | ≤2.5s | 🟢/🟡/🔴 | [what's the LCP element?] |
| INP | ≤200ms | 🟢/🟡/🔴 | [main thread blockers?] |
| CLS | ≤0.1 | 🟢/🟡/🔴 | [layout shift sources?] |

### 🔴 Critical — fails CWV, broken on mobile, SEO impact
| Issue | Rule | File | Recommended Fix |
|-------|------|------|-----------------|
| ... | ... | ... | ... |

### 🟠 Major — degraded mobile experience
| Issue | Rule | File | Recommended Fix |
|-------|------|------|-----------------|
| ... | ... | ... | ... |

### 🟡 Minor — optimization opportunity
| Issue | Rule | File | Recommended Fix |
|-------|------|------|-----------------|
| ... | ... | ... | ... |

### ✅ Well done
- [list what the project already does well for mobile]
```

Ask the user: **"Soll ich die Issues fixen? Alle oder nur die kritischen?"**

---

## Step 3: Fix issues

Apply fixes directly in the codebase. For each fix:
- Reference which mobile rule it addresses
- Test mentally at 320px, 375px, and 414px viewports
- Prioritize: (1) Core Web Vitals, (2) touch targets, (3) responsive layout, (4) performance
- Never break desktop experience while fixing mobile
- Follow the project's existing code style and design system

---

## Step 4: Summary

```
Mobile Audit Complete!

✅ [N] issues fixed
⚠️ [N] issues flagged for manual review

Core Web Vitals estimate:
- LCP: [status] — [key change]
- INP: [status] — [key change]
- CLS: [status] — [key change]

Top 3 highest-impact changes:
1. [change] — [expected impact on CWV/mobile UX]
2. [change] — [expected impact on CWV/mobile UX]
3. [change] — [expected impact on CWV/mobile UX]

Recommended next steps:
- Run Google PageSpeed Insights (mobile) and verify ≥90
- Test on real device (iPhone SE, Android mid-range)
- Check Core Web Vitals in Google Search Console (28-day data)
- Test at 320px, 375px, 390px, 414px viewports
- Verify no horizontal scroll at any viewport
- Run Lighthouse mobile audit in Chrome DevTools
```

---

## Rules

- **Audit mobile experience specifically**, not general UX or visual design
- **320px is the floor** — everything must work at 320px viewport width
- Don't duplicate `/ui-audit` — reference it for visual consistency, focus here on mobile-specific issues
- Don't duplicate `/a11y-audit` — reference it for WCAG, focus here on mobile touch/viewport issues
- Core Web Vitals are hard requirements, not nice-to-haves (Google ranks by them)
- Test at real mobile viewports (320px, 375px, 390px, 414px), not just "responsive mode"
- Never add `user-scalable=no` or `maximum-scale=1` — these are accessibility violations
- Performance fixes should not sacrifice functionality
- Mobile fixes must not break desktop layout
- Follow the project's existing code style and component patterns
