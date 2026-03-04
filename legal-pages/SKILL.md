---
name: legal-pages
description: Use when creating or updating legal pages for a website — Datenschutz, Impressum, AGB, Cookie-Hinweis. Generates DSGVO-compliant Austrian legal pages for 120 Ventures projects with automatic third-party tool detection.
---

# Legal Pages — Austrian Legal Page Generator

This skill generates DSGVO-compliant legal pages for 120 Ventures web projects: Datenschutzerklärung, Impressum, AGB, and Cookie-Hinweis. It scans the codebase for third-party tools, gathers project-specific variables, and creates complete legal pages matching the project's existing patterns.

No arguments needed. Just run `/legal-pages` and the skill handles everything.

**Difference from `/legal-audit`:**
- `/legal-audit` **audits** an existing website for legal compliance issues and flags violations
- `/legal-pages` **generates** the legal pages from scratch (or regenerates them) using standardized templates

**Important:** This skill generates legal text based on templates, not legal advice. Always recommend professional legal review for final sign-off.

---

## Step 0: Gather project info

Read `CLAUDE.md` and `README.md` to determine:

| Variable | Source | Example |
|---|---|---|
| `brandName` | CLAUDE.md | "Fitua", "HeyVenture" |
| `contactEmail` | CLAUDE.md | "hello@fitua.at" |
| `websiteUrl` | CLAUDE.md | "https://fitua.at" |
| `hasHealthData` | Ask user if unclear | true/false |
| `hasPaidFeatures` | Ask user if unclear | true/false |

### Hardcoded company data (always the same)

These values are constant across all 120 Ventures projects:

```
Firma:           120 Ventures GmbH
Firmenbuchnummer: FN 617650
UID-Nummer:      ATU80155458
Adresse:         Baumgasse 129, 1030 Wien, Österreich
Firmenbuchgericht: Handelsgericht Wien
Geschäftsführer: Dipl.-Kfm. Sebastian Hermans
```

If `brandName`, `contactEmail`, or `websiteUrl` cannot be determined from CLAUDE.md, ask the user before proceeding.

---

## Step 1: Scan for integrated tools

Search the codebase for third-party tools and services. Use Grep to detect each tool by its search patterns:

| Tool | Search patterns |
|---|---|
| Google Analytics | `gtag`, `GA_MEASUREMENT_ID` |
| Google Tag Manager | `GTM-`, `googletagmanager` |
| Google Ads | `google_ads`, `AW-` |
| PostHog | `posthog`, `POSTHOG_` |
| Hotjar | `hotjar`, `HOTJAR_` |
| Supabase | `supabase`, `SUPABASE_` |
| Stripe | `stripe`, `STRIPE_` |
| Brevo | `brevo`, `sendinblue` |
| Vercel | `vercel` |
| Netlify | `netlify` |
| Cloudflare | `cloudflare`, `turnstile` |
| Make | `make.com`, `integromat` |

Search in all source files, `.env*` files, and config files (`vite.config.*`, `package.json`, etc.).

**MUST confirm with user before proceeding:**

```
Detected tools:
- Supabase (Auth + DB)
- PostHog (Analytics)
- Stripe (Payments)
- Vercel (Hosting)

Are these correct? Anything missing or wrong?
```

Wait for user confirmation. Do NOT generate pages until the tool list is confirmed.

---

## Step 2: Check existing project patterns

Before generating pages, scan the project for:

### Component patterns
- Does a `LegalPageWrapper` component exist? Search for `LegalPageWrapper` in the codebase.
- What layout components are used? (`PageWrapper`, `Container`, `Layout`, etc.)
- What heading/text styles does the project use?

### Routing
- Which router is used? (React Router, TanStack Router, etc.)
- Where are routes defined? (`App.tsx`, `router.tsx`, `routes/` directory)
- Are existing routes lazy-loaded?

### Design system
- Tailwind classes used for content pages
- Existing page structure (headers, spacing, max-width)
- Footer component location and link patterns

### Existing legal pages
- Do any legal pages already exist? Check for `/datenschutz`, `/impressum`, `/agb`, `/privacy`, `/legal`
- If they exist, note their structure so the new pages match

---

## Step 3: Generate pages

Reference `legal-templates.md` (in this skill directory) for all legal text content. Replace template variables (`{{brandName}}`, `{{contactEmail}}`, etc.) with the values from Step 0. Include only sections relevant to the detected tools from Step 1.

### 3a: Datenschutzerklärung (`/datenschutz`)

Generate with these sections:
1. Verantwortlicher (company data)
2. Überblick der Verarbeitungen (summary of data processing)
3. Rechtsgrundlagen (Art. 6 DSGVO legal bases used)
4. Sicherheitsmaßnahmen (Art. 32 DSGVO)
5. Übermittlung an Drittländer (third-country transfers, per detected tool)
6. Cookies und Tracking (per detected tool, with name/purpose/duration/provider)
7. Hosting (Vercel/Netlify/Cloudflare — whichever is detected)
8. Webanalyse (Google Analytics/PostHog/Hotjar — whichever is detected)
9. Zahlungsdienstleister (Stripe — if detected)
10. E-Mail-Versand (Brevo — if detected)
11. Betroffenenrechte (Art. 15-21 DSGVO — always included)
12. Beschwerderecht bei der Datenschutzbehörde (always included)

Conditional sections:
- Include health data section (Art. 9 DSGVO) only if `hasHealthData === true`
- Include payment/Stripe section only if Stripe is detected
- Include email/Brevo section only if Brevo is detected
- Include only the analytics tools that were actually detected

### 3b: Impressum (`/impressum`)

Generate with these sections:
1. Angaben gemäß §5 ECG (company data, FN, UID, Firmenbuchgericht, GF)
2. Kontakt (contactEmail, websiteUrl)
3. EU-Streitbeilegung (link to ODR platform — always included)
4. Haftung für Inhalte (Haftungsausschluss)
5. Haftung für Links (Haftung für externe Links)

### 3c: AGB (`/agb`)

Generate with these sections:
1. Geltungsbereich
2. Vertragspartner (company data)
3. Vertragsgegenstand (adapted to brandName)
4. Registrierung / Nutzerkonto (if app has auth)
5. Preise und Zahlung (only if `hasPaidFeatures === true`)
6. Widerrufsrecht (FAGG §11-18, only if `hasPaidFeatures === true`)
7. Gewährleistung und Haftung
8. Datenschutz (reference to Datenschutzerklärung)
9. Schlussbestimmungen (Austrian law, Gerichtsstand Wien)

If `hasPaidFeatures === false`, omit sections 5 and 6 and adapt the AGB to a free-service context.

### 3d: Cookie-Hinweis component

Generate a Cookie-Hinweis banner component:
- Categories: Essenziell (always on), Statistik (opt-in), Marketing (opt-in)
- "Alle akzeptieren" and "Nur essenzielle" buttons with equal prominence
- Expandable detail view with individual toggles per category
- Stores consent in localStorage
- Footer link "Cookie-Einstellungen" to reopen the banner
- Blocks non-essential scripts until consent is given
- Match the project's existing Tailwind styles

---

## Step 4: Add routing

Add lazy-loaded routes for all legal pages. Example for React Router:

```tsx
const Datenschutz = lazy(() => import('./pages/Datenschutz'));
const Impressum = lazy(() => import('./pages/Impressum'));
const AGB = lazy(() => import('./pages/AGB'));
```

Routes to add:
- `/datenschutz` → Datenschutzerklärung
- `/impressum` → Impressum
- `/agb` → AGB

The Cookie-Hinweis is a component, not a route — it renders globally (typically in `App.tsx` or the root layout).

Follow the project's existing routing pattern. If routes use a config array, add to the config. If they use JSX routes, add JSX routes. Match the existing pattern exactly.

---

## Step 5: Add footer links

Add links to the footer component (or create a minimal footer if none exists):

Required footer links:
- Datenschutz → `/datenschutz`
- Impressum → `/impressum`
- AGB → `/agb`
- Cookie-Einstellungen → triggers Cookie-Hinweis banner to reopen

Use the same link style and layout pattern as existing footer links. If the footer already has legal links, update them to point to the new pages.

---

## Layout rules

### If `LegalPageWrapper` exists:
Use it. Wrap all legal page content in `<LegalPageWrapper>`. Do not create a new wrapper.

### If no `LegalPageWrapper` exists:
Use a minimal centered layout matching the project's existing content pages:

```tsx
<div className="mx-auto max-w-3xl px-4 py-16">
  <h1 className="mb-8 text-3xl font-bold">Page Title</h1>
  {/* content */}
</div>
```

Adapt Tailwind classes to match the project's existing spacing, max-width, and typography patterns.

### Text structure for all legal pages:
- `<h1>` for page title
- `<h2>` for main sections
- `<h3>` for subsections
- `<p>` for body text
- `<ul>` / `<li>` for lists
- Anchor IDs on `<h2>` elements for deep linking (e.g., `id="cookies"`)
- German language for all content
- No Markdown rendering — use semantic HTML/JSX directly

---

## Rules

- **Austrian law only** — reference DSGVO, ECG, FAGG, DSG, MedienG. Never use German-specific laws (TMG, TTDSG).
- **Always scan tools first** (Step 1) — never generate a Datenschutzerklärung without knowing which tools are integrated.
- **Always confirm tools with user** — do not assume. Show the detected list and ask for confirmation.
- **Ask when unsure** — if `hasHealthData` or `hasPaidFeatures` is ambiguous, ask the user.
- **Match project patterns** — use existing components, router, styles. Never introduce new dependencies.
- **German content** — all legal text in German. Code (variable names, component names) in English.
- **Recommend legal review** — always end with: "Diese Seiten basieren auf Vorlagen und ersetzen keine Rechtsberatung. Bitte vor Go-Live von einem Anwalt prüfen lassen."
- **No invented legal text** — only use text from `legal-templates.md`. Never make up legal clauses.
- **Include only detected tools** — do not include boilerplate sections for tools that are not in the project.
- **One file per page** — Datenschutz.tsx, Impressum.tsx, AGB.tsx, CookieHinweis.tsx (or matching the project's file naming convention).
