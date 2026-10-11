# Confronto fra funzioni e classe di sessione — U13

Analisi del cambiamento introdotto dalla tappa M49-M50: che cosa resta
procedurale, che cosa diventa metodo, e perché. Affianca
[`modello.md`](modello.md) e [`prove.md`](prove.md).

## Prima: funzioni su liste ricevute

Il registro U12 era un insieme di funzioni — `inserisci_record`,
`aggiorna_record`, `elimina_record`, `cerca_preventivo` — che operavano su una
lista passata dal chiamante. La sessione della CLI era una variabile locale e
la lista era esplicita in ogni chiamata: lo stato non aveva un luogo
dichiarato, e chi riceveva la lista poteva conservarla o modificarla.

## Dopo: la classe conserva lo stato, il dominio conserva gli algoritmi

`RegistroPreventivi` raccoglie la lista nella sessione e offre le stesse
operazioni come metodi. Gli algoritmi restano riconoscibili e nei loro
contratti originali: ogni metodo chiama la corrispondente funzione di
`registro_dominio.py` sulla lista interna. La classe aggiunge
**responsabilità**, non riscrive i procedimenti.

| Aspetto | Funzioni (U12) | Classe di sessione (U13) |
|---|---|---|
| Stato | lista esplicita, passata dal chiamante | attributo `_preventivi` dell'istanza |
| Operazioni | funzioni sulle liste | metodi che delegano alle stesse funzioni |
| Invariante | valido per chi lo controlla | conservato dalle sole operazioni della classe |
| Conversioni | record già nella rappresentazione esterna | `per_lista()` e `sostituisci_da_lista()` esplicite |
| Sessioni indipendenti | dipendono dal chiamante | garantite dall'`__init__` di ogni istanza |
| Rifiuti | booleani | gli stessi booleani, dichiarati nei contratti |

## Perché una classe, e perché proprio questa

La classe risponde a un requisito concreto: durante una sessione il registro
conserva i preventivi inseriti o caricati, e due sessioni devono poter
procedere senza interferire. Raccogliere quello stato in un'entità rende
visibile il ciclo di vita della sessione e permette di dichiarare la politica
di copia ai suoi confini. Una classe senza stato utile — per esempio un
contenitore di funzioni senza attributi — non avrebbe lo stesso motivo
d'essere.

Il singolo preventivo resta un dizionario: la classe `Preventivo` non è
richiesta, non cambia il comportamento osservabile e andrebbe giustificata
rispetto al record. La scelta è aperta allo studente: questa realizzazione la
motiva con l'assenza di comportamento proprio del singolo preventivo.

## Limiti dichiarati

- I rifiuti restano booleani: non sono previste eccezioni di dominio né
  proprietà, che appartengono all'Unità 14.
- La classe non sostituisce le funzioni storiche: riepiloghi, viste e ricerche
  restano in `spedizione_u5.py` e si applicano alle liste prodotte da
  `per_lista()`.
- La concorrenza di più sessioni sullo stesso archivio non è gestita: la
  politica di salvataggio resta quella U12.
- La CLI mantiene i comportamenti già verificati; il raccordo avviene con le
  conversioni esplicite, senza duplicare la logica del dominio.
