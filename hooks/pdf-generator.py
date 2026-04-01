#!/usr/bin/env python3
"""
pdf-generator.py — Genera Vaelendor_temo.pdf con tutti i capitoli completati.

Include la narrativa + le sezioni post-capitolo (Geografia, Scene Salienti,
Strati Narrativi, Worldbuilding Integrato, ecc.).

Usage:
    python hooks/pdf-generator.py <libro-dir> [output.pdf]

Un capitolo è "completato" se il suo checkpoint esiste e non contiene '[Da definire]'.
"""

import sys
import os
import re
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# Verifica fpdf2
# ─────────────────────────────────────────────────────────────────────────────
try:
    from fpdf import FPDF
    import logging
    logging.getLogger('fpdf').setLevel(logging.ERROR)  # sopprime warning glifici mancanti (★ ecc.)
except ImportError:
    print("  ⚠️  fpdf2 non installato. Eseguire: pip install fpdf2")
    sys.exit(0)


# ─────────────────────────────────────────────────────────────────────────────
# Costanti tipografiche
# ─────────────────────────────────────────────────────────────────────────────
BODY_SIZE  = 11
H1_SIZE    = 18
H2_SIZE    = 14
H3_SIZE    = 12
H4_SIZE    = BODY_SIZE
LINE_H     = 6   # mm altezza riga per multi_cell / write

FONT_VARIANTS = {
    '':   [
        '/System/Library/Fonts/Supplemental/Arial.ttf',
        '/Library/Fonts/Arial.ttf',
    ],
    'B':  [
        '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
        '/Library/Fonts/Arial Bold.ttf',
    ],
    'I':  [
        '/System/Library/Fonts/Supplemental/Arial Italic.ttf',
        '/Library/Fonts/Arial Italic.ttf',
    ],
    'BI': [
        '/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf',
        '/Library/Fonts/Arial Bold Italic.ttf',
    ],
}


def _find_font(style):
    """Restituisce il primo path esistente per lo stile, o None."""
    for path in FONT_VARIANTS.get(style, []):
        if os.path.exists(path):
            return path
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Classe PDF
# ─────────────────────────────────────────────────────────────────────────────
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
        """Imposta il font, con fallback graceful se lo stile non è disponibile."""
        style = style.upper()
        if style not in self._styles:
            # prova a degradare BI → B → I → ''
            for fallback in ('B', 'I', ''):
                if fallback in self._styles:
                    style = fallback
                    break
        self.set_font(self._fname, style, size)

    def header(self):
        pass  # nessun header di pagina

    def footer(self):
        self.set_y(-15)
        self.f('', 9)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, str(self.page_no()), align='C')
        self.set_text_color(0, 0, 0)

    @property
    def text_width(self):
        return self.w - self.l_margin - self.r_margin


# ─────────────────────────────────────────────────────────────────────────────
# Rendering inline (bold/italic dentro una riga)
# ─────────────────────────────────────────────────────────────────────────────
def _write_inline(pdf: VaelendorPDF, text: str, size: int):
    """Scrive testo con supporto a **bold** e *italic* inline via write()."""
    # Separa per **bold** e *italic*
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


def _has_inline(text: str) -> bool:
    return bool(re.search(r'\*\*[^*]+?\*\*|\*[^*]+?\*', text))


def _strip_inline(text: str) -> str:
    text = re.sub(r'\*\*([^*]+?)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+?)\*',   r'\1', text)
    return text


# ─────────────────────────────────────────────────────────────────────────────
# Renderer Markdown → PDF
# ─────────────────────────────────────────────────────────────────────────────
def render_chapter(pdf: VaelendorPDF, md_text: str):
    """Renderizza il testo Markdown di un capitolo nel PDF corrente."""
    lines = md_text.splitlines()
    i = 0
    w = pdf.text_width

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        i += 1

        # ── Commenti HTML ──────────────────────────────────────────────────
        if line.strip().startswith('<!--'):
            while i < len(lines) and '-->' not in lines[i - 1]:
                i += 1
            continue

        # ── Riga vuota → spazio paragrafo ─────────────────────────────────
        if line.strip() == '':
            pdf.ln(3)
            continue

        # ── Separatore --- ─────────────────────────────────────────────────
        if line.strip() == '---':
            pdf.ln(2)
            pdf.set_draw_color(180, 180, 180)
            pdf.line(pdf.l_margin + 15, pdf.get_y(),
                     pdf.w - pdf.r_margin - 15, pdf.get_y())
            pdf.set_draw_color(0, 0, 0)
            pdf.ln(4)
            continue

        # ── Tabelle → salta l'intero blocco ───────────────────────────────
        if line.startswith('|'):
            while i < len(lines) and lines[i].startswith('|'):
                i += 1
            pdf.ln(2)
            continue

        # ── H1 ────────────────────────────────────────────────────────────
        if line.startswith('# ') and not line.startswith('## '):
            text = line[2:].strip()
            pdf.ln(4)
            pdf.f('B', H1_SIZE)
            pdf.multi_cell(w, 9, text, align='L')
            pdf.f('', BODY_SIZE)
            pdf.ln(2)
            continue

        # ── H2 ────────────────────────────────────────────────────────────
        if line.startswith('## ') and not line.startswith('### '):
            text = line[3:].strip()
            pdf.ln(5)
            pdf.f('B', H2_SIZE)
            pdf.multi_cell(w, 7, text, align='L')
            pdf.f('', BODY_SIZE)
            pdf.ln(2)
            continue

        # ── H3 ────────────────────────────────────────────────────────────
        if line.startswith('### ') and not line.startswith('#### '):
            text = line[4:].strip()
            pdf.ln(3)
            pdf.f('BI', H3_SIZE)
            pdf.multi_cell(w, 6, text, align='L')
            pdf.f('', BODY_SIZE)
            pdf.ln(1)
            continue

        # ── H4 ────────────────────────────────────────────────────────────
        if line.startswith('#### '):
            text = line[5:].strip()
            pdf.ln(2)
            pdf.f('B', H4_SIZE)
            pdf.multi_cell(w, LINE_H, _strip_inline(text), align='L')
            pdf.f('', BODY_SIZE)
            continue

        # ── Lista puntata (- / *) ─────────────────────────────────────────
        if re.match(r'^[-*] ', line):
            text = line[2:].strip()
            pdf.f('', BODY_SIZE)
            pdf.set_x(pdf.l_margin + 4)
            pdf.cell(4, LINE_H, '\u2022')   # •
            if _has_inline(text):
                _write_inline(pdf, text, BODY_SIZE)
                pdf.ln(LINE_H)
            else:
                # multi_cell per il testo del punto elenco con rientro
                x_save = pdf.get_x()
                pdf.multi_cell(w - 8, LINE_H, text, align='L')
            continue

        # ── Lista numerata ────────────────────────────────────────────────
        if re.match(r'^\d+\. ', line):
            text = re.sub(r'^\d+\. ', '', line)
            pdf.f('', BODY_SIZE)
            pdf.multi_cell(w, LINE_H, _strip_inline(text), align='L')
            continue

        # ── Corsivo/grassetto di blocco (⚠️ → testo speciale Unicode) ─────
        # Alcune righe iniziano con emoji come 🌱, ⚠️, ✅, ecc. — le rendiamo
        # come corpo testo normale (le emoji potrebbero non apparire con Arial
        # standard ma il testo circostante è leggibile)

        # ── Paragrafo normale ─────────────────────────────────────────────
        # Raccoglie le righe consecutive che appartengono allo stesso paragrafo
        para_parts = [line]
        while i < len(lines):
            peek = lines[i].rstrip()
            if (not peek.strip()                         # riga vuota
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


# ─────────────────────────────────────────────────────────────────────────────
# Rilevamento capitoli completati
# ─────────────────────────────────────────────────────────────────────────────
def _chapter_is_complete(libro_dir: Path, cap_num: int) -> bool:
    checkpoint = libro_dir / 'checkpoint' / f'dopo-capitolo-{cap_num:02d}.md'
    if not checkpoint.exists():
        return False
    content = checkpoint.read_text(encoding='utf-8', errors='replace')
    return '[Da definire]' not in content


def find_completed_chapters(libro_dir: Path):
    """Restituisce lista ordinata di (numero, path) per i capitoli completati."""
    cap_dir = libro_dir / 'capitoli'
    results = []
    for path in sorted(cap_dir.glob('capitolo-*.md')):
        m = re.search(r'capitolo-(\d+)\.md', path.name)
        if m:
            num = int(m.group(1))
            if _chapter_is_complete(libro_dir, num):
                results.append((num, path))
    return results


# ─────────────────────────────────────────────────────────────────────────────
# Copertina
# ─────────────────────────────────────────────────────────────────────────────
def add_cover(pdf: VaelendorPDF):
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
    pdf.multi_cell(w, 10, 'Libro 1 — La Scelta', align='C')

    pdf.ln(70)
    pdf.f('', 10)
    pdf.set_text_color(150, 150, 150)
    pdf.multi_cell(w, 6, 'Bozza di lavoro — Tutti i diritti riservati', align='C')
    pdf.set_text_color(0, 0, 0)


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print(f"Uso: python {sys.argv[0]} <libro-dir> [output.pdf]")
        sys.exit(1)

    libro_dir  = Path(sys.argv[1])
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'Vaelendor_temo.pdf'

    if not libro_dir.is_dir():
        print(f"  ❌ Directory non trovata: {libro_dir}")
        sys.exit(1)

    chapters = find_completed_chapters(libro_dir)
    if not chapters:
        print("  ⚠️  Nessun capitolo completato trovato.")
        sys.exit(0)

    nums = [str(n) for n, _ in chapters]
    print(f"  Capitoli trovati: {', '.join(nums)}")

    pdf = VaelendorPDF()
    add_cover(pdf)

    for cap_num, cap_path in chapters:
        pdf.add_page()
        text = cap_path.read_text(encoding='utf-8', errors='replace')
        render_chapter(pdf, text)

    pdf.output(str(output_path))
    print(f"  ✅ {output_path} — {len(chapters)} capitoli, {pdf.page} pagine")


if __name__ == '__main__':
    main()
