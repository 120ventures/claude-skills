---
name: setup-gtm
description: Set up Google Tag Manager container with GA4, Meta Pixel, PostHog, Consent Mode v2, and custom events
argument-hint: [GTM-ID GA4-ID META-PIXEL-ID POSTHOG-KEY]
---

# Setup GTM Container with GA4 + Meta Pixel + PostHog + Consent Mode v2

Arguments: `$ARGUMENTS`

Format: `GTM_ID GA4_MEASUREMENT_ID META_PIXEL_ID POSTHOG_API_KEY`

Example: `/setup-gtm GTM-ABC1234 G-XYZ9876 1234567890 phc_abc123def456`

Parse the four arguments:
1. **GTM Container ID** (e.g. `GTM-ABC1234`)
2. **GA4 Measurement ID** (e.g. `G-XYZ9876`)
3. **Meta Pixel ID** (e.g. `1234567890`)
4. **PostHog Project API Key** (e.g. `phc_xxxxx`)

If any argument is missing, don't guess. Instead show this checklist so the user can grab the IDs:

```
Missing IDs. Here's where to get them:

1. GTM Container ID → https://tagmanager.google.com → Create Account → Container → Web → grab GTM-XXXXXXX
2. GA4 Measurement ID → https://analytics.google.com → Admin → Create Property → Data Streams → Web → grab G-XXXXXXX
3. Meta Pixel ID → https://business.facebook.com → Events Manager → Connect Data Sources → Web → Meta Pixel → grab the numeric ID
4. PostHog API Key → https://eu.posthog.com → Settings → Project API Key → grab phc_xxxxx

Then run: /setup-gtm GTM-XXX G-XXX 123456 phc_xxx
```

---

## Step 0: Define custom events BEFORE generating anything

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
| Consent Initialization - All Pages | Consent Initialization | Fires before any other tags |
| Consent Update | Custom Event | Event name: `consent_update` |

Plus one Custom Event trigger per custom event agreed in Step 0 (event name matches the `snake_case` name).

### Tags

All tags below that track user data must have **Consent Mode requirement: `analytics_storage = granted`** (except the Consent Default tag itself).

#### Base tags (always included):

**1. Consent Mode — Default**
- **Type:** Custom HTML
- **Fires on:** Consent Initialization - All Pages
- **Tag firing priority:** 100 (highest, fires first)
- **Code:**
```html
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('consent', 'default', {
    'analytics_storage': 'denied',
    'ad_storage': 'denied',
    'ad_user_data': 'denied',
    'ad_personalization': 'denied',
    'functionality_storage': 'granted',
    'security_storage': 'granted',
    'wait_for_update': 500
  });
</script>
```
- No consent requirement on this tag (it IS the consent setup)

**2. Consent Mode — Update**
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

**3. GTM to Analytics (GA4 Pageview)**
- **Type:** Google Tag (`googtag`)
- **Tag ID:** the GA4 Measurement ID variable
- **Fires on:** Consent Initialization - All Pages
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

## Step 3: Add GTM snippet to `index.html`

**In `<head>`** — add right after `<meta name="viewport">`:
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

---

## Step 4: Summary

After completing, tell the user:

```
Done! Here's what was set up:

✅ GTM snippet added to index.html
✅ dataLayer.push() wired into event tracking
✅ gtm-container.json generated with:
   - Google Consent Mode v2 (default denied + update on consent)
   - GA4 pageview + [N] custom events
   - Meta Pixel pageview + [N] custom events
   - PostHog pageview + [N] custom events (EU cloud)

Next steps:
1. Go to https://tagmanager.google.com → your container
2. Admin → Import Container → upload gtm-container.json
3. Choose "Existing workspace" → Merge → Overwrite conflicting tags
4. Review the imported tags, then click "Submit" → "Publish"
5. Add a consent banner that calls:
   window.dataLayer.push({event: 'consent_update'})
   when the user accepts cookies/tracking
```

---

## Rules

- PostHog host is ALWAYS `https://eu.i.posthog.com` (EU cloud)
- All tracking tags require `analytics_storage = granted` via Consent Mode
- The consent default tag fires on Consent Initialization, NOT on Page View
- Do NOT install any npm packages — all tracking loads via GTM
- Follow the project's existing code style in `index.html`
- The generated JSON must be valid GTM export format (exportFormatVersion 2)
- **Maximum 5 custom events** — always clarify events with the user first
- **Always ask about the conversion goal before generating anything**
