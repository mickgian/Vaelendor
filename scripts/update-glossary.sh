#!/bin/bash
# update-glossary.sh — Aggiornamento differenziale del glossario IT→EN
# Funziona sia dentro che fuori un repo git (basato su timestamp filesystem)

set -euo pipefail

# ── Configurazione ──────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
GLOSSARY="glossario-traduzione-en.md"
GLOSSARY_PATH="$PROJECT_ROOT/$GLOSSARY"
TIMESTAMP_FILE="$PROJECT_ROOT/.glossary-last-update"

cd "$PROJECT_ROOT"

# ── Verifica che il glossario esista ────────────────────────────
if [ ! -f "$GLOSSARY_PATH" ]; then
  echo "❌ Il glossario '$GLOSSARY' non esiste ancora."
  echo "   Generalo prima con: claude -p < prompt-glossario.md"
  echo "   oppure chiedi a Claude Code di generarlo."
  exit 0
fi

# ── Se il timestamp file non esiste, crealo con data antica ─────
if [ ! -f "$TIMESTAMP_FILE" ]; then
  echo "1970-01-01T00:00:00Z" > "$TIMESTAMP_FILE"
  # Touch con data antica così find -newer trova tutto
  touch -t 197001010000 "$TIMESTAMP_FILE"
  echo "📝 Creato $TIMESTAMP_FILE (prima esecuzione)"
fi

# ── Trova file .md modificati dopo l'ultimo aggiornamento ───────
CHANGED_FILES=$(find . -name '*.md' -newer "$TIMESTAMP_FILE" \
  -not -name "$GLOSSARY" \
  -not -name "prompt-glossario*" \
  -not -name "MEMORY.md" \
  -not -path './.git/*' \
  -not -path '*/node_modules/*' \
  -not -path './.claude/*' \
  | sort)

if [ -z "$CHANGED_FILES" ]; then
  echo "✅ Glossario aggiornato — nessun file .md modificato dall'ultimo check."
  exit 0
fi

# ── Conta e mostra i file modificati ───────────────────────────
FILE_COUNT=$(echo "$CHANGED_FILES" | wc -l | tr -d ' ')
echo "📖 Trovati $FILE_COUNT file .md modificati. Aggiornamento glossario in corso..."
echo "$CHANGED_FILES" | sed 's/^/   /'

# ── Costruisci il prompt per Claude ─────────────────────────────
FILE_LIST=""
for f in $CHANGED_FILES; do
  FILE_LIST="$FILE_LIST- $f\n"
done

PROMPT=$(cat <<'PROMPT_END'
Aggiorna il glossario di traduzione IT→EN del progetto Vaelendor.

## File da analizzare

I seguenti file .md sono stati modificati dall'ultimo aggiornamento del glossario:

FILELIST_PLACEHOLDER

## Istruzioni

1. Leggi il glossario esistente in `glossario-traduzione-en.md`
2. Leggi SOLO i file elencati sopra
3. Per ogni nuovo termine trovato (personaggio, luogo, organizzazione, titolo, termine magico, divinità, razza/lingua, oggetto, espressione, termine economico, creatura, mito, festività):
   - Aggiungilo nella categoria corretta, mantenendo l'ordine alfabetico
   - Proponi la traduzione inglese seguendo le regole del glossario
   - Se ci sono più traduzioni valide, proponi alternative con [CONSIGLIATO]
   - I nomi propri fantasy restano invariati
   - I nomi descrittivi italiani vanno tradotti mantenendo lo stesso registro
4. Per entry esistenti che necessitano correzione: aggiorna e aggiungi [AGGIORNATO] nelle Note
5. NON toccare MAI entry marcate [APPROVATO] — sono decisioni finali dell'autore
6. NON rimuovere MAI entry — se dubbie, marca con [DA VERIFICARE]
7. Segnala nuove inconsistenze nella sezione "Decisioni Aperte"
8. Aggiorna la versione (incrementa il minor: 1.0 → 1.1 → 1.2...) e la data in testa al file

## Regole di traduzione (riepilogo)
- Nomi fantasy (Vaelthrix, Zorgar, Sylas, Kaelen, etc.) → INVARIATI
- Nomi descrittivi italiani → tradotti (es: "Foresta delle Nebbie" → "Forest of Mists")
- "Sacerdote" → "Priest" (MAI "Cleric")
- "Custode del Tempio" ≠ "Templare" — due categorie DIVERSE
- NON tradurre titoli della saga o dei libri

Scrivi SOLO il file glossario-traduzione-en.md aggiornato, nient'altro.
PROMPT_END
)

# Sostituisci il placeholder con la lista file reale
PROMPT=$(echo "$PROMPT" | sed "s|FILELIST_PLACEHOLDER|$(echo -e "$FILE_LIST")|")

# ── Chiama Claude ───────────────────────────────────────────────
if command -v claude &> /dev/null; then
  echo "$PROMPT" | claude -p --allowedTools 'Read,Write,Glob,Grep' 2>&1
  CLAUDE_EXIT=$?
else
  echo "⚠️  Il comando 'claude' non è disponibile nel PATH."
  echo "   Esegui l'aggiornamento manualmente in Claude Code con: aggiorna glossario"
  exit 0
fi

if [ $CLAUDE_EXIT -ne 0 ]; then
  echo "⚠️  Claude ha restituito errore (exit code: $CLAUDE_EXIT). Il glossario potrebbe non essere stato aggiornato."
  echo "   Puoi aggiornarlo manualmente in Claude Code."
  exit 0
fi

# ── Aggiorna il timestamp ──────────────────────────────────────
date -u +"%Y-%m-%dT%H:%M:%SZ" > "$TIMESTAMP_FILE"
echo "✅ Glossario aggiornato. Timestamp salvato."

# ── Git stage se siamo in un repo ──────────────────────────────
if git rev-parse --is-inside-work-tree &>/dev/null 2>&1; then
  git add "$GLOSSARY_PATH" "$TIMESTAMP_FILE" 2>/dev/null || true
  echo "📦 File staged in git: $GLOSSARY, .glossary-last-update"
fi
