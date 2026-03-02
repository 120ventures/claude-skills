# 120 Ventures — Claude Code Skills

A shared collection of [Claude Code](https://claude.ai/code) skills we use across all 120 Ventures projects. Instead of repeating the same setup steps, audit checklists etc. in every project, we captured them as reusable skills that any team member can run with a single slash command.

## Who is this for?

Anyone on the team using Claude Code. If you're building a new venture, launching a landing page, or preparing for deployment — there's probably a skill here that saves you a few hours.

## How it works

Each skill is a single markdown file. You install it once (copy it to `~/.claude/skills/`), and from then on you can run it in any project by typing `/skill-name` in Claude Code. The skill reads your project, follows the instructions in the markdown file, and either audits your code, generates boilerplate, or runs a checklist — then reports findings and offers to fix issues directly.

No packages. No config. No dependencies. Just a `.md` file with structured instructions.

---

## Skills Overview

We have **15 skills** in 4 categories. Each one handles a specific, well-scoped task.

### Quality Audits (9 skills)

The audit suite covers every layer of a web project — from the words on the page to the legal fine print. Each audit checks a distinct layer with no overlap between them, so you can run one, a few, or all nine without getting duplicate findings.

A good pre-launch workflow: run all 9 audits, fix critical issues, ship.

| Skill | Layer | What it checks | When to run |
|-------|-------|---------------|-------------|
| [ux-audit](./ux-audit) | Behavior | Cognitive load, decision-making, Nielsen's heuristics, system feedback | After building a new flow or page |
| [ui-audit](./ui-audit) | Visual | Visual hierarchy, spacing, typography, color, Gestalt grouping, consistency | After visual changes or new components |
| [cro-audit](./cro-audit) | Conversion | Trust placement, funnel flow, persuasion structure, conversion psychology | Before launch or when conversion is low |
| [at-copy-audit](./at-copy-audit) | Words | Clarity, tone, PAS framework, microcopy, Austrian German localization | After writing or updating copy |
| [mobile-audit](./mobile-audit) | Mobile | Core Web Vitals, responsive design, touch targets, performance, navigation | Before launch (Google ranks by CWV) |
| [accessibility-audit](./accessibility-audit) | Accessibility | WCAG 2.2 Level AA — contrast, keyboard nav, ARIA, semantics | Before launch and after UI changes |
| [legal-audit](./legal-audit) | Legal | DSGVO, ECG, FAGG, ePrivacy, cookie consent, Impressum (Austria) | Before launch and quarterly |
| [health-claims-audit](./health-claims-audit) | Health Law | MPG 2021, EU-MDR, Health Claims VO, forbidden claims, wellness vs SaMD | Before publishing health-related copy |
| [security-audit](./security-audit) | Security | Hardcoded secrets, missing RLS, XSS risks, unvalidated inputs, rate limiting | Before every deployment |

**How the audits fit together:**

```
/ux-audit     → Does the flow work? (behavior, cognition)
/ui-audit     → Does it look right? (pixels, spacing, visual consistency)
/cro-audit    → Does it convert? (persuasion, trust, funnel structure)
/at-copy-audit   → Are the words right? (clarity, tone, Austrian German)
/mobile-audit → Does it work on phones? (CWV, touch, responsive)
/accessibility-audit   → Can everyone use it? (WCAG, keyboard, screen readers)
/legal-audit  → Is it legally compliant? (DSGVO, Impressum, cookies)
/health-claims-audit → Are health claims legal? (MPG, EU-MDR, Health Claims VO)
/security-audit → Is it secure? (secrets, XSS, RLS, inputs)
```

### Scaffolding & Setup (3 skills)

Skip the boilerplate. These skills generate production-ready code for common project needs, following our conventions and stack (React + Vite + TypeScript + Tailwind + Supabase).

| Skill | What it generates | Example |
|-------|------------------|---------|
| [edge-function](./edge-function) | Supabase Edge Function with auth, CORS, Zod validation, error handling | `/edge-function newsletter-signup` |
| [setup-gtm](./setup-gtm) | GTM container + GA4 + Meta Pixel + PostHog + Consent Mode v2 | `/setup-gtm` |
| [social-sharing](./social-sharing) | OG image (1200x630), favicon, meta tags, Twitter cards, JSON-LD | `/social-sharing my-project` |

### Workflow & CI (2 skills)

Pre-launch checks and test generation. Run `/pre-deploy` before every push. Run `/e2e-tests` after building a new feature.

| Skill | What it does | Example |
|-------|-------------|---------|
| [pre-deploy](./pre-deploy) | Pre-deployment checklist — types, build, lint, env vars, security, git status | `/pre-deploy` |
| [e2e-tests](./e2e-tests) | Generate Playwright E2E tests for a page or feature | `/e2e-tests landing-page` |

### Brand & Strategy (1 skill)

For the very beginning of a new venture — before any code is written.

| Skill | What it does | Example |
|-------|-------------|---------|
| [brand-identity](./brand-identity) | Interactive 6-phase brand workshop — inspo, personality, colors, assets, logo, website | `/brand-identity my-project` |

---

## Install

Each skill is a single `.md` file that gets copied to your local `~/.claude/skills/` directory. One command per skill, or install everything at once.

### Install one skill

```bash
# Replace SKILL_NAME with any skill from the tables above
mkdir -p ~/.claude/skills/SKILL_NAME && curl -sS -o ~/.claude/skills/SKILL_NAME/SKILL.md \
  https://raw.githubusercontent.com/120ventures/claude-skills/main/SKILL_NAME/SKILL.md
```

Then open Claude Code and type `/SKILL_NAME` to run it.

### Install all 15 skills

```bash
for skill in ux-audit ui-audit cro-audit at-copy-audit mobile-audit accessibility-audit legal-audit health-claims-audit security-audit edge-function setup-gtm social-sharing pre-deploy e2e-tests brand-identity; do
  mkdir -p ~/.claude/skills/$skill
  curl -sS -o ~/.claude/skills/$skill/SKILL.md \
    https://raw.githubusercontent.com/120ventures/claude-skills/main/$skill/SKILL.md
done
```

### Install just the audits

If you only want the 9 audit skills:

```bash
for skill in ux-audit ui-audit cro-audit at-copy-audit mobile-audit accessibility-audit legal-audit health-claims-audit security-audit; do
  mkdir -p ~/.claude/skills/$skill
  curl -sS -o ~/.claude/skills/$skill/SKILL.md \
    https://raw.githubusercontent.com/120ventures/claude-skills/main/$skill/SKILL.md
done
```

<details>
<summary>Individual install commands (copy-paste ready)</summary>

```bash
# Quality Audits
mkdir -p ~/.claude/skills/ux-audit && curl -sS -o ~/.claude/skills/ux-audit/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/ux-audit/SKILL.md
mkdir -p ~/.claude/skills/ui-audit && curl -sS -o ~/.claude/skills/ui-audit/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/ui-audit/SKILL.md
mkdir -p ~/.claude/skills/cro-audit && curl -sS -o ~/.claude/skills/cro-audit/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/cro-audit/SKILL.md
mkdir -p ~/.claude/skills/at-copy-audit && curl -sS -o ~/.claude/skills/at-copy-audit/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/at-copy-audit/SKILL.md
mkdir -p ~/.claude/skills/mobile-audit && curl -sS -o ~/.claude/skills/mobile-audit/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/mobile-audit/SKILL.md
mkdir -p ~/.claude/skills/accessibility-audit && curl -sS -o ~/.claude/skills/accessibility-audit/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/accessibility-audit/SKILL.md
mkdir -p ~/.claude/skills/legal-audit && curl -sS -o ~/.claude/skills/legal-audit/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/legal-audit/SKILL.md
mkdir -p ~/.claude/skills/health-claims-audit && curl -sS -o ~/.claude/skills/health-claims-audit/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/health-claims-audit/SKILL.md
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

### Updating skills

To update a skill to the latest version, just re-run the install command — it overwrites the old file.

---

## What are Claude Code skills?

[Claude Code](https://claude.ai/code) is Anthropic's CLI for coding with Claude. Skills are markdown instruction files that extend it with custom commands. When you type `/skill-name` in Claude Code, it reads the skill file and follows the instructions — reading your project, running checks, generating code, or fixing issues.

Think of it as a reusable prompt with structure: each skill has steps, checklists, and rules that Claude follows consistently every time you run it.

**Where skills live:**
- **Global skills** (available in every project): `~/.claude/skills/{name}/SKILL.md`
- **Project skills** (shared via repo, team-wide): `.claude/skills/{name}/SKILL.md`

The skills in this repo are designed as global skills. Install them once, use them everywhere.

[Claude Code docs](https://docs.anthropic.com/en/docs/claude-code) · [Skills documentation](https://docs.anthropic.com/en/docs/claude-code/skills)
