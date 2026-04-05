#!/usr/bin/env python3
"""
pov-check.py — Mostra il POV atteso per il capitolo corrente.
Chiamato da pre-edit.sh con argomenti: libro_id capitolo_num

Usage:
    python hooks/pov-check.py <libro_id> <capitolo_num>

Esempio:
    python hooks/pov-check.py libro1-la-scelta 7
"""

import sys
import re
import json
from pathlib import Path


def extract_book_key(libro_dir: str) -> str | None:
    """Estrae 'libro1' da 'libro1-la-scelta'."""
    m = re.search(r'(libro\d+)', libro_dir)
    return m.group(1) if m else None


def main():
    if len(sys.argv) < 3:
        print("Uso: pov-check.py <libro_id> <capitolo_num>")
        sys.exit(1)

    libro_raw = sys.argv[1]
    cap_num = str(sys.argv[2])

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

    cap_data = libro.get(cap_num)
    if not cap_data:
        print(f"  ⚠️  Capitolo {cap_num} non trovato nella rotazione POV.")
        sys.exit(0)

    pov = cap_data.get("pov", "NON DEFINITO")
    pov_file = cap_data.get("file", "")
    note = cap_data.get("note", "")
    prologo_pov = cap_data.get("prologo_pov", "")
    prologo_file = cap_data.get("prologo_file", "")

    print("")
    print("🎭 POV DEL CAPITOLO:")
    print("--------------------------------------------")
    if prologo_pov:
        print(f"  Prologo: {prologo_pov.upper()}")
        if prologo_file:
            print(f"  Scheda prologo: {prologo_file}")
    print(f"  Capitolo {cap_num}: {pov.upper()}")
    if pov_file:
        print(f"  Scheda: {pov_file}")
    if note:
        print(f"  Nota:   {note}")

    # Legge e stampa la sezione Voce Narrativa del prologo
    if prologo_file:
        project_root = Path(__file__).parent.parent
        pro_path = project_root / prologo_file
        if pro_path.exists():
            lines = pro_path.read_text(encoding="utf-8").splitlines()
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
            if section_lines:
                print("")
                print(f"  VOCE NARRATIVA — {prologo_pov.upper()} (prologo):")
                for l in section_lines[:10]:
                    print(f"  {l}")

    # Legge e stampa la sezione Voce Narrativa dalla scheda personaggio
    if pov_file:
        project_root = Path(__file__).parent.parent
        char_path = project_root / pov_file
        if char_path.exists():
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
            if section_lines:
                print("")
                print("  VOCE NARRATIVA:")
                for l in section_lines[:15]:
                    print(f"  {l}")
    print("")


if __name__ == "__main__":
    main()
