# LAB-PY-U15 — Starter di componenti intercambiabili

Lo starter è deliberatamente incompleto. Le soluzioni delle attività formative
insegnano i meccanismi; il completamento del laboratorio resta lavoro dello studente.

## Preparazione ed esecuzione

Usare il checkout degli esempi U15 e lavorare dalla radice `unita-15`, con Python 3.14
gestito da uv. Modello, validatori e servizio già studiati sono in `esempi/`.
I dati di `dataset()` sono sintetici in °C: `007/18`, `Lab, A/20`,
`Sonda "B"/-2`, `007/18`, in quell'ordine.

```powershell
uv sync --locked
uv run pytest laboratorio/starter/tests -q
```

La configurazione di pytest rende disponibili esempi e starter senza modifiche
manuali di `sys.path`. La suite dei riferimenti, `uv run pytest -q`, raccoglie
soltanto `tests/` e non questi test dello starter.

Esito iniziale previsto: un test riuscito e tre falliti con `NotImplementedError`.
`test_client_iniziale` passa prima dei completamenti; `test_intervallo_l03` e
`test_errori_l03` passano dopo L03; `test_delega_l05` passa dopo L05.

## Lavoro lasciato da svolgere

- L01: documentare dominio, bool, risultati, errori ed effetti.
- L02: prevedere e verificare il client iniziale, compresi ordine e duplicati.
- L03: completare `PoliticaIntervalloLaboratorio.ammette` e aggiungere prove comuni.
- L04: dichiarare e motivare ABC, Protocol o duck typing in un modulo proprio.
- L05: completare `EsportatoreMemoriaLaboratorio.esporta`; integrare poi uno degli
  esportatori CSV/JSON già insegnati e verificarne il round-trip in directory temporanea.
- L06: disegnare UML coerente, introdurre una variazione circoscritta e documentare
  esiti reali, comandi e regressione nel README del proprio lavoro.

Il client pronto `seleziona_rilevazioni` valida tutto il lotto, chiede un bool per
lettura e costruisce una nuova lista. `genera_rapporto` usa quel risultato e il
servizio già insegnato: la sostituzione dei collaboratori conserva queste chiamate.
La memoria simula il salvataggio; il parser CSV/JSON verifica il salvataggio reale.

La suite iniziale è parziale: aggiungere vuoto distinto, confini, duplicati, input
e configurazione conservati, dato invalido tardivo, collaboratori indipendenti e
guasto con file precedente preservato. Consegnare anche contratto, traccia e UML.
