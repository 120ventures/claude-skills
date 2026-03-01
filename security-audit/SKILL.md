---
name: security-audit
description: Scan the current project for security issues — hardcoded secrets, missing RLS, direct DB access from frontend, unvalidated inputs, XSS risks
context: fork
agent: Explore
allowed-tools: Read, Glob, Grep
---

# Security Audit

Run a full security audit on the current project based on the 120 Ventures Security Rules.

## Checks to perform

### 1. Hardcoded Secrets
Search the entire codebase for:
- API keys, tokens, passwords in source files (grep for `api_key`, `secret`, `password`, `token`, `private_key`, `service_role`, `sk_live`, `sk_test`)
- `.env` files that are NOT in `.gitignore`
- `SUPABASE_SERVICE_ROLE_KEY` used anywhere in `src/` (frontend)
- Any string that looks like a key pattern: `ghp_`, `sbp_`, `sk_`, `pk_`, `eyJ` (JWT)

### 2. Direct DB Access from Frontend
Search `src/` for:
- `.insert(`, `.update(`, `.delete(`, `.upsert(` calls on supabase client — these should go through Edge Functions
- `.rpc(` calls that mutate data
- Only `.select()` with RLS is acceptable from frontend

### 3. Missing Input Validation
Check:
- Edge Functions in `supabase/functions/` — do they ALL validate input with Zod?
- Forms in `src/` — do they use Zod schemas for validation?
- Any `req.body` or `req.json()` used without validation?

### 4. XSS Risks
Search for:
- `dangerouslySetInnerHTML` usage — flag every instance
- `eval()`, `new Function()`, `document.write()`
- Unescaped user input in templates

### 5. RLS & Auth
Check:
- Do all Edge Functions check `Authorization` header?
- Are there any Edge Functions without auth checks?
- Check `supabase/` for migration files — are RLS policies enabled on all tables?

### 6. CORS
Check Edge Functions for:
- `Access-Control-Allow-Origin: *` — this is NOT allowed
- CORS headers present in all functions?

### 7. Environment Variables
Check:
- Are there `VITE_` prefixed variables that expose sensitive data?
- Is `.env` in `.gitignore`?
- Is `.env.example` present (good practice)?

### 8. Dependencies
Check:
- Is `package-lock.json` committed? (should be)
- Any `postinstall` or `preinstall` scripts in `package.json`?

## Output Format

Report findings as:

```
## Security Audit Report

### Critical (fix immediately)
- [finding with file:line reference]

### Warning (should fix)
- [finding with file:line reference]

### Info (consider)
- [finding with file:line reference]

### Passed
- [checks that passed]
```

Be specific — always include file paths and line numbers. Don't flag false positives. Supabase `anon` key in frontend is OK. `.select()` from frontend with RLS is OK.
