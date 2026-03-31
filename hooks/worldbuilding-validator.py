#!/usr/bin/env python3
"""
Worldbuilding Validator per Vaelendor.
Verifica coerenza del capitolo con le regole di worldbuilding:
- Capacità vietate per personaggi (Mirael no visioni, etc.)
- Ruoli errati (Tomás non è guaritore)
- Unicità dei luoghi (Millbrook: locanda unica)
- Tono della Chiesa (positivo nel Libro 1)
- Checklist contestuale per revisione umana

Uso: python hooks/worldbuilding-validator.py <file-capitolo>
Esempio: python hooks/worldbuilding-validator.py libro1-la-scelta/capitoli/capitolo-06.md
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


def extract_book_key(filepath):
    match = re.search(r'(libro\d+)', filepath)
    if match:
        return match.group(1)
    return None


def get_narrative_text(content):
    """Extract only narrative text, excluding analysis sections."""
    markers = [
        "## Fine Capitolo", "## Strati Narrativi", "## Elementi a Doppio Strato",
        "## Momenti Chiave", "## Geografia del Capitolo", "## Cinque Scene Salienti",
        "## Note sulla Versione", "## Note Tecniche"
    ]
    for marker in markers:
        idx = content.find(marker)
        if idx != -1:
            content = content[:idx]
    return content


def check_character_capabilities(lines, config, book_id):
    """
    Co-occurrence check: character name + forbidden term within N lines.
    Catches cases like 'Mirael ebbe una visione'.
    """
    issues = []
    caps_config = config.get("personaggi", {}).get("capacita_vietate", [])

    for entry in caps_config:
        libro_check = entry.get("libro", "tutti")
        if libro_check != "tutti" and book_id and libro_check != book_id:
            continue

        personaggio = entry["personaggio"].lower()
        termini = [t.lower() for t in entry["termini"]]
        raggio = entry.get("raggio_righe", 3)
        messaggio = entry["messaggio"]
        severita = entry.get("severita", "errore")
        prefix = "❌ ERRORE CRITICO" if severita == "errore" else "⚠️ "

        reported = set()
        for i, line in enumerate(lines):
            if personaggio not in line.lower():
                continue
            start = max(0, i - raggio)
            end = min(len(lines), i + raggio + 1)
            window_text = " ".join(lines[start:end]).lower()

            for termine in termini:
                pattern = re.compile(r'\b' + re.escape(termine), re.IGNORECASE)
                if pattern.search(window_text) and termine not in reported:
                    issues.append(
                        f'{prefix}: {messaggio} '
                        f'(riga {i + 1}: "{termine}" vicino a "{entry["personaggio"]}")'
                    )
                    reported.add(termine)

    return issues


def check_character_roles(lines, config):
    """
    Pattern check: explicit wrong-role phrases.
    Catches cases like 'Tomás guarì il ferito'.
    """
    issues = []
    roles_config = config.get("personaggi", {}).get("ruoli_errati", [])
    full_text_lower = "\n".join(lines).lower()

    for entry in roles_config:
        pattern_errati = [p.lower() for p in entry["pattern_errati"]]
        messaggio = entry["messaggio"]
        severita = entry.get("severita", "errore")
        prefix = "❌ ERRORE CRITICO" if severita == "errore" else "⚠️ "

        for pattern in pattern_errati:
            if pattern in full_text_lower:
                for i, line in enumerate(lines, 1):
                    if pattern in line.lower():
                        issues.append(f'{prefix}: {messaggio} (riga {i})')
                        break

    return issues


def check_location_uniqueness(lines, config):
    """
    If a synonym for a unique location appears and the canonical name does NOT appear
    anywhere in the chapter, flag it for review.
    (Warning, not error — synonyms in a chapter that already names the canonical location
    are almost certainly anaphoric references to it.)
    """
    issues = []
    locations = config.get("luoghi", {}).get("unicita", [])
    full_text_lower = "\n".join(lines).lower()

    for entry in locations:
        nome_canonico = entry["nome"].lower()
        nome_alias = nome_canonico.split()[1] if len(nome_canonico.split()) > 1 else nome_canonico
        sinonimi = [s.lower() for s in entry["sinonimi"]]
        messaggio = entry["messaggio"]
        severita = entry.get("severita", "avviso")
        prefix = "❌ ERRORE CRITICO" if severita == "errore" else "⚠️ "

        # If the canonical name appears anywhere in the chapter, synonyms are fine
        if nome_canonico in full_text_lower or nome_alias in full_text_lower:
            continue

        # Canonical name absent — any synonym is suspicious
        for i, line in enumerate(lines):
            if any(s in line.lower() for s in sinonimi):
                issues.append(f'{prefix}: {messaggio} (riga {i + 1})')
                break

    return issues


def check_church_tone(lines, config, book_id):
    """
    If a negative term appears within N lines of a church-context term,
    flag as error (libro1 only by default).
    """
    issues = []
    chiesa_config = config.get("chiesa", {})

    libro_config = chiesa_config.get(book_id) if book_id else None
    if not libro_config:
        return issues

    termini_negativi = [t.lower() for t in libro_config.get("termini_negativi", [])]
    contesto = [c.lower() for c in libro_config.get("contesto_attivazione", [])]
    raggio = libro_config.get("raggio_righe", 5)
    messaggio = libro_config.get("messaggio", "Violazione tono Chiesa")
    severita = libro_config.get("severita", "errore")
    prefix = "❌ ERRORE CRITICO" if severita == "errore" else "⚠️ "

    for i, line in enumerate(lines):
        if not any(c in line.lower() for c in contesto):
            continue
        start = max(0, i - raggio)
        end = min(len(lines), i + raggio + 1)
        window_text = " ".join(lines[start:end]).lower()

        for termine in termini_negativi:
            if termine in window_text:
                issues.append(
                    f'{prefix}: {messaggio} '
                    f'(riga {i + 1}: "{termine}" in contesto ecclesiale)'
                )
                return issues  # One error is enough

    return issues


def print_human_checklist(content, config):
    """Print contextual review checklist based on topics detected in the chapter."""
    checklist = config.get("checklist_umana", {})
    content_lower = content.lower()

    active_topics = []
    for topic, data in checklist.items():
        triggers = data.get("trigger", [])
        if any(t in content_lower for t in triggers):
            active_topics.append((topic, data))

    if not active_topics:
        return

    print("--- Checklist revisione umana ---")
    for topic, data in active_topics:
        domande = data.get("domande", [])
        print(f"ℹ️  Topic '{topic}' rilevato — verificare:")
        for d in domande:
            print(f"    [ ] {d}")


def main():
    if len(sys.argv) < 2:
        print("Uso: python hooks/worldbuilding-validator.py <file-capitolo>")
        print("Esempio: python hooks/worldbuilding-validator.py libro1-la-scelta/capitoli/capitolo-06.md")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"❌ File non trovato: {filepath}")
        sys.exit(1)

    filename = os.path.basename(filepath)
    book_id = extract_book_key(filepath)

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    config = load_json_config("regole-worldbuilding.json")
    if not config:
        print("⚠️  Config worldbuilding non trovata — validazione saltata")
        sys.exit(0)

    narrative = get_narrative_text(content)
    lines = narrative.split('\n')

    print(f"\n=== WORLDBUILDING VALIDATOR — {filename} ===\n")

    all_errors = []
    all_warnings = []

    # 1. Capacità vietate per personaggi
    cap_issues = check_character_capabilities(lines, config, book_id)
    cap_errors = [e for e in cap_issues if e.startswith("❌")]
    cap_warnings = [e for e in cap_issues if e.startswith("⚠️")]
    if cap_issues:
        all_errors.extend(cap_errors)
        all_warnings.extend(cap_warnings)
        for e in cap_issues:
            print(e)
    else:
        print("✅ Nessuna violazione capacità personaggi")

    # 2. Ruoli errati
    role_issues = check_character_roles(lines, config)
    role_errors = [e for e in role_issues if e.startswith("❌")]
    role_warnings = [e for e in role_issues if e.startswith("⚠️")]
    if role_issues:
        all_errors.extend(role_errors)
        all_warnings.extend(role_warnings)
        for e in role_issues:
            print(e)
    else:
        print("✅ Nessun ruolo errato rilevato")

    # 3. Unicità luoghi
    loc_issues = check_location_uniqueness(lines, config)
    loc_errors = [e for e in loc_issues if e.startswith("❌")]
    loc_warnings = [e for e in loc_issues if e.startswith("⚠️")]
    if loc_issues:
        all_errors.extend(loc_errors)
        all_warnings.extend(loc_warnings)
        for e in loc_issues:
            print(e)
    else:
        print("✅ Coerenza luoghi verificata")

    # 4. Tono Chiesa (solo libro1)
    if book_id == "libro1":
        church_issues = check_church_tone(lines, config, book_id)
        church_errors = [e for e in church_issues if e.startswith("❌")]
        church_warnings = [e for e in church_issues if e.startswith("⚠️")]
        if church_issues:
            all_errors.extend(church_errors)
            all_warnings.extend(church_warnings)
            for e in church_issues:
                print(e)
        else:
            print("✅ Tono Chiesa coerente con Libro 1")

    # 5. Checklist revisione umana
    print()
    print_human_checklist(narrative, config)

    # Summary
    print()
    if all_errors:
        print(f"Risultato: ❌ {len(all_errors)} errori critici, {len(all_warnings)} avvisi")
        sys.exit(1)
    elif all_warnings:
        print(f"Risultato: ⚠️  {len(all_warnings)} avvisi (nessun errore critico)")
        sys.exit(0)
    else:
        print("Risultato: ✅ Coerente con le regole di worldbuilding")
        sys.exit(0)


if __name__ == "__main__":
    main()
