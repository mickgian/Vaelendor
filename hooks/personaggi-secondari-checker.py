#!/usr/bin/env python3
"""
Personaggi Secondari Checker per Vaelendor.
Verifica che i personaggi secondari assegnati a ogni libro siano menzionati
nel testo dei capitoli. Opera a livello di libro (non capitolo).

Uso: python hooks/personaggi-secondari-checker.py <libro-dir>
Esempio: python hooks/personaggi-secondari-checker.py libro1-la-scelta/
"""

import sys
import os
import re
import json
import glob


def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))


def load_json_config(filename):
    config_path = os.path.join(get_script_dir(), "config", filename)
    if not os.path.exists(config_path):
        print(f"⚠️  File di configurazione non trovato: {config_path}")
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_book_key(path):
    """Estrae la chiave libro (es. 'libro1') dal percorso della directory."""
    match = re.search(r'(libro\d+)', path)
    if match:
        return match.group(1)
    return None


def find_chapter_files(book_dir):
    """Trova tutti i file capitolo nella directory del libro."""
    book_dir = book_dir.rstrip("/")
    pattern = os.path.join(book_dir, "capitoli", "capitolo-*.md")
    files = sorted(glob.glob(pattern))
    return files


def get_narrative_text(content):
    """Estrae solo il testo narrativo, escludendo sezioni di analisi."""
    markers = [
        "## Fine Capitolo",
        "## Strati Narrativi",
        "## Elementi a Doppio Strato",
        "## Momenti Chiave",
        "## Geografia del Capitolo",
        "## Cinque Scene Salienti",
        "## Note sulla Versione",
    ]
    for marker in markers:
        idx = content.find(marker)
        if idx != -1:
            content = content[:idx]
    return content


def search_character_in_chapters(varianti, chapter_files):
    """
    Cerca le varianti di un personaggio in tutti i file capitolo.
    Restituisce il basename del primo capitolo in cui è trovato, o None.
    """
    for filepath in chapter_files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = get_narrative_text(f.read())
        except (IOError, OSError):
            continue

        content_lower = content.lower()
        for variante in varianti:
            if variante.lower() in content_lower:
                return os.path.basename(filepath)

    return None


def main():
    if len(sys.argv) < 2:
        print("Uso: python hooks/personaggi-secondari-checker.py <libro-dir>")
        print("Esempio: python hooks/personaggi-secondari-checker.py libro1-la-scelta/")
        sys.exit(0)

    book_dir = sys.argv[1]
    book_key = extract_book_key(book_dir)

    if not book_key:
        print(f"⚠️  Impossibile determinare il libro da: {book_dir}")
        print("    Il percorso deve contenere 'libro1', 'libro2', ecc.")
        sys.exit(0)

    config = load_json_config("personaggi-secondari-libri.json")
    if not config:
        sys.exit(0)

    if book_key not in config:
        print(f"⚠️  Nessuna configurazione trovata per: {book_key}")
        sys.exit(0)

    book_data = config[book_key]
    titolo = book_data.get("titolo", book_key)
    personaggi = book_data.get("personaggi", [])

    chapter_files = find_chapter_files(book_dir)

    print(f"\n=== PERSONAGGI SECONDARI — {book_key}: \"{titolo}\" ===")
    print(f"    Capitoli trovati: {len(chapter_files)}")
    print(f"    Personaggi attesi: {len(personaggi)}")
    print()

    if not chapter_files:
        print("    ⚠️  Nessun capitolo trovato. La directory è corretta?")
        print()
        sys.exit(0)

    presenti = 0
    mancanti = 0

    for pg in personaggi:
        nome = pg.get("nome", "?")
        varianti = pg.get("varianti", [nome])
        ruolo = pg.get("ruolo", "")

        found_in = search_character_in_chapters(varianti, chapter_files)

        nome_padded = nome.ljust(24)
        if found_in:
            print(f"  ✅ {nome_padded} — ({found_in})")
            presenti += 1
        else:
            ruolo_note = f"  [{ruolo}]" if ruolo else ""
            print(f"  ⚠️  {nome_padded} — NON ancora menzionato{ruolo_note}")
            mancanti += 1

    print()
    if mancanti == 0:
        print(f"  Risultato: ✅ Tutti {presenti}/{len(personaggi)} personaggi presenti")
    else:
        print(f"  Risultato: {presenti}/{len(personaggi)} personaggi presenti · {mancanti} mancanti")
    print()

    sys.exit(0)


if __name__ == "__main__":
    main()
