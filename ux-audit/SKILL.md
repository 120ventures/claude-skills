---
name: ux-audit
description: Audit UX against established UX laws, cognitive principles, and Nielsen's heuristics — with actionable fixes
---

# UX Audit — Laws of UX + Nielsen's Heuristics

This skill audits a project's user experience against established UX laws, cognitive principles, and design heuristics. It focuses on **behavioral outcomes** — does the flow work? is the user confused? does the system communicate well?

No arguments needed. Just run `/ux-audit` and the skill scans the project automatically.

**Difference from other audits:**
- `/ux-audit` checks **behavioral outcomes** — decision-making, cognition, system feedback, error handling
- `/ui-audit` checks **visual implementation** — spacing, typography, color, Gestalt grouping, visual consistency
- `/cro-audit` checks **conversion effectiveness** — messaging, trust placement, funnel narrative, copy

Reference sources:
- Jon Yablonski's Laws of UX: https://lawsofux.com/
- Nielsen Norman Group Heuristics: https://www.nngroup.com/articles/ten-usability-heuristics/

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

#### Nielsen's 10 Usability Heuristics

Audit against each heuristic individually:

---

#### H1: Visibility of System Status
> Always show progress, loading states, or feedback so users know what's happening.

**Check for:**
- No loading states for async operations (API calls, form submissions)
- Missing progress indicators in multi-step flows
- Current page not indicated in navigation
- Form validation feedback missing or delayed
- No confirmation after successful actions ("Saving...", "Gespeichert!")

**Fix pattern:** Add loading spinners, progress bars, active nav states, inline validation, and success/error toasts. Every user action should produce visible feedback within 400ms.

---

#### H2: Match Between System and Real World
> Use familiar language, metaphors, and layouts users expect from the real world.

**Check for:**
- Technical jargon instead of natural language
- Icons that don't match common meaning
- Logical ordering that doesn't match real-world sequences
- Unfamiliar metaphors or terminology
- Categories/labels that don't match user mental models

**Fix pattern:** Use language your users use. Follow real-world conventions for ordering (chronological, alphabetical, by importance). Test terminology with real users.

---

#### H3: User Control and Freedom
> Users make mistakes — give them undo, back buttons, and escape hatches.

**Check for:**
- No way to undo recent actions
- Missing back/cancel buttons in multi-step flows
- Modals that can't be dismissed (no X, no Escape, no backdrop click)
- Destructive actions without confirmation
- No way to exit or restart a flow mid-way

**Fix pattern:** Add undo for destructive actions, back buttons in flows, dismiss options on all overlays, and clear exit points. Users should never feel trapped.

---

#### H4: Consistency and Standards
> Same actions and behaviors everywhere in the app; align with platform norms.

**Check for:**
- Same action producing different results in different places
- Inconsistent button/link styling for same-level actions
- Non-standard platform conventions (navigation, form patterns, gestures)
- Terminology changing across pages for the same concept
- Inconsistent interaction patterns (some things click, some hover, some long-press)

**Fix pattern:** Create and enforce a component library. Same action = same visual treatment = same behavior. Follow platform conventions unless you have a strong, tested reason not to.

---

#### H5: Error Prevention
> Design to prevent mistakes before they happen, not just catch them after.

**Check for:**
- Forms that allow invalid submissions (no client-side validation)
- Missing confirmation dialogs for destructive or irreversible actions
- No smart defaults where the system could pre-fill values
- Free-text inputs where constrained inputs (dropdowns, date pickers) would prevent errors
- No input masks or formatting hints for structured data

**Fix pattern:** Use smart defaults, input constraints, confirmation dialogs, and inline validation. Disable submit buttons until required fields are valid. Prevent rather than fix.

---

#### H6: Recognition Over Recall
> Show options visibly instead of making users remember commands or previous choices.

**Check for:**
- Hidden navigation or menus requiring users to remember where things are
- Icons without labels (users must recall what each icon means)
- Forms that don't show previously selected values
- Search without recent/suggested items
- Instructions that require remembering information from a previous screen

**Fix pattern:** Label icons, show recent items, persist form state, use visible navigation. If users need to act on information, keep it visible — don't make them memorize it.

---

#### H7: Flexibility and Efficiency of Use
> Shortcuts for experts, progressive disclosure for novices.

**Check for:**
- No keyboard shortcuts for frequent actions
- Advanced features cluttering the interface for new users
- No progressive disclosure (everything shown at once)
- Missing power-user paths (bulk actions, keyboard navigation)
- One-size-fits-all flows that can't be customized or skipped

**Fix pattern:** Layer complexity — simple by default, powerful on demand. Add keyboard shortcuts, bulk actions, and "advanced" sections. Let experts skip steps they don't need.

---

#### H8: Aesthetic and Minimalist Design
> Cut clutter and focus on essentials. Every element should serve a purpose.

**Check for:**
- Irrelevant information competing with primary content
- Visual clutter that doesn't serve the user's goal
- Low content-to-chrome ratio (too much UI, too little content)
- Decorative elements that distract from key actions
- Dense pages that could benefit from progressive disclosure

**Fix pattern:** Remove what doesn't serve the current task. Prioritize content over chrome. Use whitespace deliberately. If an element doesn't help the user complete their goal, question whether it belongs.

---

#### H9: Help Users Recognize, Diagnose, and Recover from Errors
> Plain-language error messages with actionable fixes, not cryptic codes.

**Check for:**
- Technical error messages (HTTP codes, stack traces, "Error 500")
- Error messages that say what went wrong but not how to fix it
- Missing error states (silent failures)
- Error messages in a different language than the UI
- No suggested next steps after an error

**Fix pattern:** Write error messages in plain language: (1) what happened, (2) why, (3) how to fix it. Example: "E-Mail konnte nicht gesendet werden. Bitte überprüfe deine Internetverbindung und versuche es erneut."

---

#### H10: Help and Documentation
> Available when needed, discoverable but not intrusive.

**Check for:**
- No FAQ or help section for complex features
- Missing tooltips on non-obvious UI elements
- No onboarding guidance for first-time users
- Help documentation that's hard to find or out of date
- No contextual help near complex form fields

**Fix pattern:** Add contextual tooltips, an accessible FAQ, and onboarding hints for first-time users. Help should appear where users need it, not require them to go looking for it.

---

### Category 4: Emotion & Trust

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
