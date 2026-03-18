---
name: analyst-report
description: Generate a structured PDF analyst report (Nutzerverhalten-Analyse) for any 120 Ventures project — pulls data from Supabase dashboard + Meta Marketing API, analyzes traffic, campaigns, funnel, user profiles, and generates actionable recommendations.
---

# Analyst Report — Nutzerverhalten-Analyse

Generate a professional, data-driven PDF report for any 120 Ventures venture. Pulls real data from Supabase and Meta Marketing API, analyzes it, and produces a branded PDF with interpretation and recommendations.

## Prerequisites

- **Supabase:** Project must have an admin dashboard with a `dashboard-stats` Edge Function
- **Meta Marketing API:** Token + Ad Account ID configured in `~/.claude/.env`
  - `META_ACCESS_TOKEN` — System User Token with `ads_read` permission
  - `META_AD_ACCOUNT_ID` — Format: `act_123456789`
- **Fonts:** Cormorant Garamond + Inter in `~/.claude/skills/analyst-report/fonts/`
- **Python:** `reportlab` package installed (`pip3 install reportlab`)

## Workflow

### Phase 1: Context & Configuration (ask user)

1. **Read CLAUDE.md** from the current project to extract:
   - Project/venture name
   - Brand colors (CSS custom properties)
   - Font families
   - Any survey structure or funnel info

2. **Ask the user 2-3 questions:**
   - "Welcher Zeitraum?" (default: last 30 days)
   - "Fokus?" (Gesamtanalyse / nur Traffic / nur Funnel / nur Ads)
   - "Meta-Ads einbeziehen?" (ja/nein — default: ja)

3. **Determine venture name** for Meta campaign filtering:
   - Extract from project directory name or CLAUDE.md
   - Campaign naming convention: `yymm_venture` or `yymm_venture_#nr details`
   - Filter campaigns case-insensitively by venture name in campaign name

### Phase 2: Data Collection (automated)

#### Supabase Data
1. Open the admin dashboard in the browser (browser automation)
2. Get the authenticated user's JWT from localStorage
3. Call the `dashboard-stats` Edge Function via JavaScript
4. Extract the full JSON response containing:
   - Stats (sessions, surveys, completions, signups)
   - Session analytics (by date, country, device, browser, UTM source)
   - Survey responses (raw data for aggregation)
   - Funnel data (screen-by-screen conversion)
   - Event counts
   - Exit intent data

#### Meta Marketing API Data
1. Read credentials from `~/.claude/.env`
2. Fetch campaigns filtered by venture name:
   ```
   GET /v21.0/act_{id}/campaigns?fields=name,status,objective
   ```
3. For matching campaigns, fetch ad-level insights:
   ```
   GET /v21.0/{campaign_id}/insights?level=ad&fields=ad_name,impressions,reach,clicks,spend,actions,cost_per_action_type,frequency&date_preset=last_30d
   ```
4. Extract key metrics per ad:
   - Ad name, status
   - Landing Page Views (LPV) from `actions` where `action_type=landing_page_view`
   - Cost per Result (CPR) from `cost_per_action_type`
   - Impressions, Reach, Frequency, Unique Link Clicks, Spend

### Phase 3: Analysis & Interpretation

Before generating the PDF, analyze the data and produce insights:

1. **Traffic analysis:** Trends, peaks, channel mix, geo distribution, device split
2. **Campaign analysis:** Best/worst performing ads, CPR comparison, creative patterns
3. **Funnel analysis:** Drop-off points, conversion rates per step, critical leaks
4. **User profile:** Demographics aggregation, behavioral patterns
5. **Recommendations:** Prioritized by impact (Quick Wins → Mittelfristig → Strategisch)

### Phase 4: PDF Generation

1. **Read brand tokens** from CLAUDE.md:
   - Map CSS custom properties to PDF colors
   - Identify heading font (typically serif) and body font (typically sans-serif)
   - Fall back to Cormorant Garamond + Inter if not specified

2. **Run generate_report.py** with the collected data:
   - Pass data as JSON via stdin or temp file
   - Brand colors, fonts, venture name as arguments
   - Output path: `~/Desktop/{venture}_nutzerverhalten_analyse_{date}.pdf`

3. **Report sections** (include/exclude based on available data):

   | Section | Condition |
   |---------|-----------|
   | Executive Summary | Always |
   | Traffic & Akquise | Always (from Supabase sessions) |
   | Meta-Kampagnen-Performance | Only if Meta ads data available |
   | Survey Funnel | Only if survey responses exist |
   | Nutzerprofil | Only if survey demographics exist |
   | Bedürfnisse & Motivation | Only if survey desire/trigger data exists |
   | Interpretation | Always |
   | Handlungsempfehlungen | Always |

4. **Open the PDF** for the user after generation.

## Report Design Philosophy

Follow the "Terracotta Precision" design philosophy from `references/report-philosophy.md`:
- Clean, data-driven layout with generous white space
- Brand colors used sparingly — accent color for section numbers, KPIs, chart bars
- Cormorant Garamond (or project serif) for headings, Inter (or project sans) for body
- Tables: thin hairlines, no alternating row fills, right-aligned numbers
- Callout boxes for key insights (clay background + accent left bar)
- Funnel visualization as horizontal bars with drop-off indicators

## Important Notes

- **Read-only:** This skill never modifies data in Supabase or Meta
- **Campaign filtering:** Always filter by venture name using the 120V naming convention (`yymm_venture`)
- **Language:** Report content in German (Austrian), code discussion in English
- **Tone:** Sachlich, analytisch, handlungsorientiert — no hype, no fluff
- **Privacy:** Never include raw email addresses or personal data in reports
- **No pricing screens:** Only include survey screens that actually exist in the project
