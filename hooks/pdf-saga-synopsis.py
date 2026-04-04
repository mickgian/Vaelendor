#!/usr/bin/env python3
"""
pdf-saga-synopsis.py — Genera Vaelendor_sinossi_saga.pdf con le sinossi di tutti i 12 libri.

Include: struttura della serie, tecniche narrative, sinossi libro per libro.

Usage:
    python hooks/pdf-saga-synopsis.py [output.pdf]
"""

import sys
import os
import re
from pathlib import Path

try:
    from fpdf import FPDF
    import logging
    logging.getLogger('fpdf').setLevel(logging.ERROR)
except ImportError:
    print("  ⚠️  fpdf2 non installato. Eseguire: pip install fpdf2")
    sys.exit(0)


# ─────────────────────────────────────────────────────────────────────────────
# Costanti tipografiche (stesse del pdf-generator.py)
# ─────────────────────────────────────────────────────────────────────────────
BODY_SIZE  = 11
H1_SIZE    = 18
H2_SIZE    = 14
H3_SIZE    = 12
H4_SIZE    = BODY_SIZE
LINE_H     = 6

FONT_VARIANTS = {
    '':   ['/System/Library/Fonts/Supplemental/Arial.ttf', '/Library/Fonts/Arial.ttf'],
    'B':  ['/System/Library/Fonts/Supplemental/Arial Bold.ttf', '/Library/Fonts/Arial Bold.ttf'],
    'I':  ['/System/Library/Fonts/Supplemental/Arial Italic.ttf', '/Library/Fonts/Arial Italic.ttf'],
    'BI': ['/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf', '/Library/Fonts/Arial Bold Italic.ttf'],
}


def _find_font(style):
    for path in FONT_VARIANTS.get(style, []):
        if os.path.exists(path):
            return path
    return None


class VaelendorPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=25)
        self.set_margins(25, 25, 25)
        self._fname = 'Helvetica'
        self._styles = {''}
        self._setup_fonts()

    def _setup_fonts(self):
        for style in ('', 'B', 'I', 'BI'):
            path = _find_font(style)
            if path:
                self.add_font('Arial', style, path)
                self._styles.add(style)
                self._fname = 'Arial'

    def f(self, style='', size=BODY_SIZE):
        style = style.upper()
        if style not in self._styles:
            for fallback in ('B', 'I', ''):
                if fallback in self._styles:
                    style = fallback
                    break
        self.set_font(self._fname, style, size)

    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.f('', 9)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, str(self.page_no()), align='C')
        self.set_text_color(0, 0, 0)

    @property
    def text_width(self):
        return self.w - self.l_margin - self.r_margin


def _write_inline(pdf, text, size):
    parts = re.split(r'(\*\*[^*\n]+?\*\*|\*[^*\n]+?\*)', text)
    for part in parts:
        if not part:
            continue
        if part.startswith('**') and part.endswith('**') and len(part) > 4:
            pdf.f('B', size)
            pdf.write(LINE_H, part[2:-2])
        elif part.startswith('*') and part.endswith('*') and len(part) > 2:
            pdf.f('I', size)
            pdf.write(LINE_H, part[1:-1])
        else:
            pdf.f('', size)
            pdf.write(LINE_H, part)
    pdf.f('', size)


def _has_inline(text):
    return bool(re.search(r'\*\*[^*]+?\*\*|\*[^*]+?\*', text))


def _strip_inline(text):
    text = re.sub(r'\*\*([^*]+?)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+?)\*', r'\1', text)
    return text


def render_chapter(pdf, md_text):
    lines = md_text.splitlines()
    i = 0
    w = pdf.text_width

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        i += 1

        if line.strip().startswith('<!--'):
            while i < len(lines) and '-->' not in lines[i - 1]:
                i += 1
            continue

        if line.strip() == '':
            pdf.ln(3)
            continue

        if line.strip() == '---':
            pdf.ln(2)
            pdf.set_draw_color(180, 180, 180)
            pdf.line(pdf.l_margin + 15, pdf.get_y(),
                     pdf.w - pdf.r_margin - 15, pdf.get_y())
            pdf.set_draw_color(0, 0, 0)
            pdf.ln(4)
            continue

        if line.startswith('|'):
            while i < len(lines) and lines[i].startswith('|'):
                i += 1
            pdf.ln(2)
            continue

        if line.startswith('# ') and not line.startswith('## '):
            text = line[2:].strip()
            pdf.ln(4)
            pdf.f('B', H1_SIZE)
            pdf.multi_cell(w, 9, text, align='L')
            pdf.f('', BODY_SIZE)
            pdf.ln(2)
            continue

        if line.startswith('## ') and not line.startswith('### '):
            text = line[3:].strip()
            pdf.ln(5)
            pdf.f('B', H2_SIZE)
            pdf.multi_cell(w, 7, text, align='L')
            pdf.f('', BODY_SIZE)
            pdf.ln(2)
            continue

        if line.startswith('### ') and not line.startswith('#### '):
            text = line[4:].strip()
            pdf.ln(3)
            pdf.f('BI', H3_SIZE)
            pdf.multi_cell(w, 6, text, align='L')
            pdf.f('', BODY_SIZE)
            pdf.ln(1)
            continue

        if line.startswith('#### '):
            text = line[5:].strip()
            pdf.ln(2)
            pdf.f('B', H4_SIZE)
            pdf.multi_cell(w, LINE_H, _strip_inline(text), align='L')
            pdf.f('', BODY_SIZE)
            continue

        if re.match(r'^[-*] ', line):
            text = line[2:].strip()
            pdf.f('', BODY_SIZE)
            pdf.set_x(pdf.l_margin + 4)
            pdf.cell(4, LINE_H, '\u2022')
            if _has_inline(text):
                _write_inline(pdf, text, BODY_SIZE)
                pdf.ln(LINE_H)
            else:
                pdf.multi_cell(w - 8, LINE_H, text, align='L')
            continue

        if re.match(r'^\d+\. ', line):
            text = re.sub(r'^\d+\. ', '', line)
            pdf.f('', BODY_SIZE)
            pdf.multi_cell(w, LINE_H, _strip_inline(text), align='L')
            continue

        para_parts = [line]
        while i < len(lines):
            peek = lines[i].rstrip()
            if (not peek.strip()
                or peek.strip() == '---'
                or peek.startswith('#')
                or peek.startswith('|')
                or re.match(r'^[-*] ', peek)
                or re.match(r'^\d+\. ', peek)):
                break
            para_parts.append(peek)
            i += 1

        full_para = ' '.join(para_parts)
        pdf.f('', BODY_SIZE)

        if _has_inline(full_para):
            pdf.set_x(pdf.l_margin)
            _write_inline(pdf, full_para, BODY_SIZE)
            pdf.ln(LINE_H)
        else:
            pdf.multi_cell(w, LINE_H, full_para, align='J')

        pdf.ln(1)


def add_cover(pdf):
    pdf.add_page()
    w = pdf.text_width

    pdf.ln(50)
    pdf.f('B', 28)
    pdf.multi_cell(w, 14, 'VAELENDOR', align='C')

    pdf.ln(4)
    pdf.f('', 15)
    pdf.multi_cell(w, 7, 'Saga dei Draghi Incatenati', align='C')

    pdf.ln(18)
    pdf.set_draw_color(100, 100, 100)
    pdf.line(pdf.l_margin + 20, pdf.get_y(), pdf.w - pdf.r_margin - 20, pdf.get_y())
    pdf.set_draw_color(0, 0, 0)
    pdf.ln(18)

    pdf.f('B', 20)
    pdf.multi_cell(w, 10, 'Sinossi della Saga Completa', align='C')

    pdf.ln(8)
    pdf.f('', 14)
    pdf.multi_cell(w, 7, '12 Libri — Piano Narrativo', align='C')

    pdf.ln(70)
    pdf.f('', 10)
    pdf.set_text_color(150, 150, 150)
    pdf.multi_cell(w, 6, 'Bozza di lavoro — Tutti i diritti riservati', align='C')
    pdf.set_text_color(0, 0, 0)


def main():
    base_dir = Path(__file__).parent.parent
    output_path = sys.argv[1] if len(sys.argv) > 1 else str(base_dir / 'Vaelendor_sinossi_saga.pdf')

    # Raccogli i file da includere in ordine
    files_to_include = []

    # 1. Struttura della serie
    struttura = base_dir / 'serie' / 'struttura-serie.md'
    if struttura.exists():
        files_to_include.append(('Struttura della Serie', struttura))

    # 2. Tecniche narrative
    tecniche = base_dir / 'strumenti' / 'tecniche-narrative.md'
    if tecniche.exists():
        files_to_include.append(('Tecniche Narrative', tecniche))

    # 3. Sinossi libro 1 (dalla directory del libro)
    sinossi_l1 = base_dir / 'libro1-la-scelta' / 'sinossi.md'
    if sinossi_l1.exists():
        files_to_include.append(('Sinossi Libro 1', sinossi_l1))

    # 4. Sinossi libri 2-12
    for n in range(2, 13):
        path = base_dir / 'serie' / f'sinossi-libro{n}.md'
        if path.exists():
            files_to_include.append((f'Sinossi Libro {n}', path))

    if not files_to_include:
        print("  ⚠️  Nessun file trovato.")
        sys.exit(0)

    names = [name for name, _ in files_to_include]
    print(f"  File trovati: {len(files_to_include)}")
    for name in names:
        print(f"    • {name}")

    pdf = VaelendorPDF()
    add_cover(pdf)

    for name, path in files_to_include:
        pdf.add_page()
        text = path.read_text(encoding='utf-8', errors='replace')
        render_chapter(pdf, text)

    pdf.output(output_path)
    print(f"  ✅ {output_path} — {len(files_to_include)} sezioni, {pdf.page} pagine")


if __name__ == '__main__':
    main()
