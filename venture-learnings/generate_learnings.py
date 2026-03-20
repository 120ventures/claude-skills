#!/usr/bin/env python3
"""
Generate a branded Venture Learnings PDF for any 120 Ventures project.

Usage:
    python3 generate_learnings.py <data.json> <output.pdf>

The JSON data file schema is documented in SKILL.md.
"""

import json
import sys
import os
import textwrap

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

W, H = A4
ML = 45
MR = 45
MT = 50
MB = 50
CW = W - ML - MR
WHITE = HexColor('#ffffff')

FONTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')


def register_fonts():
    """Register Cormorant Garamond and Inter fonts."""
    pdfmetrics.registerFont(TTFont('Cormorant-Light', os.path.join(FONTS_DIR, 'CormorantGaramond-Light.ttf')))
    pdfmetrics.registerFont(TTFont('Cormorant-SemiBold', os.path.join(FONTS_DIR, 'CormorantGaramond-SemiBold.ttf')))
    pdfmetrics.registerFont(TTFont('Cormorant-Bold', os.path.join(FONTS_DIR, 'CormorantGaramond-Bold.ttf')))
    pdfmetrics.registerFont(TTFont('Inter', os.path.join(FONTS_DIR, 'Inter-Regular.ttf')))


class LearningsPDF:
    def __init__(self, output_path, data):
        self.data = data
        self.c = canvas.Canvas(output_path, pagesize=A4)
        self.c.setTitle(f'{data["venture"]} \u2014 Venture Learnings')
        self.c.setAuthor('120 Ventures')
        self.y = H - MT
        self.page_num = 0

        colors = data.get('colors', {})
        self.BG = HexColor(colors.get('bg', '#f4f1ec'))
        self.FG = HexColor(colors.get('fg', '#0d0c0a'))
        self.ACCENT = HexColor(colors.get('accent', '#c05c45'))
        self.MUTED = HexColor(colors.get('muted', '#4f4a42'))
        self.BORDER = HexColor(colors.get('border', '#dbd6ce'))
        self.CLAY = HexColor(colors.get('clay', '#ece7df'))

    # ── Page management ──

    def new_page(self):
        if self.page_num > 0:
            self._footer()
            self.c.showPage()
        self.page_num += 1
        self.y = H - MT
        self.c.setFillColor(self.BG)
        self.c.rect(0, 0, W, H, fill=1, stroke=0)

    def _footer(self):
        self.c.setFont('Inter', 7)
        self.c.setFillColor(self.MUTED)
        v = self.data['venture']
        d = self.data['date']
        self.c.drawString(ML, 25, f'{v} \u00b7 Venture Learnings \u00b7 {d} \u00b7 Vertraulich')
        self.c.drawRightString(W - MR, 25, f'{self.page_num}')

    def check_space(self, needed):
        if self.y - needed < MB + 30:
            self._footer()
            self.c.showPage()
            self.page_num += 1
            self.y = H - MT
            self.c.setFillColor(self.BG)
            self.c.rect(0, 0, W, H, fill=1, stroke=0)

    # ── Title page ──

    def title_page(self):
        self.new_page()
        v = self.data['venture']

        # Top accent line
        self.c.setStrokeColor(self.ACCENT)
        self.c.setLineWidth(2)
        self.c.line(ML, H - 35, W - MR, H - 35)

        # Venture name with accent dot
        self.y = H - 90
        self.c.setFont('Cormorant-Bold', 16)
        self.c.setFillColor(self.FG)
        self.c.drawString(ML, self.y, v)
        dot_x = ML + self.c.stringWidth(v, 'Cormorant-Bold', 16)
        self.c.setFillColor(self.ACCENT)
        self.c.drawString(dot_x, self.y, '.')

        # Main title
        self.y -= 120
        self.c.setFont('Cormorant-Light', 38)
        self.c.setFillColor(self.FG)
        self.c.drawString(ML, self.y, 'Venture')
        self.y -= 48
        self.c.drawString(ML, self.y, 'Learnings')

        # Subtitle
        self.y -= 35
        self.c.setFont('Inter', 11)
        self.c.setFillColor(self.MUTED)
        self.c.drawString(ML, self.y, self.data.get('subtitle', ''))

        # Accent line
        self.y -= 20
        self.c.setStrokeColor(self.ACCENT)
        self.c.setLineWidth(0.5)
        self.c.line(ML, self.y, ML + 80, self.y)

        # Summary line
        self.y -= 30
        self.c.setFont('Inter', 9)
        self.c.setFillColor(self.MUTED)
        self.c.drawString(ML, self.y, self.data.get('summary_line', ''))

        # Core insight callout box
        core = self.data.get('core_insight', '')
        if core:
            self.y -= 80
            lines = textwrap.wrap(core, width=85)
            box_h = len(lines) * 14 + 20
            self.c.setFillColor(self.CLAY)
            self.c.roundRect(ML, self.y - box_h + 12, CW, box_h, 3, fill=1, stroke=0)
            self.c.setFillColor(self.ACCENT)
            self.c.rect(ML, self.y - box_h + 12, 3, box_h, fill=1, stroke=0)
            self.c.setFont('Inter', 9)
            self.c.setFillColor(self.FG)
            for line in lines:
                self.c.drawString(ML + 14, self.y, line)
                self.y -= 14

        # Bottom info
        self.c.setFont('Inter', 8)
        self.c.setFillColor(self.MUTED)
        self.c.drawString(ML, MB + 30, 'Erstellt f\u00fcr: 120 Ventures')
        self.c.drawString(ML, MB + 16, f'Zeitraum: {self.data.get("period", "")}')

    # ── Drawing primitives ──

    def section_header(self, num, title):
        self.check_space(50)
        self.y -= 12
        self.c.setFont('Cormorant-SemiBold', 11)
        self.c.setFillColor(self.ACCENT)
        self.c.drawString(ML, self.y, f'{num:02d}')
        self.c.setStrokeColor(self.ACCENT)
        self.c.setLineWidth(0.5)
        self.c.line(ML + 20, self.y + 5, ML + 50, self.y + 5)
        self.y -= 25
        self.c.setFont('Cormorant-SemiBold', 22)
        self.c.setFillColor(self.FG)
        self.c.drawString(ML, self.y, title)
        self.y -= 28

    def subsection_title(self, title):
        if not title:
            return
        self.check_space(30)
        self.y -= 6
        self.c.setFont('Cormorant-SemiBold', 13)
        self.c.setFillColor(self.FG)
        self.c.drawString(ML, self.y, title)
        self.y -= 16

    def body_text(self, text, indent=0):
        self.c.setFont('Inter', 9)
        self.c.setFillColor(self.MUTED)
        max_chars = int((CW - indent) / 4.2)
        lines = textwrap.wrap(text, width=max_chars)
        for line in lines:
            self.check_space(14)
            self.c.drawString(ML + indent, self.y, line)
            self.y -= 13
        self.y -= 3

    def bullet(self, text, indent=10):
        self.check_space(14)
        self.c.setFont('Inter', 8.5)
        self.c.setFillColor(self.MUTED)
        self.c.drawString(ML + indent, self.y, '\u00b7')
        max_chars = int((CW - indent - 12) / 4.0)
        lines = textwrap.wrap(text, width=max_chars)
        for i, line in enumerate(lines):
            if i > 0:
                self.check_space(14)
            self.c.drawString(ML + indent + 12, self.y, line)
            self.y -= 12
        self.y -= 1

    def callout_box(self, text):
        self.check_space(45)
        lines = textwrap.wrap(text, width=88)
        box_h = len(lines) * 13 + 16
        self.c.setFillColor(self.CLAY)
        self.c.roundRect(ML, self.y - box_h + 10, CW, box_h, 3, fill=1, stroke=0)
        self.c.setFillColor(self.ACCENT)
        self.c.rect(ML, self.y - box_h + 10, 3, box_h, fill=1, stroke=0)
        self.c.setFont('Inter', 8.5)
        self.c.setFillColor(self.FG)
        for line in lines:
            self.c.drawString(ML + 14, self.y - 2, line)
            self.y -= 13
        self.y -= 10

    def takeaway_box(self, text):
        self.check_space(40)
        self.y -= 3
        full = '\u2192 ' + text
        lines = textwrap.wrap(full, width=92)
        self.c.setFont('Inter', 8.5)
        self.c.setFillColor(self.ACCENT)
        for line in lines:
            self.check_space(13)
            self.c.drawString(ML + 10, self.y, line)
            self.y -= 12
        self.y -= 5

    def table(self, headers, rows, col_widths=None):
        num_cols = len(headers)
        if col_widths is None:
            col_widths = [CW / num_cols] * num_cols

        row_count = min(len(rows), 30)  # safety limit
        self.check_space(20 + row_count * 16)

        x = ML
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
        self.c.line(ML, self.y, ML + sum(col_widths), self.y)
        self.y -= 13

        for row in rows:
            self.check_space(16)
            x = ML
            for i, cell in enumerate(row):
                if i == 0:
                    self.c.setFont('Inter', 8.5)
                    self.c.setFillColor(self.FG)
                    display = str(cell) if len(str(cell)) <= 35 else str(cell)[:33] + '\u2026'
                    self.c.drawString(x + 2, self.y, display)
                else:
                    self.c.setFont('Inter', 8.5)
                    self.c.setFillColor(self.MUTED)
                    self.c.drawRightString(x + col_widths[i] - 2, self.y, str(cell))
                x += col_widths[i]
            self.y -= 15
        self.y -= 5

    def spacer(self, h=10):
        self.y -= h

    # ── Build ──

    def build(self):
        self.title_page()

        for section in self.data.get('sections', []):
            self.new_page()
            self.section_header(section['num'], section['title'])

            for block in section.get('blocks', []):
                st = block.get('subtitle', '')
                if st:
                    self.subsection_title(st)

                # Callout box
                co = block.get('callout', '')
                if co:
                    self.callout_box(co)
                    self.spacer(3)

                # Table
                th = block.get('table_headers')
                tr = block.get('table_rows')
                if th and tr:
                    num_cols = len(th)
                    if num_cols == 2:
                        cw = [300, CW - 300]
                    elif num_cols == 3:
                        cw = [200, 150, 155]
                    else:
                        cw = [CW / num_cols] * num_cols
                    self.table(th, tr, cw)

                # Bullets
                for b in block.get('bullets', []):
                    self.bullet(b)

                # Takeaway
                ta = block.get('takeaway', '')
                if ta:
                    self.takeaway_box(ta)

                self.spacer(8)

        self._footer()
        self.c.save()
        print(f'PDF saved to {self.c._filename}')


def main():
    if len(sys.argv) != 3:
        print('Usage: python3 generate_learnings.py <data.json> <output.pdf>')
        sys.exit(1)

    data_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(data_path, 'r') as f:
        data = json.load(f)

    register_fonts()
    pdf = LearningsPDF(output_path, data)
    pdf.build()


if __name__ == '__main__':
    main()
