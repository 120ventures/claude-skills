---
name: ui-audit
description: Audit visual UI quality — layout hierarchy, spacing, typography, color, consistency, and Gestalt grouping
---

# UI Audit — Visual Design Quality

This skill audits a project's visual UI quality — the "does it look right and feel polished?" layer. It checks layout hierarchy, typography, spacing, color use, Gestalt grouping, interaction affordances, and pattern consistency. This sits between a11y (can people use it?) and UX (do people want to use it?).

No arguments needed. Just run `/ui-audit` and the skill scans the project automatically.

**Difference from `/ux-audit`:**
- `/ux-audit` checks **behavioral outcomes** — does the flow cause drop-off? is the user confused?
- `/ui-audit` checks **visual implementation** — is spacing consistent? is typography hierarchy clear? do controls look clickable?

This is what a designer would critique in a visual review — pixel-level, component-level quality.

---

## Step 0: Understand the project

Before auditing, read:
- `CLAUDE.md` / `README.md` for project context and design system
- `src/index.css` or equivalent for CSS custom properties, font imports, color tokens
- Layout constants and shared spacing tokens
- All page components (understand the visual structure)
- Component library / UI kit in use (Shadcn, MUI, etc.)

Identify:
- **Design system tokens** — colors, spacing scale, typography scale, border radii
- **Layout pattern** — max-width, padding, grid system
- **Component patterns** — how cards, buttons, inputs, sections are styled
- **Brand identity** — visual tone, premium vs. playful, serif vs. sans-serif

---

## Step 1: Audit across 4 categories

Go through **each category** below. For every issue found, note the file, the specific principle violated, and the recommended fix. Rate severity as:
- **🔴 Critical** — visually broken, clearly wrong, damages trust
- **🟠 Major** — noticeable inconsistency, looks unpolished
- **🟡 Minor** — polish opportunity, design refinement

---

### Category 1: Visual Layout & Hierarchy

#### Visual Hierarchy
> The most important elements should be the most visually prominent — through size, weight, color, and position.

**Check for:**
- Page sections where nothing stands out as the primary element
- Headlines that don't feel more important than body text
- CTAs that blend into surrounding content
- Competing visual weights where one element should dominate
- Z-pattern or F-pattern violations on content-heavy pages

**Fix pattern:** Increase size/weight contrast between hierarchy levels. Primary elements should be 1.5-2x more prominent than secondary. Use the design system's heading scale consistently.

---

#### Scale & Contrast
> Visual weight signals importance. Size differences should be meaningful, not arbitrary.

**Check for:**
- Heading sizes that are too similar (e.g., h2 and h3 nearly identical)
- Text sizes that jump erratically instead of following a type scale
- Elements that should feel different but are the same size
- Icon sizes inconsistent with adjacent text
- Decorative elements that overpower content

**Fix pattern:** Use a consistent type scale (e.g., 1.25 or 1.333 ratio). Ensure at least 2px difference between adjacent levels. Icons should match the x-height or cap-height of adjacent text.

---

#### White Space
> Space creates focus, readability, and breathing room. It's not empty — it's functional.

**Check for:**
- Sections crammed together without vertical rhythm
- Text blocks without adequate line-height (body < 1.5, headings < 1.2)
- Cards/containers with insufficient internal padding
- Inconsistent spacing between similar section types
- Content touching container edges without margin/padding

**Fix pattern:** Use the spacing scale from the design system. Section padding should be consistent (e.g., `py-16` or `py-24`). Internal card padding should be at least `p-6`. Line-height: 1.5-1.7 for body, 1.1-1.3 for headings.

---

#### Typography Hierarchy
> Clear, distinct levels: h1 → h2 → h3 → body → caption. Each should be instantly distinguishable.

**Check for:**
- Missing or unclear heading levels (h1 and h2 look the same)
- Body text competing with headings in visual weight
- Captions/labels that are too similar to body text
- Inconsistent font-weight usage across same-level headings
- Mixed font families without clear purpose (display vs. body)
- Orphaned headings (heading styles used without semantic hierarchy)

**Fix pattern:** Define 5-6 distinct text styles and use them consistently. Each level should differ in at least 2 properties (size + weight, or size + color). Document in the design system.

---

#### Color Use
> Color should be meaningful, restrained, and intentional. Every color should have a job.

**Check for:**
- Accent color used for too many things (loses impact)
- Accent color used for non-interactive elements (confuses affordance)
- Colors not from the design system palette
- Too many colors competing (>3-4 distinct hues)
- Background colors that don't create clear section boundaries
- Foreground/background combinations with insufficient contrast (< 4.5:1 for text)

**Fix pattern:** Limit accent color to interactive elements and key highlights. Use neutral tones for structure. Each color in the palette should have a clear role (bg, text, accent, muted, border).

---

### Category 2: Perception & Grouping (Gestalt for UI)

#### Proximity — Spacing as Data Structure
> Elements close together are perceived as related. Spacing communicates structure.

**Check for:**
- Label-input gaps larger than input-input gaps (label feels detached from its field)
- Card content with equal spacing between all elements (no internal grouping)
- Section headings closer to the previous section than to their own content
- Footer links with no spatial grouping by category
- List items with spacing that doesn't reflect logical groups

**Fix pattern:** Inner spacing (within a group) should be notably tighter than outer spacing (between groups). Rule of thumb: inter-group spacing ≥ 2× intra-group spacing.

---

#### Similarity — Consistent Styling for Same-Type Elements
> Elements that look the same are perceived as the same type. Visual consistency = semantic consistency.

**Check for:**
- Buttons with different border-radius, padding, or font-size for same importance level
- Card components with inconsistent styling across pages/sections
- Links styled differently in different contexts (some underlined, some colored, some both)
- Headings using different font-weights at the same semantic level
- Icon styles mixing outlined and filled within the same context

**Fix pattern:** Create and enforce component variants: `primary`, `secondary`, `ghost`. Same variant = same visual treatment everywhere. Audit all instances of each component type.

---

#### Common Region / Uniform Connectedness
> Elements within a bounded area (card, panel, background color) are perceived as a group.

**Check for:**
- Logical groups without visual containers (related items floating without a card/border/background)
- Cards or panels that contain unrelated content
- Background color changes that don't align with content grouping
- Nested cards creating confusing visual depth
- Missing dividers between distinct content sections within a container

**Fix pattern:** Use cards, subtle background shifts, or borders to group related content. One visual container = one logical group. Avoid nesting more than 2 levels deep.

---

#### Continuity — Alignment & Grid Consistency
> The eye follows smooth paths. Alignment creates visual flow and order.

**Check for:**
- Elements breaking the grid (misaligned left edges, inconsistent column widths)
- Text blocks with different left margins across sections
- Images or cards not aligned to the same grid
- Mixed alignment patterns (some sections centered, some left-aligned) without clear purpose
- Baseline misalignment between adjacent text elements

**Fix pattern:** Establish a grid (e.g., 12-column) and align everything to it. Left edges should align vertically across sections. If mixing alignment, do so deliberately (e.g., hero centered, content left-aligned).

---

#### Closure & Pragnanz — Clean, Minimal, Complete Forms
> People perceive the simplest, most complete interpretation. Incomplete or ambiguous shapes create tension.

**Check for:**
- Partially visible elements that look broken rather than intentional
- Cards or containers with inconsistent corner treatments
- Progress indicators that don't clearly show completion state
- Decorative elements that create visual noise without meaning
- Asymmetric layouts that feel unbalanced rather than intentionally dynamic

**Fix pattern:** Every visual element should feel complete and intentional. If something is partially visible (carousel peek), make the clip clearly intentional. Maintain consistent border-radius, shadows, and corner treatments.

---

### Category 3: Interaction & Controls

#### Fitts's Law — Target Size & Clickable Affordance
> Interaction targets should be appropriately sized and visually signal clickability.

**Check for:**
- Buttons/links with no hover state or cursor change
- Interactive elements that look like static text (no underline, no color, no affordance)
- Touch targets smaller than 44×44px on mobile
- Click targets where the visual element is smaller than the hit area (or vice versa)
- Primary CTAs that are the same size as secondary actions
- Text links without any visual differentiation from body text

**Fix pattern:** All interactive elements need: (1) visual affordance (color, underline, or shape), (2) hover/focus state, (3) adequate size (min 44px touch, 32px click). Primary CTA should be visually larger than secondary.

---

#### Hick's Law — Menu & Toolbar Overload
> More options = more decision time. Reduce visible choices, especially for first-time users.

**Check for:**
- Navigation with too many visible items at the same level
- Toolbars or action bars with >5 visible actions
- Dropdown menus with >10 ungrouped items
- Form fields presenting too many radio/checkbox options without structure
- Feature grids showing everything at once without progressive disclosure

**Fix pattern:** Group related actions. Show 3-5 primary options, nest the rest. Use progressive disclosure (accordion, "show more", tabs). Highlight the recommended/default option.

---

#### Aesthetic-Usability Effect — Polish = Perceived Usability + Trust
> Visually polished interfaces are perceived as easier to use and more trustworthy, even before interaction.

**Check for:**
- Inconsistent border-radius across components (some rounded-lg, some rounded-md, some sharp)
- Mixed shadow styles (some components with shadow, others without, inconsistently)
- Favicon, logo, and brand elements that look low-resolution or misaligned
- Transitions/animations that feel janky or inconsistent (some 200ms, some 500ms)
- Generic placeholder content that wasn't replaced (Lorem ipsum, placeholder.com images)
- Micro-details: bullet styles, divider consistency, icon stroke widths

**Fix pattern:** Pick consistent values for border-radius, shadow, transition duration, and apply everywhere. Audit all micro-details. Every pixel matters for trust.

---

#### Doherty Threshold — Perceived Performance & Sub-Second Feedback
> Interactions should feel responsive. Feedback within 400ms keeps users in flow.

**Check for:**
- Buttons with no visual feedback on click (no active/pressed state)
- Form submissions without immediate visual response
- Page transitions that feel abrupt (no skeleton, no fade)
- Images loading without placeholders (layout shift)
- Animations that are too slow (>500ms for micro-interactions) or too fast (<100ms, invisible)

**Fix pattern:** Add `:active` states to all buttons. Use skeleton loaders or fade-ins for async content. Micro-interactions: 150-300ms. Page transitions: 200-400ms. Always show loading state for operations >300ms.

---

### Category 4: Consistency & Patterns

#### Internal Consistency
> Same things should look and behave the same way everywhere in the UI.

**Check for:**
- Same component styled differently across pages (e.g., card on landing vs. card in survey)
- Inconsistent spacing tokens (one section uses `gap-4`, another uses `gap-6` for same layout)
- Button variants used inconsistently (primary style for secondary actions somewhere)
- Different heading styles for same hierarchy level across pages
- Inconsistent icon sizes or styles across the interface
- Color usage that varies by page (accent for links on one page, for backgrounds on another)

**Fix pattern:** Extract shared components. Create a component audit spreadsheet: list every instance of buttons, cards, headings, spacing — find and fix deviations. Use design tokens consistently.

---

#### Jakob's Law — Follow Web Conventions
> Users expect your product to work like products they already know. Don't reinvent standard patterns.

**Check for:**
- Logo not in top-left (or center for mobile)
- Navigation not at the top of the page
- Non-standard hamburger menu behavior
- Footer missing expected links (privacy, terms, contact)
- Form inputs that don't look like inputs (no border, no background differentiation)
- Modals/overlays that can't be dismissed with Escape or background click
- Scroll behavior that hijacks native scrolling

**Fix pattern:** Follow platform conventions. Use standard patterns for nav, forms, modals, footers. Only deviate when the custom pattern is clearly better AND thoroughly tested.

---

#### Postel's Law for Inputs — Generous Acceptance, Strict Display
> Accept diverse input formats gracefully. Display output consistently and cleanly.

**Check for:**
- Email inputs that reject valid formats (plus addressing, long TLDs)
- Phone inputs requiring specific formatting (parentheses, dashes)
- Date inputs that only accept one format
- Name fields that reject special characters (apostrophes, hyphens, umlauts)
- Search that requires exact matches instead of fuzzy matching
- Error messages that say "invalid" without showing the expected format

**Fix pattern:** Accept liberally, normalize internally, display consistently. Show format examples in placeholders. Auto-format on blur. Error messages should show what's expected, not just what's wrong.

---

## Step 2: Report findings

Present findings grouped by severity:

```
## UI Audit Results

### 🔴 Critical — visually broken, damages trust
| Issue | Principle | File | Recommended Fix |
|-------|-----------|------|-----------------|
| ... | ... | ... | ... |

### 🟠 Major — noticeable inconsistency
| Issue | Principle | File | Recommended Fix |
|-------|-----------|------|-----------------|
| ... | ... | ... | ... |

### 🟡 Minor — polish opportunities
| Issue | Principle | File | Recommended Fix |
|-------|-----------|------|-----------------|
| ... | ... | ... | ... |

### ✅ Well done
- [list what the project already does well, referencing which principles it follows]
```

Ask the user: **"Soll ich die Issues fixen? Alle oder nur die kritischen?"**

---

## Step 3: Fix issues

Apply fixes directly in the codebase. For each fix:
- Reference which visual principle it addresses in a brief code comment (only if non-obvious)
- Prioritize fixes that affect above-the-fold content and primary conversion flow
- Never break existing functionality
- Follow the project's existing code style and design system
- Use design system tokens — never introduce hardcoded values

---

## Step 4: Summary

```
UI Audit Complete!

✅ [N] issues fixed
⚠️ [N] issues flagged for manual review

Principles applied:
- [list which visual principles were most relevant]

Top 3 highest-impact changes:
1. [change] — [which principle, visual impact]
2. [change] — [which principle, visual impact]
3. [change] — [which principle, visual impact]

Recommended next steps:
- Screenshot comparison (before/after) on key breakpoints
- Cross-browser check (Safari, Firefox, Chrome) for rendering consistency
- Mobile device testing for touch targets and spacing
- Design review with stakeholders on visual hierarchy changes
```

---

## Rules

- **Audit the visual implementation**, not behavioral UX or code quality
- Focus on **above-the-fold content and the primary flow** first
- Reference specific design principles by name — this creates shared vocabulary with designers
- Don't over-optimize for one principle at the expense of another (they can conflict)
- Respect the project's brand and design system — enhance, don't override
- Fixes should use existing design tokens and components, not introduce new ones
- German UI text for German-language projects
- Use the project's existing spacing scale, color palette, and typography — never hardcode values
- Follow the project's existing code style and component patterns
- Check at both mobile (375px) and desktop (1440px) breakpoints
