#!/usr/bin/env python3
"""
sync-antispoiler.py — Sincronizza strumenti/anti-spoiler.md
verso hooks/config/anti-spoiler.json.

Eseguire ogni volta che si modifica anti-spoiler.md:
  python3 hooks/sync-antispoiler.py

Opzionale: aggiungere a post-edit.sh o a un pre-commit hook git.
"""

import re
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
SOURCE_MD = PROJECT_ROOT / "strumenti" / "anti-spoiler.md"
OUTPUT_JSON = PROJECT_ROOT / "hooks" / "config" / "anti-spoiler.json"

# Regex per blocchi AS
BLOCK_RE = re.compile(
    r'<!--\s*AS:\s*(?P<attrs>[^>]+?)\s*-->'
    r'(?P<body>.*?)'
    r'<!--\s*/AS\s*-->',
    re.DOTALL
)

ATTR_RE = re.compile(r'(\w+)=(\S+)')


def parse_attrs(attr_string: str) -> dict:
    attrs = {}
    for m in ATTR_RE.finditer(attr_string):
        key, val = m.group(1), m.group(2)
        if val.isdigit():
            val = int(val)
        attrs[key] = val
    return attrs


def strip_code_fences(text: str) -> str:
    """Remove content inside ``` code fences to avoid matching examples."""
    return re.sub(r'```.*?```', '', text, flags=re.DOTALL)


def parse_markdown(md_path: Path) -> dict:
    text = strip_code_fences(md_path.read_text(encoding="utf-8"))
    result = {}
    warnings = 0

    for i, match in enumerate(BLOCK_RE.finditer(text)):
        raw_attrs = match.group("attrs")
        body = match.group("body").strip()

        attrs = parse_attrs(raw_attrs)

        rule_id = attrs.get("id")
        libro = attrs.get("libro")

        if not rule_id or not libro:
            line_num = text[:match.start()].count('\n') + 1
            print(f"⚠️  Blocco alla riga {line_num}: manca 'id' o 'libro' — attributi: {raw_attrs}")
            warnings += 1
            continue

        if not body:
            print(f"⚠️  Blocco {rule_id}: corpo vuoto — ignorato")
            warnings += 1
            continue

        da = attrs.get("da", None)
        a = attrs.get("a", None)

        # Prima riga del body = regola principale
        lines = [l.strip() for l in body.splitlines() if l.strip()]
        regola = lines[0] if lines else ""
        dettaglio = " ".join(lines[1:]) if len(lines) > 1 else ""

        entry = {
            "id": rule_id,
            "regola": regola,
            "dettaglio": dettaglio,
        }
        if da is not None:
            entry["da"] = da
        if a is not None:
            entry["a"] = a

        is_range = (da is not None or a is not None)

        if libro not in result:
            result[libro] = {"globali": [], "per_range": []}

        if is_range:
            result[libro]["per_range"].append(entry)
        else:
            result[libro]["globali"].append(entry)

    if warnings:
        print(f"\n⚠️  {warnings} blocchi con problemi (vedere sopra)")

    return result


def main():
    if not SOURCE_MD.exists():
        print(f"❌ File non trovato: {SOURCE_MD}")
        sys.exit(1)

    print(f"📖 Leggo: {SOURCE_MD}")
    data = parse_markdown(SOURCE_MD)

    if not data:
        print("❌ Nessuna regola trovata — verificare il formato del markdown")
        sys.exit(1)

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    total = sum(
        len(v["globali"]) + len(v["per_range"])
        for v in data.values()
    )
    print(f"✅ Scritto: {OUTPUT_JSON}")
    print(f"   Libri: {list(data.keys())}")
    print(f"   Regole totali: {total}")

    for libro, rules in sorted(data.items()):
        g = len(rules["globali"])
        r = len(rules["per_range"])
        print(f"   {libro}: {g} globali, {r} per range")


if __name__ == "__main__":
    main()
