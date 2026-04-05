#!/usr/bin/env python3
"""
Review Report per Vaelendor — Modalità 2 (Revisione).
Genera un rapporto di revisione completo per un capitolo scritto dall'utente.

Uso: python hooks/review-report.py <file-capitolo>
Esempio: python hooks/review-report.py libro1-la-scelta/capitoli/capitolo-12.md
"""

import sys
import os
import re
import subprocess

def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))

def get_project_root():
    return os.path.dirname(get_script_dir())

def extract_chapter_info(filepath):
    basename = os.path.basename(filepath)
    if basename == "prologo.md":
        chapter_num = "pro"
    elif basename == "epilogo.md":
        chapter_num = "epi"
    else:
        chapter_match = re.search(r'capitolo-(\d+)', basename)
        chapter_num = int(chapter_match.group(1)) if chapter_match else None

    book_dir_match = re.search(r'(libro\d+-[^/]+)', filepath)
    book_match = re.search(r'(libro\d+)', filepath)
    book_dir = book_dir_match.group(1) if book_dir_match else None
    book_id = book_match.group(1) if book_match else None

    return book_id, book_dir, chapter_num

def read_file_safe(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def run_hook(script_name, filepath):
    """Run a hook script and capture output."""
    script_dir = get_script_dir()
    script_path = os.path.join(script_dir, script_name)

    try:
        result = subprocess.run(
            [sys.executable, script_path, filepath],
            capture_output=True, text=True, timeout=30
        )
        return result.stdout, result.stderr, result.returncode
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return "", str(e), 1

def count_words(text):
    """Count words excluding metadata and analysis sections."""
    # Remove analysis sections
    markers = ["## Strati Narrativi", "## Elementi a Doppio Strato", "## Momenti Chiave"]
    for marker in markers:
        idx = text.find(marker)
        if idx != -1:
            text = text[:idx]

    lines = text.split('\n')
    word_count = 0
    for line in lines:
        stripped = line.strip()
        if (stripped.startswith('#') or stripped.startswith('**POV:') or
            stripped.startswith('**Giorno') or stripped.startswith('**Luogo') or
            stripped.startswith('---') or stripped.startswith('<!--') or stripped == ''):
            continue
        word_count += len(stripped.split())
    return word_count

def analyze_tone(content):
    """Rough estimate of warmth vs unease ratio."""
    warmth_indicators = [
        "sorrise", "rise", "ridere", "abbracci", "amico", "calore",
        "scherzò", "battuta", "compagno", "fiducia", "insieme",
        "sorriso", "allegr", "gioia", "confort"
    ]
    unease_indicators = [
        "ombra", "oscur", "freddo", "paura", "timore", "inquiet",
        "silenzio", "strano", "sbagliato", "dolore", "pericolo",
        "minacci", "tenebr", "incubo", "angosci"
    ]

    content_lower = content.lower()
    warmth_count = sum(1 for w in warmth_indicators if w in content_lower)
    unease_count = sum(1 for w in unease_indicators if w in content_lower)

    total = warmth_count + unease_count
    if total == 0:
        return 50, 50  # No indicators found

    warmth_pct = int((warmth_count / total) * 100)
    unease_pct = 100 - warmth_pct
    return warmth_pct, unease_pct

def get_party_members(chapter_num):
    if chapter_num in ("pro", "epi"):
        return ["Zorgar", "Sylas", "Dain", "Aldric", "Elara", "Mirael", "Fizzle", "Vera"]
    members = ["Zorgar", "Sylas", "Dain", "Aldric", "Elara", "Mirael"]
    if chapter_num >= 3:
        members.append("Fizzle")
    if chapter_num >= 10:
        members.append("Vera")
    return members

def main():
    if len(sys.argv) < 2:
        print("Uso: python hooks/review-report.py <file-capitolo>")
        print("Esempio: python hooks/review-report.py libro1-la-scelta/capitoli/capitolo-12.md")
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

    cap_label = "Prologo" if chapter_num == "pro" else "Epilogo" if chapter_num == "epi" else f"Capitolo {chapter_num:02d}"
    print(f"\n{'='*60}")
    print(f"  RAPPORTO DI REVISIONE — {cap_label}")
    print(f"{'='*60}\n")

    # Run linter
    print("--- Esecuzione Narrative Linter ---")
    linter_out, linter_err, linter_code = run_hook("narrative-linter.py", filepath)
    if linter_out:
        print(linter_out)
    if linter_err:
        print(f"  (Errori: {linter_err})")

    # Run validator
    print("--- Esecuzione Tracker Validator ---")
    validator_out, validator_err, validator_code = run_hook("tracker-validator.py", filepath)
    if validator_out:
        print(validator_out)
    if validator_err:
        print(f"  (Errori: {validator_err})")

    # Character analysis
    print(f"\n{'='*60}")
    print("  ANALISI PERSONAGGI")
    print(f"{'='*60}\n")

    if chapter_num:
        members = get_party_members(chapter_num)
        content_lower = content.lower()

        print("Presenze:")
        for member in members:
            present = member.lower() in content_lower
            status = "✅ presente" if present else "❌ ASSENTE"
            extra = ""
            if member == "Fizzle" and not present and chapter_num >= 3:
                extra = " ⚠️ CRITICO: deve essere sempre presente!"
            print(f"  {member}: {status}{extra}")

        print()
        print("Voce e dialogo:")
        print("  [Verificare manualmente che ogni personaggio parli in modo coerente")
        print("   con il suo profilo in personaggi/party/]")

        print()
        print("Conoscenze:")
        print("  [Verificare che nessun personaggio sappia cose che non dovrebbe")
        print("   secondo memoria-personaggi/]")

    # Style analysis
    print(f"\n{'='*60}")
    print("  STILE E TONO")
    print(f"{'='*60}\n")

    # Word count
    word_count = count_words(content)
    wc_status = "✅" if 5000 <= word_count <= 5800 else "⚠️"
    print(f"Lunghezza: {wc_status} {word_count} parole (target: 5.000–5.800)")

    # Tone analysis
    warmth, unease = analyze_tone(content)
    tone_status = "✅" if 75 <= warmth <= 95 else "⚠️"
    print(f"Tono: {tone_status} ~{warmth}% calore, ~{unease}% inquietudine (target: 85/15)")

    # Worldbuilding style
    print("Worldbuilding: [Verificare manualmente — integrato nell'azione o espositivo?]")

    # POV check
    pov_rotation = {1: "Zorgar", 2: "Elara", 3: "Dain"}
    if chapter_num and chapter_num in pov_rotation:
        expected_pov = pov_rotation[chapter_num]
        print(f"POV: atteso {expected_pov} (verificare coerenza)")

    # Summary
    print(f"\n{'='*60}")
    print("  RIEPILOGO")
    print(f"{'='*60}\n")

    has_critical = linter_code != 0 or validator_code != 0

    if has_critical:
        print("⚠️  Il capitolo presenta errori che devono essere corretti.")
        print("   Controllare i risultati del linter e del validator sopra.")
    else:
        print("✅ Nessun errore critico rilevato.")
        print("   Verificare manualmente le sezioni contrassegnate come [Verificare manualmente].")

    print()
    print("Prossimi passi:")
    print("  1. Correggere eventuali errori critici")
    print("  2. Verificare le segnalazioni manuali")
    cp_name = "dopo-prologo" if chapter_num == "pro" else "dopo-epilogo" if chapter_num == "epi" else f"dopo-capitolo-{chapter_num:02d}"
    print(f"  3. Aggiornare checkpoint/{cp_name}.md")
    print("  4. Aggiornare le memorie dei personaggi coinvolti")
    print()

if __name__ == "__main__":
    main()
