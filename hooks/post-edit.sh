#!/bin/bash
# ============================================================================
# POST-EDIT HOOK — Verifica che tutti i tracker siano aggiornati
# ============================================================================
# Uso: ./hooks/post-edit.sh <libro> <capitolo|pro|epi>
# Esempio: ./hooks/post-edit.sh libro1-la-scelta 12
#          ./hooks/post-edit.sh libro1-la-scelta pro
#          ./hooks/post-edit.sh libro1-la-scelta epi
# ============================================================================

set -euo pipefail

LIBRO="${1:?Errore: specificare il libro (es: libro1-la-scelta)}"
CAP_INPUT="${2:?Errore: specificare il capitolo (es: 12, pro, epi)}"

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LIBRO_DIR="$BASE_DIR/$LIBRO"
SERIE_DIR="$BASE_DIR/serie"

# Determina file e label
case "$CAP_INPUT" in
    pro|prologo)
        CAP_FILE="$LIBRO_DIR/capitoli/prologo.md"
        CAP_LABEL="Prologo"
        CHECKPOINT_FILE="$LIBRO_DIR/checkpoint/dopo-prologo.md"
        CAP_NUM_FOR_MEMORIA="Prologo"
        ;;
    epi|epilogo)
        CAP_FILE="$LIBRO_DIR/capitoli/epilogo.md"
        CAP_LABEL="Epilogo"
        CHECKPOINT_FILE="$LIBRO_DIR/checkpoint/dopo-epilogo.md"
        CAP_NUM_FOR_MEMORIA="Epilogo"
        ;;
    *)
        CAP_PADDED=$(printf "%02d" "$CAP_INPUT")
        CAP_FILE="$LIBRO_DIR/capitoli/capitolo-${CAP_PADDED}.md"
        CAP_LABEL="Capitolo $CAP_INPUT"
        CHECKPOINT_FILE="$LIBRO_DIR/checkpoint/dopo-capitolo-${CAP_PADDED}.md"
        CAP_NUM_FOR_MEMORIA="$CAP_INPUT"
        ;;
esac

ERRORS=0
WARNINGS=0

echo "============================================"
echo "  POST-EDIT CHECK — $CAP_LABEL ($LIBRO)"
echo "============================================"
echo ""

# Funzioni di utilità
check_pass() { echo "  ✅ $1"; }
check_fail() { echo "  ❌ BLOCCANTE: $1"; ERRORS=$((ERRORS + 1)); }
check_warn() { echo "  ⚠️  $1"; WARNINGS=$((WARNINGS + 1)); }

# 1. Verifica che il file esista
echo "📄 File:"
if [ -f "$CAP_FILE" ]; then
    check_pass "$(basename "$CAP_FILE") esiste"
else
    check_fail "$(basename "$CAP_FILE") NON TROVATO"
fi

# 2. Linter
echo ""
echo "🔍 Linter narrativo:"
if command -v python3 &>/dev/null && [ -f "$BASE_DIR/hooks/narrative-linter.py" ]; then
    LINT_OUTPUT=$(python3 "$BASE_DIR/hooks/narrative-linter.py" "$CAP_FILE" 2>&1) || true
    if echo "$LINT_OUTPUT" | grep -q "❌"; then
        check_fail "Linter ha trovato errori critici"
        echo "$LINT_OUTPUT" | grep "❌" | sed 's/^/    /'
    else
        check_pass "Linter superato"
    fi
else
    check_warn "Linter non eseguibile (python3 o script non trovato)"
fi

# 3. Tracker validator
echo ""
echo "🔗 Tracker validator:"
if command -v python3 &>/dev/null && [ -f "$BASE_DIR/hooks/tracker-validator.py" ]; then
    VALID_OUTPUT=$(python3 "$BASE_DIR/hooks/tracker-validator.py" "$CAP_FILE" 2>&1) || true
    if echo "$VALID_OUTPUT" | grep -q "❌"; then
        check_fail "Validator ha trovato contraddizioni"
        echo "$VALID_OUTPUT" | grep "❌" | sed 's/^/    /'
    else
        check_pass "Validator superato"
    fi
else
    check_warn "Validator non eseguibile (python3 o script non trovato)"
fi

# 4. Checkpoint aggiornato
echo ""
echo "📍 Checkpoint:"
if [ -f "$CHECKPOINT_FILE" ]; then
    check_pass "$(basename "$CHECKPOINT_FILE") esiste"
else
    check_fail "$(basename "$CHECKPOINT_FILE") NON aggiornato"
fi

# 5. Memorie personaggi aggiornate
echo ""
echo "🧠 Memorie personaggi:"
MEMORIA_DIR="$LIBRO_DIR/memoria-personaggi"
if [ -d "$MEMORIA_DIR" ]; then
    for mem_file in "$MEMORIA_DIR"/*.md; do
        if [ -f "$mem_file" ]; then
            nome=$(basename "$mem_file" .md)
            if grep -q "$CAP_NUM_FOR_MEMORIA" "$mem_file" 2>/dev/null || grep -q "Cap $CAP_NUM_FOR_MEMORIA" "$mem_file" 2>/dev/null; then
                check_pass "Memoria di $nome aggiornata al $CAP_LABEL"
            else
                check_warn "Memoria di $nome potrebbe non essere aggiornata al $CAP_LABEL"
            fi
        fi
    done
else
    check_fail "Directory memoria-personaggi non trovata"
fi

# 6. Tracker della serie
echo ""
echo "📊 Tracker serie:"

TRACKER_FILES=(
    "morti.md:Registro morti"
    "rivelazioni.md:Registro rivelazioni"
    "relazioni.md:Tracker relazioni"
    "foreshadowing-cross.md:Foreshadowing cross-libro"
    "regole-mondo.md:Regole del mondo"
    "geopolitica.md:Geopolitica"
)

for entry in "${TRACKER_FILES[@]}"; do
    file="${entry%%:*}"
    label="${entry##*:}"
    tracker_path="$SERIE_DIR/tracker/$file"
    if [ -f "$tracker_path" ]; then
        check_pass "$label esiste"
    else
        check_fail "$label NON TROVATO"
    fi
done

# Riepilogo
echo ""
echo "============================================"
if [ "$ERRORS" -gt 0 ]; then
    echo "  ❌ $CAP_LABEL NON COMPLETO"
    echo "  $ERRORS errori bloccanti, $WARNINGS avvisi"
    echo "  Correggere gli errori prima di procedere."
else
    echo "  ✅ $CAP_LABEL COMPLETO"
    echo "  Tutti i controlli superati ($WARNINGS avvisi)."
    echo ""
    echo "  Suggerimento:"
    echo "  git add . && git commit -m \"$CAP_LABEL completato\""
    echo ""
    echo "📚 Rigenerazione PDF del libro..."
    python3 "$BASE_DIR/hooks/pdf-generator.py" "$LIBRO_DIR" "$BASE_DIR/Vaelendor_temo.pdf" 2>&1 | sed 's/^/  /'
fi
echo "============================================"

exit $ERRORS
