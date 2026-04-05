# Anti-Spoiler — Vaelendor

Questo file è la fonte di verità per tutte le regole anti-spoiler
della saga. È letto da `hooks/sync-antispoiler.py` che genera
`hooks/config/anti-spoiler.json` per gli hook automatici.

**Non modificare il JSON direttamente.**
Modifica questo file, poi esegui: `python3 hooks/sync-antispoiler.py`

---

## Come si legge questo file

Ogni regola ha questa forma:

```
<!-- AS: id=XX libro=YY da=N a=M -->
Testo della regola leggibile.
Dettaglio opzionale su più righe.
<!-- /AS -->
```

- `id` — identificatore univoco (es. AS-L1-01)
- `libro` — libro a cui si applica (es. libro1, tutti)
- `da` / `a` — range capitoli (usa `fine` per "fino alla fine del libro")
- Ometti `da` e `a` per regole valide per tutto il libro

---

## LIBRO 1 — La Scelta

### Regole Globali (tutti i capitoli)

<!-- AS: id=AS-L1-01 libro=libro1 -->
I draghi non devono MAI essere menzionati o suggeriti.
Termini proibiti: "drago", "draghi", "draconico", "draconica", "dragon",
"dragons", "drake", "wyvern" e qualsiasi variante. Il lettore deve poter
immaginare dei antichi, titani, forze primordiali — mai draghi.
La rivelazione dei Draghi deve essere uno shock genuino.
<!-- /AS -->

<!-- AS: id=AS-L1-02 libro=libro1 -->
L'antagonista è sempre e solo "il Sabotatore" — mai nominato.
Il nome "Kaelen Valdris" non viene mai pronunciato nel Libro 1.
Nessun dettaglio fisico che permetta di riconoscerlo in anticipo.
Il momento esatto della rivelazione del nome è TBD.
<!-- /AS -->

<!-- AS: id=AS-L1-03 libro=libro1 -->
La parola "Stirpe" non viene mai usata nel testo narrativo come etichetta.
Elara e Vera hanno percezioni e reazioni — non vengono mai classificate
con un termine che le colleghi a qualcosa di più grande o cosmico.
Il legame tra Elara e Vera è percepito ma non nominato.
<!-- /AS -->

<!-- AS: id=AS-L1-04 libro=libro1 -->
Mirael è specializzata in evocazione (Scuola della Furia).
NON ha visioni, presagi, profezie, divinazione o percezione del futuro.
Termini vietati vicino a Mirael: "visione", "presagio", "profezia",
"divinazione", "profetico", "divinatoria", "predizione", "oracolo",
"scuola dell'eco".
<!-- /AS -->

<!-- AS: id=AS-L1-05 libro=libro1 -->
Elara non deve sembrare speciale o mostrare abilità mistiche evidenti.
Le sue reazioni sono "strane" ma spiegabili come sensibilità personale.
Non è una veggente, non è una maga — è una ragazza che percepisce troppo.
<!-- /AS -->

<!-- AS: id=AS-L1-06 libro=libro1 -->
I personaggi della Stirpe (Elara, Vera) percepiscono un dolore nascosto
nella magia divina. La magia non "fallisce" — loro sentono qualcosa di
sbagliato sotto la superficie. Personaggi non-Stirpe come Dain possono
notare qualcosa di "strano" senza capire perché.
<!-- /AS -->

<!-- AS: id=AS-L1-07 libro=libro1 -->
Dain può sentire che qualcosa è "strano" nelle leggende o nella pietra,
ma non può interpretarlo. Non sa cosa sono i Draghi veramente.
Le sue leggende sono vere, ma lui non ne conosce le implicazioni cosmiche.
Le storie sono "storie del nonno", non "rivelazioni".
<!-- /AS -->

<!-- AS: id=AS-L1-08 libro=libro1 -->
I cinque Draghi (Saeryth, Vaelthrix, Ithrendal, Zheraan, Nethrak) non
vengono mai nominati per nome. Non esistono nel vocabolario del Libro 1.
Nessun personaggio conosce questi nomi, nemmeno nelle leggende di Dain.
<!-- /AS -->

<!-- AS: id=AS-L1-09 libro=libro1 -->
Il Patto originale e il Tradimento non vengono mai descritti in termini
cosmici. Non esistono "fatti cosmici verificati" — solo leggende, miti,
storie attorno al fuoco. Il worldbuilding cosmico è nascosto nel folklore.
<!-- /AS -->

### Regole per Range di Capitoli

<!-- AS: id=AS-L1-10 libro=libro1 da=1 a=8 -->
La Chiesa dei Tre appare genuinamente positiva e affidabile.
Nessun commento sarcastico, nessuna lode sospetta, nessun indizio di
corruzione. Deve sembrare davvero buona. Aldric crede nella Chiesa e
il suo dubbio è interno, sottile, mai dichiarato apertamente.
Termini negativi proibiti in contesto ecclesiale: "corrotta", "corruzione",
"corrotto", "tradisce", "tradita", "inganno", "inganna", "ingannare",
"segreto oscuro", "manipolazione", "manipola", "complotto", "cospirazione".
<!-- /AS -->

<!-- AS: id=AS-L1-11 libro=libro1 da=9 a=fine -->
La Chiesa può mostrare comportamenti ambigui o contraddittori.
La rivelazione del Sanatorio inizia a incrinare l'immagine — in modo
graduale e attraverso le azioni dei personaggi, non commenti autoriali.
La Chiesa rimane un'istituzione con persone buone (Aldric, Aldwyn):
il problema è sistemico, non individuale. Non "villain cartoonesco".
Il tradimento cosmico (Draghi incatenati, Traditori) resta nascosto.
<!-- /AS -->

<!-- AS: id=AS-L1-12 libro=libro1 da=1 a=9 -->
Elara non sa cosa sia. Le sue percezioni sono un peso e un mistero,
non un dono compreso. Non nominarle, non spiegarle, non collegarle
ad altri personaggi o eventi in modo che risultino classificabili.
Dal capitolo 10 il legame con Vera inizia a emergere, ma senza etichette.
<!-- /AS -->

<!-- AS: id=AS-L1-13 libro=libro1 da=1 a=9 -->
Vera non è ancora nel party. Non è presente nelle scene di gruppo.
La sua esistenza è nota solo come "la ragazza sulla collina" (dal Cap 6).
Aldric non l'ha ancora incontrata fino al Capitolo 9.
<!-- /AS -->

---

## LIBRO 2 — Le Montagne Ricordano

<!-- Aggiungere regole quando il Libro 2 è in lavorazione -->

---

## Note Trasversali (tutti i libri)

<!-- AS: id=AS-GLOBAL-01 libro=tutti -->
I cinque Draghi non vengono mai nominati per nome prima che la
rivelazione sia prevista dalla sinossi del libro in lavorazione.
Verificare sempre la sinossi prima di usare nomi come Saeryth,
Vaelthrix, Ithrendal, Zheraan, Nethrak nel testo narrativo.
<!-- /AS -->

<!-- AS: id=AS-GLOBAL-02 libro=tutti -->
Il Patto originale e il Tradimento non vengono mai descritti in termini
cosmici prima delle rivelazioni pianificate nella sinossi.
Dain può citare "leggende" — non "fatti cosmici verificati".
<!-- /AS -->

<!-- AS: id=AS-GLOBAL-03 libro=tutti -->
Mirael appartiene alla Scuola della Furia (evocazione/elementi).
NON usa divinazione, visioni, profezie o magia temporale (Scuola dell'Eco).
Questa regola vale per TUTTI i libri della saga.
<!-- /AS -->
