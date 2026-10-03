# Il flusso sorgente → interprete → processo → output

Spiegazione della tappa U1 richiesta dalla consegna del progetto, applicata a
questa raccolta. Il testo accompagna i tre programmi di `programmi/` e si
legge insieme a loro.

## I quattro momenti

Il **sorgente** è il file `.py` scritto dal programmatore: per questa raccolta
sono `01_hello.py`, `02_benvenuto.py` e `03_messaggio_multiriga.py`. Contiene
istruzioni in testo ordinato, leggibile e modificabile, ma non produce nulla da
solo.

L'**interprete** è CPython, il programma che legge il sorgente e ne esegue le
istruzioni una dopo l'altra. Nella raccolta lo si avvia con
`uv run python programmi/01_hello.py`: `uv` prepara l'ambiente dichiarato in
`pyproject.toml` e affida il file all'interprete.

Il **processo** è l'esecuzione in corso: un'istanza dell'interprete che ha
letto quel sorgente e ne compie le istruzioni. Finisce quando l'ultima
istruzione è stata eseguita; di quel processo rimane ciò che ha prodotto.

L'**output** è il testo che il processo invia allo standard output e che il
terminale mostra come righe successive. In questi programmi ogni istruzione
`print` produce una riga e va a capo: quattro `print` in `03_messaggio_multiriga.py`
producono quattro righe, nell'ordine in cui compaiono nel sorgente.

## Applicato a un programma della raccolta

Si consideri `02_benvenuto.py`. Il sorgente contiene tre istruzioni `print` in
ordine. All'avvio del processo, l'interprete esegue la prima istruzione e il
terminale mostra `Benvenuto nella raccolta di programmi.`; poi la seconda e la
terza, ciascuna sulla propria riga. Nessuna istruzione viene saltata e nessuna
ne esegue un'altra: l'ordine dell'output coincide con l'ordine del sorgente.

La distinzione fra i quattro momenti serve nella diagnosi. Se il terminale non
mostra nulla, il problema può essere nella fase di avvio — comando errato,
percorso errato — e non nel sorgente. Se il processo si ferma con un errore, il
messaggio indica quale istruzione l'interprete non ha potuto eseguire. Se
l'output non è quello previsto, il sorgente contiene istruzioni diverse da
quelle che si credeva di aver scritto: si confrontano le righe del file con le
righe stampate.

## Cosa non è ancora in gioco

In questa tappa il sorgente non legge dati dall'utente e non prende decisioni:
ogni esecuzione produce sempre lo stesso output. Input, conversioni, f-string e
diagnosi dei casi non conformi sono della tappa U2; selezioni e validazione
della U3; ripetizioni e stato della U4.
