# Contratti e rappresentazione del modello robusto — U14

Modello, invarianti, scelte di rappresentazione e contratti di
[`registro_modello_u14.py`](../../programmi/registro_modello_u14.py).
Documento di lavoro della milestone M52, affiancato da
[`componenti-e-conversioni.md`](componenti-e-conversioni.md) e
[`prove-e-revisione.md`](prove-e-revisione.md).

## Il modello in due responsabilità

| Tipo | Ruolo | Mutabilità |
|---|---|---|
| `Preventivo` | valore del dominio: codice, destinazione, totale | **immutabile** (`dataclass frozen`) |
| `RegistroPreventivi` | raccolta responsabile: unicità, ordine, aggiornamenti | mutabile sotto controllo |

Il singolo preventivo diventa un valore perché ha dati dichiarati e
ugaglianza propria: due preventivi con gli stessi campi sono lo stesso
preventivo dal punto di vista del dominio. La dataclass frozen espone campi,
`repr` leggibile e uguaglianza per contenuto, e impedisce l'aggiornamento dei
campi: la mutazione degli oggetti di dati non è parte del modello.

## Invarianti

- **Valore** (`Preventivo.__post_init__`): `codice` stringa non vuota,
  `destinazione` fra `locale` e `nazionale`, `totale_cent` intero non booleano
  non negativo. Il candidato completo viene validato alla costruzione: un
  valore non ammesso non esiste, solleva `DatoNonAmmesso`.
- **Raccolta** (`RegistroPreventivi`): codici unici con confronto esatto,
  ordine di inserimento conservato, ogni aggiornamento sostituisce l'intero
  valore nella posizione del codice.

Le regole dei valori restano quelle già verificate: `__post_init__` richiama
`valida_dominio_record`, così dominio e diagnosi non si duplicano fra U12 e
U14 e un cambiamento delle regole ha una sola sede.

## Dati derivati, non duplicati

`numero` e `totale_complessivo_cent` sono **proprietà derivate**: calcolano
dai valori già validati e non conservano campi aggiuntivi. Dopo un
inserimento o un'eliminazione i risultati cambiano senza alcun aggiornamento
da ricordare — la riprova è `test_proprio_dati_derivati_aggiornati`.

## Uguaglianza, identità e alias

- `Preventivo("007", "locale", 450) == Preventivo("007", "locale", 450)` è
  `True`: l'uguaglianza è per contenuto sui tre campi; `is` resta `False` e
  distingue le istanze (PU14-01).
- L'aggiornamento **sostituisce** il valore: chi conserva un riferimento al
  valore precedente continua a osservarlo, mentre la raccolta espone il
  valore nuovo. Gli alias non si legano alle sorti l'uno dell'altro (PU14-05).
- Lo snapshot `preventivi()` è una **tuple di valori frozen**: né gli elementi
  né il contenitore possono essere modificati dal ricevente.

## Errori di dominio

| Eccezione | Quando | Effetto |
|---|---|---|
| `DatoNonAmmesso` | un campo del candidato non rispetta il dominio | nessun valore consegnato, nessuna modifica |
| `CodiceDuplicato` | la raccolta contiene già il codice esatto | nessun inserimento, nessuna sostituzione |
| `CodiceAssente` | operazione su un codice non presente | nessuna modifica |

Sono sottoclassi di `ValueError`: chi conosce già i contratti storici può
intercettarle insieme, mentre la CLI le distingue per presentare la diagnosi
appropriata. L'alternativa — esiti booleani come in U13 — resta valida per
interfacce minime; qui le cause dei rifiuti sono tre e meritano nomi propri,
come richiede la consegna.

## Limiti dichiarati

- La rappresentazione interna resta una lista: non sono richieste strutture
  indicizzate né la ricerca dicotomica sulla raccolta.
- La concorrenza di più sessioni sullo stesso archivio non è gestita.
- `Preventivo` non ha metodi di calcolo: tariffe e totali delle spedizioni
  restano nelle funzioni storiche, che operano sulle proiezioni.
