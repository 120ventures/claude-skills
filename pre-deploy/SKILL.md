---
name: pre-deploy
description: Run a pre-deployment checklist — type safety, build test, security scan, env vars, RLS check
context: fork
agent: Explore
allowed-tools: Read, Glob, Grep, Bash(npm run build), Bash(npm run lint), Bash(npx tsc --noEmit)
---

# Pre-Deploy Checklist

Run a full pre-deployment validation on the current project.

## Checks to perform

### 1. TypeScript
- Run `npx tsc --noEmit` — report any type errors
- Check for `any` types in `src/` that should be properly typed

### 2. Build
- Run `npm run build` — does it succeed without errors?
- Check for build warnings

### 3. Linting
- Run `npm run lint` — any ESLint errors?

### 4. Environment Variables
- Read `.env.example` — list all required variables
- Check that no `VITE_` variable exposes sensitive data
- Verify `.env` is in `.gitignore`
- Check for hardcoded URLs that should be env vars (localhost, staging URLs in production code)

### 5. Security Quick-Scan
- Search for `console.log` with sensitive data patterns (user, token, password, email)
- Check for `dangerouslySetInnerHTML`
- Check for hardcoded secrets (API keys, tokens)
- Verify no `service_role` key in frontend code

### 6. Supabase / RLS
- Check if any Edge Functions are missing auth checks
- Look for direct `.insert()`, `.update()`, `.delete()` calls from `src/` (should go through Edge Functions)

### 7. Dependencies
- Check `package-lock.json` exists and is committed
- Look for any `postinstall` scripts that seem suspicious

### 8. Git Status
- Any uncommitted changes?
- Any untracked files that should be committed?
- Is the branch up to date with remote?

## Output Format

```
## Pre-Deploy Report

### PASS
- [checks that passed]

### FAIL (must fix before deploy)
- [critical issues with file:line]

### WARN (should fix)
- [non-critical issues]

### Summary
Ready to deploy: YES / NO
```

Be specific with file paths and line numbers. Don't flag false positives.
