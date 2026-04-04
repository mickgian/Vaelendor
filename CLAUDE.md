# CLAUDE.md — Vaelendor: Saga dei Draghi Incatenati

Questo file contiene le regole fondamentali per lavorare su questo progetto.
Ogni regola è **non negoziabile** salvo esplicita modifica da parte dell'autore.

---

## 📂 Struttura del Progetto

```
vaelendor/
├── CLAUDE.md                          # Questo file
├── worldbuilding/                     # Lore del mondo
├── personaggi/                        # Schede personaggi (party, secondari, antagonisti)
├── libro1-la-scelta/                  # Libro 1: "La Scelta" (22 capitoli)
│   ├── sinossi.md                     # Sinossi completa
│   ├── timeline.md                    # Timeline giorno per giorno
│   ├── capitoli/                      # Testo dei capitoli
│   ├── checkpoint/                    # Stato del mondo dopo ogni capitolo
│   ├── memoria-personaggi/            # Cosa sa ogni personaggio
│   └── note/                          # Foreshadowing e note
├── serie/                             # Arco complessivo della saga (12 libri)
│   ├── tracker/                       # Tracking cross-libro
├── strumenti/                         # Guide di stile e tecniche narrative
└── hooks/                             # Script di automazione coerenza narrativa
```

---

## 🚫 REGOLE ANTI-SPOILER (CRITICHE)

### Draghi
I **DRAGHI** non devono MAI essere menzionati o suggeriti nei capitoli del Libro 1.
Il lettore deve immaginare varie possibilità (dei antichi, titani, forze primordiali).
La rivelazione dei Draghi deve essere uno **shock genuino**.

**Termini proibiti nel Libro 1:** "drago", "draghi", "draconico", "draconica", "dragon" e qualsiasi variante.

### Il Sabotatore
Nel Libro 1, l'antagonista è chiamato **"il Sabotatore"**.
Il momento esatto in cui rivelare il nome completo **"Kaelen Valdris"** è ancora da definire (TBD).

### La Chiesa
La **Chiesa dei Tre** deve apparire genuinamente positiva e affidabile nei **Capitoli 1–8**.
- Nessun commento sarcastico
- Nessuna lode sospetta
- Nessun indizio che sia corrotta
- Deve sembrare **davvero buona**

**Dal Capitolo 9 in poi:** la rivelazione del Sanatorio inizia a incrinare questa immagine — in modo graduale e attraverso le azioni dei personaggi, non commenti autoriali diretti. La Chiesa rimane un'istituzione con persone buone al suo interno (Aldric, Aldwyn agisce con onore): il problema è sistemico, non individuale. Il validator non deve bloccare Cap 9+ per "indizi di corruzione" intenzionali nell'arco narrativo.

### Elara
**Elara** non deve sembrare speciale o mostrare abilità mistiche evidenti.
Le sue reazioni sono "strane" ma spiegabili come sensibilità personale.

### La Stirpe
I personaggi della Stirpe (Elara, Vera) percepiscono un **dolore nascosto** nella magia divina — la magia non "fallisce", loro sentono qualcosa di sbagliato sotto la superficie.
Personaggi non-Stirpe come Dain possono notare qualcosa di "strano" senza capire perché.

---

## 👥 REGOLE SUI PERSONAGGI

### Composizione del Party
Il party è composto da **7 membri dal Capitolo 3** in poi:
1. **Zorgar** — Mezz'orco barbaro
2. **Sylas** — Ladro umano
3. **Dain** — Nano guerriero/custode delle storie
4. **Aldric** — Sacerdote della Chiesa
5. **Elara** — Strega della Stirpe
6. **Mirael** — Maga di evocazione + Micio (gatto nero)
7. **Fizzle** — Gnomo alchimista

Con **Vera** sono 8 persone dal Capitolo 10.

### Fizzle (⚠️ ATTENZIONE SPECIALE)
- Si unisce al party nel **Capitolo 3** alla taverna "La Spiga e il Tino"
- **NON** durante un inseguimento
- Deve essere **SEMPRE presente** in tutte le scene di gruppo dal Capitolo 3 in avanti
- Fizzle viene cronicamente dimenticato — **verificare SEMPRE la sua presenza**

### Mirael
- Specialista in **evocazione** (conjuration)
- **NON** ha visioni
- **NON** ha poteri divinatori

### Zorgar
- Parla **normalmente**, con stile diretto ed economico
- **NON** usa linguaggio primitivo da stereotipo fantasy ("Me colpire", "Zorgar fare")

### Tomás e Willem
- **Tomás** è un ex-soldato in pensione, **NON** un guaritore
- **Willem** è il guaritore del villaggio

### Aldric
- È un **sacerdote** (mai "chierico")
- Genuinamente devoto e buono

### Guardie di Millbrook
- **Aldwyn** — capitano delle guardie, Custode del Tempio
- **Brennan** — giovane guardia, Custode del Tempio; parte per la capitale nella notte del Capitolo 6
- Aldwyn e Brennan sono **NPC**, non membri del party

### Custodi del Tempio
- Le guardie della Chiesa si chiamano **"Custodi del Tempio"** (singolare: Custode del Tempio)
- Aldric viaggia scortato da Custodi del Tempio — Aldwyn e Brennan lo sono
- **"Templari"** è una categoria DIVERSA: non usare "templari" per riferirsi a Aldwyn, Brennan, o a chiunque scorti Aldric
- ⚠️ Verificare SEMPRE: Custode del Tempio ≠ Templare

### Vincolo Timeline — Prima Visita di Aldric a Vera
- Aldric **non ha ancora incontrato Vera** fino alla fine del Capitolo 8
- La sua prima visita avviene in **Capitolo 9** (Giorno 5, mattina)
- ⚠️ Verificare `memoria-personaggi/aldric.md` prima di scrivere qualsiasi scena con Vera + Aldric

---

## 🌍 REGOLE DI WORLDBUILDING

- **Millbrook** ha una sola locanda: **"La Spiga e il Tino"** (gestita da Rorik). Un solo guaritore (Willem). Infrastrutture limitate — è un piccolo villaggio rurale.
- I personaggi sanno **SOLO** ciò che hanno visto o che gli è stato detto fino a quel punto della narrazione. **Nessuna conoscenza anticipata.**
- La **magia divina** ha un costo visibile su chi la usa (fatica, pallore).

---

## ✍️ REGOLE DI STILE

- **TONO:** 85% calore/avventura/cameratismo, 15% malinconia/inquietudine sottile. Mai oscurità esplicita nel Libro 1.
- **LINGUA:** Italiano. Attenzione agli accenti (è, à, ì, ò, ù) — verificare sempre l'encoding UTF-8.
- **LUNGHEZZA CAPITOLI:** target 5.000–5.800 parole. Libro 1 totale: ~121.000 parole su 22 capitoli.
- **POV:** capitoli a POV rotante. Cap 1 = Zorgar, Cap 2 = Elara, Cap 3 = Dain, poi continua a rotare.
- **WORLDBUILDING:** integrato direttamente nell'azione e nei dialoghi. Mai come "intermezzi" separati o blocchi espositivi.
- **Terminologia:** "sacerdote" (mai "chierico")

---

## ⚙️ REGOLE DI PROCESSO — SISTEMA CHECKPOINT

### ⛔ PRIMA di QUALSIASI scrittura o modifica al Capitolo N:

**Passo 0 obbligatorio — NON sostituibile con contesto riepilogato:**
```
./hooks/pre-edit.sh <libro> <capitolo>
```
Se pre-edit.sh non è stato eseguito nella sessione corrente, **non iniziare la scrittura**.

1. Leggere `checkpoint/dopo-capitolo-{N-1}.md` (stato del mondo all'inizio del capitolo)
2. Leggere i file `memoria-personaggi/*.md` per i personaggi presenti nel capitolo
3. Leggere il capitolo N stesso (se esiste già)

> **NON** è necessario leggere tutti i capitoli precedenti. I checkpoint contengono tutto il contesto necessario.

### Dopo QUALSIASI modifica a un capitolo:
1. Aggiornare **immediatamente** il checkpoint corrispondente (`checkpoint/dopo-capitolo-N.md`)
2. Aggiornare i file `memoria-personaggi/*.md` dei personaggi coinvolti
3. Se il cambiamento ha impatto sui capitoli successivi: ⚠️ **PROPAGAZIONE NECESSARIA**

### Verifiche obbligatorie:
- Chi è presente nella scena
- Cosa sa ogni personaggio a quel punto
- Nomi corretti
- Terminologia coerente
- Espandere scene esistenti **PRIMA** di aggiungerne di nuove

### Sezione di analisi:
Ogni capitolo completato deve includere una sezione di analisi con:
- Strati narrativi
- Elementi a doppio strato
- Momenti chiave per personaggio

---

## 🔄 TRE MODALITÀ DI LAVORO

Gli hook funzionano in tutte e tre le modalità.

### Modalità 1 — CLAUDE SCRIVE
L'utente fornisce indicazioni (POV, eventi, tono, vincoli). Claude esegue pre-edit.sh,
scrive il capitolo rispettando checkpoint e memorie, poi esegue l'intera pipeline di hook.

**Flusso:** indicazioni utente → pre-edit → scrittura → linter → validator → checkpoint → memorie → post-edit

### Modalità 2 — L'UTENTE SCRIVE, CLAUDE REVISIONA
L'utente scrive il capitolo e chiede a Claude di revisionarlo.
Claude esegue la pipeline di hook come revisione, poi produce un **RAPPORTO DI REVISIONE**
con errori, incongruenze e suggerimenti, **SENZA modificare il testo** dell'utente a meno che
non venga esplicitamente chiesto.

**Flusso:** push/file utente → pre-edit (contesto) → linter → validator → rapporto revisione → utente approva → checkpoint → memorie → post-edit

### Modalità 3 — IBRIDA (BOZZA + ESPANSIONE)
L'utente scrive una bozza (anche incompleta o schematica). Claude la legge, esegue
pre-edit per avere il contesto, poi espande/raffina il testo mantenendo la voce e le
scelte dell'utente. Dopo l'espansione, esegue la pipeline completa.

**Flusso:** bozza utente → pre-edit → espansione rispettando la bozza → linter → validator → checkpoint → memorie → post-edit

### Come capire quale modalità:
| Comando | Modalità |
|---|---|
| "Scrivi il capitolo 12" | Modalità 1 |
| "Revisiona il capitolo 12" / "Controlla il capitolo 12" | Modalità 2 |
| "Espandi questa bozza" / "Raffina il capitolo 12" | Modalità 3 |

In caso di dubbio, **chiedere all'utente**.

---

## 🔧 SISTEMA DI HOOK

### Flusso completo di lavoro su un capitolo:
```
[1] INIZIO LAVORO → pre-edit.sh           (carica contesto + tecnica narrativa)
[2] SCRITTURA/MODIFICA del capitolo
[3] SALVATAGGIO → narrative-linter.py     (encoding, termini proibiti, nomi, lunghezza)
[4] SE OK → worldbuilding-validator.py    (capacità personaggi, luoghi, tono Chiesa)
[5] SE OK → tracker-validator.py          (morti, regole mondo, rivelazioni, foreshadowing)
[6] SE OK → checkpoint-generator.py       (aggiorna checkpoint)
[7] INFINE → memoria-updater.py           (aggiorna memorie personaggi)
[8] POST-EDIT → post-edit.sh              (verifica che tutto sia aggiornato)
[9] FINE ✅

[OPZIONALE] python hooks/personaggi-secondari-checker.py <libro-dir>
            (verifica a livello libro che i personaggi secondari siano menzionati)
```

### Comandi hook:
| Hook | Comando |
|---|---|
| Pre-edit | `./hooks/pre-edit.sh <libro> <capitolo>` |
| Linter | `python hooks/narrative-linter.py <file>` |
| Worldbuilding | `python hooks/worldbuilding-validator.py <file>` |
| Validator | `python hooks/tracker-validator.py <file>` |
| Checkpoint | `python hooks/checkpoint-generator.py <file>` |
| Memorie | `python hooks/memoria-updater.py <file>` |
| Post-edit | `./hooks/post-edit.sh <libro> <capitolo>` |
| Tecnica narrativa | `python hooks/tecnica-check.py <libro> <capitolo>` |
| Revisione | `python hooks/review-report.py <file>` |
| Personaggi secondari | `python hooks/personaggi-secondari-checker.py <libro-dir>` |

Per i dettagli su ogni hook, vedere i file nella directory `hooks/`.

---

## 🌐 Glossario di Traduzione

Il file `glossario-traduzione-en.md` è il glossario di traduzione IT→EN per la futura pubblicazione in inglese.

### Regole
- Dopo ogni sessione di scrittura o modifica di capitoli/worldbuilding, esegui `bash scripts/update-glossary.sh` per aggiornare il glossario.
- Se l'utente dice "aggiorna glossario" o "update glossary", esegui lo script.
- Se l'utente chiede di tradurre un capitolo, carica SEMPRE il glossario prima di iniziare e usa le traduzioni consolidate.
- Le entry marcate **[APPROVATO]** sono decisioni finali dell'autore: non modificarle mai.
- Le entry marcate **[DA VERIFICARE]** richiedono attenzione dell'autore.

### Generazione iniziale
Se il glossario non esiste ancora, generalo scansionando tutti i file .md del progetto (capitoli, worldbuilding, personaggi, serie) ed estraendo tutti i termini propri, luoghi, organizzazioni, titoli, termini magici, divinità, razze, oggetti, espressioni, termini economici.

### Aggiornamento
| Comando | Contesto |
|---------|----------|
| `bash scripts/update-glossary.sh` | Aggiornamento manuale da terminale |
| `git push` | Automatico via hook pre-push |
| "aggiorna glossario" in Claude Code | Claude esegue lo script |
