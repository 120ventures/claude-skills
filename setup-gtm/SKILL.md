---
name: setup-gtm
description: Set up Google Tag Manager container with GA4, Meta Pixel, PostHog, Consent Mode v2, and custom events
---

# Setup GTM Container with GA4 + Meta Pixel + PostHog + Consent Mode v2

This skill is fully interactive — no arguments needed. Just run `/setup-gtm` and follow the prompts.

## Step 0: Collect IDs one by one

Ask the user for each ID individually. For each one, tell them where to find it if they don't have it yet.

**1. GTM Container ID**
```
Hast du schon einen GTM Container? Gib mir die ID (z.B. GTM-XXXXXXX).

Falls nicht: https://tagmanager.google.com → Account erstellen → Container → Web
```
Wait for the user's answer before continuing.

**2. GA4 Measurement ID**
```
GA4 Measurement ID? (z.B. G-XXXXXXX)

Falls nicht: https://analytics.google.com → Admin → Property erstellen → Data Stream → Web
```
Wait for the user's answer before continuing.

**3. Meta Pixel ID**
```
Meta Pixel ID? (die numerische ID)

Falls nicht: https://business.facebook.com → Events Manager → Connect Data Sources → Web → Meta Pixel
```
Wait for the user's answer before continuing.

**4. PostHog API Key**
```
PostHog Project API Key? (z.B. phc_xxxxx)

Falls nicht: https://eu.posthog.com → Settings → Project API Key
```
Wait for the user's answer before continuing.

**5. Additional tools**
```
Wollt ihr noch andere Tools einbinden? (z.B. Hotjar, Clarity, TikTok Pixel, LinkedIn Insight Tag, Hubspot, etc.)

Falls ja: Sag mir welches Tool + die jeweilige ID/Key.
Falls nein: Einfach "nein" und wir machen weiter.
```
Wait for the user's answer before continuing.

If the user wants additional tools, collect each tool name + ID. For each additional tool, create:
- A **Constant variable** for the tool's ID/key
- A **Pageview tag** (Custom HTML) that loads the tool's standard snippet, fires on All Pages, with `analytics_storage = granted` consent requirement
- For each custom event: an additional **Custom HTML tag** that sends the event to that tool (if the tool supports custom events)

Use the tool's official embed snippet. Common patterns:
- **Hotjar:** `(function(h,o,t,j,a,r){...})(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');`
- **Microsoft Clarity:** `(function(c,l,a,r,i,t,y){...})(window,document,"clarity","script","PROJECT_ID");`
- **TikTok Pixel:** `ttq.load('PIXEL_ID'); ttq.page();`
- **LinkedIn Insight Tag:** `_linkedin_partner_id = "PARTNER_ID"; ...`

---

## Step 1: Define custom events BEFORE generating anything

**STOP. Do not generate the container JSON yet.** First, ask the user two questions:

1. **"Was ist euer Conversion Goal?"** — The one action that matters most (e.g. waitlist signup, purchase, booking, demo request). This becomes the primary conversion event and fires `fbq('track', 'Lead')` (or `'Purchase'`, etc.) on Meta for ad optimization.

2. **"Welche 2–4 Schritte führen dahin?"** — The key steps in the user journey leading to the conversion (e.g. CTA click, survey start, add to cart). These become the custom events.

### Rules for events:
- **Maximum 5 custom events total** (including the conversion event). Less is more.
- Events should map to meaningful user intent, not UI interactions.
- Name events in `snake_case` (e.g. `cta_click`, `waitlist_signup`, `survey_start`).
- Choose the right Meta standard event for the conversion (Lead, Purchase, CompleteRegistration, etc.) — use `fbq('trackCustom', ...)` for non-standard events.

### Example event discussion:

```
Before I set up GTM, let's define your events.

1. Was ist euer Conversion Goal?
   (z.B. Waitlist-Signup, Kauf, Buchung, Demo-Anfrage)

2. Welche 2–4 Schritte führen dahin?
   (z.B. CTA-Klick, Survey gestartet, Produkt angesehen)
```

Once the user confirms the events, proceed to Step 1.

---

## Step 1: Generate `gtm-container.json`

Create a file `gtm-container.json` in the project root. This is a standard GTM container export (exportFormatVersion 2) that the user imports via **GTM Admin > Import Container**.

Use placeholder values for `accountId`, `containerId`, `containerName`, `fingerprint` — they get overwritten on import.

### Variables

| Variable | Type | Value |
|----------|------|-------|
| GA4 Measurement ID | Constant | (from argument) |
| Meta Pixel ID | Constant | (from argument) |
| PostHog API Key | Constant | (from argument) |
| PostHog Host | Constant | `https://eu.i.posthog.com` |

### Triggers

Always include these base triggers:

| Trigger | Type | Details |
|---------|------|---------|
| All Pages | Page View | Standard pageview trigger |
| Consent Update | Custom Event | Event name: `consent_update` |

Plus one Custom Event trigger per custom event agreed in Step 0 (event name matches the `snake_case` name).

**NOTE:** Do NOT create a "Consent Initialization" trigger or a "Consent Mode - Default" tag in the GTM container. Consent defaults are set in `index.html` before GTM loads (see Step 3). Setting defaults inside GTM causes them to override the region-specific defaults and results in 0% consent rate for non-EEA traffic.

### Tags

All tags below that track user data must have **Consent Mode requirement: `analytics_storage = granted`**.

#### Base tags (always included):

**1. Consent Mode — Update**
- **Type:** Custom HTML
- **Fires on:** Consent Update trigger (`consent_update`)
- **Code:**
```html
<script>
  function gtag(){dataLayer.push(arguments);}
  gtag('consent', 'update', {
    'analytics_storage': 'granted',
    'ad_storage': 'granted',
    'ad_user_data': 'granted',
    'ad_personalization': 'granted'
  });
</script>
```
- No consent requirement on this tag

**2. GTM to Analytics (GA4 Pageview)**
- **Type:** Google Tag (`googtag`)
- **Tag ID:** the GA4 Measurement ID variable
- **Fires on:** All Pages (NOT Consent Initialization — the init trigger fires too early for GA4 to receive valid page data)
- **Consent required:** `analytics_storage = granted`

**4. Meta Pixel — Pageview**
- **Type:** Custom HTML
- **Fires on:** All Pages
- **Consent required:** `analytics_storage = granted`
- **Code:** Standard Meta Pixel init + `fbq('track', 'PageView')` using the Meta Pixel ID variable

**5. PostHog — Pageview**
- **Type:** Custom HTML
- **Fires on:** All Pages
- **Consent required:** `analytics_storage = granted`
- **Code:** Standard PostHog snippet using PostHog API Key and PostHog Host variables

#### Custom event tags (from Step 0):

For each custom event, create **3 tags** (one per platform):

**GA4_{event_name}**
- **Type:** GA4 Event (`gaawe`)
- **Event name:** the event name
- **Measurement ID:** reference to "GTM to Analytics" tag
- **Fires on:** the event's Custom Event trigger
- **Consent required:** `analytics_storage = granted`

**Meta_{event_name}**
- **Type:** Custom HTML
- **Fires on:** the event's Custom Event trigger
- **Consent required:** `analytics_storage = granted`
- **Code:** For the primary conversion event, use the appropriate standard Meta event (`fbq('track', 'Lead')`, `fbq('track', 'Purchase')`, etc.). For other events, use `fbq('trackCustom', 'event_name')`.

**PostHog_{event_name}**
- **Type:** Custom HTML
- **Fires on:** the event's Custom Event trigger
- **Consent required:** `analytics_storage = granted`
- **Code:** `<script>posthog.capture('event_name');</script>`

---

## Step 2: Wire up dataLayer in the codebase

Find the project's event tracking hook or utility (e.g. `useTrackEvent`, `trackEvent`, or similar). Add a `window.dataLayer.push({ event: eventType })` call so GTM picks up events fired from the app.

If no tracking utility exists, create a minimal one that pushes to dataLayer.

Make sure each custom event from Step 0 is actually fired somewhere in the codebase. If an event doesn't have a corresponding call yet, add it in the appropriate component.

---

## Step 3: Add Consent Defaults + GTM snippet to `index.html`

**CRITICAL: Consent defaults MUST be set BEFORE the GTM script loads.** This is the Google-recommended approach and prevents the 0% consent rate issue. Do NOT set consent defaults inside the GTM container — that overrides region-specific rules.

**In `<head>`** — add right after `<meta name="viewport">`:

First, the region-specific consent defaults:
```html
<!-- Consent Mode v2 — region-specific defaults (before GTM) -->
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}

// Default: grant all for non-EEA regions
gtag('consent', 'default', {
  'analytics_storage': 'granted',
  'ad_storage': 'granted',
  'ad_user_data': 'granted',
  'ad_personalization': 'granted',
  'functionality_storage': 'granted',
  'security_storage': 'granted',
});

// EEA + UK + CH: deny until user consents (GDPR/DSGVO)
gtag('consent', 'default', {
  'analytics_storage': 'denied',
  'ad_storage': 'denied',
  'ad_user_data': 'denied',
  'ad_personalization': 'denied',
  'region': ['AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI',
    'FR', 'GR', 'HR', 'HU', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT', 'NL',
    'PL', 'PT', 'RO', 'SE', 'SI', 'SK', 'IS', 'LI', 'NO', 'GB', 'CH'],
  'wait_for_update': 500,
});
</script>
```

Then, immediately after, the GTM container script:
```html
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM_ID_HERE');</script>
<!-- End Google Tag Manager -->
```

**Right after `<body>`** — add the noscript fallback:
```html
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM_ID_HERE"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
```

Replace `GTM_ID_HERE` with the actual GTM Container ID from the arguments.

**Why this order matters:** Google's Consent Mode reads defaults synchronously before any tags fire. If defaults are set inside a GTM tag (even a Consent Initialization tag), they can override the region-specific `region` parameter with a global `denied`, causing 0% consent rate for all non-EEA traffic.

---

## Step 4: Cookie Consent Banner Integration

After generating the GTM container and wiring up dataLayer, check if the project already has a cookie consent banner.

### If a cookie consent banner EXISTS:

Search the codebase for cookie consent components (e.g. `CookieConsent`, `CookieBanner`, `consent`). Verify:

1. **The consent update event name matches the GTM trigger exactly.** The GTM container expects the event `consent_update`. If the banner fires a different event name (e.g. `cookie_consent_update`, `consent_granted`, etc.), fix it to match.

2. **The `gtag('consent', 'update', ...)` call works reliably.** Do NOT rely on `window.gtag` existing — instead push directly to dataLayer:
```typescript
// CORRECT — always works with GTM
window.dataLayer = window.dataLayer || [];
function gtag(...args: unknown[]) {
  window.dataLayer!.push(args);
}
gtag('consent', 'update', {
  'analytics_storage': prefs.analytics ? 'granted' : 'denied',
  'ad_storage': prefs.marketing ? 'granted' : 'denied',
  'ad_user_data': prefs.marketing ? 'granted' : 'denied',
  'ad_personalization': prefs.marketing ? 'granted' : 'denied',
});

// ALSO fire the custom event so the GTM "Consent Update" trigger fires
window.dataLayer.push({
  event: 'consent_update',
  analytics_consent: prefs.analytics,
  marketing_consent: prefs.marketing,
});
```

3. **A floating re-open button exists** so users can change their cookie preferences after the initial choice. If not, add one — a small icon button (e.g. cookie icon) fixed to bottom-left with `z-index` below the banner but above page content.

### If NO cookie consent banner exists:

Create one. Requirements:
- Three choices: "Alle akzeptieren", "Nur notwendige", "Einstellungen" (with toggles for analytics/marketing)
- On accept/reject: store preferences in `localStorage`, call `gtag('consent', 'update', ...)` via dataLayer push, and fire `window.dataLayer.push({ event: 'consent_update' })`
- On page load: check localStorage — if consent already given, call `gtag('consent', 'update', ...)` with saved preferences
- Show a floating cookie icon button (bottom-left) after consent is given so users can reopen settings
- Modal backdrop with `z-index: 9999+`
- Must use `<Link>` to privacy policy page
- WCAG: focus management, Escape key closes with "reject all", `aria-modal`, `role="dialog"`

**CRITICAL:** The event name in `dataLayer.push({ event: '...' })` MUST be exactly `consent_update` — this is what the GTM container trigger listens for. A mismatch here means GTM never fires the consent update tag, resulting in 0% consent rate in GTM.

---

## Step 5: Summary

After completing, tell the user:

```
Done! Here's what was set up:

✅ Region-specific Consent Mode v2 defaults in index.html (before GTM)
✅ GTM snippet added to index.html
✅ dataLayer.push() wired into event tracking
✅ Cookie consent banner integrated with Consent Mode v2
✅ gtm-container.json generated with:
   - Consent Mode update tag (fires on cookie banner interaction)
   - GA4 pageview + [N] custom events
   - Meta Pixel pageview + [N] custom events
   - PostHog pageview + [N] custom events (EU cloud)

How consent works:
- Non-EEA visitors: all consent granted by default → full tracking immediately
- EEA/UK/CH visitors: all consent denied → tracking only after cookie banner acceptance

Next steps:
1. Go to https://tagmanager.google.com → your container
2. Admin → Import Container → upload gtm-container.json
3. Choose "Existing workspace" → Merge → Overwrite conflicting tags
4. IMPORTANT: Make sure there is NO "Consent Mode - Default" tag in the container
   (defaults are handled in index.html — a GTM default tag would override them)
5. Review the imported tags, then click "Submit" → "Publish"
6. Test: check GTM Preview Mode — non-EEA traffic should show consent as granted
```

---

## Rules

- PostHog host is ALWAYS `https://eu.i.posthog.com` (EU cloud) unless the user's snippet explicitly uses a different host (e.g. `https://us.i.posthog.com`)
- All tracking tags require `analytics_storage = granted` via Consent Mode
- **Consent defaults MUST be set in `index.html` before the GTM script, NOT inside GTM** — this enables region-specific defaults. A "Consent Mode - Default" tag inside GTM will override the region parameter and cause 0% consent rate for non-EEA traffic.
- Do NOT install any npm packages — all tracking loads via GTM
- Follow the project's existing code style in `index.html`
- The generated JSON must be valid GTM export format (exportFormatVersion 2)
- **Maximum 5 custom events** — always clarify events with the user first
- **Always ask about the conversion goal before generating anything**
- **GA4 config tag fires on "All Pages" trigger, NOT "Consent Initialization"** — the init trigger fires too early for GA4 to receive valid page data.
- **Consent update event name must be exactly `consent_update`** — this must match between the cookie banner's `dataLayer.push({ event: '...' })` and the GTM trigger. A mismatch = 0% consent rate.
- **Always push gtag consent updates via dataLayer** — never rely on `window.gtag` existing. Use `window.dataLayer.push(arguments)` pattern instead.
- **Always verify or create a cookie consent banner** as part of this skill — GTM Consent Mode is useless without one
- **Each tool (GA4, Meta, PostHog, etc.) is optional** — the user can skip any tool. Only generate variables, tags, and triggers for tools the user actually provides IDs for.

## GTM Container JSON Format — Critical Rules (learned from import failures)

These rules are **non-negotiable** for the JSON to import successfully into GTM:

1. **Custom HTML tag type MUST be lowercase `"html"`**, NOT `"HTML"`. GTM rejects uppercase.
   ```json
   "type": "html"    ✅ CORRECT
   "type": "HTML"    ❌ REJECTED — "Unbekannter Entitätstyp"
   ```

2. **Do NOT include `consentSettings` in the JSON export.** GTM's import parser does not understand the `consentSettings` object format. The import will fail with "Argument is not an object: analytics_storage". Instead, tell the user to set consent requirements manually per tag in the GTM UI after import (Tag → Advanced Settings → Consent Settings → Require additional consent → `analytics_storage`).

3. **Valid tag types for GTM container JSON:**
   - `"html"` — Custom HTML (lowercase!)
   - `"googtag"` — Google Tag (gtag.js config)
   - `"gaawe"` — GA4 Event
   - `"c"` — Constant variable

4. **Valid trigger types:**
   - `"PAGEVIEW"` — All Pages
   - `"CUSTOM_EVENT"` — Custom Event

5. **Always validate the JSON** before telling the user to import it:
   ```bash
   python3 -c "import json; json.load(open('gtm-container.json')); print('Valid JSON')"
   ```

## Pitfall: 0% Consent Rate (learned from production issue)

**Symptom:** GTM diagnostics shows "0% consent rate detected in some regions" and "100% of consent signals are marked as denied" — even outside the EEA.

**Root cause:** A "Consent Mode - Default" tag inside GTM that sets all consent to `denied` globally (without a `region` parameter). This overrides any region-specific defaults set in `index.html`.

**Fix:** Remove any "Consent Mode - Default" tag from the GTM container. Set consent defaults exclusively in `index.html` before the GTM script, using the `region` parameter to differentiate EEA vs. rest of world. The GTM container should only contain a "Consent Mode - Update" tag that fires on the `consent_update` event from the cookie banner.
