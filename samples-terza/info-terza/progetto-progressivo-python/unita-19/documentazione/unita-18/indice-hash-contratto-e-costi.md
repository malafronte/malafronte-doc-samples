# Contratto e costi dell'indice hash - tappa U18

## Fotografia del registro e ciclo di vita

L'indice di consultazione è costruito su una **fotografia** dei preventivi del
registro: la tupla restituita dalla proiezione pubblica `preventivi()` del
modello U14, letta **dopo il caricamento** dell'archivio. L'indice così
costruito risponde a più interrogazioni senza essere ricostruito e conserva
l'associazione fra ogni codice e il record del momento della costruzione.

Il ciclo di vita è esplicito. Una modifica del registro — inserimento,
aggiornamento o eliminazione — richiede una **nuova costruzione** dell'indice;
la vecchia fotografia continua a rappresentare i dati precedenti, perché i
valori `Preventivo` sono immutabili e l'indice non condivide con il registro
né contenitori mutabili né aggiornamenti. La prova PU18-08 verifica i due
indici costruiti prima e dopo l'inserimento di `021`: il primo non contiene il
nuovo codice, il secondo lo restituisce, e il codice `"007"` resta identico in
entrambi. Questa scelta rende verificabili coerenza e costo senza introdurre
una sincronizzazione automatica fra due raccolte.

## Chiavi stringa: dominio, hash e validazione

La tabella didattica del capitolo PY-34 ammette chiavi di tipo esatto `int`
oppure `str`; l'indice adotta la **variante dichiarata a chiavi stringa**,
perché i codici del registro sono stringhe con zeri significativi e non
ammettono conversioni.

| Aspetto | Regola dichiarata |
|---|---|
| Dominio della chiave | Stringa non vuota, come il campo `codice` dello schema del registro |
| Validazione | Riusata dal modello: `valida_chiave` richiama `valida_dominio_record` sul campo `codice` |
| Errori di chiave | Tipo diverso da `str` → `TypeError`; stringa vuota → `ValueError`; entrambi prima di ogni effetto |
| Funzione hash | Didattica del capitolo: accumulatore con base 31 e modulo 65521 |
| Zeri significativi | `"007"` e `"7"` sono chiavi diverse; `"007"` ha hash 47671 |
| Costo di hash e confronti | Proporzionale ai testi trattati; i conteggi delle chiavi esaminate non includono questo costo |

## Contratto dell'indice

| Operazione | Risultato | Effetto | Errore |
|---|---|---|---|
| `costruisci_indice(preventivi, capacita=5)` | Indice completo | Nessuno sulla sorgente | `TypeError`/`ValueError` per record o codici non ammessi; duplicato → `ValueError` |
| `cerca(codice)` | Record associato | Stato conservato | `KeyError` per codice assente |
| `contiene(codice)` | `bool` | Stato conservato | `False` sul vuoto o sul codice assente |
| `inserisci(codice, record)` | `None` | Nuova voce; crescita oltre la soglia | Duplicato → `ValueError` |
| `aggiorna(codice, record)` | `None` | Record sostituito | Assente → `KeyError` |
| `rimuovi(codice)` | `True`/`False` | Voce eliminata una volta | Assente → `False`, stato conservato |
| `len(indice)` | Numero di voci | Stato conservato | `0` sul vuoto |
| `fotografia_ordinata()` | Lista nuova di coppie ordinate | Stato conservato | Ordine lessicografico, fuori dal contratto di ricerca |

## Scelta della struttura e costi

L'indice hash soddisfa **query esatte** con un numero atteso di candidati
limitato, sotto le ipotesi del capitolo: distribuzione adeguata dei codici,
carico controllato dalla soglia 1.0 e operazioni sulle chiavi a costo
limitato. La costruzione di `n` voci costa `Θ(n)` atteso con catene brevi;
il caso peggiore con tutte le chiavi nella stessa catena costa `Θ(n²)` per la
verifica di unicità a ogni inserimento.

L'indice BST della tappa U17 conserva il proprio ruolo nelle **query ordinate
e d'intervallo**: la fotografia ordinata dell'indice hash serve alla
presentazione, mentre gli intervalli restano interrogazioni dell'indice della
tappa precedente. La prova PU18-10 verifica che i due indici e la scansione
del registro restituiscano lo stesso record sulle query esatte ammesse.

La crescita per raddoppio oltre la soglia 1.0 ricolloca ogni voce con il nuovo
indice; il contributo ammortizzato della redistribuzione è costante. La prova
PU18-07 con dodici codici produce capacità 20 e conserva tutte le associazioni.

## Traccia canonica (M64)

Registro `007/locale/450`, `012/nazionale/0`, `003/locale/1200`; capacità 5.
Gli hash didattici sono 47671, 47697, 47667 con indici 1, 2, 2: `012` e `003`
condividono il bucket 2 e restano consultabili separatamente; `007` occupa il
bucket 1. Il carico è `3 / 5 = 0.6`.
