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
La **Chiesa dei Tre** deve apparire genuinamente positiva e affidabile nei primi libri.
- Nessun commento sarcastico
- Nessuna lode sospetta
- Nessun indizio che sia corrotta
- Deve sembrare **davvero buona**

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
- **Aldwyn** — capitano delle guardie
- **Brennan** — giovane guardia, parte per la capitale nella notte del Capitolo 6

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

### Prima di QUALSIASI modifica al Capitolo N:
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
[1] INIZIO LAVORO → pre-edit.sh           (carica contesto)
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
| Revisione | `python hooks/review-report.py <file>` |
| Personaggi secondari | `python hooks/personaggi-secondari-checker.py <libro-dir>` |

Per i dettagli su ogni hook, vedere i file nella directory `hooks/`.
