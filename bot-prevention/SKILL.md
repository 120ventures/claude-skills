---
name: bot-prevention
description: Add Cloudflare Turnstile bot protection + DB-based rate limiting — no npm packages needed, native Supabase Auth captchaToken support
argument-hint: [component-name or "all"]
---

# Bot Prevention with Cloudflare Turnstile + Rate Limiting

Add invisible Cloudflare Turnstile bot protection to form(s) specified by `$ARGUMENTS`. Covers frontend widget integration, Supabase native captchaToken support for auth forms, custom verification for non-auth forms, and DB-based rate limiting.

## Two Approaches

| Use Case | Approach |
|---|---|
| **Auth forms** (login, signup, password reset) | Supabase native `captchaToken` — no server code needed |
| **Non-auth forms** (waitlist, contact, etc.) | Custom verification in Edge Function |
| **API rate limiting** | DB-based usage tracking (complements CAPTCHA) |

## Prerequisites

- **No npm package needed** — Turnstile loads via script tag
- Cloudflare Turnstile widget created at https://dash.cloudflare.com → Turnstile section (NOT domain registration)
- Site Key in env as `VITE_TURNSTILE_SITE_KEY`
- Secret Key destination depends on approach (see below)

## Checklist before starting

1. **Read the target form component(s)** to understand submit flow
2. **Determine approach**: Auth form → Supabase native | Non-auth → Edge Function
3. **Check `.env`** for `VITE_TURNSTILE_SITE_KEY`

---

## Step 1: Cloudflare Turnstile Dashboard Setup

### Where to find it
Cloudflare Dashboard → **Turnstile** (left sidebar) — NOT under domain registration. You don't need a Cloudflare-managed domain.

### Domain configuration
Add ALL domains where forms will be used:
- `localhost` (for local dev)
- `www.yourdomain.com`
- `yourdomain.com` (if used without www)
- Any preview/staging domains (e.g. `*.vercel.app`)

### Widget settings
- Mode: **Managed** (invisible for most users, challenges only suspicious traffic)
- **Pre-clearance: No** — Choose "No" for sites NOT proxied through Cloudflare (e.g. Vercel, Netlify)

### Keys
- **Site Key** → Frontend env variable (`VITE_TURNSTILE_SITE_KEY` on Vercel/hosting platform)
- **Secret Key** → Depends on approach:
  - Auth forms: Supabase Dashboard → Authentication → Attack Protection → Enable CAPTCHA → paste secret
  - Non-auth forms: Supabase Edge Function secret

## Step 2: Environment Variables

### Frontend (Vercel dashboard or `.env`)
```env
# Use test keys for local dev:
# VITE_TURNSTILE_SITE_KEY="1x00000000000000000000AA"
VITE_TURNSTILE_SITE_KEY="your-real-site-key"
```

Set `VITE_TURNSTILE_SITE_KEY` in the hosting platform's environment variables. Vite injects it at build time.

### For Auth forms (Supabase native)
1. Supabase Dashboard → **Authentication** → **Attack Protection**
2. Enable **CAPTCHA protection**
3. Choose **Turnstile by Cloudflare**
4. Paste your **Secret Key**
5. Save

**No Edge Function secrets needed for auth forms.**

### For Non-auth forms (Edge Function verification)
```bash
npx supabase secrets set TURNSTILE_SECRET_KEY="your-secret-key"
```
After setting secrets, redeploy: `npx supabase functions deploy <function-name>`

## Step 3: HTML Script Tag

Add to `index.html` — **no npm package needed**:

```html
<!-- Cloudflare Turnstile (bot protection) -->
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit" async defer></script>
```

The `render=explicit` parameter prevents auto-rendering — we control when/where the widget renders.

## Step 4: Frontend Integration (No NPM Package)

### TypeScript declaration (add once per project, in any form component or a global .d.ts)

```typescript
declare global {
  interface Window {
    turnstile?: {
      render: (container: HTMLElement, options: Record<string, unknown>) => string;
      reset: (widgetId: string) => void;
      remove: (widgetId: string) => void;
    };
  }
}
```

### Pattern for each form component

```tsx
import { useState, useEffect, useRef, useCallback } from "react";

const TURNSTILE_SITE_KEY = import.meta.env.VITE_TURNSTILE_SITE_KEY as string | undefined;

// Inside component:
const [captchaToken, setCaptchaToken] = useState<string | null>(null);
const turnstileRef = useRef<HTMLDivElement>(null);
const widgetIdRef = useRef<string | null>(null);

const onCaptchaVerify = useCallback((token: string) => {
  setCaptchaToken(token);
}, []);

useEffect(() => {
  if (!TURNSTILE_SITE_KEY || !turnstileRef.current) return;

  // Poll for script load (async script may not be ready yet)
  const interval = setInterval(() => {
    if (window.turnstile && turnstileRef.current && !widgetIdRef.current) {
      clearInterval(interval);
      widgetIdRef.current = window.turnstile.render(turnstileRef.current, {
        sitekey: TURNSTILE_SITE_KEY,
        callback: onCaptchaVerify,
        "expired-callback": () => setCaptchaToken(null),
        theme: "light",
        size: "invisible",
      });
    }
  }, 100);

  return () => {
    clearInterval(interval);
    if (widgetIdRef.current && window.turnstile) {
      window.turnstile.remove(widgetIdRef.current);
      widgetIdRef.current = null;
    }
  };
}, [onCaptchaVerify]);
```

### Widget placement in JSX
Place an empty div inside the form (between fields and submit button):
```tsx
{/* Cloudflare Turnstile (invisible) */}
<div ref={turnstileRef} />
```

### Reset on error
After a failed submit, reset the widget to get a fresh token:
```tsx
if (error) {
  if (widgetIdRef.current && window.turnstile) {
    window.turnstile.reset(widgetIdRef.current);
    setCaptchaToken(null);
  }
}
```

## Step 5a: Auth Forms — Supabase Native captchaToken

### CRITICAL: Apply to ALL auth endpoints

When you enable CAPTCHA in Supabase Dashboard, it applies to **ALL auth endpoints** — not just signup. You MUST add Turnstile to:
- **Signup page** ✅
- **Login page** ✅ ← Easy to forget! Users can't log in without a token.
- **Password reset page** ✅ (if you have one)

### Auth function pattern

```typescript
// src/lib/auth.ts
export async function signUpWithEmail(email: string, password: string, captchaToken?: string) {
  return supabase.auth.signUp({
    email,
    password,
    options: captchaToken ? { captchaToken } : undefined,
  });
}

export async function signInWithEmail(email: string, password: string, captchaToken?: string) {
  return supabase.auth.signInWithPassword({
    email,
    password,
    options: captchaToken ? { captchaToken } : undefined,
  });
}

export async function resetPassword(email: string, captchaToken?: string) {
  return supabase.auth.resetPasswordForEmail(email, {
    redirectTo: `${window.location.origin}/login`,
    captchaToken,
  });
}
```

### Pass token in form submit
```tsx
async function handleSubmit(e: FormEvent) {
  e.preventDefault();
  setError(null);
  setLoading(true);
  const { error } = await signInWithEmail(email, password, captchaToken ?? undefined);
  setLoading(false);
  if (error) {
    setError(error.message);
    // Reset Turnstile for fresh token
    if (widgetIdRef.current && window.turnstile) {
      window.turnstile.reset(widgetIdRef.current);
      setCaptchaToken(null);
    }
  } else {
    navigate("/app");
  }
}
```

**No server-side verification code needed** — Supabase handles it automatically.

## Step 5b: Non-Auth Forms — Edge Function Verification

For non-auth forms (waitlist, contact, etc.), verify the token server-side:

### Send token in request body
```tsx
await supabase.functions.invoke("your-function", {
  body: { ...formData, turnstileToken: captchaToken },
});
```

### Verification helper (Supabase Edge Function)
```typescript
async function verifyTurnstile(token: string): Promise<boolean> {
  const secret = Deno.env.get('TURNSTILE_SECRET_KEY');
  if (!secret) {
    console.error('TURNSTILE_SECRET_KEY not set');
    return false;
  }
  const res = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ secret, response: token }),
  });
  const data = await res.json();
  if (!data.success) {
    console.error('Turnstile verification failed:', JSON.stringify(data));
  }
  return data.success === true;
}
```

---

## Step 6: DB-Based Rate Limiting (Complementary to CAPTCHA)

CAPTCHA prevents bots, but doesn't limit legitimate users from abusing expensive APIs (e.g. AI calls). Use DB-based rate limiting for that.

### Why not in-memory?
In-memory rate limiters (Maps, counters) reset on every serverless cold start (Vercel, AWS Lambda). A DB table persists across deployments.

### Migration

```sql
-- supabase/migrations/XXXXX_ai_usage_rate_limit.sql
create table if not exists public.ai_usage (
  user_id uuid not null references auth.users(id) on delete cascade,
  date date not null default current_date,
  count int not null default 1,
  primary key (user_id, date)
);

alter table public.ai_usage enable row level security;

create policy "Users can read own usage"
  on public.ai_usage for select
  using (auth.uid() = user_id);

create policy "Users can insert own usage"
  on public.ai_usage for insert
  with check (auth.uid() = user_id);

create policy "Users can update own usage"
  on public.ai_usage for update
  using (auth.uid() = user_id);
```

### Checking usage (IMPORTANT: use .maybeSingle() not .single())

```typescript
const today = new Date().toISOString().split("T")[0];
const DAILY_LIMIT = 20;

// ⚠️ MUST use .maybeSingle() — .single() throws error when no rows exist!
const { data: usage } = await supabase
  .from("ai_usage")
  .select("count")
  .eq("user_id", user.id)
  .eq("date", today)
  .maybeSingle();

if (usage && usage.count >= DAILY_LIMIT) {
  return new Response(JSON.stringify({ error: "daily_limit_reached" }), {
    status: 429,
    headers: { "Content-Type": "application/json" },
  });
}
```

### Incrementing usage (after successful operation, not before)

```typescript
// Increment AFTER successful AI call, not before
if (usage) {
  await supabase
    .from("ai_usage")
    .update({ count: usage.count + 1 })
    .eq("user_id", user.id)
    .eq("date", today);
} else {
  await supabase
    .from("ai_usage")
    .insert({ user_id: user.id, date: today, count: 1 });
}
```

### Frontend 429 handling

```typescript
// src/lib/ai.ts
export class RateLimitError extends Error {
  constructor() {
    super("daily_limit_reached");
    this.name = "RateLimitError";
  }
}

async function handleAiResponse(res: Response): Promise<ParsedRecipe> {
  if (res.status === 429) throw new RateLimitError();
  if (!res.ok) throw new Error("AI request failed");
  return res.json();
}
```

```tsx
// In form component
import { RateLimitError } from "@/lib/ai";

try {
  const result = await parseRecipe(url);
} catch (err) {
  if (err instanceof RateLimitError) {
    setError(t("recipeForm.rateLimitError")); // "You've reached your daily limit..."
  } else {
    setError(t("recipeForm.genericError"));
  }
}
```

---

## Step 7: Email Verification (Manual — No Code)

Enable in Supabase Dashboard → **Authentication** → **Auth Providers** → **Email** → **Confirm email** = ON

This ensures users must verify their email before accessing the app. No code changes needed.

---

## Verification

### Local testing
1. Ensure `localhost` is in Cloudflare Turnstile allowed domains
2. Use test keys for local dev:
   - Site Key: `1x00000000000000000000AA` (always passes)
   - Site Key: `2x00000000000000000000AB` (always blocks)
   - Site Key: `3x00000000000000000000FF` (forces interactive challenge)
3. **Test keys only work with test secret key** (`1x0000000000000000000000000000000AA`) — don't mix with real secret
4. `npm run dev` → test login AND signup → both must work

### Production testing
1. Hard refresh (`Cmd+Shift+R`) to clear cached JS
2. **Test signup** — should succeed without visible captcha
3. **Test login** — should succeed without visible captcha ← Don't forget!
4. **Test password reset** — if applicable
5. Check for `captcha verification process failed` errors — means a page is missing the Turnstile widget

### Debugging auth "captcha verification process failed"
| Symptom | Cause | Fix |
|---|---|---|
| Login fails, signup works | Turnstile only on signup page | Add Turnstile to login page too |
| Both fail | Secret key wrong in Supabase | Check Authentication → Attack Protection |
| Works locally, fails in prod | Missing `VITE_TURNSTILE_SITE_KEY` in hosting env | Add env var in Vercel/Netlify dashboard |
| `captcha verification process failed` | No `captchaToken` sent to Supabase Auth | Ensure token is passed in `options: { captchaToken }` |

### Debugging non-auth 403 errors
| Error code | Meaning | Fix |
|---|---|---|
| `missing-input-secret` | `TURNSTILE_SECRET_KEY` not set | `npx supabase secrets set ...` + redeploy |
| `invalid-input-secret` | Wrong secret key | Check key in Cloudflare dashboard |
| `missing-input-response` | No token sent from frontend | Check frontend sends token in body |
| `invalid-input-response` | Token malformed or expired | Token expires after 300s |
| `timeout-or-duplicate` | Token already used | Ensure reset after submit |
| Error `110200` in browser | Domain not allowed | Add domain in Cloudflare Turnstile dashboard |

## Learnings & Gotchas

1. **No npm package needed.** `@marsidev/react-turnstile` works but adds unnecessary dependency. The script tag + `window.turnstile.render()` with `render=explicit` is simpler and has zero bundle impact.
2. **Supabase CAPTCHA applies to ALL auth endpoints.** When you enable CAPTCHA in Supabase Dashboard, login, signup, AND password reset all require a token. If you only add Turnstile to signup, users can't log in. This is the #1 mistake.
3. **Supabase native captchaToken = no server code.** For auth forms, just pass `captchaToken` in the options object. Supabase verifies it server-side automatically. No Edge Function needed.
4. **Pre-clearance = No for Vercel/Netlify.** The Cloudflare "pre-clearance" setting only works for sites proxied through Cloudflare. For Vercel/Netlify-hosted sites, always choose "No".
5. **Site Key → Vercel, Secret Key → Supabase Dashboard.** Don't put both in the same place. Site key is public (frontend), secret key goes to Supabase Auth settings (not env vars).
6. **Use `.maybeSingle()` not `.single()` for DB queries that may return 0 rows.** `.single()` throws an error when no rows exist (e.g. first AI usage of the day). `.maybeSingle()` returns `null` gracefully.
7. **In-memory rate limiting is useless on serverless.** Vercel/Lambda cold starts reset all in-memory state. Use a DB table for persistent rate limiting.
8. **Increment usage AFTER success, not before.** If the AI call fails, the user shouldn't lose a usage count.
9. **Test keys don't mix with real secrets.** Cloudflare test site key generates test tokens that only pass with the test secret. Use matching pairs.
10. **Deploy order matters for non-auth forms.** If you deploy the Edge Function (requiring token) before the frontend (sending token), existing users get 403. Make token optional first, deploy frontend, then make required.
11. **Log AI provider errors with response body.** Don't just `throw new Error("AI failed")` — read the response body for the actual error (quota exceeded, invalid key, etc.): `throw new Error(\`Provider ${response.status}: ${await response.text()}\`)`.
