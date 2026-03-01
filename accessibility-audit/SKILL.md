---
name: accessibility-audit
description: Audit and fix accessibility issues following WCAG 2.2 Level AA + a11y project best practices
---

# Accessibility Audit (WCAG 2.2 + a11y)

This skill audits a project for accessibility issues and fixes them. Based on:
- **WCAG 2.2** (Level A + AA): https://www.w3.org/TR/WCAG22/
- **The A11Y Project checklist**: https://www.a11yproject.com/checklist/

No arguments needed. Just run `/accessibility-audit` and the skill scans the project automatically.

---

## Step 0: Scan the project

Read the project's `index.html`, all page components, layout components, and form components. Build a mental map of:
- Which pages exist
- Which components handle user interaction (forms, buttons, links, modals, accordions)
- Which components have animations or media (video, audio)
- What CSS framework is used (Tailwind, vanilla, etc.)
- Whether `prefers-reduced-motion` is already handled

---

## Step 1: Audit — check every category

Go through **each category** below. For every issue found, note the file, line, and which WCAG criterion it violates. Group findings by severity (Critical → Major → Minor).

### 1. Global Code
| Check | WCAG | How to verify |
|-------|------|---------------|
| `<html lang="...">` is set and correct | 3.1.1 (A) | Read `index.html` |
| Each page has a unique `<title>` | 2.4.2 (A) | Check all pages |
| Viewport zoom is NOT disabled (`maximum-scale=1` or `user-scalable=no` must be absent) | 1.4.4 (AA) | Check `<meta name="viewport">` |
| Landmark elements used (`<main>`, `<nav>`, `<header>`, `<footer>`, `<section>`) | 4.1.2 (A) | Check page structure |
| Linear content flow / logical DOM order | 2.4.3 (A) | Check for CSS-only reordering |
| No `autofocus` attribute on inputs | 2.4.3 (A) | Grep for `autofocus` |
| No `title` attribute tooltips on interactive elements | 4.1.2 (A) | Grep for `title=` |

### 2. Headings
| Check | WCAG | How to verify |
|-------|------|---------------|
| Only one `<h1>` per page | 2.4.6 (AA) | Check all pages |
| Heading levels don't skip (h1 → h3 without h2) | 2.4.6 (AA) | Check heading hierarchy |
| Headings introduce content sections | 2.4.6 (AA) | Check section structure |

### 3. Images & Icons
| Check | WCAG | How to verify |
|-------|------|---------------|
| All `<img>` have `alt` attribute | 1.1.1 (A) | Grep for `<img` without `alt` |
| Decorative images have `alt=""` | 1.1.1 (A) | Check decorative images |
| SVG icons have `aria-hidden="true"` or accessible label | 1.1.1 (A) | Check SVG usage |
| Complex images (charts, graphs) have text alternatives | 1.1.1 (A) | Check if applicable |

### 4. Color Contrast
| Check | WCAG | How to verify |
|-------|------|---------------|
| Normal text: 4.5:1 contrast ratio minimum | 1.4.3 (AA) | Check all text colors against backgrounds |
| Large text (18px+ or 14px+ bold): 3:1 minimum | 1.4.3 (AA) | Check large text |
| UI components & icons: 3:1 minimum | 1.4.11 (AA) | Check borders, icons, focus rings |
| No opacity modifiers that reduce contrast below threshold | 1.4.3 (AA) | Grep for opacity on text |
| Color is not the only way to convey info | 1.4.1 (A) | Check error states, status indicators |

### 5. Keyboard & Focus
| Check | WCAG | How to verify |
|-------|------|---------------|
| All interactive elements are keyboard accessible | 2.1.1 (A) | Check for `onClick` without keyboard handler |
| Visible focus styles on all interactive elements | 2.4.7 (AA) | Check `:focus` / `focus-visible` styles |
| Focus order matches visual layout | 1.3.2 (A) | Check `tabIndex` usage |
| No keyboard traps | 2.1.2 (A) | Check modals, dropdowns |
| Focus not obscured by sticky headers/bars | 2.4.11 (AA) | Check sticky/fixed elements |
| Skip link present and visible on focus | 2.4.1 (A) | Check for skip navigation |

### 6. Forms
| Check | WCAG | How to verify |
|-------|------|---------------|
| All inputs have associated `<label>` (or `aria-label` / `aria-labelledby`) | 3.2.2 (A) | Check all form inputs |
| Required fields marked with `aria-required="true"` | 3.3.2 (A) | Check required inputs |
| Error messages associated with inputs (`aria-describedby` or `aria-invalid`) | 3.3.1 (A) | Check error handling |
| Errors not communicated by color alone | 1.4.1 (A) | Check error states |
| `autocomplete` attributes on common fields (name, email, etc.) | 1.3.5 (AA) | Check form inputs |
| `fieldset` + `legend` for grouped inputs (radio groups, checkboxes) | 1.3.1 (A) | Check grouped inputs |

### 7. Links & Buttons
| Check | WCAG | How to verify |
|-------|------|---------------|
| Links use `<a>`, buttons use `<button>` (not `<div onClick>`) | 1.3.1 (A) | Check interactive elements |
| Link/button text is descriptive (no "click here", "read more" without context) | 2.4.4 (A) | Check link text |
| Links opening in new tab have indication (`aria-label` or visual + sr text) | G201 | Grep for `target="_blank"` |
| Links are visually distinguishable (not just by color) | 1.4.1 (A) | Check link styling |

### 8. Media & Animation
| Check | WCAG | How to verify |
|-------|------|---------------|
| No autoplay audio/video with sound | 1.4.2 (A) | Check media elements |
| Video has captions/subtitles | 1.2.2 (A) | Check video elements |
| All media can be paused | 2.2.2 (AA) | Check media controls |
| `prefers-reduced-motion` disables animations | 2.3.3 (AAA) | Check CSS + JS animations |
| No content flashes more than 3 times per second | 2.3.1 (A) | Check animations |

### 9. Mobile & Touch
| Check | WCAG | How to verify |
|-------|------|---------------|
| Touch targets minimum 24×24px (44×44px recommended) | 2.5.8 (AA) | Check buttons, links on mobile |
| No horizontal scrolling at 320px viewport | 1.4.10 (AA) | Check responsive layout |
| Content works in both orientations | 1.3.4 (AA) | Check orientation lock |
| Dragging actions have alternatives | 2.5.7 (AA) | Check drag interactions |

### 10. ARIA & Semantics
| Check | WCAG | How to verify |
|-------|------|---------------|
| ARIA roles used correctly (not on wrong elements) | 4.1.2 (A) | Check ARIA usage |
| `aria-hidden="true"` on decorative elements | 4.1.2 (A) | Check decorative content |
| Live regions (`aria-live`) for dynamic updates | 4.1.3 (AA) | Check toast/notification components |
| Modals/dialogs have `role="dialog"` + `aria-modal` + focus trap | 4.1.2 (A) | Check modal components |
| Accordion/disclosure patterns use proper ARIA | 4.1.2 (A) | Check accordion components |

### 11. WCAG 2.2 New Criteria
| Check | WCAG | How to verify |
|-------|------|---------------|
| Help mechanisms are consistent across pages (chat, FAQ link, etc.) | 3.2.6 (A) | Check help patterns |
| No redundant entry — don't ask users to re-enter info already provided | 3.3.7 (A) | Check multi-step forms |
| No cognitive function tests for auth (CAPTCHA alternatives) | 3.3.8 (AA) | Check auth flows |

---

## Step 2: Report findings

Present findings as a table grouped by severity:

```
## Accessibility Audit Results

### 🔴 Critical (breaks access for some users)
| Issue | File | WCAG | Fix |
|-------|------|------|-----|
| ... | ... | ... | ... |

### 🟠 Major (significant barrier)
| Issue | File | WCAG | Fix |
|-------|------|------|-----|
| ... | ... | ... | ... |

### 🟡 Minor (improvement opportunity)
| Issue | File | WCAG | Fix |
|-------|------|------|-----|
| ... | ... | ... | ... |

### ✅ Passing
- [list what's already good]
```

Ask the user: **"Soll ich alle Issues automatisch fixen?"** (or selectively).

---

## Step 3: Fix issues

Apply fixes directly in the codebase. For each fix:
- Edit the file
- Add a brief comment only if the fix isn't self-explanatory
- Never break existing functionality

### Common fixes:

**Missing alt text:**
```tsx
// Decorative → alt=""
<img src="..." alt="" />

// Meaningful → descriptive alt
<img src="..." alt="Beschreibung des Bildinhalts" />
```

**Missing labels:**
```tsx
<label htmlFor="email">E-Mail</label>
<input id="email" type="email" aria-required="true" />

// Or for icon-only buttons:
<button aria-label="Menü öffnen">
  <MenuIcon aria-hidden="true" />
</button>
```

**Focus styles:**
```css
:focus-visible {
  outline: 2px solid var(--c-accent);
  outline-offset: 2px;
}
```

**Skip link:**
```tsx
<a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-white focus:text-black">
  Zum Inhalt springen
</a>
```

**prefers-reduced-motion:**
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**External links:**
```tsx
<a href="..." target="_blank" rel="noopener noreferrer">
  Link Text <span className="sr-only">(öffnet in neuem Tab)</span>
</a>
```

**aria-live for dynamic content:**
```tsx
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>
```

---

## Step 4: Summary

After fixing, present:

```
Accessibility Audit Complete!

✅ [N] issues fixed
⚠️ [N] issues need manual testing (keyboard nav, screen reader)
📊 WCAG 2.2 Level AA compliance: [estimated %]

Fixed:
- [list of fixes applied]

Manual testing recommended:
- Tab through all pages — verify focus order and visibility
- Test with screen reader (VoiceOver: Cmd+F5 on Mac)
- Test at 200% zoom — verify no content is cut off
- Test at 320px width — verify no horizontal scroll
- Test with prefers-reduced-motion enabled

Tools for further testing:
- axe DevTools: browser extension for automated checks
- WAVE: https://wave.webaim.org/
- Lighthouse Accessibility audit in Chrome DevTools
```

---

## Rules

- Target **WCAG 2.2 Level AA** (not AAA, unless already implemented)
- `prefers-reduced-motion` handling is mandatory, not optional
- Never remove existing accessibility features
- German `sr-only` text for German-language sites (e.g. "Zum Inhalt springen", not "Skip to content")
- Follow the project's existing code style and framework conventions
- Do NOT install any npm packages — use native HTML/ARIA
- Automated tools catch ~30% of issues — this audit is the manual review layer
- Always recommend manual testing with keyboard + screen reader after fixes
