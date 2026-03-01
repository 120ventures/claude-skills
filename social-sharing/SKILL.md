---
name: social-sharing
description: Generate OG preview image, favicon, meta tags, and all social sharing assets for a project based on its brand guidelines
argument-hint: [project-name or page]
---

# Social Sharing Setup

Generate all social sharing assets for `$ARGUMENTS` — OG image, favicon, meta tags, Twitter cards, and structured data.

## Step 0: Check what's missing FIRST

Before generating anything, scan the project for what already exists and what's missing:

```
Scanning for social sharing setup...

- [ ] OG preview image (1200x630) — exists at public/og-preview.png?
- [ ] Favicon SVG — exists at public/favicon.svg?
- [ ] Apple touch icon — exists at public/apple-touch-icon.png?
- [ ] og:title, og:description, og:image in index.html?
- [ ] og:image:width + og:image:height set?
- [ ] twitter:card, twitter:title, twitter:image in index.html?
- [ ] theme-color meta tag?
- [ ] canonical URL?
- [ ] JSON-LD structured data?
- [ ] site.webmanifest?

Missing: [list what's not there]
```

Only generate what's missing. Don't duplicate existing work.

---

## 1. OG Preview Image

Create a static HTML file at `public/og-preview.html` that can be screenshotted to produce the image.

### Dimensions & Specs
- **Exactly 1200 x 630px** — this is non-negotiable
- Padding: minimum 60px on all sides
- File format: PNG (not JPEG, not WebP — maximum compatibility)
- File size: under 1MB
- File location: `public/og-preview.png`

### Design Rules
- Background: brand primary color or gradient
- Logo: present but not dominant
- Headline: 36–48px, bold, brand font — max 2 lines
- Description: 18–24px, regular — max 2 lines
- **Never below 14px** for any text
- High contrast (WCAG AA)
- Must look good at thumbnail size (WhatsApp, Slack, LinkedIn previews are tiny)
- No stock photos, no generic AI aesthetics

### Screenshot command
```bash
npx playwright screenshot --viewport-size=1200,630 public/og-preview.html public/og-preview.png
```

---

## 2. Favicon

- Create `public/favicon.svg` — brand mark in SVG, crisp at all sizes
- If text-only brand: use first letter/initials + brand accent color
- Add to `index.html`:
```html
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
<link rel="alternate icon" href="/favicon.ico" />
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
```

---

## 3. Meta Tags

Add to `index.html` `<head>`:

```html
<!-- Primary -->
<title>{Brand} — {Tagline}</title>
<meta name="description" content="{max 155 chars}" />
<meta name="author" content="{Brand}" />
<meta name="theme-color" content="{brand bg color}" />
<meta name="robots" content="index, follow" />
<link rel="canonical" href="{production URL}/" />

<!-- Open Graph (Facebook, LinkedIn, WhatsApp) -->
<meta property="og:type" content="website" />
<meta property="og:url" content="{production URL}/" />
<meta property="og:title" content="{Brand} — {Tagline}" />
<meta property="og:description" content="{1-2 sentences}" />
<meta property="og:image" content="{production URL}/og-preview.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:type" content="image/png" />
<meta property="og:locale" content="{de_AT or en_US}" />

<!-- Twitter / X -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{Brand} — {Tagline}" />
<meta name="twitter:description" content="{1-2 sentences}" />
<meta name="twitter:image" content="{production URL}/og-preview.png" />
<meta name="twitter:image:alt" content="{describe the image}" />
```

### Common mistakes to avoid:
- `og:image` must be an **absolute URL** (https://...), not a relative path
- `og:image:width` and `og:image:height` must be set — without them some platforms won't show the preview
- Description over 155 chars gets cut off in Google
- Title over 60 chars gets cut off in Google
- Missing `og:image:type` — some crawlers need it

---

## 4. JSON-LD Structured Data

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "{Brand}",
  "url": "{production URL}",
  "description": "{description}",
  "inLanguage": "{de-DE or en-US}"
}
</script>
```

Add Organization schema if company info is available (name, logo, contact).
Add FAQPage schema if the page has an FAQ section.

---

## 5. Web App Manifest

Create `public/site.webmanifest`:

```json
{
  "name": "{Brand — Full Name}",
  "short_name": "{Brand}",
  "description": "{description}",
  "start_url": "/",
  "display": "standalone",
  "background_color": "{brand bg color}",
  "theme_color": "{brand primary color}",
  "icons": [
    { "src": "/favicon.svg", "type": "image/svg+xml", "sizes": "any" },
    { "src": "/apple-touch-icon.png", "sizes": "180x180", "type": "image/png" }
  ]
}
```

Add to `index.html`: `<link rel="manifest" href="/site.webmanifest" />`

---

## After setup — validate

Tell the user to test with:
- **https://www.opengraph.xyz** — paste the production URL, check preview
- **LinkedIn Post Inspector** — https://www.linkedin.com/post-inspector/
- **Google Rich Results Test** — check JSON-LD

## Rules

- Read the project's brand guidelines (CLAUDE.md, design system, index.css) before generating anything
- Use brand colors, fonts, and tone — never generic
- OG image is always **1200x630px PNG** — no exceptions
- All URLs in meta tags must be absolute (https://...)
- `og:image:width` + `og:image:height` are always required
- Locale: `de_AT` for DACH projects, `en_US` for English projects
- Don't create a React component for the OG image — just the static HTML version
