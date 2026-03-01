# 120 Ventures — Claude Code Skills

Shared [Claude Code](https://claude.ai/code) skills for our ventures. Each skill automates a recurring setup task so you don't have to do it by hand.

## Available Skills

| Skill | What it does | Install |
|-------|-------------|---------|
| [setup-gtm](./setup-gtm) | GTM + GA4 + Meta Pixel + PostHog + Consent Mode v2 + custom events | [↓ Install](#setup-gtm) |
| [social-sharing](./social-sharing) | OG preview image (1200x630), favicon, meta tags, Twitter cards, JSON-LD | [↓ Install](#social-sharing) |
| [edge-function](./edge-function) | Supabase Edge Function with auth, CORS, Zod validation, error handling | [↓ Install](#edge-function) |
| [security-audit](./security-audit) | Scan for hardcoded secrets, missing RLS, XSS risks, unvalidated inputs | [↓ Install](#security-audit) |
| [pre-deploy](./pre-deploy) | Pre-deployment checklist — types, build, lint, env vars, security, git status | [↓ Install](#pre-deploy) |
| [e2e-tests](./e2e-tests) | Generate Playwright E2E tests for a page or feature | [↓ Install](#e2e-tests) |

## How to install

Each skill is a single file. Pick the ones you need:

### setup-gtm
```bash
mkdir -p ~/.claude/skills/setup-gtm && curl -sS -o ~/.claude/skills/setup-gtm/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/setup-gtm/SKILL.md
```
Then in Claude Code: `/setup-gtm GTM-XXXXXXX G-XXXXXXX 1234567890 phc_xxxxx`

### social-sharing
```bash
mkdir -p ~/.claude/skills/social-sharing && curl -sS -o ~/.claude/skills/social-sharing/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/social-sharing/SKILL.md
```
Then in Claude Code: `/social-sharing my-project`

### edge-function
```bash
mkdir -p ~/.claude/skills/edge-function && curl -sS -o ~/.claude/skills/edge-function/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/edge-function/SKILL.md
```
Then in Claude Code: `/edge-function save-booking`

### security-audit
```bash
mkdir -p ~/.claude/skills/security-audit && curl -sS -o ~/.claude/skills/security-audit/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/security-audit/SKILL.md
```
Then in Claude Code: `/security-audit`

### pre-deploy
```bash
mkdir -p ~/.claude/skills/pre-deploy && curl -sS -o ~/.claude/skills/pre-deploy/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/pre-deploy/SKILL.md
```
Then in Claude Code: `/pre-deploy`

### e2e-tests
```bash
mkdir -p ~/.claude/skills/e2e-tests && curl -sS -o ~/.claude/skills/e2e-tests/SKILL.md https://raw.githubusercontent.com/120ventures/claude-skills/main/e2e-tests/SKILL.md
```
Then in Claude Code: `/e2e-tests landing-page`

## Install all at once

If you want everything:

```bash
for skill in setup-gtm social-sharing edge-function security-audit pre-deploy e2e-tests; do
  mkdir -p ~/.claude/skills/$skill
  curl -sS -o ~/.claude/skills/$skill/SKILL.md \
    https://raw.githubusercontent.com/120ventures/claude-skills/main/$skill/SKILL.md
done
```

## What are Claude Code skills?

Skills are markdown instruction files that live in `~/.claude/skills/`. When you type `/skill-name` in Claude Code, it follows the instructions in that file. No packages, no config — just a `.md` file.

- **Global skills** (for you): `~/.claude/skills/{name}/SKILL.md`
- **Project skills** (shared via repo): `.claude/skills/{name}/SKILL.md`

[Learn more about Claude Code](https://docs.anthropic.com/en/docs/claude-code)
