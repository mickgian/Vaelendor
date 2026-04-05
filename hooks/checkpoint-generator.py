#!/usr/bin/env python3
"""
Checkpoint Generator per Vaelendor.
Genera o aggiorna il checkpoint dopo un capitolo.

Uso: python hooks/checkpoint-generator.py <file-capitolo>
Esempio: python hooks/checkpoint-generator.py libro1-la-scelta/capitoli/capitolo-12.md
"""

import sys
import os
import re

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
    book_dir = book_dir_match.group(1) if book_dir_match else None

    return book_dir, chapter_num

def read_file_safe(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def get_party_members(chapter_num):
    """Return list of party members based on chapter number."""
    # Prologo e epilogo: tutti presenti
    if chapter_num in ("pro", "epi"):
        return ["Zorgar", "Sylas", "Dain", "Aldric", "Elara", "Mirael (+Micio)", "Fizzle", "Vera"]
    members = ["Zorgar", "Sylas", "Dain", "Aldric", "Elara", "Mirael (+Micio)"]
    if chapter_num >= 3:
        members.append("Fizzle")
    if chapter_num >= 10:
        members.append("Vera")
    return members

def main():
    if len(sys.argv) < 2:
        print("Uso: python hooks/checkpoint-generator.py <file-capitolo>")
        print("Esempio: python hooks/checkpoint-generator.py libro1-la-scelta/capitoli/capitolo-12.md")
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

    # Paths
    checkpoint_dir = os.path.join(project_root, book_dir, "checkpoint")
    if chapter_num == "pro":
        checkpoint_path = os.path.join(checkpoint_dir, "dopo-prologo.md")
        prev_checkpoint_path = None
    elif chapter_num == "epi":
        checkpoint_path = os.path.join(checkpoint_dir, "dopo-epilogo.md")
        # Previous = last numbered checkpoint
        import glob
        caps = sorted(glob.glob(os.path.join(checkpoint_dir, "dopo-capitolo-*.md")))
        prev_checkpoint_path = caps[-1] if caps else None
    else:
        checkpoint_path = os.path.join(checkpoint_dir, f"dopo-capitolo-{chapter_num:02d}.md")
        if chapter_num == 1:
            prev_checkpoint_path = os.path.join(checkpoint_dir, "dopo-prologo.md")
        else:
            prev_checkpoint_path = os.path.join(checkpoint_dir, f"dopo-capitolo-{chapter_num-1:02d}.md")

    # Read chapter
    with open(filepath, "r", encoding="utf-8") as f:
        chapter_content = f.read()

    # Read previous checkpoint
    prev_checkpoint = read_file_safe(prev_checkpoint_path) if prev_checkpoint_path else None

    # Read existing checkpoint
    existing_checkpoint = read_file_safe(checkpoint_path)

    cap_label = "Prologo" if chapter_num == "pro" else "Epilogo" if chapter_num == "epi" else f"Capitolo {chapter_num:02d}"
    print(f"\n=== CHECKPOINT GENERATOR — {cap_label} ===\n")

    # Check if chapter has actual content
    narrative_lines = [l for l in chapter_content.split('\n')
                      if l.strip() and not l.startswith('#') and not l.startswith('**')
                      and not l.startswith('---') and not l.startswith('<!--')]

    if len(narrative_lines) < 10:
        print("ℹ️  Il capitolo non sembra avere ancora contenuto narrativo sufficiente.")
        print("    Il checkpoint deve essere scritto manualmente dopo la stesura del capitolo.")
        print(f"\n📄 File checkpoint: {checkpoint_path}")
        if existing_checkpoint:
            print("    (checkpoint esistente trovato)")
        else:
            print("    (checkpoint da creare)")
        sys.exit(0)

    # Show context
    if prev_checkpoint:
        print("📋 Checkpoint precedente trovato:")
        # Show summary from previous checkpoint
        for line in prev_checkpoint.split('\n'):
            if line.startswith('## '):
                print(f"   {line}")
    else:
        if prev_checkpoint_path:
            print(f"⚠️  Checkpoint precedente ({os.path.basename(prev_checkpoint_path)}) non trovato!")

    print()

    # Party members for this chapter
    members = get_party_members(chapter_num)
    print(f"👥 Membri del party ({cap_label}): {', '.join(members)}")
    print()

    if existing_checkpoint:
        print("📄 Checkpoint esistente trovato — da AGGIORNARE manualmente.")
        print(f"   Percorso: {checkpoint_path}")
        print()
        print("   Sezioni da verificare/aggiornare:")
        print("   - Giorno nella timeline")
        print("   - Luogo attuale del party")
        print("   - Riassunto eventi chiave")
        print("   - Conseguenze immediate")
        print("   - Relazioni modificate")
        print("   - Oggetti acquisiti/persi")
        print("   - Semi piantati")
        print("   - Vincoli per il capitolo successivo")
    else:
        print(f"📄 Checkpoint da creare: {checkpoint_path}")
        print()
        # Generate template
        template = f"""# Checkpoint — Dopo {cap_label}

## Giorno nella Timeline
[Da compilare]

## Luogo Attuale del Party
[Da compilare]

## Membri del Party Presenti
{chr(10).join('- ' + m for m in members)}

## Riassunto Eventi Chiave
[Da compilare — 3-5 righe]

## Conseguenze Immediate
[Da compilare]

## Relazioni Modificate
[Da compilare]

## Oggetti Acquisiti/Persi
[Da compilare]

## Semi Piantati
[Da compilare]

## Vincoli per il Capitolo Successivo
[Da compilare]
"""
        os.makedirs(checkpoint_dir, exist_ok=True)
        with open(checkpoint_path, "w", encoding="utf-8") as f:
            f.write(template)
        print(f"✅ Template checkpoint creato: {checkpoint_path}")
        print("   ⚠️  Compilare manualmente con i dettagli del capitolo!")

    # Check propagation
    if chapter_num == "pro":
        next_checkpoint_path = os.path.join(checkpoint_dir, "dopo-capitolo-01.md")
    elif chapter_num == "epi":
        next_checkpoint_path = None
    else:
        next_checkpoint_path = os.path.join(checkpoint_dir, f"dopo-capitolo-{chapter_num+1:02d}.md")
    if next_checkpoint_path and os.path.exists(next_checkpoint_path):
        next_content = read_file_safe(next_checkpoint_path)
        if next_content and "[Da compilare]" not in next_content and "[Da definire]" not in next_content:
            print()
            print(f"⚠️  PROPAGAZIONE: Il checkpoint dopo-capitolo-{chapter_num+1:02d}.md "
                  f"esiste già e potrebbe essere invalidato dalle modifiche!")

    print()
    print("✅ Checkpoint generator completato.")

if __name__ == "__main__":
    main()
