# Cosa Curare Manualmente — Vaelendor

Guida minimale per l'autore. Solo quello che tocchi tu.
Gli hook li lancia Claude Code — tu curi i file che gli hook leggono.

---

## Chi fa cosa

| Azione | Chi la fa |
|--------|-----------|
| Lanciare `pre-edit.sh`, linter, validator, `post-edit.sh` | **Claude Code** (automaticamente) |
| Scrivere/espandere il capitolo | **Claude Code** (Modalità 1/3) oppure **tu** (Modalità 2) |
| Aggiornare checkpoint e memorie dopo la scrittura | **Claude Code** (li genera nella pipeline post-edit) |
| Verificare checkpoint e memorie generati | **Tu** (correggi se servono aggiustamenti) |
| Aggiornare i tracker della serie (timeline, foreshadowing, relazioni, rivelazioni, morti, regole-mondo) | **Claude Code** (li aggiorna nella pipeline post-capitolo) |
| Verificare i tracker aggiornati | **Tu** (correggi se servono aggiustamenti) |
| Sinossi del libro | **Già pronta** per tutti i 22 capitoli — tu la verifichi solo se vuoi cambiare qualcosa |

**Il ciclo normale:**
1. Dici "Scrivi il capitolo N" (con le tue indicazioni su eventi, tono, vincoli)
2. Claude Code esegue tutta la pipeline (pre-edit → scrittura → linter → validator → checkpoint → memorie → tracker serie → post-edit)
3. Tu verifichi checkpoint, memorie e tracker — correggi se necessario — commit

---

## Prima di chiedere a Claude Code di scrivere

La sinossi copre già tutti i 22 capitoli. Checkpoint e memorie del capitolo precedente li ha generati Claude Code nella pipeline post-edit.

Di norma **non devi fare nulla** — dici "Scrivi il capitolo N" e Claude Code ha tutto il contesto.

**Solo se hai deciso cambiamenti** tra un capitolo e l'altro:

| File | Cosa fare | Quando |
|------|-----------|--------|
| `libro1-la-scelta/sinossi.md` | Verificare che sia ancora in linea con quello che vuoi | Se hai cambiato idea sulla trama |
| `personaggi/party/*.md` | Aggiornare la scheda se hai deciso cambiamenti all'arco del personaggio | Quando cambi qualcosa |
| `personaggi/secondari/*.md` | Creare la scheda se il capitolo introduce un personaggio secondario nuovo | Quando appare un nuovo secondario |
| `worldbuilding/*.md` | Aggiornare se il capitolo introduce nuovi elementi del mondo | Quando aggiungi lore nuova |

---

## Dopo che Claude Code ha scritto il capitolo

Claude Code genera automaticamente checkpoint, memorie e tracker nella pipeline post-capitolo.
Tu **verifichi** che siano corretti e **correggi** se necessario.

| File | Generato da | Tu fai |
|------|-------------|--------|
| `libro1-la-scelta/checkpoint/dopo-capitolo-NN.md` | Claude Code | Verifichi che sia corretto |
| `libro1-la-scelta/memoria-personaggi/*.md` | Claude Code | Verifichi cosa sa/sospetta/non sa |
| `libro1-la-scelta/timeline.md` | Claude Code | Verifichi giorno ed eventi |
| `libro1-la-scelta/note/foreshadowing-tracker.md` | Claude Code | Verifichi semi 🌱🌿🌳 |
| `serie/tracker/relazioni.md` | Claude Code | Verifichi evoluzione rapporti |
| `serie/tracker/rivelazioni.md` | Claude Code | Verifichi rivelazioni e sezione "Pianificate" |
| `serie/tracker/morti.md` | Claude Code | Verifichi (se qualcuno muore) |
| `serie/tracker/foreshadowing-cross.md` | Claude Code | Verifichi semi cross-libro |
| `serie/tracker/regole-mondo.md` | Claude Code | Verifichi regole stabilite nel testo |

---

## File che NON tocchi mai

- `hooks/config/termini-proibiti.json` — usato dal linter, derivato dalle regole in CLAUDE.md
- `hooks/config/nomi-canonici.json` — usato dal linter per validare nomi
- `hooks/config/regole-worldbuilding.json` — usato dal worldbuilding-validator
- `hooks/config/anti-spoiler.json` — usato dall'antispoiler-check
- `hooks/config/pov-rotazione.json` — usato dal pov-check
- `hooks/config/tecniche-narrative.json` — usato dal tecnica-check
- `hooks/config/personaggi-secondari-libri.json` — usato dal personaggi-secondari-checker
- `glossario-traduzione-en.md` — rigenerato da `scripts/update-glossary.sh`
- `libro1-la-scelta/tracker-parole.md` — generato automaticamente

Se hai bisogno di aggiungere un termine proibito o un nome canonico, modifica il JSON corrispondente in `hooks/config/` — ma solo se sai cosa fai.

---

## Stato attuale

### Checkpoint (libro1-la-scelta)

| File | Stato |
|------|-------|
| `checkpoint/dopo-capitolo-01.md` … `09.md` | ✅ PRONTO — compilati, nessun placeholder |
| `checkpoint/dopo-capitolo-10.md` … `22.md` | ⚠️ PARZIALE — template con 2 sezioni `[Da compilare]` ciascuno |

### Memorie personaggi (libro1-la-scelta)

| File | Stato |
|------|-------|
| Tutti gli 8 file (`zorgar`, `sylas`, `dain`, `aldric`, `elara`, `mirael`, `fizzle`, `vera`) | ⚠️ PARZIALE — aggiornati al Capitolo 9, mancano Cap 10–22 |

### Tracker serie

| File | Stato |
|------|-------|
| `serie/tracker/morti.md` | ✅ PRONTO — struttura presente, nessun morto registrato (corretto per Libro 1) |
| `serie/tracker/regole-mondo.md` | ✅ PRONTO — 22 righe con regole stabilite |
| `serie/tracker/geopolitica.md` | ✅ PRONTO — 71 righe compilate |
| `serie/tracker/pov-tracker.md` | ✅ PRONTO — 65 righe compilate |
| `serie/tracker/prequel-hints.md` | ✅ PRONTO — 119 righe compilate |
| `serie/tracker/relazioni.md` | ⚠️ PARZIALE — solo template, nessuna relazione registrata |
| `serie/tracker/rivelazioni.md` | ⚠️ PARZIALE — solo 3 rivelazioni pianificate, nessuna avvenuta |
| `serie/tracker/foreshadowing-cross.md` | ⚠️ PARZIALE — solo template, nessun seme registrato |

### Altri file

| File | Stato |
|------|-------|
| `libro1-la-scelta/sinossi.md` | ✅ PRONTO — 302 righe |
| `libro1-la-scelta/timeline.md` | ⚠️ PARZIALE — solo 3 righe compilate su 22 capitoli |
| `libro1-la-scelta/note/foreshadowing-tracker.md` | ⚠️ PARZIALE — template vuoto, nessun seme registrato |
| `worldbuilding/cosmologia.md` | ⚠️ PARZIALE — solo placeholder HTML |
| `worldbuilding/religione.md` | ⚠️ PARZIALE — solo placeholder HTML |
| `worldbuilding/storia.md` | ⚠️ PARZIALE — solo placeholder HTML |
| Tutti gli altri `worldbuilding/*.md` | ✅ PRONTO — compilati (cultura, magia, geografia, economia, ecc.) |
| Schede `personaggi/party/*.md` | ✅ PRONTO — tutte compilate (200-370 righe ciascuna) |

---

## Ordine di lavoro consigliato per il prossimo capitolo

Il prossimo capitolo da allineare è il **Capitolo 10** (primo con checkpoint e memorie non aggiornati).

**Tu fai (prima — una tantum):**
1. Compilare i tracker arretrati dei capitoli 1–9: `timeline.md`, `foreshadowing-tracker.md`, `relazioni.md`, `rivelazioni.md`

**Dici a Claude Code:** "Scrivi il capitolo 10" (con le tue indicazioni su eventi, tono, vincoli)

**Claude Code fa:** pre-edit → scrittura → linter → validator → checkpoint → memorie → tracker serie → post-edit

**Tu fai (dopo):**
3. **Verificare** checkpoint, memorie e tracker generati — correggere se necessario
4. Commit

⚠️ **DA VERIFICARE CON L'AUTORE:** I checkpoint 10–22 hanno contenuto parziale (28 righe con 2 placeholder ciascuno). Non è chiaro se siano stati pre-compilati con dati reali o se contengano solo il template. Verificare prima di procedere.
