---
name: exit-intent-survey
description: Generate an exit intent survey — detection hook, UI component, edge function, and DB migration — adapted to the project's design system and context
---

# Exit Intent Survey

This skill is fully interactive — no arguments needed. Just run `/exit-intent-survey` and follow the prompts.

It generates 4 artifacts:
1. **Detection hook** (`useExitIntent`) — always identical across projects
2. **UI component** (`ExitIntentSurvey`) — styled to match the project's design system
3. **Edge function** or direct insert — backend persistence
4. **SQL migration** — `exit_intent_responses` table with RLS + indexes

---

## Step 0: Read project context (silent)

Before asking any questions, silently:

1. **Read the design system** — find CSS custom properties, Tailwind config, color tokens, typography classes. Check:
   - `src/index.css` or similar for CSS variables
   - `tailwind.config.*` for theme extensions
   - Any `constants/` or `tokens/` files
2. **Find the session ID utility** — search for `sessionId`, `getOrCreateSessionId`, `useSessionId`, or similar. Note the import path.
3. **Find the Supabase client** — search for `createClient`, `supabase/client`, or similar. Note the import path.
4. **Check for existing exit intent code** — search for `exitIntent`, `exit-intent`, `useExitIntent`. If found, inform the user and ask whether to replace or skip.

Store all findings internally — use them to generate code that matches the project perfectly.

---

## Step 1: Ask 3 setup questions (one at a time)

### Question 1: Page context

```
Wo wird das Exit Intent Survey eingebaut?

1. Survey Flow (z.B. mehrstufige Umfrage)
2. Checkout (z.B. Kaufprozess)
3. Landing Page (z.B. Produkt-Landingpage)
4. Produktseite (z.B. Detailseite)

Und was ist euer Conversion Goal? (z.B. Umfrage abschließen, Kauf, Waitlist-Signup)
```

Wait for the user's answer before continuing.

### Question 2: Context variable

Based on the page context, suggest the most useful context variable:

- **Survey flow:** `currentScreen` (number) — which step they left on
- **Checkout:** `cartValue` (number) or `productName` (text)
- **Landing page:** nothing extra (just page URL)
- **Produktseite:** `productName` (text) or `productId` (text)

```
Welche Kontextvariable soll mitgeloggt werden?

Für [context type] empfehle ich: [suggestion] — das zeigt euch [why it's useful].

Passt das, oder wollt ihr etwas anderes tracken?
```

Wait for the user's answer before continuing.

### Question 3: Persistence method

```
Wie soll das Feedback gespeichert werden?

1. Edge Function (empfohlen) — Zod-Validierung + Rate Limiting serverseitig
2. Direkte Supabase-Insert — schneller aufgesetzt, aber keine serverseitige Validierung

Für die meisten Projekte empfehle ich Option 1.
```

Wait for the user's answer before continuing.

---

## Step 2: Define exit reasons

Based on the page context from Step 1, suggest 6 default reasons:

### Survey Flow
```typescript
const EXIT_REASONS = [
  { id: "price", label: "Zu teuer" },
  { id: "not_ready", label: "Noch zu früh, komme später wieder" },
  { id: "unclear_value", label: "Nutzen nicht klar genug" },
  { id: "too_personal", label: "Thema zu privat für eine App" },
  { id: "just_looking", label: "Nur umgeschaut" },
  { id: "other", label: "Sonstiges" },
] as const;
```

### Checkout
```typescript
const EXIT_REASONS = [
  { id: "price", label: "Preis zu hoch" },
  { id: "unclear_value", label: "Nutzen nicht klar genug" },
  { id: "not_right", label: "Passt nicht zu mir" },
  { id: "looking_elsewhere", label: "Suche etwas anderes" },
  { id: "tech_doubts", label: "Technische Zweifel" },
  { id: "other", label: "Sonstiges" },
] as const;
```

### Landing Page
```typescript
const EXIT_REASONS = [
  { id: "not_relevant", label: "Passt nicht zu mir" },
  { id: "not_understood", label: "Nicht ganz verstanden" },
  { id: "not_now", label: "Nicht jetzt, vielleicht später" },
  { id: "trust", label: "Unsicher ob seriös" },
  { id: "just_looking", label: "Nur umgeschaut" },
  { id: "other", label: "Sonstiges" },
] as const;
```

### Produktseite
```typescript
const EXIT_REASONS = [
  { id: "price", label: "Preis zu hoch" },
  { id: "not_right", label: "Passt nicht zu meinen Bedürfnissen" },
  { id: "comparison", label: "Vergleiche noch andere Optionen" },
  { id: "unclear_info", label: "Informationen nicht ausreichend" },
  { id: "not_now", label: "Nicht jetzt, vielleicht später" },
  { id: "other", label: "Sonstiges" },
] as const;
```

Present the matching defaults and ask:

```
Hier sind die Standard-Gründe für [context type]:

[list reasons]

Passen die so, oder willst du welche anpassen? (max. 6, der letzte sollte immer "Sonstiges" sein)
```

Wait for confirmation or customization before continuing.

---

## Step 3: Generate detection hook

Create `src/hooks/useExitIntent.ts` — this is **always identical** regardless of project:

```typescript
import { useState, useEffect, useCallback, useRef } from "react";

const ACTIVATION_DELAY_MS = 5000;

interface UseExitIntentOptions {
  /** Don't trigger when already completed */
  enabled: boolean;
}

export function useExitIntent({ enabled }: UseExitIntentOptions) {
  const [isVisible, setIsVisible] = useState(false);
  const hasShownRef = useRef(false);
  const isActiveRef = useRef(false);

  const showPopup = useCallback(() => {
    if (hasShownRef.current || !isActiveRef.current || !enabled) return;
    hasShownRef.current = true;
    sessionStorage.setItem("exit_intent_shown", "true");
    setIsVisible(true);
  }, [enabled]);

  // Activation delay + session check
  useEffect(() => {
    if (!enabled) return;
    const shown = sessionStorage.getItem("exit_intent_shown");
    if (shown) {
      hasShownRef.current = true;
      return;
    }
    const timer = setTimeout(() => {
      isActiveRef.current = true;
    }, ACTIVATION_DELAY_MS);
    return () => clearTimeout(timer);
  }, [enabled]);

  // Desktop: mouse leaves viewport top edge
  useEffect(() => {
    if (!enabled) return;
    const isMobile = "ontouchstart" in window || navigator.maxTouchPoints > 0;
    if (isMobile) return;

    const handleMouseLeave = (e: MouseEvent) => {
      if (e.clientY <= 5) showPopup();
    };

    document.addEventListener("mouseleave", handleMouseLeave);
    return () => document.removeEventListener("mouseleave", handleMouseLeave);
  }, [enabled, showPopup]);

  // Mobile: tab switch (visibilitychange) + repeated scroll-up
  useEffect(() => {
    if (!enabled) return;
    const isMobile = "ontouchstart" in window || navigator.maxTouchPoints > 0;
    if (!isMobile) return;

    const handleVisibilityChange = () => {
      if (document.visibilityState === "hidden") showPopup();
    };

    let lastScrollY = window.scrollY;
    let scrollUpCount = 0;

    const handleScroll = () => {
      const currentScrollY = window.scrollY;
      const diff = lastScrollY - currentScrollY;
      if (diff > 60) {
        scrollUpCount++;
        if (scrollUpCount >= 2) showPopup();
      } else if (diff < -30) {
        scrollUpCount = 0;
      }
      lastScrollY = currentScrollY;
    };

    document.addEventListener("visibilitychange", handleVisibilityChange);
    window.addEventListener("scroll", handleScroll, { passive: true });

    return () => {
      document.removeEventListener("visibilitychange", handleVisibilityChange);
      window.removeEventListener("scroll", handleScroll);
    };
  }, [enabled, showPopup]);

  const dismiss = useCallback(() => setIsVisible(false), []);

  return { isVisible, dismiss };
}
```

---

## Step 4: Generate UI component

Create the component in the appropriate location:
- If `src/components/survey/` exists → `src/components/survey/ExitIntentSurvey.tsx`
- Otherwise → `src/components/ExitIntentSurvey.tsx`

**CRITICAL: Use the project's actual design tokens** found in Step 0. Do NOT hardcode colors — use CSS variables, Tailwind classes, or whatever the project uses.

### Component structure

```
┌─────────────────────────────┐
│ [X close]                   │
│                             │
│ Bevor du gehst              │  ← title
│ Was hat nicht gepasst?      │  ← subtitle
│                             │
│ ○ Reason 1                  │
│ ○ Reason 2                  │  ← single-select radio buttons
│ ● Reason 3 (selected)       │
│ ○ Reason 4                  │
│ ○ Reason 5                  │
│ ○ Sonstiges                 │
│                             │
│ [ Feedback senden ]         │  ← submit button (disabled until selection)
│     Überspringen            │  ← dismiss link
└─────────────────────────────┘
```

After submit → success state:
```
┌─────────────────────────────┐
│                             │
│        ✓ (checkmark)        │
│  Danke für das Feedback!    │
│                             │
└─────────────────────────────┘
```

### Requirements

- **Layout:** bottom-sheet on mobile (slides up from bottom, rounded top corners), centered modal on desktop (rounded all corners)
- **Backdrop:** semi-transparent overlay (`bg-black/40` or equivalent)
- **z-index:** `10001` (above cookie banners which typically use 9999–10000)
- **Animation:** slide-in from bottom on mobile, zoom-in on desktop (use CSS animations or Tailwind `animate-in` if available)
- **Accessibility:** `role="dialog"`, `aria-modal="true"`, `aria-labelledby` on title, `aria-label="Schließen"` on close button, Escape key dismisses
- **Submit flow:** select reason → click "Feedback senden" → loading state ("Wird gesendet...") → success checkmark → auto-dismiss after 1500ms
- **Best-effort:** wrap API call in try/catch, never block user on failure
- **Icons:** only `X` from `lucide-react` (close button), inline SVG for checkmark

### Props interface

Adapt based on context variable from Step 1:

```typescript
// Survey flow
interface ExitIntentSurveyProps {
  currentScreen: number;
  onDismiss: () => void;
}

// Checkout
interface ExitIntentSurveyProps {
  productName?: string;
  cartValue?: number;
  onDismiss: () => void;
}

// Landing page
interface ExitIntentSurveyProps {
  onDismiss: () => void;
}
```

### API call

**If Edge Function (recommended):**
```typescript
await supabase.functions.invoke("save-exit-intent", {
  body: {
    sessionId: getOrCreateSessionId(),
    reason: selectedReason,
    reasonLabel: EXIT_REASONS.find((r) => r.id === selectedReason)?.label,
    [contextField]: contextValue, // e.g. currentScreen, productName
    pageUrl: window.location.href,
  },
});
```

**If direct insert:**
```typescript
await supabase.from("exit_intent_responses").insert({
  session_id: getOrCreateSessionId(),
  reason: selectedReason,
  reason_label: EXIT_REASONS.find((r) => r.id === selectedReason)?.label,
  [contextColumn]: contextValue,
  page_url: window.location.href,
});
```

Use the **actual Supabase client import path** and **session ID utility** found in Step 0.

---

## Step 5: Generate backend

### Option A: Edge Function (recommended)

Create `supabase/functions/save-exit-intent/index.ts`:

```typescript
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import { z } from 'https://deno.land/x/zod/mod.ts'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

// Adapt schema based on context variable
const exitIntentSchema = z.object({
  sessionId: z.string().uuid(),
  reason: z.string().max(50),
  reasonLabel: z.string().max(200).optional(),
  // Context field — adapt per project:
  // currentScreen: z.number().int().min(1).max(20),    // survey
  // productName: z.string().max(200).optional(),        // checkout/product
  pageUrl: z.string().max(500).optional(),
})

// Rate limiting — 3 per session per minute
const rateLimitStore = new Map<string, { count: number; resetTime: number }>()

function checkRateLimit(sessionId: string): boolean {
  const now = Date.now()
  const record = rateLimitStore.get(sessionId)
  if (!record || now > record.resetTime) {
    rateLimitStore.set(sessionId, { count: 1, resetTime: now + 60000 })
    return true
  }
  if (record.count >= 3) return false
  record.count++
  return true
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders })
  }

  try {
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? '',
      { auth: { autoRefreshToken: false, persistSession: false } }
    )

    const rawBody = await req.json()
    const parsed = exitIntentSchema.safeParse(rawBody)

    if (!parsed.success) {
      return new Response(
        JSON.stringify({ error: 'Validation failed', details: parsed.error.format() }),
        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    const { sessionId, reason, reasonLabel, pageUrl, ...contextFields } = parsed.data

    if (!checkRateLimit(sessionId)) {
      return new Response(
        JSON.stringify({ error: 'Rate limit exceeded' }),
        { status: 429, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    const { error } = await supabase
      .from('exit_intent_responses')
      .insert({
        session_id: sessionId,
        reason,
        reason_label: reasonLabel,
        page_url: pageUrl,
        ...contextFields, // spread context column(s)
      })

    if (error) {
      console.error('Error saving exit intent:', error)
      throw error
    }

    return new Response(
      JSON.stringify({ success: true }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    console.error('Exit intent error:', error)
    return new Response(
      JSON.stringify({ error: 'Internal server error' }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  }
})
```

### Option B: Direct insert

Skip edge function creation. Note the tradeoff to the user:
```
⚠️ Direkte Supabase-Insert: Keine serverseitige Validierung oder Rate Limiting.
Jeder mit dem anon key könnte theoretisch Daten einfügen.
Für Low-Traffic-Seiten okay, für Produktion empfehle ich die Edge Function.
```

---

## Step 6: Generate SQL migration

Create a migration file at `supabase/migrations/[timestamp]_create_exit_intent_responses.sql`.

Adapt the context column based on Step 1:

```sql
-- Exit intent survey responses
CREATE TABLE IF NOT EXISTS exit_intent_responses (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  session_id UUID NOT NULL,
  reason TEXT NOT NULL,
  reason_label TEXT,
  -- Context column (adapt per project):
  -- current_screen INTEGER,           -- survey flow
  -- product_name TEXT,                 -- checkout / product page
  -- cart_value NUMERIC(10,2),          -- checkout
  page_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_exit_intent_session ON exit_intent_responses (session_id);
CREATE INDEX idx_exit_intent_reason ON exit_intent_responses (reason);
CREATE INDEX idx_exit_intent_created ON exit_intent_responses (created_at DESC);

-- RLS: no direct access from client (edge function uses service_role)
ALTER TABLE exit_intent_responses ENABLE ROW LEVEL SECURITY;

-- If using direct insert instead of edge function, add this policy:
-- CREATE POLICY "Allow anonymous inserts" ON exit_intent_responses
--   FOR INSERT TO anon WITH CHECK (true);
```

If the user chose direct insert in Step 1, uncomment the RLS policy for anonymous inserts.

---

## Step 7: Wire into target component

Show the exact integration code for the user's specific file. Find the target component from Step 1 context and provide a snippet like:

```typescript
// In the target component (e.g. SurveyWizard.tsx, CheckoutPage.tsx, etc.)

import { useExitIntent } from "@/hooks/useExitIntent";
import ExitIntentSurvey from "@/components/survey/ExitIntentSurvey";

// Inside the component:
const { isVisible: showExitIntent, dismiss: dismissExitIntent } = useExitIntent({
  enabled: !isCompleted, // adapt condition: e.g. !isPurchased, true for landing pages
});

// In the JSX return:
{showExitIntent && (
  <ExitIntentSurvey
    currentScreen={currentScreen} // or productName, or nothing — depends on context
    onDismiss={dismissExitIntent}
  />
)}
```

Point to the **exact file and location** where this should be added.

---

## Step 8: Summary

After all files are generated, show:

```
Done! Exit Intent Survey eingerichtet:

✅ src/hooks/useExitIntent.ts — Detection (Desktop top-edge + Mobile scroll-up/tab-switch)
✅ src/components/[path]/ExitIntentSurvey.tsx — UI (bottom-sheet mobile / modal desktop)
✅ supabase/functions/save-exit-intent/index.ts — Edge Function mit Zod + Rate Limiting
   (oder: direkte Supabase-Insert)
✅ supabase/migrations/[timestamp]_create_exit_intent_responses.sql — Tabelle + RLS + Indexes
✅ Integration in [target component] gezeigt

Nächste Schritte:
1. Migration anwenden: supabase db push (oder supabase migration up)
2. Edge Function deployen: supabase functions deploy save-exit-intent
3. Testen: Seite öffnen → 5s warten → Maus über Viewport-Oberkante bewegen
4. Prüfen: Zeile in exit_intent_responses erscheint
```

---

## Rules

- **Always read the design system first** — never hardcode colors. Use the project's CSS variables, Tailwind classes, or design tokens.
- **Max 6 reasons** — always end with "Sonstiges"
- **German copy default** — "Bevor du gehst" / "Was hat nicht gepasst?" / "Feedback senden" / "Überspringen"
- **5s activation delay**, once per session (sessionStorage), desktop top-edge detection only (clientY ≤ 5)
- **Mobile detection:** visibilitychange + 2× scroll-up > 60px
- **Hook separate from UI** — `useExitIntent` returns `{ isVisible, dismiss }`, component is stateless regarding detection
- **Best-effort submission** — try/catch, never block the user or show error states
- **No npm packages** — only `lucide-react` for the X icon, inline SVG for checkmark
- **Edge function:** always include Zod validation + rate limiting (3/session/min)
- **Direct insert:** always warn about missing server-side validation
- **z-index: 10001** — above cookie banners
- **Accessibility:** `role="dialog"`, `aria-modal="true"`, Escape closes, `aria-label` on close button
- **Auto-dismiss:** 1500ms after successful submission
