# Contratti — coppie e tabelle di sintesi (U7)

Documento della tappa U7, scritto prima del codice. Le nuove funzioni operano
**sopra** i dati già verificati: la CLI della tariffa non cambia e nessuna
funzione di tariffazione viene riscritta.

## Mappa delle rappresentazioni

| Livello | Rappresentazione | Unità | Dove nasce |
|---|---|---|---|
| U5, parte scalare | interi da `totale_spedizione` | **euro** | chiamate dirette alle funzioni di tariffazione |
| U5, M26-M27 | lista di soli importi | **euro** | registrazione, anteprima, riepilogo |
| U6, M28-M30 | lista di interi per `totale_preventivi_ric` | **centesimi** | conversione dalla lista U5 |
| U7, M31-M33 | lista di tuple `(destinazione, totale_cent)` | **centesimi** | `prepara_coppie` |

Tre vincoli derivano dalla storia del progetto: il listino ammette solo
`locale` e `nazionale`; le destinazioni **non si ricostruiscono** dagli importi
storici della lista U5, che contengono soltanto numeri — le coppie si
costruiscono ora dai dati di spedizione; la conversione euro → centesimi si
esegue **una sola volta**, quando la coppia viene costruita.

## Funzioni richieste

| Firma | Contratto |
|---|---|
| `normalizza_destinazione(destinazione: str) -> str` | Applica `strip()` e `casefold()`. Precondizione: il risultato è `locale` oppure `nazionale`. Non elimina spazi interni, non cambia accenti, non traduce sinonimi. La stringa ricevuta resta invariata; nessuna garanzia di identità diversa per il risultato. |
| `preventivi_sopra_media(preventivi) -> list` | Riceve coppie già normalizzate. Restituisce una lista **nuova**, in ordine originale, con le coppie il cui totale è strettamente sopra la media dei totali, **senza arrotondamento**; conserva duplicati e input; vuoto → `[]`. Le tuple selezionate possono essere condivise, perché i loro elementi sono immutabili. |
| `matrice_riepilogo(preventivi) -> tuple[list, list]` | Riceve coppie già normalizzate. Restituisce `(conteggi, somme_cent)`: due liste nuove e distinte, due elementi ciascuna, nell'ordine fisso `locale`, `nazionale`; vuoto → `([0, 0], [0, 0])`. L'input resta conservato. |

## Funzione di preparazione

`prepara_coppie(dati_spedizione) -> list` riceve le terne
`(peso_g, destinazione_testo, urgenza)` e costruisce le coppie U7. Il flusso è:
normalizzare la destinazione con `normalizza_destinazione`, calcolare
`totale_spedizione` in euro e convertire **una sola volta** con
`totale_euro * 100`. Per esempio `(100, "locale", "n")` produce 3 euro e la
coppia `("locale", 300)`, non `("locale", 3)` né `("locale", 30000)`.

La **verifica** dei dati normalizzati con `errore_dati_spedizione` resta un
passo esplicito del flusso di preparazione e si esercita nei test di raccordo
insieme al rifiuto di `estero`: la funzione di preparazione ha precondizione
dati ammessi e non duplica il validatore, che conserva il proprio contratto.

## Test unitari e test di raccordo

I test unitari delle tre funzioni ricevono liste di coppie già normalizzate e
controllano ordine, duplicati, media stretta, liste nuove e conservazione
dell'input. I test di raccordo partono dai **dati di spedizione** e verificano
anche normalizzazione e conversione singola: confrontare due liste già
predisposte in centesimi non basterebbe a rilevare una conversione ripetuta.

## Errori da evitare

- Convertire due volte: `totale_cent * 100` sugli importi già in centesimi
  produce totali cento volte maggiori senza errori in esecuzione.
- Confondere la lista U5 di importi in euro con la lista U7 di coppie in
  centesimi: sono rappresentazioni diverse e non si sostituiscono.
- Arrotondare la media prima del confronto: la specifica chiede il confronto
  stretto senza arrotondamento.
