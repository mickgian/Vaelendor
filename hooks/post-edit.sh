#!/bin/bash
# ============================================================================
# POST-EDIT HOOK — Verifica che tutti i tracker siano aggiornati
# ============================================================================
# Uso: ./hooks/post-edit.sh <libro> <capitolo>
# Esempio: ./hooks/post-edit.sh libro1-la-scelta 12
# ============================================================================

set -euo pipefail

LIBRO="${1:?Errore: specificare il libro (es: libro1-la-scelta)}"
CAP_NUM="${2:?Errore: specificare il numero del capitolo (es: 12)}"

CAP_PADDED=$(printf "%02d" "$CAP_NUM")

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LIBRO_DIR="$BASE_DIR/$LIBRO"
SERIE_DIR="$BASE_DIR/serie"
CAP_FILE="$LIBRO_DIR/capitoli/capitolo-${CAP_PADDED}.md"

ERRORS=0
WARNINGS=0

echo "============================================"
echo "  POST-EDIT CHECK — Capitolo $CAP_NUM ($LIBRO)"
echo "============================================"
echo ""

# Funzioni di utilità
check_pass() { echo "  ✅ $1"; }
check_fail() { echo "  ❌ BLOCCANTE: $1"; ERRORS=$((ERRORS + 1)); }
check_warn() { echo "  ⚠️  $1"; WARNINGS=$((WARNINGS + 1)); }

# 1. Verifica che il capitolo esista
echo "📄 Capitolo:"
if [ -f "$CAP_FILE" ]; then
    check_pass "capitolo-${CAP_PADDED}.md esiste"
else
    check_fail "capitolo-${CAP_PADDED}.md NON TROVATO"
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
CHECKPOINT="$LIBRO_DIR/checkpoint/dopo-capitolo-${CAP_PADDED}.md"
if [ -f "$CHECKPOINT" ]; then
    check_pass "checkpoint/dopo-capitolo-${CAP_PADDED}.md esiste"
else
    check_fail "checkpoint/dopo-capitolo-${CAP_PADDED}.md NON aggiornato"
fi

# 5. Memorie personaggi aggiornate
echo ""
echo "🧠 Memorie personaggi:"
MEMORIA_DIR="$LIBRO_DIR/memoria-personaggi"
if [ -d "$MEMORIA_DIR" ]; then
    for mem_file in "$MEMORIA_DIR"/*.md; do
        if [ -f "$mem_file" ]; then
            nome=$(basename "$mem_file" .md)
            if grep -q "Capitolo $CAP_NUM" "$mem_file" 2>/dev/null || grep -q "Cap $CAP_NUM" "$mem_file" 2>/dev/null; then
                check_pass "Memoria di $nome aggiornata al Cap $CAP_NUM"
            else
                check_warn "Memoria di $nome potrebbe non essere aggiornata al Cap $CAP_NUM"
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
    echo "  ❌ CAPITOLO NON COMPLETO"
    echo "  $ERRORS errori bloccanti, $WARNINGS avvisi"
    echo "  Correggere gli errori prima di procedere."
else
    echo "  ✅ CAPITOLO $CAP_NUM COMPLETO"
    echo "  Tutti i controlli superati ($WARNINGS avvisi)."
    echo ""
    echo "  Suggerimento:"
    echo "  git add . && git commit -m \"Capitolo $CAP_NUM completato\""
    echo ""
    echo "📚 Rigenerazione PDF del libro..."
    python3 "$BASE_DIR/hooks/pdf-generator.py" "$LIBRO_DIR" "$BASE_DIR/Vaelendor_temo.pdf" 2>&1 | sed 's/^/  /'
fi
echo "============================================"

exit $ERRORS
