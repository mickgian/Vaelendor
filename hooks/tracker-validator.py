#!/usr/bin/env python3
"""
Tracker Validator per Vaelendor.
Verifica coerenza tra un capitolo e tutti i tracker della serie.

Uso: python hooks/tracker-validator.py <file-capitolo>
Esempio: python hooks/tracker-validator.py libro1-la-scelta/capitoli/capitolo-12.md
"""

import sys
import os
import re

def get_project_root():
    """Get project root (parent of hooks/)."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read_file_safe(filepath):
    """Read a file safely, return empty string if not found."""
    if not os.path.exists(filepath):
        return ""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def extract_chapter_info(filepath):
    """Extract book and chapter number from filepath."""
    basename = os.path.basename(filepath)
    if basename == "prologo.md":
        chapter_num = "pro"
    elif basename == "epilogo.md":
        chapter_num = "epi"
    else:
        chapter_match = re.search(r'capitolo-(\d+)', basename)
        chapter_num = int(chapter_match.group(1)) if chapter_match else None

    book_match = re.search(r'(libro\d+)-', filepath)
    book_id = book_match.group(1) if book_match else None
    book_dir_match = re.search(r'(libro\d+-[^/]+)', filepath)
    book_dir = book_dir_match.group(1) if book_dir_match else None

    return book_id, book_dir, chapter_num

def extract_proper_nouns(text):
    """Extract potential proper nouns (capitalized words) from text."""
    # Find words that start with uppercase (potential names)
    words = re.findall(r'\b([A-Z][a-zà-ú]+)\b', text)
    # Filter out common Italian sentence starters
    common_starts = {
        "Il", "La", "Lo", "Le", "Li", "Gli", "Un", "Una", "Uno",
        "Di", "Da", "In", "Con", "Su", "Per", "Tra", "Fra",
        "Ma", "Se", "Che", "Non", "Come", "Quando", "Dove",
        "Poi", "Anche", "Così", "Già", "Più", "Ogni", "Quale",
        "Era", "Aveva", "Disse", "Rispose", "Guardò", "Sentì",
    }
    return [w for w in set(words) if w not in common_starts]

def check_deaths(content, project_root):
    """Check that dead characters don't appear alive."""
    errors = []
    morti_path = os.path.join(project_root, "serie", "tracker", "morti.md")
    morti_content = read_file_safe(morti_path)

    if not morti_content or "Nessun morto ancora" in morti_content:
        return errors

    # Extract dead character names from the table
    dead_names = []
    for line in morti_content.split('\n'):
        if '|' in line and not line.strip().startswith('|---') and 'Personaggio' not in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 2 and parts[1] and not parts[1].startswith('<!--'):
                dead_names.append(parts[1])

    # Flashback indicators that allow mentioning dead characters
    flashback_indicators = [
        "ricordò", "pensò a", "la voce di", "il ricordo di",
        "aveva detto", "quella volta", "un tempo", "in passato"
    ]

    for name in dead_names:
        if not name:
            continue
        pattern = re.compile(r'\b' + re.escape(name) + r'\b', re.IGNORECASE)
        for i, line in enumerate(content.split('\n'), 1):
            if pattern.search(line):
                # Check if it's in a flashback context
                line_lower = line.lower()
                is_flashback = any(ind in line_lower for ind in flashback_indicators)
                if not is_flashback:
                    errors.append(
                        f'❌ CONTRADDIZIONE: "{name}" è registrato come morto '
                        f'ma appare vivo (riga {i}). Se è un flashback, '
                        f'usare indicatori come "ricordò", "pensò a", ecc.'
                    )

    return errors

def check_world_rules(content, project_root):
    """Check consistency with established world rules."""
    warnings = []
    rules_path = os.path.join(project_root, "serie", "tracker", "regole-mondo.md")
    rules_content = read_file_safe(rules_path)

    if not rules_content:
        return warnings

    # Check for travel time mentions
    travel_pattern = re.compile(
        r'(?:viaggio|cammino|cavalcata|marcia).*?(?:durò|richiese|impiegò).*?'
        r'(\d+)\s*(?:giorni|ore|settimane)',
        re.IGNORECASE
    )
    matches = travel_pattern.finditer(content)
    for match in matches:
        warnings.append(
            f'⚠️  Tempo di viaggio menzionato: "{match.group()}" — '
            f'verificare coerenza con regole-mondo.md'
        )

    return warnings

def check_revelations(content, project_root, book_id, chapter_num):
    """Check that no character references future knowledge."""
    warnings = []
    riv_path = os.path.join(project_root, "serie", "tracker", "rivelazioni.md")
    riv_content = read_file_safe(riv_path)

    if not riv_content:
        return warnings

    # Parse planned revelations
    in_planned = False
    for line in riv_content.split('\n'):
        if "Pianificate" in line or "NON ancora" in line:
            in_planned = True
            continue
        if in_planned and '|' in line and not line.strip().startswith('|---'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 2 and parts[1] and not parts[1].startswith('<!--'):
                revelation = parts[1]
                # Check if the chapter text mentions this revelation
                if revelation.lower() in content.lower():
                    warnings.append(
                        f'⚠️  Possibile rivelazione prematura: "{revelation}" '
                        f'è pianificata per un momento futuro'
                    )

    return warnings

def check_relationships(content, project_root):
    """Check relationship consistency."""
    warnings = []
    rel_path = os.path.join(project_root, "serie", "tracker", "relazioni.md")
    rel_content = read_file_safe(rel_path)

    if not rel_content or "Aggiungere relazioni" in rel_content:
        return warnings

    # Basic check: if relationships are tracked, note for manual review
    if len(rel_content.split('\n')) > 15:
        warnings.append(
            "ℹ️  Relazioni tra personaggi registrate nel tracker — "
            "verificare manualmente la coerenza del tono"
        )

    return warnings

def check_foreshadowing(content, project_root):
    """Check foreshadowing seeds."""
    notes = []
    fore_path = os.path.join(project_root, "serie", "tracker", "foreshadowing-cross.md")
    fore_content = read_file_safe(fore_path)

    if not fore_content:
        return notes

    # Check for seed collection markers
    if "🌱" in fore_content:
        active_seeds = [line for line in fore_content.split('\n')
                       if "🌱" in line and '|' in line]
        if active_seeds:
            notes.append(
                f"ℹ️  {len(active_seeds)} semi attivi nel tracker foreshadowing — "
                f"verificare se qualcuno germoglia in questo capitolo"
            )

    return notes

def check_geopolitics(content, project_root):
    """Check geopolitical consistency."""
    warnings = []
    geo_path = os.path.join(project_root, "serie", "tracker", "geopolitica.md")
    geo_content = read_file_safe(geo_path)

    if not geo_content:
        return warnings

    # Check for mentions of power structures, factions
    power_terms = ["re ", "regina", "governatore", "lord", "consiglio", "trono"]
    content_lower = content.lower()

    for term in power_terms:
        if term in content_lower:
            warnings.append(
                f'ℹ️  Riferimento a struttura di potere ("{term.strip()}") trovato — '
                f'verificare coerenza con geopolitica.md'
            )
            break  # One warning is enough

    return warnings

def main():
    if len(sys.argv) < 2:
        print("Uso: python hooks/tracker-validator.py <file-capitolo>")
        print("Esempio: python hooks/tracker-validator.py libro1-la-scelta/capitoli/capitolo-12.md")
        sys.exit(1)

    filepath = sys.argv[1]

    if not os.path.exists(filepath):
        print(f"❌ File non trovato: {filepath}")
        sys.exit(1)

    project_root = get_project_root()
    book_id, book_dir, chapter_num = extract_chapter_info(filepath)
    filename = os.path.basename(filepath)

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    print(f"\n=== TRACKER VALIDATOR — {filename} ===\n")

    all_errors = []
    all_warnings = []
    all_notes = []

    # 1. Check deaths
    death_errors = check_deaths(content, project_root)
    if death_errors:
        all_errors.extend(death_errors)
        for e in death_errors:
            print(e)
    else:
        print("✅ Nessun conflitto con registro morti")

    # 2. Check world rules
    rule_warnings = check_world_rules(content, project_root)
    if rule_warnings:
        all_warnings.extend(rule_warnings)
        for w in rule_warnings:
            print(w)
    else:
        print("✅ Nessun conflitto con regole del mondo")

    # 3. Check revelations
    rev_warnings = check_revelations(content, project_root, book_id, chapter_num)
    if rev_warnings:
        all_warnings.extend(rev_warnings)
        for w in rev_warnings:
            print(w)
    else:
        print("✅ Nessuna rivelazione prematura rilevata")

    # 4. Check relationships
    rel_warnings = check_relationships(content, project_root)
    if rel_warnings:
        all_notes.extend(rel_warnings)
        for w in rel_warnings:
            print(w)
    else:
        print("✅ Relazioni — nessun conflitto rilevato")

    # 5. Check foreshadowing
    fore_notes = check_foreshadowing(content, project_root)
    if fore_notes:
        all_notes.extend(fore_notes)
        for n in fore_notes:
            print(n)
    else:
        print("✅ Foreshadowing — nessuna azione richiesta")

    # 6. Check geopolitics
    geo_warnings = check_geopolitics(content, project_root)
    if geo_warnings:
        all_notes.extend(geo_warnings)
        for w in geo_warnings:
            print(w)
    else:
        print("✅ Geopolitica — nessun conflitto rilevato")

    # Summary
    print()
    if all_errors:
        print(f"Risultato: ❌ {len(all_errors)} contraddizioni, "
              f"{len(all_warnings)} avvisi, {len(all_notes)} note")
        sys.exit(1)
    elif all_warnings:
        print(f"Risultato: ⚠️  {len(all_warnings)} avvisi, {len(all_notes)} note "
              f"(nessuna contraddizione)")
        sys.exit(0)
    else:
        print(f"Risultato: ✅ Coerente con tutti i tracker")
        sys.exit(0)

if __name__ == "__main__":
    main()
