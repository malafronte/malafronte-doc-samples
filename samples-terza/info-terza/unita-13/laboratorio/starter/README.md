# LAB-PY-U13 — Starter: disponibilità di kit didattici

Starter del laboratorio **LAB-PY-U13 — Dalla gestione procedurale al modello a
oggetti**. Questa cartella contiene la versione procedurale funzionante e la
cornice di esecuzione: **non** contiene la classe risolutiva né una suite già
completata.

## File forniti

| File | Contenuto |
|---|---|
| `depositi_procedurali.py` | Versione procedurale completa: record del deposito, carico, prelievo, spazio libero, situazione e confronto fra sessioni. |
| `dimostrazione_depositi.py` | Cornice di esecuzione: esegue i casi pubblici LAB13-01…LAB13-12 sulla versione procedurale e ne stampa la trascrizione. |
| `casi-pubblici.md` | Casi pubblici con risultato e stato atteso. |

## Ambiente e comandi

CPython sul computer, dalla directory che contiene questi file.

```powershell
python dimostrazione_depositi.py
```

La trascrizione è deterministica. Per la suite si usa `pytest` secondo la
[guida del corso](https://github.com/malafronte/malafronte-doc-samples):
i test vanno scritti dallo studente in questa cartella.

## Lavoro da completare

1. **Eseguire** la dimostrazione e compilare la scheda di traccia: per ogni
   passo, chiamata, ricevente, argomenti, esito e stato.
2. **Individuare** responsabilità, stato minimo, invariante e API candidata
   nella scheda di progetto. L'interazione con l'utente resta separata dal
   dominio: nessuna classe va creata soltanto per contenere funzioni.
3. **Scrivere** la classe `Deposito` con inizializzazione valida, carico,
   prelievo, spazio libero e proiezione dello stato. Nessun aggiornamento
   prima delle guardie; i valori restituiti sono quelli del contratto della
   versione procedurale.
4. **Creare** due istanze e un alias, intercalare le operazioni e registrare
   la traccia dei riferimenti e dello stato.
5. **Collegare** la dimostrazione alla nuova interfaccia e confrontare il
   comportamento con la versione procedurale: stessi risultati, stessi stati.
6. **Scrivere** test nominali, di rifiuto e di errore, più un test proprio
   discriminante e motivato.
7. **Diagnosticare** nel debugger un difetto attributo/locale e correggerlo,
   registrando il test fallito prima e superato dopo.
8. **Documentare** le scelte, eseguire Ruff e la suite, registrare una tappa
   Git significativa.

## Limiti dichiarati

- La persistenza **non** è necessaria al risultato centrale: nessun file
  va letto o scritto.
- Questo laboratorio non realizza il magazzino CSV del cap. PY-20 né il
  registro dei preventivi del progetto progressivo.
- La difficoltà riguarda responsabilità, stato ed effetti: la toolchain e i
  test sono prerequisiti già acquisiti.
