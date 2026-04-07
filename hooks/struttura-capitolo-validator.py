#!/usr/bin/env python3
"""
Struttura Capitolo Validator per Vaelendor.
Verifica che tutte le sezioni di fine capitolo siano presenti e complete.

Uso: python hooks/struttura-capitolo-validator.py <file-capitolo>
Esempio: python hooks/struttura-capitolo-validator.py libro1-la-scelta/capitoli/capitolo-10.md
"""

import sys
import os
import re


# Sezioni obbligatorie nell'ordine atteso
REQUIRED_SECTIONS = [
    "## Fine Capitolo",
    "## Geografia del Capitolo",
    "## Scene Salienti",
    "## Scene Consigliate per Illustrazione",
    "## Strati Narrativi",
    "## Voci Narrative",          # match anche "Voci Narrative del Capitolo"
    "## Worldbuilding Integrato",
    "## Note Tecniche",
]

# Sotto-sezioni obbligatorie dentro Strati Narrativi
STRATI_SUBSECTIONS = [
    "### Strato di Superficie",
    "### Strato Nascosto",
    "### Elementi a Doppio Strato",
]

# Keyword obbligatorie dentro Note Tecniche
NOTE_TECNICHE_KEYWORDS = [
    "POV",
    "Tono",
    "Funzione",
    "Setup per Capitolo",
    "Momenti Chiave per Personaggio",
]

MIN_SCENE_SALIENTI = 5


def extract_chapter_number(filepath):
    match = re.search(r'capitolo-(\d+)', os.path.basename(filepath))
    if match:
        return int(match.group(1))
    return None


def is_draft(content):
    """Check if the chapter is just a draft/outline (under 500 narrative words)."""
    markers = ["## Fine Capitolo", "## Strati Narrativi", "## Geografia del Capitolo",
               "## Note Tecniche", "## Scene Salienti"]
    narrative = content
    for marker in markers:
        idx = narrative.find(marker)
        if idx != -1:
            narrative = narrative[:idx]
    words = len(narrative.split())
    return words < 500


def get_section_content(content, section_header, next_headers):
    """Extract text between a section header and the next section header."""
    # Find the section with flexible matching
    pattern = re.compile(r'^' + re.escape(section_header), re.MULTILINE)
    match = pattern.search(content)
    if not match:
        # Try partial match for "Voci Narrative" which can be "Voci Narrative del Capitolo"
        if "Voci Narrative" in section_header:
            pattern = re.compile(r'^## Voci Narrative', re.MULTILINE)
            match = pattern.search(content)
        if not match:
            return None

    start = match.end()

    # Find the next section header
    end = len(content)
    for nh in next_headers:
        nh_pattern = re.compile(r'^## ', re.MULTILINE)
        for nh_match in nh_pattern.finditer(content[start:]):
            candidate_end = start + nh_match.start()
            if candidate_end < end:
                end = candidate_end
                break

    return content[start:end].strip()


def check_section_present(content, section_name):
    """Check if a section header exists in the content."""
    if "Voci Narrative" in section_name:
        # Flexible match: "## Voci Narrative" or "## Voci Narrative del Capitolo"
        return bool(re.search(r'^## Voci Narrative', content, re.MULTILINE))
    return section_name in content


def count_scene_salienti(content):
    """Count numbered entries in Scene Salienti section."""
    # Find Scene Salienti section
    match = re.search(r'^## Scene Salienti\b', content, re.MULTILINE)
    if not match:
        return 0

    start = match.end()

    # Find next ## section
    next_section = re.search(r'^## [^#]', content[start:], re.MULTILINE)
    end = start + next_section.start() if next_section else len(content)

    section_text = content[start:end]

    # Count ### entries (### 1., ### 2., etc.)
    entries = re.findall(r'^### \d+\.', section_text, re.MULTILINE)
    return len(entries)


def check_strati_subsections(content):
    """Check for required subsections within Strati Narrativi."""
    missing = []
    for sub in STRATI_SUBSECTIONS:
        if sub not in content:
            missing.append(sub)
    return missing


def check_note_tecniche_keywords(content):
    """Check for required keywords within Note Tecniche section."""
    match = re.search(r'^## Note Tecniche\b', content, re.MULTILINE)
    if not match:
        return NOTE_TECNICHE_KEYWORDS  # All missing

    start = match.end()
    # Find next ## section or end
    next_section = re.search(r'^## [^#]', content[start:], re.MULTILINE)
    end = start + next_section.start() if next_section else len(content)

    section_text = content[start:end]

    missing = []
    for keyword in NOTE_TECNICHE_KEYWORDS:
        if keyword not in section_text:
            missing.append(keyword)
    return missing


def main():
    if len(sys.argv) < 2:
        print("Uso: python hooks/struttura-capitolo-validator.py <file-capitolo>")
        sys.exit(1)

    filepath = sys.argv[1]

    if not os.path.exists(filepath):
        print(f"❌ File non trovato: {filepath}")
        sys.exit(1)

    filename = os.path.basename(filepath)
    chapter_num = extract_chapter_number(filepath)

    print(f"\n=== STRUTTURA CAPITOLO VALIDATOR — {filename} ===\n")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip validation for drafts
    if is_draft(content):
        print("ℹ️  Capitolo in bozza (< 500 parole narrative) — validazione struttura saltata")
        sys.exit(0)

    all_errors = []
    all_warnings = []

    # 1. Check required sections
    print("📋 Sezioni obbligatorie:")
    missing_sections = []
    for section in REQUIRED_SECTIONS:
        if check_section_present(content, section):
            print(f"  ✅ {section}")
        else:
            display_name = section
            missing_sections.append(display_name)
            msg = f"  ❌ MANCANTE: {display_name}"
            all_errors.append(msg)
            print(msg)

    if not missing_sections:
        print("  ✅ Tutte le sezioni presenti")

    # 2. Check Scene Salienti count
    print()
    print("🎬 Scene Salienti:")
    scene_count = count_scene_salienti(content)
    if scene_count >= MIN_SCENE_SALIENTI:
        print(f"  ✅ {scene_count} scene (minimo: {MIN_SCENE_SALIENTI})")
    elif scene_count > 0:
        msg = f"  ❌ Solo {scene_count} scene (minimo richiesto: {MIN_SCENE_SALIENTI})"
        all_errors.append(msg)
        print(msg)
    else:
        if "## Scene Salienti" not in content:
            print("  ⚠️  Sezione non trovata (già segnalato sopra)")
        else:
            msg = f"  ❌ Nessuna scena trovata (formato atteso: ### 1. Titolo)"
            all_errors.append(msg)
            print(msg)

    # 3. Check Strati Narrativi subsections
    print()
    print("📖 Strati Narrativi:")
    missing_strati = check_strati_subsections(content)
    if not missing_strati:
        print("  ✅ Tutte le sotto-sezioni presenti")
    else:
        for sub in missing_strati:
            msg = f"  ❌ MANCANTE: {sub}"
            all_errors.append(msg)
            print(msg)

    # 4. Check Note Tecniche keywords
    print()
    print("📝 Note Tecniche:")
    missing_keywords = check_note_tecniche_keywords(content)
    if not missing_keywords:
        print("  ✅ Tutte le sotto-sezioni presenti")
    else:
        for kw in missing_keywords:
            msg = f"  ❌ MANCANTE in Note Tecniche: {kw}"
            all_errors.append(msg)
            print(msg)

    # Summary
    print()
    if all_errors:
        print(f"Risultato: ❌ {len(all_errors)} sezioni mancanti o incomplete")
        sys.exit(1)
    elif all_warnings:
        print(f"Risultato: ⚠️  {len(all_warnings)} avvisi")
        sys.exit(0)
    else:
        print("Risultato: ✅ Struttura capitolo completa")
        sys.exit(0)


if __name__ == "__main__":
    main()