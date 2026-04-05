#!/bin/bash
# ============================================================================
# PRE-EDIT HOOK — Carica contesto prima di lavorare su un capitolo
# ============================================================================
# Uso: ./hooks/pre-edit.sh <libro> <capitolo>
# Esempio: ./hooks/pre-edit.sh libro1-la-scelta 12
# ============================================================================

set -euo pipefail

LIBRO="${1:?Errore: specificare il libro (es: libro1-la-scelta)}"
CAP_NUM="${2:?Errore: specificare il numero del capitolo (es: 12)}"

# Formatta il numero con zero iniziale
CAP_PADDED=$(printf "%02d" "$CAP_NUM")
PREV_CAP=$((CAP_NUM - 1))
PREV_PADDED=$(printf "%02d" "$PREV_CAP")

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LIBRO_DIR="$BASE_DIR/$LIBRO"
SERIE_DIR="$BASE_DIR/serie"

echo "============================================"
echo "  BRIEFING — Capitolo $CAP_NUM ($LIBRO)"
echo "============================================"
echo ""

# 1. Checkpoint precedente
CHECKPOINT="$LIBRO_DIR/checkpoint/dopo-capitolo-${PREV_PADDED}.md"
if [ "$CAP_NUM" -gt 1 ] && [ -f "$CHECKPOINT" ]; then
    echo "📍 STATO DEL MONDO (dopo Capitolo $PREV_CAP):"
    echo "--------------------------------------------"
    cat "$CHECKPOINT"
    echo ""
elif [ "$CAP_NUM" -eq 1 ]; then
    echo "📍 Capitolo 1 — Nessun checkpoint precedente."
    echo ""
else
    echo "⚠️  Checkpoint dopo-capitolo-${PREV_PADDED}.md NON TROVATO"
    echo ""
fi

# 1b. POV del capitolo corrente
POV_SCRIPT="$BASE_DIR/hooks/pov-check.py"
if [ -f "$POV_SCRIPT" ]; then
    python3 "$POV_SCRIPT" "$LIBRO" "$CAP_NUM" 2>/dev/null || true
fi

# 2. Memorie personaggi
echo "🧠 MEMORIE PERSONAGGI:"
echo "--------------------------------------------"
MEMORIA_DIR="$LIBRO_DIR/memoria-personaggi"
if [ -d "$MEMORIA_DIR" ]; then
    for mem_file in "$MEMORIA_DIR"/*.md; do
        if [ -f "$mem_file" ]; then
            nome=$(basename "$mem_file" .md)
            echo ""
            echo "--- $nome ---"
            cat "$mem_file"
        fi
    done
else
    echo "⚠️  Directory memoria-personaggi non trovata"
fi
echo ""

# 3. Foreshadowing cross-libro
FORESHADOWING="$SERIE_DIR/tracker/foreshadowing-cross.md"
if [ -f "$FORESHADOWING" ]; then
    echo "🌱 SEMI DI FORESHADOWING ATTIVI:"
    echo "--------------------------------------------"
    # Mostra semi piantati (🌱) e in crescita (🌿)
    grep -E "🌱|🌿" "$FORESHADOWING" 2>/dev/null || echo "(nessun seme attivo)"
    echo ""
fi

# 4. Relazioni
RELAZIONI="$SERIE_DIR/tracker/relazioni.md"
if [ -f "$RELAZIONI" ]; then
    echo "💬 STATO RELAZIONI:"
    echo "--------------------------------------------"
    cat "$RELAZIONI"
    echo ""
fi

# 5. Morti
MORTI="$SERIE_DIR/tracker/morti.md"
if [ -f "$MORTI" ]; then
    echo "💀 PERSONAGGI MORTI (NON farli apparire vivi):"
    echo "--------------------------------------------"
    grep -E "^\|" "$MORTI" 2>/dev/null | grep -v "Nessun morto" || echo "(nessun morto registrato)"
    echo ""
fi

# 6. Regole del mondo
REGOLE="$SERIE_DIR/tracker/regole-mondo.md"
if [ -f "$REGOLE" ]; then
    echo "📏 REGOLE DEL MONDO RILEVANTI:"
    echo "--------------------------------------------"
    cat "$REGOLE"
    echo ""
fi

# 7. Tecnica narrativa del libro
TECNICA_SCRIPT="$BASE_DIR/hooks/tecnica-check.py"
if [ -f "$TECNICA_SCRIPT" ]; then
    python3 "$TECNICA_SCRIPT" "$LIBRO" "$CAP_NUM" 2>/dev/null || true
fi

echo "============================================"
echo "  BRIEFING COMPLETATO — Buona scrittura!"
echo "============================================"
