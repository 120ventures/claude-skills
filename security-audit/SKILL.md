---
name: security-audit
description: Scan the current project for security issues — hardcoded secrets, missing RLS, direct DB access from frontend, unvalidated inputs, XSS risks, missing rate limiting, unsanitized user inputs
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
- Do admin/sensitive Edge Functions check user roles (not just auth presence)?
- Are there endpoints that only check authentication but skip authorization (e.g., any logged-in user can access admin actions)?

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
- Run `npm audit` or check for known vulnerabilities in dependencies

### 9. Rate Limiting
Check:
- Do Edge Functions implement rate limiting? (e.g., per-user or per-IP request throttling)
- Are public-facing endpoints (auth, contact forms, webhooks) protected against abuse?
- Is there a rate limiting middleware or helper used consistently across functions?
- Flag any endpoint without rate limiting as a warning

### 10. Input Sanitization
Check:
- Is all user input sanitized before processing? (strip HTML, escape special characters)
- Are database inputs parameterized or using ORM/query builders (not raw string concatenation)?
- Are file uploads validated for type, size, and content?
- Is user-provided content sanitized before rendering or storing?

### 11. Error Detail Leaking
Check Edge Functions for:
- Responses that expose `error.message`, `error.stack`, or raw exception details to the client
- API error responses should return generic messages — internal details only in server logs
- Search for patterns like `JSON.stringify({ error: error.message` or `stack` in response bodies

### 12. Sensitive Data in Logs
Search for:
- `console.log` / `console.info` / `console.debug` that output user data, tokens, passwords, or secrets
- Logging of full request bodies that may contain sensitive fields
- Any `console.*` in `src/` that references `token`, `password`, `secret`, `authorization`, or `user` objects

### 13. Role-Based Authorization
Check:
- Are there admin-only or role-restricted Edge Functions?
- Do they verify the user's role/permissions beyond just checking auth?
- Search for role checks like `user.role`, `user_metadata.role`, or custom claims
- Flag admin endpoints that only check `Authorization` header without role verification

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

## Notes
- Checks 11-13 were added to align with SECURITY_RULES.md in the boilerplate
- The audit should cover all 13 checks before producing the report
