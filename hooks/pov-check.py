#!/usr/bin/env python3
"""
pov-check.py — Mostra il POV atteso per il capitolo corrente.
Chiamato da pre-edit.sh con argomenti: libro_id capitolo_num

Accetta numeri (1-22) e valori speciali: "pro" (prologo), "epi" (epilogo).

Usage:
    python hooks/pov-check.py <libro_id> <capitolo_num>

Esempio:
    python hooks/pov-check.py libro1-la-scelta 7
    python hooks/pov-check.py libro1-la-scelta pro
    python hooks/pov-check.py libro1-la-scelta epi
"""

import sys
import re
import json
from pathlib import Path


def extract_book_key(libro_dir: str) -> str | None:
    """Estrae 'libro1' da 'libro1-la-scelta'."""
    m = re.search(r'(libro\d+)', libro_dir)
    return m.group(1) if m else None


def read_voce_narrativa(char_path: Path, max_lines: int = 15) -> list[str]:
    """Legge la sezione 'Voce Narrativa' da una scheda personaggio."""
    if not char_path.exists():
        return []
    lines = char_path.read_text(encoding="utf-8").splitlines()
    in_section = False
    section_lines = []
    for line in lines:
        if "## Voce Narrativa" in line:
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section:
            section_lines.append(line)
    return section_lines[:max_lines]


def format_label(cap_key: str) -> str:
    """Converte la chiave in etichetta leggibile."""
    if cap_key == "pro":
        return "PROLOGO"
    if cap_key == "epi":
        return "EPILOGO"
    return f"Capitolo {cap_key}"


def main():
    if len(sys.argv) < 3:
        print("Uso: pov-check.py <libro_id> <capitolo_num|pro|epi>")
        sys.exit(1)

    libro_raw = sys.argv[1]
    cap_key = sys.argv[2].lower()

    libro_id = extract_book_key(libro_raw)
    if not libro_id:
        print(f"  ⚠️  Impossibile determinare il libro da: {libro_raw}")
        sys.exit(0)

    config_path = Path(__file__).parent / "config" / "pov-rotazione.json"

    if not config_path.exists():
        print("  ⚠️  pov-rotazione.json non trovato. POV non verificabile.")
        sys.exit(0)

    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    libro = config.get(libro_id, {})
    if not libro:
        print(f"  ⚠️  Nessuna rotazione POV definita per {libro_id}.")
        sys.exit(0)

    cap_data = libro.get(cap_key)
    if not cap_data:
        print(f"  ⚠️  '{cap_key}' non trovato nella rotazione POV di {libro_id}.")
        sys.exit(0)

    pov = cap_data.get("pov", "NON DEFINITO")
    pov_file = cap_data.get("file", "")
    note = cap_data.get("note", "")
    label = format_label(cap_key)

    print("")
    print("🎭 POV DEL CAPITOLO:")
    print("--------------------------------------------")
    print(f"  {label}: {pov.upper()}")
    if pov_file:
        print(f"  Scheda: {pov_file}")
    if note:
        print(f"  Nota:   {note}")

    # Legge e stampa la sezione Voce Narrativa dalla scheda personaggio
    if pov_file:
        project_root = Path(__file__).parent.parent
        voce_lines = read_voce_narrativa(project_root / pov_file)
        if voce_lines:
            print("")
            print("  VOCE NARRATIVA:")
            for l in voce_lines:
                print(f"  {l}")
    print("")


if __name__ == "__main__":
    main()
