#!/usr/bin/env python3
"""
Memoria Updater per Vaelendor.
Aggiorna le memorie dei personaggi dopo la modifica di un capitolo.

Uso: python hooks/memoria-updater.py <file-capitolo>
Esempio: python hooks/memoria-updater.py libro1-la-scelta/capitoli/capitolo-12.md
"""

import sys
import os
import re

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def extract_chapter_info(filepath):
    chapter_match = re.search(r'capitolo-(\d+)', os.path.basename(filepath))
    book_dir_match = re.search(r'(libro\d+-[^/]+)', filepath)

    chapter_num = int(chapter_match.group(1)) if chapter_match else None
    book_dir = book_dir_match.group(1) if book_dir_match else None

    return book_dir, chapter_num

def read_file_safe(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def get_characters_for_chapter(chapter_num):
    """Return characters that should be present in the chapter."""
    characters = ["zorgar", "sylas", "dain", "aldric", "elara", "mirael"]
    if chapter_num >= 3:
        characters.append("fizzle")
    if chapter_num >= 10:
        characters.append("vera")
    return characters

def check_character_in_chapter(name, content):
    """Check if a character appears in the chapter text."""
    return name.lower() in content.lower()

def main():
    if len(sys.argv) < 2:
        print("Uso: python hooks/memoria-updater.py <file-capitolo>")
        print("Esempio: python hooks/memoria-updater.py libro1-la-scelta/capitoli/capitolo-12.md")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"❌ File non trovato: {filepath}")
        sys.exit(1)

    project_root = get_project_root()
    book_dir, chapter_num = extract_chapter_info(filepath)

    if not book_dir or not chapter_num:
        print("❌ Impossibile determinare libro/capitolo dal percorso del file")
        sys.exit(1)

    # Read chapter
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Paths
    memoria_dir = os.path.join(project_root, book_dir, "memoria-personaggi")

    print(f"\n=== MEMORIA UPDATER — Capitolo {chapter_num:02d} ===\n")

    # Check if chapter has content
    narrative_lines = [l for l in content.split('\n')
                      if l.strip() and not l.startswith('#') and not l.startswith('**')
                      and not l.startswith('---') and not l.startswith('<!--')]

    if len(narrative_lines) < 10:
        print("ℹ️  Il capitolo non sembra avere ancora contenuto narrativo sufficiente.")
        print("    Le memorie devono essere aggiornate dopo la stesura del capitolo.")
        sys.exit(0)

    # Get characters for this chapter
    characters = get_characters_for_chapter(chapter_num)

    present_characters = []
    absent_characters = []

    for char in characters:
        if check_character_in_chapter(char, content):
            present_characters.append(char)
        else:
            absent_characters.append(char)

    print("👥 Personaggi presenti nel capitolo:")
    for char in present_characters:
        memoria_path = os.path.join(memoria_dir, f"{char}.md")
        exists = os.path.exists(memoria_path)
        status = "✅" if exists else "❌ file memoria mancante!"
        print(f"   {status} {char.capitalize()}")

    if absent_characters:
        print()
        print("👤 Personaggi NON menzionati:")
        for char in absent_characters:
            warning = " ⚠️  ATTENZIONE: dovrebbe essere presente!" if char == "fizzle" and chapter_num >= 3 else ""
            print(f"   — {char.capitalize()}{warning}")

    print()

    # Check each present character's memory file
    needs_update = []
    for char in present_characters:
        memoria_path = os.path.join(memoria_dir, f"{char}.md")
        if not os.path.exists(memoria_path):
            needs_update.append((char, "CREARE file memoria"))
            continue

        memoria_content = read_file_safe(memoria_path)

        # Check if already updated for this chapter
        cap_marker = f"Cap {chapter_num}:"
        cap_marker_alt = f"Capitolo {chapter_num}"

        if cap_marker in memoria_content or f"Aggiornato al: Capitolo {chapter_num}" in memoria_content:
            print(f"✅ {char.capitalize()}: già aggiornato al Capitolo {chapter_num}")
        else:
            needs_update.append((char, "aggiornare"))
            print(f"⚠️  {char.capitalize()}: memoria NON aggiornata al Capitolo {chapter_num}")

    print()

    if needs_update:
        print("📝 Azioni richieste:")
        for char, action in needs_update:
            memoria_path = os.path.join(memoria_dir, f"{char}.md")
            print(f"   — {char.capitalize()}: {action}")
            print(f"     File: {memoria_path}")
            print(f"     Aggiungere con prefisso 'Cap {chapter_num}:' per ogni nuova voce")
            print(f"     Sezioni da aggiornare:")
            print(f"       • Cosa SA (nuovi fatti appresi)")
            print(f"       • Cosa SOSPETTA (nuove intuizioni)")
            print(f"       • Cosa NON SA (verificare se qualcosa è stato rivelato)")
            print(f"       • Relazioni (cambiamenti nei rapporti)")
            print(f"       • Stato Fisico/Emotivo (condizione attuale)")
            print(f"     Aggiornare 'Aggiornato al: Capitolo {chapter_num}'")
            print()

        print(f"Risultato: ⚠️  {len(needs_update)} memorie da aggiornare")
    else:
        print("Risultato: ✅ Tutte le memorie aggiornate")

if __name__ == "__main__":
    main()
