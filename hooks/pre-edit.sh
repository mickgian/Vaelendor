#!/bin/bash
# ============================================================================
# PRE-EDIT HOOK — Carica contesto prima di lavorare su un capitolo
# ============================================================================
# Uso: ./hooks/pre-edit.sh <libro> <capitolo|pro|epi>
# Esempio: ./hooks/pre-edit.sh libro1-la-scelta 12
#          ./hooks/pre-edit.sh libro1-la-scelta pro
#          ./hooks/pre-edit.sh libro1-la-scelta epi
# ============================================================================

set -euo pipefail

LIBRO="${1:?Errore: specificare il libro (es: libro1-la-scelta)}"
CAP_INPUT="${2:?Errore: specificare il capitolo (es: 12, pro, epi)}"

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LIBRO_DIR="$BASE_DIR/$LIBRO"
SERIE_DIR="$BASE_DIR/serie"

# Determina tipo di unità narrativa e checkpoint precedente
CAP_LABEL=""
PREV_CHECKPOINT=""

case "$CAP_INPUT" in
    pro|prologo)
        CAP_LABEL="Prologo"
        CAP_KEY="pro"
        # Il prologo non ha checkpoint precedente
        ;;
    epi|epilogo)
        CAP_LABEL="Epilogo"
        CAP_KEY="epi"
        # Checkpoint precedente = ultimo capitolo
        # Cerca il checkpoint più alto disponibile
        LAST_CP=$(ls "$LIBRO_DIR/checkpoint"/dopo-capitolo-*.md 2>/dev/null | sort -V | tail -1)
        if [ -n "$LAST_CP" ]; then
            PREV_CHECKPOINT="$LAST_CP"
        fi
        ;;
    *)
        # Capitolo numerico
        CAP_NUM="$CAP_INPUT"
        CAP_PADDED=$(printf "%02d" "$CAP_NUM")
        PREV_CAP=$((CAP_NUM - 1))
        PREV_PADDED=$(printf "%02d" "$PREV_CAP")
        CAP_LABEL="Capitolo $CAP_NUM"
        CAP_KEY="$CAP_NUM"

        if [ "$CAP_NUM" -gt 1 ]; then
            PREV_CHECKPOINT="$LIBRO_DIR/checkpoint/dopo-capitolo-${PREV_PADDED}.md"
        elif [ "$CAP_NUM" -eq 1 ]; then
            # Cap 1: checkpoint precedente è il prologo (se esiste)
            PREV_CHECKPOINT="$LIBRO_DIR/checkpoint/dopo-prologo.md"
        fi
        ;;
esac

echo "============================================"
echo "  BRIEFING — $CAP_LABEL ($LIBRO)"
echo "============================================"
echo ""

# 1. Checkpoint precedente
if [ -n "$PREV_CHECKPOINT" ] && [ -f "$PREV_CHECKPOINT" ]; then
    PREV_NAME=$(basename "$PREV_CHECKPOINT" .md)
    echo "📍 STATO DEL MONDO ($PREV_NAME):"
    echo "--------------------------------------------"
    cat "$PREV_CHECKPOINT"
    echo ""
elif [ "$CAP_KEY" = "pro" ]; then
    echo "📍 Prologo — Nessun checkpoint precedente."
    echo ""
elif [ "$CAP_KEY" = "1" ]; then
    # Cap 1 senza checkpoint prologo
    echo "📍 Capitolo 1 — Nessun checkpoint precedente (prologo non ha checkpoint o non trovato)."
    echo ""
elif [ -n "$PREV_CHECKPOINT" ]; then
    echo "⚠️  Checkpoint $(basename "$PREV_CHECKPOINT") NON TROVATO"
    echo ""
fi

# 1b. POV del capitolo corrente
POV_SCRIPT="$BASE_DIR/hooks/pov-check.py"
if [ -f "$POV_SCRIPT" ]; then
    python3 "$POV_SCRIPT" "$LIBRO" "$CAP_KEY" 2>/dev/null || true
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
    python3 "$TECNICA_SCRIPT" "$LIBRO" "$CAP_KEY" 2>/dev/null || true
fi

echo "============================================"
echo "  BRIEFING COMPLETATO — Buona scrittura!"
echo "============================================"
