# Confronto delle consultazioni — viste ordinate (U10)

Documento sui costi delle viste ordinate costruite in questa tappa. Tre voci
distinte: **preparazione** della vista, **consultazione** singola o ripetuta,
**aggiornamento** dopo una modifica ai dati. Per ciascuna si distinguono la
prova teorica, il conteggio esatto e la misura empirica, secondo il protocollo
del capitolo sulla complessità.

## Prova teorica e conteggi

| Voce | Procedimento | Operazione contata | Costo teorico | Conteggio esatto |
|---|---|---|---|---|
| Preparazione di una vista | ordinamento per inserimento su una copia della lista | confronti fra chiavi e spostamenti | da Θ(n) a Θ(n²) secondo l'ordine iniziale | confronti: `n-1` con lista già ordinata, `n(n-1)/2` con lista in ordine inverso |
| Consultazione per codice | ricerca dicotomica sulla vista ordinata | confronti fra codici | Θ(log n) | al massimo `⌊log₂ n⌋ + 1` confronti |
| `q` consultazioni | ripetizione della ricerca | confronti | Θ(q · log n) | somma dei confronti delle singole ricerche |
| Aggiornamento | ricostruzione della vista dopo una modifica ai dati | come la preparazione | come la preparazione | come la preparazione |

Ipotesi: i codici sono stringhe di lunghezza limitata e il costo di un
confronto si considera costante; i record sono condivisi fra registro e vista,
quindi la copia riguarda la sola lista di riferimenti, non i record.

## Scelta del procedimento

La vista per codice e la vista per totale usano l'**ordinamento per
inserimento**: procedimento elementare studiato, stabile perché i confronti
sono stretti, con spazio aggiuntivo di una sola lista. La stabilità serve alla
vista per totale, dove i record con importo uguale devono conservare l'ordine
relativo del registro; alla vista per codice non serve, ma non guasta.

`sorted` viene usato come **oracolo**: il test `test_oracolo_sorted_sugli
stessi_criteri` confronta i risultati e non viene chiamato dalle funzioni
richieste, che implementano il procedimento scelto.

## Preparazione contro consultazione

La preparazione costa molto più di una consultazione singola: per `n = 1000`
l'ordinamento per inserimento nell'ordine peggiore esegue circa 500.000
confronti, mentre una ricerca dicotomica ne esegue al massimo 10. Con poche
consultazioni conviene quindi guardare al costo della preparazione; con molte
consultazioni ripetute lo stesso costo si distribuisce su `q` ricerche e la
vista diventa conveniente.

L'aggiornamento non è incrementale: un record **aggiunto** alla sorgente dopo
la costruzione non compare nella vista e un campo **mutato** può invalidarne
l'ordinamento. In entrambi i casi la vista si ricostruisce e si paga di nuovo
il costo di preparazione. Per dati che cambiano spesso e consultazioni poche,
la scansione lineare sul registro — la ricerca di U8 — resta la scelta
ragionevole.

## Che cosa è provato e che cosa va misurato

Il conteggio delle operazioni è esatto e indipendente dalla macchina: è ciò
che **prova** la forma dei costi. Le durate dipendono dall'interprete e dalla
postazione: vanno misurate con lo stesso protocollo della tappa U9 —
`time.perf_counter`, lotti, ripetizioni, campioni conservati — e non
sostituiscono i conteggi. L'esperimento comparativo fra procedimenti è
l'oggetto della tappa U11, che usa questa tappa come base di confronto.
