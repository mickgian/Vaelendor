#!/usr/bin/env python3
"""
antispoiler-check.py — Mostra le regole anti-spoiler attive
per il libro e capitolo correnti.

Chiamato da pre-edit.sh.

Usage:
    python3 hooks/antispoiler-check.py <libro_id> <capitolo|pro|epi>

Esempio:
    python3 hooks/antispoiler-check.py libro1-la-scelta 7
    python3 hooks/antispoiler-check.py libro1-la-scelta pro
"""

import sys
import re
import json
from pathlib import Path

CONFIG = Path(__file__).parent / "config" / "anti-spoiler.json"


def extract_book_key(libro_dir: str) -> str | None:
    """Estrae 'libro1' da 'libro1-la-scelta'."""
    m = re.search(r'(libro\d+)', libro_dir)
    return m.group(1) if m else None


def cap_to_num(cap_key: str) -> int | None:
    """Converte la chiave capitolo in numero per il confronto range."""
    if cap_key == "pro":
        return 0
    if cap_key == "epi":
        return 9999
    try:
        return int(cap_key)
    except ValueError:
        return None


def wrap_text(text: str, width: int = 50, indent: str = "       ") -> list[str]:
    """Spezza il testo in righe con indentazione."""
    words = text.split()
    lines = []
    line = []
    for w in words:
        if sum(len(x) + 1 for x in line) + len(w) > width:
            lines.append(indent + " ".join(line))
            line = [w]
        else:
            line.append(w)
    if line:
        lines.append(indent + " ".join(line))
    return lines


def main():
    if len(sys.argv) < 3:
        print("Uso: antispoiler-check.py <libro_id> <capitolo|pro|epi>")
        sys.exit(1)

    libro_raw = sys.argv[1]
    cap_key = sys.argv[2].lower()

    libro_id = extract_book_key(libro_raw)
    if not libro_id:
        print(f"  ⚠️  Impossibile determinare il libro da: {libro_raw}")
        sys.exit(0)

    cap_num = cap_to_num(cap_key)
    if cap_num is None:
        print(f"  ⚠️  Capitolo non valido: {cap_key}")
        sys.exit(0)

    if not CONFIG.exists():
        print("  ⚠️  anti-spoiler.json non trovato.")
        print("     Esegui: python3 hooks/sync-antispoiler.py")
        sys.exit(0)

    with open(CONFIG, encoding="utf-8") as f:
        config = json.load(f)

    # Raccoglie regole: globali del libro + globali "tutti" + range attivi
    regole_attive = []

    for scope in [libro_id, "tutti"]:
        libro = config.get(scope, {})

        for r in libro.get("globali", []):
            regole_attive.append(r)

        for r in libro.get("per_range", []):
            da = r.get("da", 0)
            a = r.get("a", 9999)
            if isinstance(a, str) and a == "fine":
                a = 9999
            if isinstance(da, str):
                try:
                    da = int(da)
                except ValueError:
                    da = 0
            if da <= cap_num <= a:
                regole_attive.append(r)

    if not regole_attive:
        return

    print("")
    print("🚫 ANTI-SPOILER ATTIVI:")
    print("--------------------------------------------")
    for r in regole_attive:
        rule_id = r.get("id", "?")
        regola = r.get("regola", "")
        dettaglio = r.get("dettaglio", "")

        print(f"  [{rule_id}] {regola}")
        if dettaglio:
            for line in wrap_text(dettaglio):
                print(line)
    print("")


if __name__ == "__main__":
    main()
