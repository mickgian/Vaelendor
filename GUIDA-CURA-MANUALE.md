# Cosa Curare Manualmente — Vaelendor

Guida minimale per l'autore. Solo quello che tocchi tu.
Gli script fanno il resto.

---

## Prima di scrivere un capitolo

| File | Cosa fare | Quando |
|------|-----------|--------|
| `libro1-la-scelta/sinossi.md` | Verificare che il capitolo da scrivere sia coperto dalla sinossi | Prima di ogni capitolo nuovo |
| `libro1-la-scelta/timeline.md` | Compilare la riga del giorno/capitolo (ora è quasi vuota) | Prima di ogni capitolo |
| `personaggi/party/*.md` | Aggiornare la scheda se hai deciso cambiamenti al personaggio | Quando cambi qualcosa nell'arco del personaggio |
| `personaggi/secondari/*.md` | Creare la scheda se introduci un personaggio secondario nuovo | Quando appare un nuovo secondario |
| `worldbuilding/*.md` | Aggiornare se il capitolo introduce nuovi elementi del mondo | Quando aggiungi lore nuova |

Poi lancia `./hooks/pre-edit.sh libro1-la-scelta <capitolo>` e verifica che il briefing sia corretto.

---

## Dopo aver scritto un capitolo

| File | Cosa fare | Quando |
|------|-----------|--------|
| `libro1-la-scelta/checkpoint/dopo-capitolo-NN.md` | Compilare tutte le sezioni `[Da compilare]` con gli eventi reali del capitolo | Dopo ogni capitolo — lo script crea il template, tu lo riempi |
| `libro1-la-scelta/memoria-personaggi/*.md` | Per ogni personaggio presente: aggiungere cosa sa, sospetta, non sa. Aggiornare la riga `Aggiornato al:` | Dopo ogni capitolo |
| `libro1-la-scelta/timeline.md` | Completare giorno ed eventi principali | Dopo ogni capitolo |
| `libro1-la-scelta/note/foreshadowing-tracker.md` | Aggiungere semi piantati nel capitolo (🌱), aggiornare semi cresciuti (🌿) o raccolti (🌳) | Dopo ogni capitolo che pianta o raccoglie un seme |
| `serie/tracker/relazioni.md` | Aggiungere/aggiornare coppie di personaggi se il rapporto evolve | Quando una relazione cambia in modo significativo |
| `serie/tracker/rivelazioni.md` | Registrare rivelazioni avvenute; spostare da "Pianificate" ad "Avvenute" | Quando il lettore o un personaggio scopre qualcosa |
| `serie/tracker/morti.md` | Registrare il decesso | Quando un personaggio muore |
| `serie/tracker/foreshadowing-cross.md` | Aggiungere semi che si raccoglieranno in libri futuri | Quando pianti un seme cross-libro |
| `serie/tracker/regole-mondo.md` | Aggiungere regole stabilite nel testo (distanze, tempi, limiti magia) | Quando il testo stabilisce un fatto vincolante |

Poi lancia `./hooks/post-edit.sh libro1-la-scelta <capitolo>` per verificare che tutto sia a posto.

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

1. **Compilare** `libro1-la-scelta/timeline.md` — riempire i giorni dei capitoli 1–9 (li hai già scritti, basta riportare i dati)
2. **Compilare** `libro1-la-scelta/note/foreshadowing-tracker.md` — registrare i semi piantati nei capitoli 1–9
3. **Compilare** `serie/tracker/relazioni.md` — registrare le relazioni significative emerse nei capitoli 1–9
4. **Compilare** `serie/tracker/rivelazioni.md` — registrare le rivelazioni avvenute nei capitoli 1–9
5. Lancia `./hooks/pre-edit.sh libro1-la-scelta 10`
6. Scrivi (o revisiona) il capitolo
7. **Compilare** `checkpoint/dopo-capitolo-10.md` — riempire le sezioni `[Da compilare]`
8. **Aggiornare** `memoria-personaggi/*.md` per i personaggi presenti — portare a "Aggiornato al: Capitolo 10"
9. Lancia `./hooks/post-edit.sh libro1-la-scelta 10`
10. Verifica ✅ e commit

⚠️ **DA VERIFICARE CON L'AUTORE:** I checkpoint 10–22 hanno contenuto parziale (28 righe con 2 placeholder ciascuno). Non è chiaro se siano stati pre-compilati con dati reali o se contengano solo il template. Verificare prima di procedere.
