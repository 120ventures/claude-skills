---
name: ux-audit
description: Audit UX against established UX laws, cognitive principles, Gestalt perception, and Nielsen's heuristics — with actionable fixes
---

# UX Audit — Laws of UX + Heuristics + Gestalt Principles

This skill audits a project's user experience against established UX laws, cognitive principles, and design heuristics. It identifies violations, explains which law applies, and fixes issues directly in the codebase.

No arguments needed. Just run `/ux-audit` and the skill scans the project automatically.

Reference sources:
- Jon Yablonski's Laws of UX: https://lawsofux.com/
- Nielsen Norman Group Heuristics: https://www.nngroup.com/articles/ten-usability-heuristics/
- Gestalt Principles of Perception

---

## Step 0: Understand the project

Before auditing, read:
- `CLAUDE.md` / `README.md` for project context
- All page components (understand the user journey)
- Navigation structure and routing
- Forms and multi-step flows
- CTAs and conversion funnels
- Layout and component hierarchy

Identify:
- **Primary conversion goal** (what's the one thing the user should do?)
- **User journey** (landing → exploration → conversion)
- **Key decision points** (where users choose between options)

---

## Step 1: Audit against UX Laws

Go through **each category** below. For every issue found, note the file, the specific UX law violated, and the recommended fix. Rate severity as:
- **🔴 Critical** — likely causing drop-off or confusion
- **🟠 Major** — friction that degrades experience
- **🟡 Minor** — improvement opportunity

---

### Category 1: Decision-Making & Cognition

#### Hick's Law
> Decision time increases as the number and complexity of choices increases.

**Check for:**
- Navigation with too many items (>7 top-level links)
- Forms presenting too many options at once
- Pages with multiple competing CTAs
- Feature sections with >5 items shown simultaneously without hierarchy

**Fix pattern:** Reduce choices, group into categories, use progressive disclosure, highlight recommended option.

---

#### Miller's Law
> Working memory holds about 7±2 items — chunk information.

**Check for:**
- Long unbroken lists (>7 items without grouping)
- Forms with >7 fields on one screen
- Navigation menus with >7 ungrouped items
- Phone numbers, codes, or IDs displayed without chunking

**Fix pattern:** Group into chunks of 3-5 items, use headings/dividers, split long forms into steps.

---

#### Tesler's Law (Conservation of Complexity)
> Every system has inherent complexity — you can only shift it between system and user.

**Check for:**
- Complex configuration pushed to the user when the system could have smart defaults
- Required fields that could be auto-filled or inferred
- Manual steps the system could automate

**Fix pattern:** Move complexity to the system — smart defaults, auto-detection, progressive disclosure.

---

#### Occam's Razor
> Prefer the simplest solution; avoid unnecessary complexity.

**Check for:**
- Over-engineered UI patterns (custom widgets where native elements work)
- Unnecessary steps in user flows
- Visual clutter that doesn't serve the user's goal
- Features that exist "just in case"

**Fix pattern:** Remove what doesn't serve the primary goal. Simplify.

---

#### Pareto Principle (80/20)
> A small set of features delivers most of the value.

**Check for:**
- All features given equal visual weight
- Primary CTA not clearly dominant
- Secondary actions competing with primary actions

**Fix pattern:** Visually prioritize the 20% of features that deliver 80% of value. De-emphasize the rest.

---

#### Goal-Gradient Effect
> Users accelerate as they perceive proximity to goal completion.

**Check for:**
- Multi-step forms/surveys without progress indicators
- Checkout flows without step count
- Onboarding without completion tracking

**Fix pattern:** Add progress bars, step indicators ("Schritt 2 von 5"), completion percentages.

---

#### Zeigarnik Effect
> Incomplete tasks are remembered better — visible incomplete states motivate completion.

**Check for:**
- Abandoned form states not saved
- No "continue where you left off" for multi-step flows
- Profile completion without progress indicator

**Fix pattern:** Show incomplete state, save progress, prompt to continue.

---

#### Serial Position Effect
> Items at beginning and end of a list are remembered best.

**Check for:**
- Most important features buried in the middle of lists
- Key CTAs in the middle of navigation
- Critical info in the middle of long content sections

**Fix pattern:** Place most important items first and last. Primary CTA at top and bottom of page.

---

#### Von Restorff Effect (Isolation Effect)
> Visually distinct items are more memorable.

**Check for:**
- Primary CTA that doesn't stand out from secondary actions
- All buttons/links styled the same regardless of importance
- No visual hierarchy between primary and secondary content

**Fix pattern:** Make the primary action visually distinct — different color, size, or style from everything else.

---

### Category 2: Interaction & Performance

#### Fitts's Law
> Time to reach a target depends on size and distance. Make key targets large and close.

**Check for:**
- Small click/tap targets (<44px on mobile, <32px on desktop)
- Primary CTAs far from the user's current focus area
- Important actions in hard-to-reach corners
- Close buttons that are too small
- Links/buttons with tiny hit areas (text-only without padding)

**Fix pattern:** Increase target size (min 44×44px touch), place primary actions within thumb reach on mobile, add generous padding to interactive elements.

---

#### Doherty Threshold
> Response times under ~400ms keep users in flow.

**Check for:**
- No loading states for async operations
- No optimistic UI updates
- Heavy animations that delay perceived responsiveness
- Form submissions without immediate feedback

**Fix pattern:** Add loading spinners/skeletons, use optimistic updates, show immediate visual feedback on interaction.

---

#### Postel's Law
> Be liberal in what you accept, conservative in what you send.

**Check for:**
- Overly strict form validation (rejecting valid input formats)
- Phone/date inputs that require exact formatting
- Error messages that don't explain what's expected
- Case-sensitive inputs where case doesn't matter

**Fix pattern:** Accept multiple input formats, auto-format on blur, show clear examples in placeholders.

---

#### Peak-End Rule
> Experience is judged by its peak moment and its ending.

**Check for:**
- Anticlimactic completion states (form submitted → blank page)
- No celebration/confirmation after key conversions
- Error-heavy endings (payment page full of warnings)
- Abrupt session endings

**Fix pattern:** Design a satisfying peak moment and a memorable ending — success animations, confirmation messages, clear next steps.

---

### Category 3: Familiarity & Consistency

#### Jakob's Law
> Users expect your product to work like products they already use.

**Check for:**
- Non-standard navigation patterns
- Logo not linking to homepage
- Shopping cart not in top-right (for e-commerce)
- Unconventional form patterns
- Custom scrolling behavior that overrides native scroll

**Fix pattern:** Follow platform conventions. Use established patterns unless you have a strong reason not to.

---

#### Mental Models
> Interfaces should match users' existing expectations.

**Check for:**
- Terminology that doesn't match user language
- Workflows that don't match real-world processes
- Icons that don't match their common meaning
- Categories/grouping that doesn't match user expectations

**Fix pattern:** Use language your users use. Test terminology. Match real-world mental models.

---

#### Nielsen's 10 Heuristics

Audit against each:

| # | Heuristic | What to check |
|---|-----------|---------------|
| 1 | **Visibility of system status** | Loading states, progress indicators, current page indication in nav, form validation feedback |
| 2 | **Match between system and real world** | Natural language, familiar icons, logical ordering, real-world metaphors |
| 3 | **User control and freedom** | Undo/back actions, exit points from flows, ability to dismiss modals, cancel operations |
| 4 | **Consistency and standards** | Same action = same result everywhere, consistent styling, platform conventions |
| 5 | **Error prevention** | Confirmation for destructive actions, input constraints, disable invalid submit |
| 6 | **Recognition over recall** | Visible options vs. hidden menus, labels on icons, recently used items |
| 7 | **Flexibility and efficiency** | Keyboard shortcuts, power-user paths, personalization options |
| 8 | **Aesthetic and minimalist design** | No irrelevant info, clean visual hierarchy, content-to-chrome ratio |
| 9 | **Help users recognize, diagnose, recover from errors** | Clear error messages, suggested fixes, non-technical language |
| 10 | **Help and documentation** | FAQ, tooltips, onboarding guidance, contextual help |

---

### Category 4: Visual Perception (Gestalt Principles)

#### Law of Prägnanz (Simplicity)
> People perceive complex images in their simplest form.

**Check for:**
- Overly complex layouts that aren't scannable
- Too many visual elements competing for attention
- Unclear visual hierarchy

**Fix pattern:** Simplify. Use clear sections, whitespace, and visual hierarchy.

---

#### Law of Proximity
> Elements close together are perceived as related.

**Check for:**
- Related items spaced too far apart (label far from its input)
- Unrelated items too close together (causing false grouping)
- Inconsistent spacing between related vs. unrelated elements

**Fix pattern:** Group related elements with tight spacing. Separate unrelated elements with more space.

---

#### Law of Similarity
> Similar-looking elements are seen as part of the same group.

**Check for:**
- Buttons that look the same but do different things
- Different element types that look identical
- Inconsistent styling for same-type elements

**Fix pattern:** Style similar functions similarly. Differentiate different functions visually.

---

#### Law of Common Region
> Elements within a bounded area are perceived as grouped.

**Check for:**
- Card/section boundaries that don't match logical grouping
- Missing visual containers for related content
- Content that logically belongs together but isn't visually grouped

**Fix pattern:** Use cards, borders, or background colors to group related content.

---

#### Law of Common Fate
> Elements moving in the same direction are perceived as grouped.

**Check for:**
- Animations where unrelated elements move together
- Scroll effects that group unrelated content
- Carousel items that should feel independent but move as one

**Fix pattern:** Animate related elements together, unrelated elements independently.

---

#### Law of Continuity
> People prefer smooth, continuous paths.

**Check for:**
- Broken visual lines or alignment
- Inconsistent grid alignment across sections
- Progress flows that feel disconnected

**Fix pattern:** Maintain visual continuity. Align elements on a consistent grid.

---

#### Law of Closure
> People mentally complete incomplete shapes.

**Check for:**
- Intentional use: carousel items partially visible at edge (signals scrollability)
- Unintentional: cut-off content that looks broken vs. intentional peek

**Fix pattern:** Use partial visibility intentionally to signal more content. Avoid accidental cutoffs.

---

### Category 5: Emotion, Aesthetics & Trust

#### Aesthetic-Usability Effect
> Attractive interfaces are perceived as easier to use and more trustworthy.

**Check for:**
- Inconsistent visual design across pages
- Dated or generic UI patterns
- Mismatched typography or color usage
- Low-quality images or icons

**Fix pattern:** Ensure consistent, polished visual design. Every detail matters for trust.

---

#### Social Proof & Authority
> Users are influenced by what others do and who endorses the product.

**Check for:**
- Missing testimonials or reviews
- No trust indicators (logos, certifications, user counts)
- Claims without backing evidence
- No "used by" or "as seen in" signals

**Fix pattern:** Add testimonials, user counts, trust badges, expert endorsements where authentic.

---

#### Scarcity & Loss Aversion
> Limited availability and potential loss influence decisions.

**Check for:**
- No urgency signals where appropriate (limited spots, deadlines)
- No indication of what users miss by not acting
- Overuse of fake scarcity (damages trust)

**Fix pattern:** Use authentic scarcity signals. Frame value in terms of what users gain AND what they'd miss.

---

## Step 2: Report findings

Present findings grouped by severity:

```
## UX Audit Results

### 🔴 Critical — likely causing drop-off
| Issue | UX Law | File | Recommended Fix |
|-------|--------|------|-----------------|
| ... | ... | ... | ... |

### 🟠 Major — noticeable friction
| Issue | UX Law | File | Recommended Fix |
|-------|--------|------|-----------------|
| ... | ... | ... | ... |

### 🟡 Minor — polish opportunities
| Issue | UX Law | File | Recommended Fix |
|-------|--------|------|-----------------|
| ... | ... | ... | ... |

### ✅ Well done
- [list what the project already does well, referencing which UX laws it follows]
```

Ask the user: **"Soll ich die Issues fixen? Alle oder nur die kritischen?"**

---

## Step 3: Fix issues

Apply fixes directly in the codebase. For each fix:
- Reference which UX law it addresses in a brief code comment (only if non-obvious)
- Prioritize fixes that affect the primary conversion funnel
- Never break existing functionality
- Follow the project's existing code style and design system

---

## Step 4: Summary

```
UX Audit Complete!

✅ [N] issues fixed
⚠️ [N] issues flagged for manual review

Laws applied:
- [list which UX laws were most relevant]

Top 3 highest-impact changes:
1. [change] — [which law, expected impact]
2. [change] — [which law, expected impact]
3. [change] — [which law, expected impact]

Recommended next steps:
- User testing with 3-5 real users on the primary flow
- Heatmap analysis (PostHog/Hotjar) on key pages
- A/B test the primary CTA placement and copy
```

---

## Rules

- **Audit the actual user experience**, not just code quality
- Focus on the **primary conversion funnel** first
- Reference specific UX laws by name — this creates shared vocabulary with designers
- Don't over-optimize for one law at the expense of another (they can conflict)
- Respect the project's brand and design system — don't suggest changes that break brand identity
- Fixes should be practical and implementable, not theoretical
- German UI text for German-language projects
- Never add dark patterns (fake urgency, manipulative scarcity, confirm-shaming)
- Follow the project's existing code style and component patterns
