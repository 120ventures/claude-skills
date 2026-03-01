---
name: legal-audit
description: Audit website legal compliance for Austria — DSGVO, E-Commerce-Gesetz, FAGG, ePrivacy, cookie consent, Impressum, third-party transfers
---

# Legal Audit — Austrian Website Compliance

This skill audits a website for legal compliance under Austrian and EU law. It checks mandatory pages, DSGVO (GDPR) implementation, cookie consent, form handling, third-party data transfers, and security headers. It identifies violations and fixes them directly in the codebase.

No arguments needed. Just run `/legal-audit` and the skill scans the project automatically.

**Difference from other audits:**
- `/security-audit` checks **code-level security** — secrets, XSS, RLS, input validation
- `/a11y-audit` checks **WCAG accessibility** — contrast, keyboard nav, ARIA, semantics
- `/legal-audit` checks **legal compliance** — DSGVO, Impressum, cookie consent, data processing, Austrian law

**Important:** This skill provides technical compliance checks, not legal advice. Recommend professional legal review for final sign-off.

Reference sources:
- DSGVO (EU-GDPR): Verordnung (EU) 2016/679
- E-Commerce-Gesetz (ECG): BGBl. I Nr. 152/2001
- Mediengesetz (MedienG): BGBl. Nr. 314/1981, §24a
- Fern- und Auswärtsgeschäfte-Gesetz (FAGG): BGBl. I Nr. 33/2014
- Telekommunikationsgesetz (TKG 2021): BGBl. I Nr. 190/2021
- Datenschutzgesetz (DSG 2018): BGBl. I Nr. 165/1999 idgF
- Bundesgesetz über Barrierefreiheit (BaFG): BGBl. I Nr. 76/2023

---

## Step 0: Understand the project

Before auditing, read:
- `CLAUDE.md` / `README.md` for project context
- All legal pages (Impressum, Datenschutz, AGB, Widerruf)
- Cookie consent implementation
- All forms and data collection points
- Third-party scripts and services (analytics, fonts, CDNs, APIs)
- Hosting configuration and server location
- Security headers and SSL setup

Identify:
- **Business type** — B2C, B2B, or mixed? (affects FAGG obligations)
- **Data flows** — where does user data go? which third parties?
- **Consent mechanism** — how are cookies/tracking handled?
- **Legal entity** — Einzelunternehmen, GmbH, etc.? (affects Impressum requirements)

---

## Step 1: Audit across 8 categories

Go through **each category** below. For every issue found, note the file, the legal requirement, and the recommended fix. Rate severity as:
- **🔴 Critical** — legal violation, risk of Abmahnung or DSGVO fine
- **🟠 Major** — incomplete compliance, should fix before launch
- **🟡 Minor** — best practice, recommended but not strictly required

---

### Category 1: Pflichtseiten (Mandatory Pages)

#### Impressum — §5 ECG / §24a MedienG
> Every commercial Austrian website must have a complete, easily accessible Impressum.

**Check for:**
- Impressum page exists and is linked from every page (typically footer)
- Contains all required fields:
  - Firmenname / vollständiger Name des Inhabers
  - Rechtsform (GmbH, e.U., etc.)
  - Firmenbuchnummer + Firmenbuchgericht (if applicable)
  - UID-Nummer (Umsatzsteuer-Identifikationsnummer)
  - Sitz / Geschäftsanschrift (full postal address)
  - Kontakt: E-Mail (required), Telefon (recommended)
  - Mitglied der WKO / Berufsverband (if applicable, Gewerbeordnung)
  - Aufsichtsbehörde (if regulated profession)
  - Anwendbare Rechtsvorschriften (if regulated profession)
- Link labeled "Impressum" (not hidden behind "About" or "Legal")
- Reachable within 2 clicks from any page
- Not behind a login or paywall

**Fix pattern:** Create or update Impressum page with all required fields. Add footer link on all pages. Use label "Impressum" (legally recognized term).

---

#### Datenschutzerklärung — Art. 13/14 DSGVO
> A complete privacy policy must be accessible from every page and before every form.

**Check for:**
- Datenschutz page exists
- Linked from footer on every page
- Linked before/near every form that collects personal data
- Contains all required sections:
  - Verantwortlicher (name, address, contact)
  - Datenschutzbeauftragter (if applicable, >250 employees or sensitive data)
  - Zwecke und Rechtsgrundlagen der Verarbeitung (per data type)
  - Empfänger / Kategorien von Empfängern
  - Drittlandtransfers (especially USA — adequacy decision, SCCs, etc.)
  - Speicherdauer / Löschfristen (specific, not "so lange wie nötig")
  - Betroffenenrechte (Auskunft, Berichtigung, Löschung, Einschränkung, Widerspruch, Datenübertragbarkeit)
  - Beschwerderecht bei der Datenschutzbehörde (DSB, Wien)
  - Cookies und Tracker einzeln aufgelistet (Name, Zweck, Speicherdauer, Anbieter)
  - Ob Bereitstellung der Daten gesetzlich/vertraglich erforderlich ist

**Fix pattern:** Create comprehensive Datenschutzerklärung covering every data processing activity. List every cookie/tracker individually. Link from footer + near every form.

---

#### AGB — Allgemeine Geschäftsbedingungen
> Required for e-commerce / paid services. Must be accessible before purchase.

**Check for:**
- AGB page exists (if selling products/services)
- Accessible before checkout / purchase flow
- Contains:
  - Geltungsbereich
  - Vertragsschluss (wann kommt der Vertrag zustande?)
  - Preise inkl. USt. + alle Nebenkosten
  - Zahlungsbedingungen + akzeptierte Zahlungsarten
  - Lieferbedingungen + Lieferfristen
  - Haftung + Gewährleistung
  - Streitbeilegung (OS-Plattform-Link für B2C: https://ec.europa.eu/consumers/odr)
- Checkbox or explicit acceptance before purchase (not just "by using this site...")

**Fix pattern:** Create AGB with all required sections. Add acceptance mechanism before purchase. Include OS-Plattform link.

---

#### Widerrufsbelehrung — FAGG §11-18 (B2C only)
> Consumers have 14-day right of withdrawal for distance contracts.

**Check for:**
- Widerrufsbelehrung exists (if B2C with paid services)
- 14-Tage-Rücktrittsrecht clearly stated
- Muster-Widerrufsformular provided (FAGG Anhang I Teil B)
- Contact address for Widerruf clearly stated
- Ausnahmen vom Widerrufsrecht listed (if applicable, §18 FAGG)
- Information provided BEFORE contract conclusion

**Fix pattern:** Add Widerrufsbelehrung with model withdrawal form. State 14-day period, exceptions, and return address clearly.

---

### Category 2: Cookie Consent & ePrivacy

#### Cookie Banner — ePrivacy + DSGVO
> Non-essential cookies require informed, freely given, specific opt-in consent.

**Check for:**
- Cookie consent banner exists
- Opt-in required for non-essential cookies (not pre-checked)
- Granular categories (Essentiell / Statistik / Marketing — separately toggleable)
- "Ablehnen" button equally prominent as "Akzeptieren" (no dark patterns)
- No tracking scripts fire before consent is given
- Consent is stored and respected across sessions
- Re-consent mechanism available (Cookie-Einstellungen link in footer)
- Banner doesn't block content entirely (still usable while deciding)

**Fix pattern:** Implement consent-first approach. Block all non-essential scripts until explicit opt-in. Equal prominence for accept/reject. Add footer link to change settings.

---

#### Third-Party Script Blocking
> No third-party tracking/analytics scripts may load before user consent.

**Check for in code:**
- Google Analytics / GA4 — loads before consent?
- Google Tag Manager — fires tags before consent?
- Google Fonts — loaded from Google servers? (data transfer to USA)
- Meta Pixel / Facebook SDK — loads before consent?
- PostHog / Hotjar / Mixpanel — loads before consent?
- YouTube / Vimeo embeds — load before consent? (use facade/click-to-load)
- Social media embeds (Twitter, Instagram) — load before consent?
- CDN-hosted libraries from US providers — necessary or self-hostable?

**Fix pattern:** Wrap all non-essential scripts in consent checks. Use GTM Consent Mode v2 or manual consent gating. Self-host Google Fonts. Use video facades (click to load).

---

#### Cookie Documentation
> Every cookie must be documented in the Datenschutzerklärung.

**Check for:**
- Each cookie listed by name in Datenschutzerklärung
- For each cookie: Name, Zweck, Anbieter, Speicherdauer, Typ (essential/statistics/marketing)
- Cookies actually set match what's documented (no undocumented cookies)
- Third-party cookies from embedded content documented

**Fix pattern:** Audit actual cookies set (DevTools → Application → Cookies). Document each one. Remove undocumented cookies or add documentation.

---

### Category 3: Formulare & Datenverarbeitung

#### Rechtsgrundlage pro Formular — Art. 6 DSGVO
> Every form that collects personal data needs a clear legal basis.

**Check for each form:**
- **Kontaktformular:** berechtigtes Interesse (Art. 6/1f) — no checkbox needed, but privacy link required
- **Newsletter-Anmeldung:** Einwilligung (Art. 6/1a) — explicit checkbox required + Double-Opt-In
- **Account-Erstellung:** Vertragserfüllung (Art. 6/1b) — privacy link required
- **Umfrage / Survey:** Einwilligung (Art. 6/1a) — checkbox or clear info before submission
- Privacy policy link visible near every form
- No pre-checked consent checkboxes
- Consent text is specific (not bundled with other agreements)

**Fix pattern:** Add appropriate consent mechanism per form type. Link to Datenschutzerklärung near every form. Newsletter = Double-Opt-In mandatory.

---

#### Newsletter — Double-Opt-In
> Newsletter subscriptions in Austria require Double-Opt-In (DOI).

**Check for:**
- DOI flow implemented (submit email → confirmation email → click link → subscribed)
- Confirmation email sent (not just "thanks, you're subscribed")
- Abmeldelink in every newsletter email
- Newsletter signup form has explicit consent checkbox
- Consent text references Datenschutzerklärung
- Subscriber list only contains confirmed opt-ins

**Fix pattern:** Implement full DOI flow. Add unsubscribe link to all emails. Store DOI timestamp as proof of consent.

---

#### Datenminimierung — Art. 5/1c DSGVO
> Collect only data that's strictly necessary for the stated purpose.

**Check for:**
- Forms collecting more data than needed (e.g., phone number for newsletter)
- Required fields that should be optional
- Fields without clear purpose (why do you need this?)
- Collecting personal data "just in case" or "for future use"

**Fix pattern:** Mark non-essential fields as optional. Remove fields without clear purpose. Only require what's needed for the stated Zweck.

---

### Category 4: Drittland-Transfers (Third-Country Transfers)

#### USA-Dienste — Schrems II / EU-US Data Privacy Framework
> Transferring personal data to the USA requires specific safeguards.

**Check for:**
- Google Analytics → USA transfer (self-host or use Matomo?)
- Google Fonts → USA transfer (self-host!)
- Google Tag Manager → USA transfer (consent-gated?)
- Cloudflare → check EU-only settings
- Supabase → server location? (EU region available)
- Vercel / Netlify → server location?
- Mailchimp / SendGrid → DPA + SCCs in place?
- Any other US-based SaaS receiving personal data

**For each US service, verify:**
- EU-US Data Privacy Framework (DPF) certification of the provider
- OR: Standard Contractual Clauses (SCCs) + Transfer Impact Assessment (TIA)
- Documented in Datenschutzerklärung with specific legal basis for transfer
- Consent obtained before transfer (if consent-based)

**Fix pattern:** Self-host where possible (fonts, analytics). Use EU-hosted alternatives. For necessary US services: verify DPF certification or implement SCCs. Document all transfers in Datenschutzerklärung.

---

#### Auftragsverarbeitungsverträge (AVV) — Art. 28 DSGVO
> A Data Processing Agreement must exist with every processor handling personal data.

**Check for AVVs with:**
- Hosting provider (Hetzner, AWS, Vercel, Netlify, etc.)
- Analytics provider (Google, PostHog, Matomo Cloud, etc.)
- Newsletter / email provider (Mailchimp, SendGrid, Brevo, etc.)
- Database provider (Supabase, PlanetScale, etc.)
- CDN provider (Cloudflare, Fastly, etc.)
- Payment processor (Stripe, Mollie, etc.)
- Any SaaS that processes user data on your behalf

**Fix pattern:** List all processors. Verify AVV/DPA exists for each. Most large providers offer standard DPAs — link to them in Datenschutzerklärung. Keep signed copies on file.

---

### Category 5: HTTPS & Security Headers

#### SSL/TLS — Art. 32 DSGVO
> Encryption in transit is a mandatory technical measure.

**Check for:**
- HTTPS active on all pages (no mixed content)
- HTTP → HTTPS redirect (301 permanent)
- Valid SSL certificate (not expired, correct domain)
- HSTS header set (`Strict-Transport-Security: max-age=31536000; includeSubDomains`)

**Fix pattern:** Enable HTTPS everywhere. Set up 301 redirect. Add HSTS header. Most hosts (Vercel, Netlify, Cloudflare) handle this automatically — verify it's active.

---

#### Security Headers
> Required/recommended headers for data protection compliance.

**Check for:**
- `Content-Security-Policy` — restricts script/resource sources
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY` or `SAMEORIGIN`
- `Referrer-Policy: strict-origin-when-cross-origin` (or stricter)
- `Permissions-Policy` — restricts browser features (camera, microphone, geolocation)

**Note:** For detailed security implementation, run `/security-audit`.

**Fix pattern:** Add security headers via hosting config, `_headers` file, or middleware. CSP should whitelist only necessary sources.

---

### Category 6: Verzeichnisse & Dokumentation

#### Verarbeitungsverzeichnis (VVT) — Art. 30 DSGVO
> A record of processing activities must be maintained (not on the website, but should be informed by what the website does).

**Check that the website's data processing is documentable:**
- All forms and their data fields are identifiable
- All third-party services and their data flows are traceable
- Cookie inventory matches actual cookies set
- Data retention periods are defined per data type
- Purpose limitation is clear for each processing activity

**Flag for manual review:**
- "Do you have a VVT (Verarbeitungsverzeichnis) that covers this website's data processing?"
- "Are deletion periods documented and implemented?"

---

#### Löschkonzept
> Personal data must be deleted when no longer needed.

**Check for:**
- Defined retention periods in Datenschutzerklärung
- Server logs: max 7-14 days recommended
- Contact form data: max 6 months after inquiry resolved
- Newsletter: immediate deletion upon unsubscribe
- Analytics data: anonymized or deleted after 14-26 months
- Account data: deleted upon account deletion request
- No "we keep everything forever" statements

**Fix pattern:** Define specific retention periods per data type in Datenschutzerklärung. Implement automated deletion where possible.

---

### Category 7: E-Commerce Specifics (if applicable)

#### Preisangaben — PAngV / ECG
> Prices must be transparent and complete.

**Check for:**
- All prices include USt. (Umsatzsteuer / MwSt.)
- "inkl. USt." or "inkl. 20% USt." clearly stated
- Versandkosten stated before checkout (or "zzgl. Versand: X €")
- No hidden costs that appear only at checkout
- Gesamtpreis visible before purchase confirmation

**Fix pattern:** Show prices as "XX,XX € inkl. USt." Add shipping info upfront. No surprise costs at checkout.

---

#### Bestellprozess — ECG §9-10
> The ordering process must meet specific information requirements.

**Check for:**
- Technical steps to contract conclusion explained
- Order correction possible before final submission
- "Zahlungspflichtig bestellen" or equivalent clear button text (not just "Weiter")
- Order confirmation sent by email
- AGB + Widerrufsbelehrung accessible before purchase

**Fix pattern:** Add clear "zahlungspflichtig bestellen" button. Implement order summary with correction option. Send confirmation email.

---

#### Streitbeilegung — ODR-Verordnung
> B2C websites must link to the EU Online Dispute Resolution platform.

**Check for:**
- Link to https://ec.europa.eu/consumers/odr present (in AGB or Impressum)
- Statement about willingness/unwillingness to participate in Streitbeilegungsverfahren

**Fix pattern:** Add ODR link + statement to AGB or Impressum.

---

### Category 8: Barrierefreiheit — BaFG / Web-Zugänglichkeits-Gesetz

#### Legal Accessibility Requirements
> The Barrierefreiheitsgesetz (BaFG) implements the European Accessibility Act. Deadlines are approaching for commercial websites.

**Check for:**
- Awareness: is the team aware of BaFG deadlines? (28. Juni 2025 for new products/services)
- Barrierefreiheitserklärung (accessibility statement) — required for public sector, recommended for private
- Basic compliance indicators (contrast, alt texts, keyboard nav, semantic HTML)

**Note:** For full WCAG 2.2 Level AA compliance, run `/a11y-audit`. This category only flags the legal requirement.

**Fix pattern:** Add Barrierefreiheitserklärung if required. Run `/a11y-audit` for comprehensive technical check. Plan for BaFG compliance timeline.

---

## Step 2: Report findings

Present findings grouped by severity:

```
## Legal Audit Results — Österreich

### 🔴 Critical — legal violation, Abmahnung/fine risk
| Issue | Legal Basis | File / Location | Required Fix |
|-------|------------|-----------------|--------------|
| ... | ... | ... | ... |

### 🟠 Major — incomplete compliance
| Issue | Legal Basis | File / Location | Required Fix |
|-------|------------|-----------------|--------------|
| ... | ... | ... | ... |

### 🟡 Minor — best practice, recommended
| Issue | Legal Basis | File / Location | Required Fix |
|-------|------------|-----------------|--------------|
| ... | ... | ... | ... |

### 📋 Manual Review Required
- [ ] AVV/DPA with [provider] — verify signed agreement exists
- [ ] VVT (Verarbeitungsverzeichnis) — verify it covers this website
- [ ] Löschkonzept — verify automated deletion is implemented
- [ ] [other items requiring offline verification]

### ✅ Compliant
- [list what's already legally sound]
```

Ask the user: **"Soll ich die technischen Issues fixen? (Pflichtseiten-Inhalte und AVVs müssen manuell/rechtlich geprüft werden.)"**

---

## Step 3: Fix issues

Apply fixes directly in the codebase. For each fix:
- Reference the specific legal basis (Art./§)
- Only fix technical implementation — never draft legal text without flagging it for lawyer review
- Prioritize: (1) consent blocking, (2) missing page links, (3) form compliance, (4) security headers
- Never break existing functionality
- Follow the project's existing code style and design system

**What this skill CAN fix technically:**
- Cookie consent implementation (blocking scripts before consent)
- Missing footer links (Impressum, Datenschutz, AGB)
- Privacy links near forms
- HTTPS redirects and security headers
- Google Fonts self-hosting
- Newsletter Double-Opt-In flow
- Consent checkboxes on forms
- Script loading order (consent-gated)

**What this skill CANNOT fix (flag for manual/legal review):**
- Legal page content (Impressum details, Datenschutzerklärung text, AGB clauses)
- AVV/DPA agreements with third parties
- VVT (Verarbeitungsverzeichnis) creation
- Tax and pricing compliance
- Widerrufsbelehrung text

---

## Step 4: Summary

```
Legal Audit Complete — Österreich

✅ [N] technical issues fixed
📋 [N] items flagged for manual/legal review
⚠️ [N] items need lawyer sign-off

Legal bases checked:
- DSGVO (Art. 5, 6, 7, 12-14, 28, 30, 32)
- ECG §5 (Impressum)
- MedienG §24a
- FAGG §11-18 (Widerruf)
- TKG 2021 (ePrivacy/Cookies)
- BaFG (Barrierefreiheit)

Top 3 highest-priority fixes:
1. [fix] — [legal basis, risk level]
2. [fix] — [legal basis, risk level]
3. [fix] — [legal basis, risk level]

Recommended next steps:
- Have a lawyer review Impressum, Datenschutzerklärung, AGB text
- Verify AVVs exist with all data processors
- Create/update Verarbeitungsverzeichnis (VVT)
- Test cookie consent flow end-to-end (DevTools → verify no pre-consent cookies)
- Run `/a11y-audit` for full WCAG compliance
- Run `/security-audit` for code-level security
- Schedule annual legal compliance review
```

---

## Rules

- **Audit legal compliance**, not code quality, UX, or visual design
- **Austrian law first** — reference ECG, FAGG, DSG, MedienG, not German TMG/TTDSG
- **Never draft legal text** — flag content for lawyer review, only fix technical implementation
- Reference specific legal articles (Art. X DSGVO, §Y ECG) for every finding
- Clearly separate what you CAN fix (technical) from what needs MANUAL review (legal content)
- Don't duplicate `/a11y-audit` — reference it for WCAG, only flag the legal requirement here
- Don't duplicate `/security-audit` — reference it for code security, only check legally required headers here
- Err on the side of caution — if unsure whether something is required, flag it as 🟠 Major
- **Never recommend removing legally required elements** for aesthetic or UX reasons
- Follow the project's existing code style and component patterns
