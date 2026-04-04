#!/usr/bin/env python3
"""
tecnica-check.py — Verifica e mostra la tecnica narrativa prima della scrittura.

Mostra al writer la tecnica dominante del libro, le regole da seguire,
gli errori comuni da evitare, e una checklist per il capitolo.

Usage:
    python hooks/tecnica-check.py <libro-dir> <capitolo>

Esempio:
    python hooks/tecnica-check.py libro1-la-scelta 12
    python hooks/tecnica-check.py libro2-i-sussurri 5
"""

import sys
import os
import json
import re
from pathlib import Path


def extract_book_number(libro_dir: str) -> int | None:
    """Estrae il numero del libro dal nome della directory (es: libro1-la-scelta → 1)."""
    m = re.search(r'libro(\d+)', libro_dir)
    return int(m.group(1)) if m else None


def load_config() -> dict:
    """Carica la configurazione delle tecniche narrative."""
    config_path = Path(__file__).parent / 'config' / 'tecniche-narrative.json'
    if not config_path.exists():
        print(f"  ⚠️  Config non trovato: {config_path}")
        sys.exit(0)
    with open(config_path, encoding='utf-8') as f:
        return json.load(f)


def print_section(title: str, icon: str = ""):
    """Stampa un header di sezione."""
    print(f"\n{icon} {title}")
    print("─" * 50)


def main():
    if len(sys.argv) < 3:
        print(f"Uso: python {sys.argv[0]} <libro-dir> <capitolo>")
        sys.exit(1)

    libro_dir = sys.argv[1]
    cap_num = int(sys.argv[2])

    book_num = extract_book_number(libro_dir)
    if book_num is None:
        print(f"  ⚠️  Impossibile determinare il numero del libro da: {libro_dir}")
        sys.exit(0)

    config = load_config()
    book_key = str(book_num)

    if book_key not in config.get('libri', {}):
        print(f"  ⚠️  Nessuna tecnica configurata per il libro {book_num}")
        sys.exit(0)

    tech = config['libri'][book_key]

    # Header
    print("")
    print("╔══════════════════════════════════════════════╗")
    print(f"║  TECNICA NARRATIVA — Libro {book_num}: {tech['titolo']}")
    print(f"║  Capitolo {cap_num}")
    print("╚══════════════════════════════════════════════╝")

    # Tecnica principale
    print_section("TECNICA DOMINANTE", "🎭")
    print(f"  Principale: {tech['tecnica_principale']}")
    print(f"  Secondaria: {tech['tecnica_secondaria']}")
    print(f"  Tema:       {tech['tema_supportato']}")

    # Regole
    print_section("REGOLE DA SEGUIRE", "📏")
    for i, regola in enumerate(tech['regole'], 1):
        print(f"  {i}. {regola}")

    # Errori comuni
    print_section("ERRORI DA EVITARE", "⚠️")
    for errore in tech['errori_comuni']:
        print(f"  ✗ {errore}")

    # Checklist
    print_section(f"CHECKLIST CAPITOLO {cap_num}", "✅")
    for item in tech['checklist_capitolo']:
        print(f"  [ ] {item}")

    # Reminder finale
    print("")
    print("─" * 50)
    print("  Ricorda: la tecnica SERVE la storia, non viceversa.")
    print("  Ref: strumenti/tecniche-narrative.md")
    print("─" * 50)
    print("")


if __name__ == '__main__':
    main()