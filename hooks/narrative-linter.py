#!/usr/bin/env python3
"""
Narrative Linter per Vaelendor.
Verifica testo dei capitoli: termini proibiti, presenza personaggi,
encoding, nomi canonici, lunghezza.

Uso: python hooks/narrative-linter.py <file-capitolo>
Esempio: python hooks/narrative-linter.py libro1-la-scelta/capitoli/capitolo-12.md
"""

import sys
import os
import re
import json

def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def load_json_config(filename):
    config_path = os.path.join(get_script_dir(), "config", filename)
    if not os.path.exists(config_path):
        print(f"⚠️  File di configurazione non trovato: {config_path}")
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_chapter_number(filepath):
    match = re.search(r'capitolo-(\d+)', os.path.basename(filepath))
    if match:
        return int(match.group(1))
    return None

def extract_book_key(filepath):
    # Extract book identifier from path like "libro1-la-scelta/capitoli/..."
    match = re.search(r'(libro\d+)', filepath)
    if match:
        return match.group(1)
    return None

def get_narrative_text(content):
    """Extract only narrative text, excluding analysis sections."""
    markers = ["## Fine Capitolo", "## Strati Narrativi", "## Elementi a Doppio Strato", "## Momenti Chiave", "## Geografia del Capitolo", "## Cinque Scene Salienti", "## Note sulla Versione"]
    for marker in markers:
        idx = content.find(marker)
        if idx != -1:
            content = content[:idx]
    return content

def count_words(text):
    """Count words in text, ignoring markdown headers and metadata."""
    lines = text.split('\n')
    word_count = 0
    for line in lines:
        stripped = line.strip()
        # Skip headers, metadata, empty lines, HTML comments
        if (stripped.startswith('#') or
            stripped.startswith('**POV:') or
            stripped.startswith('**Giorno') or
            stripped.startswith('**Luogo') or
            stripped.startswith('---') or
            stripped.startswith('<!--') or
            stripped == ''):
            continue
        word_count += len(stripped.split())
    return word_count

def check_encoding(filepath):
    """Check for UTF-8 encoding issues."""
    errors = []
    corruption_patterns = ["Ã¨", "Ã ", "Ã¬", "Ã²", "Ã¹", "Ã©", "Ã ", "Ã¼"]

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError as e:
        errors.append(f"❌ ERRORE CRITICO: File non è UTF-8 valido — {e}")
        return errors, None

    for i, line in enumerate(content.split('\n'), 1):
        for pattern in corruption_patterns:
            if pattern in line:
                errors.append(f"❌ ERRORE CRITICO: Pattern corrotto '{pattern}' trovato (riga {i})")

    return errors, content

def check_forbidden_terms(content, book_key):
    """Check for forbidden terms based on book."""
    errors = []
    config = load_json_config("termini-proibiti.json")

    if not config or book_key not in config:
        return errors

    forbidden = config[book_key]
    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        # Skip comments and metadata
        stripped = line.strip()
        if stripped.startswith('<!--') or stripped.startswith('#'):
            continue
        for term in forbidden:
            # Case-insensitive search with word boundaries
            pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
            matches = pattern.findall(line)
            if matches:
                for match in matches:
                    errors.append(f'❌ ERRORE CRITICO: Termine proibito "{match}" trovato (riga {i})')

    return errors

def check_character_presence(content, chapter_num):
    """Check that required characters are mentioned."""
    warnings = []
    content_lower = content.lower()

    # Core party members (always present from their introduction)
    party = {
        "Zorgar": 1,
        "Sylas": 1,
        "Dain": 1,
        "Aldric": 1,
        "Elara": 1,
        "Mirael": 1,
    }

    for name, from_chapter in party.items():
        if chapter_num >= from_chapter:
            if name.lower() not in content_lower:
                warnings.append(f"⚠️  {name} non menzionato nel capitolo")

    # Fizzle - special attention, from chapter 3
    if chapter_num >= 3:
        if "fizzle" not in content_lower:
            warnings.append(f"❌ ERRORE CRITICO: Fizzle NON menzionato (dal Cap 3 deve essere SEMPRE presente)")

    # Vera - from chapter 10
    if chapter_num >= 10:
        if "vera" not in content_lower:
            warnings.append(f"⚠️  Vera non menzionata (dal Cap 10 fa parte del gruppo)")

    return warnings

def check_canonical_names(content):
    """Check for canonical name usage."""
    warnings = []
    config = load_json_config("nomi-canonici.json")

    if not config:
        return warnings

    for entry in config.get("nomi", []):
        canonical = entry["canonico"]
        wrong_variants = entry.get("varianti_errate", [])

        for variant in wrong_variants:
            pattern = re.compile(r'\b' + re.escape(variant) + r'\b', re.IGNORECASE)
            matches = list(pattern.finditer(content))
            if matches:
                for match in matches:
                    # Find line number
                    line_num = content[:match.start()].count('\n') + 1
                    warnings.append(
                        f'⚠️  Nome non canonico "{match.group()}" trovato (riga {line_num}) '
                        f'— forma corretta: "{canonical}"'
                    )

    # Check roles
    for entry in config.get("ruoli", []):
        wrong_terms = entry.get("varianti_errate", [])
        correct = entry["canonico"]

        for term in wrong_terms:
            pattern = re.compile(r'\b' + re.escape(term) + r'\b', re.IGNORECASE)
            matches = list(pattern.finditer(content))
            if matches:
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    warnings.append(
                        f'⚠️  Terminologia non canonica "{match.group()}" (riga {line_num}) '
                        f'— usare: "{correct}"'
                    )

    return warnings

def main():
    if len(sys.argv) < 2:
        print("Uso: python hooks/narrative-linter.py <file-capitolo>")
        print("Esempio: python hooks/narrative-linter.py libro1-la-scelta/capitoli/capitolo-12.md")
        sys.exit(1)

    filepath = sys.argv[1]

    if not os.path.exists(filepath):
        print(f"❌ File non trovato: {filepath}")
        sys.exit(1)

    filename = os.path.basename(filepath)
    chapter_num = extract_chapter_number(filepath)
    book_key = extract_book_key(filepath)

    print(f"\n=== NARRATIVE LINTER — {filename} ===\n")

    all_errors = []
    all_warnings = []

    # 1. Encoding check
    encoding_errors, content = check_encoding(filepath)
    if encoding_errors:
        all_errors.extend(encoding_errors)
        for e in encoding_errors:
            print(e)
        if content is None:
            print(f"\nRisultato: ❌ {len(all_errors)} errori critici — file non leggibile")
            sys.exit(1)
    else:
        print("✅ Encoding UTF-8 valido")

    # 2. Forbidden terms
    if book_key:
        term_errors = check_forbidden_terms(content, book_key)
        if term_errors:
            all_errors.extend(term_errors)
            for e in term_errors:
                print(e)
        else:
            print("✅ Nessun termine proibito trovato")

    # 3. Character presence
    if chapter_num:
        presence_issues = check_character_presence(content, chapter_num)
        for issue in presence_issues:
            if issue.startswith("❌"):
                all_errors.append(issue)
            else:
                all_warnings.append(issue)
            print(issue)
        if not presence_issues:
            print("✅ Tutti i personaggi presenti")

    # 4. Canonical names
    name_warnings = check_canonical_names(content)
    if name_warnings:
        all_warnings.extend(name_warnings)
        for w in name_warnings:
            print(w)
    else:
        print("✅ Nomi canonici verificati")

    # 5. Word count
    narrative_text = get_narrative_text(content)
    word_count = count_words(narrative_text)
    if word_count < 100:
        print(f"ℹ️  Capitolo non ancora scritto ({word_count} parole)")
    elif word_count < 4500:
        msg = f"⚠️  Lunghezza: {word_count} parole (sotto il minimo di 4.500)"
        all_warnings.append(msg)
        print(msg)
    elif word_count > 6500:
        msg = f"⚠️  Lunghezza: {word_count} parole (sopra il massimo di 6.500)"
        all_warnings.append(msg)
        print(msg)
    else:
        print(f"✅ Lunghezza: {word_count} parole (target: 5.000–5.800)")

    # Summary
    print()
    if all_errors:
        print(f"Risultato: ❌ {len(all_errors)} errori critici, {len(all_warnings)} avvisi")
        sys.exit(1)
    elif all_warnings:
        print(f"Risultato: ⚠️  {len(all_warnings)} avvisi (nessun errore critico)")
        sys.exit(0)
    else:
        print("Risultato: ✅ Tutti i controlli superati")
        sys.exit(0)

if __name__ == "__main__":
    main()
