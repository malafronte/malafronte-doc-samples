# Contratti — funzioni del preventivo in forma di funzioni pure (U5)

Documento delle interfacce della tappa U5, redatto prima del codice. La
tariffa, i messaggi e la priorità degli errori sono quelli della versione U3:
il refactoring separa le responsabilità senza cambiare il comportamento.

## Funzioni di logica

| Firma | Contratto |
|---|---|
| `errore_dati_spedizione(peso_g: int, destinazione: str, urgenza: str) -> str` | Accetta qualsiasi valore dei tre tipi dichiarati. Restituisce `""` se i tre dati sono ammessi, altrimenti il primo errore secondo la priorità peso → destinazione → urgenza: `Peso non ammesso`, `Destinazione non ammessa`, `Urgenza non ammessa`. Nessuna normalizzazione dei testi. Non legge, non stampa, nessun effetto. |
| `costo_base_spedizione(peso_g: int) -> int` | Precondizione: peso ammesso (1-10000 g). Restituisce l'importo intero in euro secondo la fascia: 3 fino a 500 g, 5 fino a 2000 g, 8 oltre. Nessuna formattazione. |
| `supplemento_destinazione(destinazione: str) -> int` | Precondizione: token ammesso. Restituisce 0 per `locale`, 4 per `nazionale`, in euro interi. |
| `supplemento_urgenza(urgenza: str) -> int` | Precondizione: token ammesso. Restituisce 0 per `n`, 2 per `s`, in euro interi. |
| `totale_spedizione(peso_g: int, destinazione: str, urgenza: str) -> int` | Precondizione: dati ammessi. Restituisce la somma dei tre importi in euro interi, chiamando le tre funzioni sopra. Nessun effetto. |

Le cinque funzioni non leggono input, non stampano e non dipendono da globali
variabili: ogni risultato dipende soltanto dai parametri. Le componenti del
prezzo si possono verificare separatamente e la loro somma è il totale: questa
è la ragione della decomposizione.

## Operazioni sui preventivi (milestone M26-M27)

Dominio comune: lista di importi **interi non negativi in euro**, lista vuota
compresa; l'importo aggiuntivo è un intero non negativo in euro. Le unità sono
euro: la conversione in centesimi non appartiene a questa tappa.

| Firma | Effetti | Risultato |
|---|---|---|
| `registra_preventivo(preventivi, importo_euro) -> None` | Modifica la lista **in posto**, aggiungendo l'importo in coda | `None` |
| `anteprima_preventivo(preventivi, importo_euro) -> list` | Nessun effetto sulla lista ricevuta | Lista **nuova** con gli importi noti e quello aggiuntivo in coda; oggetto diverso dall'originale |
| `riepilogo_preventivi(preventivi) -> tuple[int, int]` | Nessun effetto sulla lista ricevuta | Tupla `(numero, somma)`; lista vuota → `(0, 0)` |

Sull'identità si fa una promessa limitata: `registra_preventivo` restituisce
`None` e agisce sulla lista ricevuta, `anteprima_preventivo` restituisce un
oggetto diverso dall'argomento. Nessuna promessa sulle liste **contenute**:
gli importi sono interi immutabili e non ci sono liste annidate.

## CLI

`main() -> None` effettua l'interazione: legge i tre testi nell'ordine di U3,
converte il peso con `int`, chiama `errore_dati_spedizione` e, se l'esito è
vuoto, stampa il riepilogo e le quattro righe `Costo base`, `Supplemento
destinazione`, `Supplemento urgenza`, `Totale`, con due cifre decimali e la
parola `euro`. Su errore stampa il solo messaggio del validatore, senza righe
di costo. La guardia `if __name__ == "__main__":` garantisce che l'import del
modulo non avvii l'interazione.
