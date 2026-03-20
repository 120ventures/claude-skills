---
name: venture-learnings
description: Use when a venture is being shut down or paused and the user wants a structured learnings document for future ventures. Triggered by requests like "Learnings erstellen", "was haben wir gelernt", "Venture einstellen", "kill the venture", "post-mortem", "shutdown learnings".
---

# Venture Learnings

Generate a branded PDF documenting what worked, what didn't, market insights, technical learnings, and recommendations for future ventures. Pulls real data from all available sources.

## Prerequisites

- **Supabase:** Project must have an admin dashboard with a `dashboard-stats` Edge Function
- **Meta Marketing API** (optional): `META_ACCESS_TOKEN` + `META_AD_ACCOUNT_ID` in `~/.claude/.env`
- **Google Analytics** (optional): Accessible via browser
- **Google Ads** (optional): Accessible via browser
- **PostHog** (optional): Accessible via browser
- **Fonts:** Symlinked from `~/.claude/skills/analyst-report/fonts/`
- **Python:** `reportlab` package installed

## Workflow

### Phase 1: Context & Configuration

1. **Read CLAUDE.md** from the current project to extract:
   - Venture name, URL, hosting, backend
   - Brand colors (CSS custom properties)
   - Tech stack details
   - Any funnel/survey structure

2. **Ask the user 3-4 questions:**
   - "Welcher Zeitraum?" (default: gesamte Laufzeit)
   - "Welche Datenquellen sind verfügbar?" (Supabase, Meta, GA4, Google Ads, PostHog)
   - "Grund für die Einstellung?" (kurzer Satz — wird in Kern-Erkenntnis eingebaut)
   - "Gibt es spezifische Learnings die du festhalten willst?"

3. **Determine venture name** for campaign filtering:
   - Extract from CLAUDE.md or project directory
   - Meta campaign convention: `yymm_venture` or `yymm_venture_#nr details`

### Phase 2: Data Collection (automated, parallel where possible)

#### Supabase Data (required)
1. Open admin dashboard in browser (browser automation)
2. Get JWT from localStorage (`sb-{ref}-auth-token`)
3. Call `dashboard-stats` Edge Function via JavaScript
4. Extract: sessions, surveys, completions, signups, carts, checkouts, survey responses, session analytics

#### Meta Marketing API (if configured)
1. Read credentials from `~/.claude/.env`
2. Fetch campaigns filtered by venture name:
   ```
   GET /v21.0/act_{id}/campaigns?fields=name,status,objective
   ```
3. For matching campaigns, fetch ad-level insights:
   ```
   GET /v21.0/{campaign_id}/insights?level=ad&fields=ad_name,impressions,reach,clicks,spend,actions,cost_per_action_type,frequency&date_preset=maximum
   ```
4. Extract: LPV, CPR, Impressions, Reach, Spend per ad

#### Google Analytics (if available)
1. Open GA4 property in browser
2. Extract via JavaScript or page scraping:
   - Traffic sources breakdown
   - Channel groupings with session counts
   - Geo distribution
   - Bounce rate / engagement rate
   - Top landing pages

#### Google Ads (if available)
1. Open Google Ads dashboard in browser
2. Extract:
   - Campaign performance (clicks, impressions, CPC, conversions, ROAS)
   - Ad group level data
   - Search terms report (if Search campaigns)

#### PostHog (if available)
1. Open PostHog dashboard in browser
2. Extract:
   - Event counts and trends
   - Funnel conversion rates
   - Retention cohorts
   - Feature flag usage
   - Session recordings summary (count, avg duration)

### Phase 3: Analysis & Interpretation

Before generating the PDF, analyze ALL collected data and produce:

1. **Kern-Erkenntnis:** One sentence that captures the fundamental learning (e.g., "Interesse war da, Zahlungsbereitschaft nicht")
2. **Was funktioniert hat:** Identify 3-5 things that worked well, with data to back them up
3. **Was nicht funktioniert hat:** Identify 3-5 things that failed, with specific numbers showing where/why
4. **Markt-Insights:** Aggregate survey/user data into actionable market understanding
5. **Technische Learnings:** Stack evaluation, what to keep, what to change
6. **Empfehlungen:** Prioritized by timeline (Quick Wins / Mittelfristig / Strategisch)
7. **Benchmarks:** Key metrics as reference for future ventures

### Phase 4: PDF Generation

1. **Map brand colors** from CLAUDE.md to Terracotta Precision palette:
   - `bg`: warm off-white `#f4f1ec`
   - `fg`: project's primary/dark color
   - `accent`: project's signal/accent color
   - `muted`: warm gray derived from fg
   - `border`: `#dbd6ce`
   - `clay`: `#ece7df`

2. **Build JSON data file** with all sections (see generate_learnings.py for schema)

3. **Run generate_learnings.py:**
   ```bash
   python3 ~/.claude/skills/venture-learnings/generate_learnings.py \
     /tmp/{venture}_learnings_data.json \
     ~/Desktop/{venture}_venture_learnings.pdf
   ```

4. **Open the PDF** for the user.

### JSON Data Schema

```json
{
  "venture": "venture-name",
  "date": "YYYY-MM-DD",
  "period": "Monat YYYY – Monat YYYY",
  "colors": { "bg", "fg", "accent", "muted", "border", "clay" },
  "title": "Venture Learnings",
  "subtitle": "One-line venture description",
  "summary_line": "~N Monate Betrieb · ~X € Ad Spend · Y Sessions · Z Käufe",
  "sections": [
    {
      "num": 1,
      "title": "Section Title",
      "blocks": [
        {
          "subtitle": "Block Title",
          "callout": "Optional highlighted text",
          "bullets": ["bullet 1", "bullet 2"],
          "takeaway": "Optional → takeaway text",
          "table_headers": ["Col1", "Col2"],
          "table_rows": [["val1", "val2"]]
        }
      ]
    }
  ]
}
```

### Standard Sections

Always include these sections (adapt content based on available data):

| # | Section | Content |
|---|---------|---------|
| 1 | Was funktioniert hat | 3-5 successes with data, each with takeaway for next venture |
| 2 | Was nicht funktioniert hat | 3-5 failures with specific drop-off numbers, each with takeaway |
| 3 | Markt-Insights | Survey aggregations, user demographics, demand signals |
| 4 | Technische Learnings | Stack evaluation table, what to keep/change |
| 5 | Empfehlungen fürs nächste Venture | Domain-specific + generelle D2C-Learnings + Benchmarks |
| 6 | Daten-Assets die bleiben | What data/code/insights carry forward |

Omit Section 3 if no survey/user data exists. All other sections are always included.

## Important Notes

- **Read-only:** Never modify data in any source system
- **Language:** Report content in German (Austrian), code/technical terms in English
- **Tone:** Sachlich, analytisch, handlungsorientiert — kein Hype, kein Blame
- **Privacy:** Never include raw email addresses or personal data
- **Numbers:** Double-check all percentages against raw data before generating PDF
- **Venture filtering:** For Meta campaigns, filter case-insensitively by venture name using 120V naming convention (`yymm_venture`)
- **Design:** Follow Terracotta Precision philosophy — see `references/report-philosophy.md`
