# 120 Ventures — Claude Code Skills

Shared [Claude Code](https://claude.ai/code) skills for our ventures. Each skill automates a recurring task so you don't have to do it by hand.

---

## Available Skills

### Quality Audits

Run these regularly to catch issues before users (or Google) do. Each audit covers a distinct layer — no overlap between them.

| Skill | Layer | What it checks |
|-------|-------|---------------|
| [ux-audit](./ux-audit) | Behavior | Cognitive load, decision-making, Nielsen's heuristics, system feedback |
| [ui-audit](./ui-audit) | Visual | Visual hierarchy, spacing, typography, color, Gestalt grouping, consistency |
| [cro-audit](./cro-audit) | Conversion | Trust placement, funnel flow, persuasion structure, conversion psychology |
| [copy-audit](./copy-audit) | Words | Clarity, tone, PAS framework, microcopy, Austrian German localization |
| [mobile-audit](./mobile-audit) | Mobile | Core Web Vitals, responsive design, touch targets, performance, navigation |
| [a11y-audit](./a11y-audit) | Accessibility | WCAG 2.2 Level AA — contrast, keyboard nav, ARIA, semantics |
| [legal-audit](./legal-audit) | Legal | DSGVO, ECG, FAGG, ePrivacy, cookie consent, Impressum (Austria) |
| [security-audit](./security-audit) | Security | Hardcoded secrets, missing RLS, XSS risks, unvalidated inputs |

### Scaffolding & Setup

Generate boilerplate for common project needs.

| Skill | What it does |
|-------|-------------|
| [edge-function](./edge-function) | Supabase Edge Function with auth, CORS, Zod validation, error handling |
| [setup-gtm](./setup-gtm) | GTM container + GA4 + Meta Pixel + PostHog + Consent Mode v2 + custom events |
| [new-page](./new-page) | New page with route, lazy-loading, SEO meta, and mobile-first layout |
| [social-sharing](./social-sharing) | OG preview image (1200x630), favicon, meta tags, Twitter cards, JSON-LD |

### Workflow & CI

Pre-launch checks and test generation.

| Skill | What it does |
|-------|-------------|
| [pre-deploy](./pre-deploy) | Pre-deployment checklist — types, build, lint, env vars, security, git status |
| [e2e-tests](./e2e-tests) | Generate Playwright E2E tests for a page or feature |

### Brand & Strategy

Foundational work for new ventures.

| Skill | What it does |
|-------|-------------|
| [brand-identity](./brand-identity) | Interactive 6-phase brand workshop — inspo, personality, colors, assets, logo, website |

---

## Install

Each skill is a single `.md` file. Pick what you need, or install everything.

### Install one skill

```bash
# Replace SKILL_NAME with any skill from the tables above
mkdir -p ~/.claude/skills/SKILL_NAME && curl -sS -o ~/.claude/skills/SKILL_NAME/SKILL.md \
  https://raw.githubusercontent.com/120ventures/claude-skills/main/SKILL_NAME/SKILL.md
```

Then in Claude Code: `/SKILL_NAME`

<details>
<summary>Individual install commands (copy-paste ready)</summary>

```bash
# Quality Audits
mkdir -p ~/.claude/skills/ux-audit && curl -sS -o ~/.claude/skills/ux-audit/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/ux-audit/SKILL.md
mkdir -p ~/.claude/skills/ui-audit && curl -sS -o ~/.claude/skills/ui-audit/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/ui-audit/SKILL.md
mkdir -p ~/.claude/skills/cro-audit && curl -sS -o ~/.claude/skills/cro-audit/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/cro-audit/SKILL.md
mkdir -p ~/.claude/skills/copy-audit && curl -sS -o ~/.claude/skills/copy-audit/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/copy-audit/SKILL.md
mkdir -p ~/.claude/skills/mobile-audit && curl -sS -o ~/.claude/skills/mobile-audit/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/mobile-audit/SKILL.md
mkdir -p ~/.claude/skills/a11y-audit && curl -sS -o ~/.claude/skills/a11y-audit/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/a11y-audit/SKILL.md
mkdir -p ~/.claude/skills/legal-audit && curl -sS -o ~/.claude/skills/legal-audit/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/legal-audit/SKILL.md
mkdir -p ~/.claude/skills/security-audit && curl -sS -o ~/.claude/skills/security-audit/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/security-audit/SKILL.md

# Scaffolding & Setup
mkdir -p ~/.claude/skills/edge-function && curl -sS -o ~/.claude/skills/edge-function/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/edge-function/SKILL.md
mkdir -p ~/.claude/skills/setup-gtm && curl -sS -o ~/.claude/skills/setup-gtm/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/setup-gtm/SKILL.md
mkdir -p ~/.claude/skills/social-sharing && curl -sS -o ~/.claude/skills/social-sharing/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/social-sharing/SKILL.md

# Workflow & CI
mkdir -p ~/.claude/skills/pre-deploy && curl -sS -o ~/.claude/skills/pre-deploy/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/pre-deploy/SKILL.md
mkdir -p ~/.claude/skills/e2e-tests && curl -sS -o ~/.claude/skills/e2e-tests/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/e2e-tests/SKILL.md

# Brand & Strategy
mkdir -p ~/.claude/skills/brand-identity && curl -sS -o ~/.claude/skills/brand-identity/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/brand-identity/SKILL.md
```

</details>

### Install all at once

```bash
for skill in ux-audit ui-audit cro-audit copy-audit mobile-audit a11y-audit legal-audit security-audit edge-function setup-gtm social-sharing pre-deploy e2e-tests brand-identity; do
  mkdir -p ~/.claude/skills/$skill
  curl -sS -o ~/.claude/skills/$skill/SKILL.md \
    https://raw.githubusercontent.com/120ventures/claude-skills/main/$skill/SKILL.md
done
```

### Install by category

```bash
# All 8 audits
for skill in ux-audit ui-audit cro-audit copy-audit mobile-audit a11y-audit legal-audit security-audit; do
  mkdir -p ~/.claude/skills/$skill
  curl -sS -o ~/.claude/skills/$skill/SKILL.md \
    https://raw.githubusercontent.com/120ventures/claude-skills/main/$skill/SKILL.md
done
```

---

## What are Claude Code skills?

Skills are markdown instruction files that live in `~/.claude/skills/`. When you type `/skill-name` in Claude Code, it follows the instructions in that file. No packages, no config — just a `.md` file.

- **Global skills** (for you): `~/.claude/skills/{name}/SKILL.md`
- **Project skills** (shared via repo): `.claude/skills/{name}/SKILL.md`

[Learn more about Claude Code](https://docs.anthropic.com/en/docs/claude-code)
