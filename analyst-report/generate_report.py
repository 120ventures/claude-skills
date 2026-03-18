#!/usr/bin/env python3
"""
Generate a branded PDF analyst report for any 120 Ventures project.

Usage:
    python3 generate_report.py --data report_data.json --output ~/Desktop/report.pdf

The JSON data file should contain:
{
  "venture": "attuned",
  "date": "2026-03-18",
  "period": "Letzte 30 Tage",
  "colors": { "bg": "#f4f1ec", "fg": "#0d0c0a", "accent": "#c05c45", "muted": "#4f4a42", "border": "#dbd6ce", "clay": "#ece7df" },
  "stats": { ... },
  "sessionAnalytics": { ... },
  "funnel": [ ... ],
  "surveyAggregation": { ... },
  "metaAds": [ ... ],
  "metaInterpretation": "...",
  "interpretation": { ... },
  "recommendations": { ... }
}
"""

import json
import sys
import os
import textwrap
import argparse

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Constants
W, H = A4
MARGIN_LEFT = 45
MARGIN_RIGHT = 45
MARGIN_TOP = 50
MARGIN_BOTTOM = 50
CONTENT_W = W - MARGIN_LEFT - MARGIN_RIGHT
WHITE = HexColor('#ffffff')

FONTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')


def register_fonts():
    """Register Cormorant Garamond and Inter fonts."""
    pdfmetrics.registerFont(TTFont('Cormorant-Light', os.path.join(FONTS_DIR, 'CormorantGaramond-Light.ttf')))
    pdfmetrics.registerFont(TTFont('Cormorant-SemiBold', os.path.join(FONTS_DIR, 'CormorantGaramond-SemiBold.ttf')))
    pdfmetrics.registerFont(TTFont('Cormorant-Bold', os.path.join(FONTS_DIR, 'CormorantGaramond-Bold.ttf')))
    pdfmetrics.registerFont(TTFont('Inter', os.path.join(FONTS_DIR, 'Inter-Regular.ttf')))


class ReportPDF:
    def __init__(self, output_path, data):
        self.data = data
        self.c = canvas.Canvas(output_path, pagesize=A4)
        self.c.setTitle(f'{data["venture"]} — Nutzerverhalten-Analyse')
        self.c.setAuthor('120 Ventures')
        self.y = H - MARGIN_TOP
        self.page_num = 0

        # Colors from data
        colors = data.get('colors', {})
        self.BG = HexColor(colors.get('bg', '#f4f1ec'))
        self.FG = HexColor(colors.get('fg', '#0d0c0a'))
        self.ACCENT = HexColor(colors.get('accent', '#c05c45'))
        self.MUTED = HexColor(colors.get('muted', '#4f4a42'))
        self.BORDER = HexColor(colors.get('border', '#dbd6ce'))
        self.CLAY = HexColor(colors.get('clay', '#ece7df'))

    def new_page(self):
        if self.page_num > 0:
            self._draw_footer()
            self.c.showPage()
        self.page_num += 1
        self.y = H - MARGIN_TOP
        self.c.setFillColor(self.BG)
        self.c.rect(0, 0, W, H, fill=1, stroke=0)

    def _draw_footer(self):
        self.c.setFont('Inter', 7)
        self.c.setFillColor(self.MUTED)
        venture = self.data['venture']
        date = self.data['date']
        self.c.drawString(MARGIN_LEFT, 25, f'{venture} · Nutzerverhalten-Analyse · {date} · Vertraulich')
        self.c.drawRightString(W - MARGIN_RIGHT, 25, f'{self.page_num}')

    def check_space(self, needed):
        if self.y - needed < MARGIN_BOTTOM + 30:
            self._draw_footer()
            self.c.showPage()
            self.page_num += 1
            self.y = H - MARGIN_TOP
            self.c.setFillColor(self.BG)
            self.c.rect(0, 0, W, H, fill=1, stroke=0)

    # ── Drawing primitives ──

    def section_header(self, num, title):
        self.check_space(50)
        self.y -= 10
        self.c.setFont('Cormorant-SemiBold', 11)
        self.c.setFillColor(self.ACCENT)
        self.c.drawString(MARGIN_LEFT, self.y, f'{num:02d}')
        self.c.setStrokeColor(self.ACCENT)
        self.c.setLineWidth(0.5)
        self.c.line(MARGIN_LEFT + 20, self.y + 5, MARGIN_LEFT + 50, self.y + 5)
        self.y -= 25
        self.c.setFont('Cormorant-SemiBold', 22)
        self.c.setFillColor(self.FG)
        self.c.drawString(MARGIN_LEFT, self.y, title)
        self.y -= 28

    def subsection_title(self, title):
        self.check_space(35)
        self.y -= 8
        self.c.setFont('Cormorant-SemiBold', 14)
        self.c.setFillColor(self.FG)
        self.c.drawString(MARGIN_LEFT, self.y, title)
        self.y -= 18

    def body_text(self, text, indent=0):
        self.c.setFont('Inter', 9)
        self.c.setFillColor(self.MUTED)
        max_chars = int((CONTENT_W - indent) / 4.2)
        lines = textwrap.wrap(text, width=max_chars)
        for line in lines:
            self.check_space(14)
            self.c.drawString(MARGIN_LEFT + indent, self.y, line)
            self.y -= 13
        self.y -= 3

    def bullet(self, text, indent=10):
        self.check_space(14)
        self.c.setFont('Inter', 9)
        self.c.setFillColor(self.MUTED)
        self.c.drawString(MARGIN_LEFT + indent, self.y, '·')
        max_chars = int((CONTENT_W - indent - 12) / 4.2)
        lines = textwrap.wrap(text, width=max_chars)
        for i, line in enumerate(lines):
            if i > 0:
                self.check_space(14)
            self.c.drawString(MARGIN_LEFT + indent + 12, self.y, line)
            self.y -= 13

    def kpi_row(self, metrics):
        self.check_space(55)
        col_w = CONTENT_W / len(metrics)
        for i, (val, label, sub) in enumerate(metrics):
            x = MARGIN_LEFT + i * col_w
            self.c.setFont('Cormorant-SemiBold', 24)
            self.c.setFillColor(self.ACCENT)
            self.c.drawString(x, self.y, str(val))
            self.c.setFont('Inter', 8.5)
            self.c.setFillColor(self.FG)
            self.c.drawString(x, self.y - 17, label)
            if sub:
                self.c.setFont('Inter', 7)
                self.c.setFillColor(self.MUTED)
                self.c.drawString(x, self.y - 28, sub)
        self.y -= 50

    def table(self, headers, rows, col_widths=None, highlight_col=None):
        num_cols = len(headers)
        if col_widths is None:
            col_widths = [CONTENT_W / num_cols] * num_cols

        self.check_space(20 + len(rows) * 17)

        x = MARGIN_LEFT
        self.c.setFont('Inter', 7.5)
        self.c.setFillColor(self.MUTED)
        for i, h in enumerate(headers):
            if i == 0:
                self.c.drawString(x + 2, self.y, h)
            else:
                self.c.drawRightString(x + col_widths[i] - 2, self.y, h)
            x += col_widths[i]

        self.y -= 6
        self.c.setStrokeColor(self.BORDER)
        self.c.setLineWidth(0.5)
        self.c.line(MARGIN_LEFT, self.y, MARGIN_LEFT + sum(col_widths), self.y)
        self.y -= 13

        for row in rows:
            self.check_space(17)
            x = MARGIN_LEFT
            for i, cell in enumerate(row):
                if i == 0:
                    self.c.setFont('Inter', 8.5)
                    self.c.setFillColor(self.FG)
                    self.c.drawString(x + 2, self.y, str(cell))
                else:
                    self.c.setFont('Inter', 8.5)
                    if highlight_col and i == highlight_col:
                        self.c.setFillColor(self.ACCENT)
                    else:
                        self.c.setFillColor(self.MUTED)
                    self.c.drawRightString(x + col_widths[i] - 2, self.y, str(cell))
                x += col_widths[i]
            self.y -= 16
        self.y -= 5

    def funnel_chart(self, steps):
        self.check_space(100)
        max_count = steps[0]['count'] if steps else 1
        bar_max_w = CONTENT_W - 120

        for step in steps:
            self.check_space(28)
            self.c.setFont('Inter', 7.5)
            self.c.setFillColor(self.MUTED)
            self.c.drawString(MARGIN_LEFT, self.y + 2, f'S{step["screen"]}')

            bar_w = (step['count'] / max_count) * bar_max_w if max_count > 0 else 0
            bar_x = MARGIN_LEFT + 22

            self.c.setFillColor(self.BORDER)
            self.c.roundRect(bar_x, self.y - 3, bar_max_w, 14, 2, fill=1, stroke=0)

            if bar_w > 0:
                self.c.setFillColor(self.ACCENT)
                self.c.roundRect(bar_x, self.y - 3, bar_w, 14, 2, fill=1, stroke=0)

            self.c.setFont('Inter', 7.5)
            pct = step.get('pct', '')
            count = step['count']
            self.c.setFillColor(WHITE if bar_w > 60 else self.FG)
            text_x = bar_x + min(bar_w - 5, bar_max_w - 80) if bar_w > 60 else bar_x + bar_w + 5
            self.c.drawString(text_x, self.y, f'{count} ({pct})')

            self.c.setFont('Inter', 7)
            self.c.setFillColor(self.MUTED)
            self.c.drawRightString(MARGIN_LEFT + CONTENT_W, self.y, step.get('label', ''))

            drop = step.get('dropoff', '')
            if drop and drop != '—':
                self.c.setFont('Inter', 6.5)
                self.c.setFillColor(self.ACCENT)
                self.c.drawRightString(MARGIN_LEFT + CONTENT_W - 90, self.y, f'↓ {drop}')

            self.y -= 22
        self.y -= 5

    def horizontal_bar(self, items, max_val=None):
        if max_val is None:
            max_val = max(v for _, v in items) if items else 1
        bar_max_w = CONTENT_W - 140

        for label, val in items:
            self.check_space(22)
            self.c.setFont('Inter', 8)
            self.c.setFillColor(self.FG)
            display_label = label if len(label) <= 35 else label[:33] + '…'
            self.c.drawString(MARGIN_LEFT, self.y, display_label)

            bar_w = (val / max_val) * bar_max_w if max_val > 0 else 0
            bar_x = MARGIN_LEFT + 5
            self.y -= 12
            self.c.setFillColor(self.ACCENT)
            self.c.roundRect(bar_x, self.y, max(bar_w, 2), 9, 1.5, fill=1, stroke=0)

            self.c.setFont('Inter', 7.5)
            self.c.setFillColor(self.MUTED)
            self.c.drawString(bar_x + bar_w + 5, self.y + 1, str(val))
            self.y -= 10
        self.y -= 5

    def callout_box(self, text):
        self.check_space(50)
        lines = textwrap.wrap(text, width=90)
        box_h = len(lines) * 13 + 16

        self.c.setFillColor(self.CLAY)
        self.c.roundRect(MARGIN_LEFT, self.y - box_h + 10, CONTENT_W, box_h, 3, fill=1, stroke=0)

        self.c.setFillColor(self.ACCENT)
        self.c.rect(MARGIN_LEFT, self.y - box_h + 10, 3, box_h, fill=1, stroke=0)

        self.c.setFont('Inter', 8.5)
        self.c.setFillColor(self.FG)
        for line in lines:
            self.c.drawString(MARGIN_LEFT + 14, self.y - 2, line)
            self.y -= 13
        self.y -= 10

    def labeled_item(self, letter, title):
        self.check_space(20)
        self.c.setFont('Cormorant-SemiBold', 11)
        self.c.setFillColor(self.ACCENT)
        self.c.drawString(MARGIN_LEFT, self.y, letter)
        self.c.setFont('Inter', 9.5)
        self.c.setFillColor(self.FG)
        self.c.drawString(MARGIN_LEFT + 18, self.y, title)
        self.y -= 16

    def spacer(self, h=10):
        self.y -= h

    # ── Page builders ──

    def title_page(self):
        self.new_page()
        venture = self.data['venture']
        date = self.data['date']
        period = self.data.get('period', 'Letzte 30 Tage')

        self.c.setStrokeColor(self.ACCENT)
        self.c.setLineWidth(2)
        self.c.line(MARGIN_LEFT, H - 35, W - MARGIN_RIGHT, H - 35)

        self.y = H - 90
        self.c.setFont('Cormorant-Bold', 16)
        self.c.setFillColor(self.FG)
        self.c.drawString(MARGIN_LEFT, self.y, venture)
        dot_x = MARGIN_LEFT + self.c.stringWidth(venture, 'Cormorant-Bold', 16)
        self.c.setFillColor(self.ACCENT)
        self.c.drawString(dot_x, self.y, '.')

        self.y -= 120
        self.c.setFont('Cormorant-Light', 38)
        self.c.setFillColor(self.FG)
        self.c.drawString(MARGIN_LEFT, self.y, 'Nutzerverhalten-')
        self.y -= 48
        self.c.drawString(MARGIN_LEFT, self.y, 'Analyse')

        self.y -= 40
        self.c.setFont('Inter', 10)
        self.c.setFillColor(self.MUTED)
        self.c.drawString(MARGIN_LEFT, self.y, f'Datenbasierte Analyse · Stand {date}')

        self.y -= 25
        self.c.setStrokeColor(self.ACCENT)
        self.c.setLineWidth(0.5)
        self.c.line(MARGIN_LEFT, self.y, MARGIN_LEFT + 80, self.y)

        # KPI preview
        stats = self.data.get('stats', {})
        self.y -= 70
        metrics = [
            (str(stats.get('totalSessions', '—')), 'Sessions'),
            (f'{self._pct(stats.get("totalSurveys", 0), stats.get("totalSessions", 1))}%', 'Survey-Rate'),
            (f'{self._pct(stats.get("completedSurveys", 0), max(stats.get("totalSurveys", 1), 1))}%', 'Completion'),
            (self.data.get('mobilePercent', '—'), 'Mobile'),
        ]
        col_w = CONTENT_W / 4
        for i, (val, label) in enumerate(metrics):
            x = MARGIN_LEFT + i * col_w
            self.c.setFont('Cormorant-SemiBold', 28)
            self.c.setFillColor(self.ACCENT)
            self.c.drawString(x, self.y, val)
            self.c.setFont('Inter', 8)
            self.c.setFillColor(self.MUTED)
            self.c.drawString(x, self.y - 18, label)

        self.c.setFont('Inter', 8)
        self.c.setFillColor(self.MUTED)
        self.c.drawString(MARGIN_LEFT, MARGIN_BOTTOM + 30, f'Erstellt für: 120 Ventures / {venture}')
        self.c.drawString(MARGIN_LEFT, MARGIN_BOTTOM + 16, f'Zeitraum: {period}')

    def build_executive_summary(self):
        self.new_page()
        self.section_header(1, 'Executive Summary')

        summary = self.data.get('executiveSummary', '')
        if summary:
            self.body_text(summary)
            self.spacer(8)

        stats = self.data.get('stats', {})
        sa = self.data.get('sessionAnalytics', {})
        total = stats.get('totalSessions', 0)
        surveys = stats.get('totalSurveys', 0)
        completed = stats.get('completedSurveys', 0)
        signups = stats.get('newsletterSignups', 0)

        self.kpi_row([
            (str(total), 'Sessions', f'Heute: {sa.get("today", "—")} · Woche: {sa.get("week", "—")}'),
            (str(surveys), 'Survey Starts', f'{self._pct(surveys, total)}% der Sessions'),
            (str(completed), 'Completed', f'{self._pct(completed, max(surveys, 1))}% Completion Rate'),
            (str(signups), 'Signups', f'{self._pct(signups, total)}% der Sessions'),
        ])

        core_insight = self.data.get('coreInsight', '')
        if core_insight:
            self.callout_box(core_insight)

    def build_traffic(self):
        self.spacer(15)
        self.section_header(2, 'Traffic & Akquise')

        sa = self.data.get('sessionAnalytics', {})

        self.subsection_title('2.1  Sessions')
        session_bullets = self.data.get('sessionBullets', [])
        for b in session_bullets:
            self.bullet(b)

        channels = self.data.get('channels', [])
        if channels:
            self.spacer(8)
            self.subsection_title('2.2  Kanäle')
            self.table(
                ['Kanal', 'Sessions', 'Anteil'],
                channels,
                col_widths=[200, 150, 155]
            )

        countries = self.data.get('countries', [])
        if countries:
            self.spacer(5)
            self.subsection_title('2.3  Geografie')
            self.table(
                ['Land', 'Sessions', 'Anteil'],
                countries,
                col_widths=[200, 150, 155]
            )

        devices = self.data.get('deviceBullets', [])
        if devices:
            self.spacer(5)
            self.subsection_title('2.4  Geräte & Browser')
            for b in devices:
                self.bullet(b)

    def build_meta_ads(self):
        meta_ads = self.data.get('metaAds', [])
        if not meta_ads:
            return

        self.check_space(200)
        self.section_header(3, 'Meta-Kampagnen-Performance')

        meta_summary = self.data.get('metaSummary', '')
        if meta_summary:
            self.body_text(meta_summary)
            self.spacer(5)

        # Determine column widths based on number of fields
        self.table(
            ['Ad', 'Status', 'LPV', 'CPR (€)', 'Spend (€)', 'Impr.', 'Reach', 'Clicks'],
            meta_ads,
            col_widths=[110, 52, 35, 50, 55, 55, 52, 46],
            highlight_col=3
        )

        meta_insight = self.data.get('metaInsight', '')
        if meta_insight:
            self.spacer(5)
            self.callout_box(meta_insight)

        meta_bullets = self.data.get('metaBullets', [])
        if meta_bullets:
            self.spacer(8)
            self.subsection_title('Interpretation')
            for b in meta_bullets:
                self.bullet(b)

    def build_funnel(self):
        funnel = self.data.get('funnel', [])
        if not funnel:
            return

        self.spacer(15)
        self.section_header(4, 'Survey Funnel')

        funnel_intro = self.data.get('funnelIntro', '')
        if funnel_intro:
            self.body_text(funnel_intro)
            self.spacer(8)

        self.subsection_title('Conversion-Funnel')
        self.funnel_chart(funnel)

        funnel_insight = self.data.get('funnelInsight', '')
        if funnel_insight:
            self.spacer(5)
            self.callout_box(funnel_insight)

    def build_user_profile(self):
        profile = self.data.get('userProfile', {})
        if not profile:
            return

        self.check_space(200)
        self.section_header(5, 'Nutzerprofil')

        # Relationship duration
        rel_duration = profile.get('relationshipDuration', [])
        if rel_duration:
            self.subsection_title('Beziehungsdauer')
            self.horizontal_bar(rel_duration)

        # Demographics
        demo_bullets = profile.get('demographicBullets', [])
        if demo_bullets:
            self.spacer(5)
            self.subsection_title('Demografie')
            for b in demo_bullets:
                self.bullet(b)

        # Age table
        age_table = profile.get('ageTable', [])
        if age_table:
            self.spacer(3)
            self.table(
                ['Altersgruppe', 'Anteil (ausfüllend)', 'Anteil (Partner)'],
                age_table,
                col_widths=[180, 160, 165]
            )

        # Living situation
        living = profile.get('livingSituation', [])
        if living:
            self.spacer(5)
            self.subsection_title('Lebenssituation')
            self.table(
                ['Situation', 'Anzahl', 'Anteil'],
                living,
                col_widths=[250, 100, 155]
            )

        # Besonderheiten
        besonderheiten = profile.get('besonderheiten', [])
        if besonderheiten:
            self.spacer(5)
            self.subsection_title('Besonderheiten')
            self.horizontal_bar(besonderheiten)

    def build_needs(self):
        needs = self.data.get('needs', {})
        if not needs:
            return

        self.spacer(10)
        self.section_header(6, 'Bedürfnisse & Motivation')

        desires = needs.get('desires', [])
        if desires:
            self.subsection_title('Wünsche')
            self.horizontal_bar(desires)

        triggers = needs.get('triggers', [])
        if triggers:
            self.spacer(5)
            self.subsection_title('Trigger')
            self.horizontal_bar(triggers)

        needs_insight = needs.get('insight', '')
        if needs_insight:
            self.spacer(5)
            self.callout_box(needs_insight)

    def build_interpretation(self):
        interp = self.data.get('interpretation', {})
        if not interp:
            return

        self.check_space(200)
        section_num = self._next_section()
        self.section_header(section_num, 'Interpretation')

        for sub in interp.get('sections', []):
            self.subsection_title(sub['title'])
            self.body_text(sub['text'])
            self.spacer(5)

    def build_recommendations(self):
        recs = self.data.get('recommendations', {})
        if not recs:
            return

        self.check_space(200)
        section_num = self._next_section()
        self.section_header(section_num, 'Handlungsempfehlungen')

        for group in recs.get('groups', []):
            self.subsection_title(group['title'])
            self.spacer(3)
            for item in group.get('items', []):
                self.labeled_item(item['letter'], item['title'])
                for b in item.get('bullets', []):
                    self.bullet(b)
                self.spacer(8)

    # ── Helpers ──

    def _pct(self, part, total):
        if total == 0:
            return '0'
        return f'{(part / total) * 100:.1f}'

    def _next_section(self):
        if not hasattr(self, '_section_counter'):
            # Count sections that were built
            self._section_counter = 2  # starts after exec summary (1) + traffic (2)
            if self.data.get('metaAds'):
                self._section_counter += 1
            if self.data.get('funnel'):
                self._section_counter += 1
            if self.data.get('userProfile'):
                self._section_counter += 1
            if self.data.get('needs'):
                self._section_counter += 1
        self._section_counter += 1
        return self._section_counter

    def build(self):
        self.title_page()
        self.build_executive_summary()
        self.build_traffic()
        self.build_meta_ads()
        self.build_funnel()
        self.build_user_profile()
        self.build_needs()
        self.build_interpretation()
        self.build_recommendations()

        self._draw_footer()
        self.c.save()
        print(f'PDF saved to {self.c._filename}')


def main():
    parser = argparse.ArgumentParser(description='Generate analyst report PDF')
    parser.add_argument('--data', required=True, help='Path to JSON data file')
    parser.add_argument('--output', required=True, help='Output PDF path')
    args = parser.parse_args()

    with open(args.data, 'r') as f:
        data = json.load(f)

    register_fonts()
    report = ReportPDF(args.output, data)
    report.build()


if __name__ == '__main__':
    main()
