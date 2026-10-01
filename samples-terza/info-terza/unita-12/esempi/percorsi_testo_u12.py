"""Percorsi, apertura, modalità, righe ed EOF: dimostrazioni sui file reali.

Questo modulo accompagna il cap. PY-19 con esperimenti **osservabili** sulle
fixture della cartella `dati/testi/` e su un file di prova creato in una
cartella temporanea. Ogni funzione raccoglie un esperimento e ne restituisce i
risultati; la stampa è soltanto in `main()`, sotto la guardia di avvio.

Nuclei:

- `radici_di_lavoro()` - directory corrente, cartella del sorgente, risoluzione
  dello stesso percorso relativo e variabile d'ambiente con default;
- `riepilogo_percorso(percorso)` - fatti osservabili di un percorso;
- `leggi_con_iterazione`, `leggi_con_readline`, `leggi_con_readlines` - i tre
  modi di leggere le righe, con il confronto su EOF e terminatore;
- `esperimento_modalita(cartella)` - effetti di `w`, `a` e `x` su un file di
  prova, troncatura compresa;
- `byte_iniziali(percorso, quantita)` - primi byte del file senza decodificarli,
  per osservare la firma UTF-8;
- `prova_apertura(percorso)` - esito dell'apertura in lettura, con la sola
  classe dell'errore nominata.

Ambiente: CPython sul computer. Gli esperimenti di scrittura usano una cartella
temporanea: le fixture di `dati/testi/` restano in sola lettura.
"""

import os
from pathlib import Path

CARTELLA_DATI = Path(__file__).resolve().parent.parent / "dati" / "testi"


def radici_di_lavoro():
    """Confronta le radici rispetto alle quali si risolvono i percorsi.

    Il risultato è un dizionario nuovo con i fatti della sessione corrente:
    la directory di lavoro vista da `os` e da `pathlib`, la cartella che
    contiene questo sorgente, la risoluzione dello **stesso** percorso relativo
    rispetto a due radici diverse e il valore di una variabile d'ambiente
    dimostrativa con il proprio default.
    """
    relativo = Path("dati/testi/analisi_canonica.txt")
    sorgente = Path(__file__).resolve().parent
    return {
        "os.getcwd()": os.getcwd(),
        "Path.cwd()": str(Path.cwd()),
        "cartella del sorgente": str(sorgente),
        "relativo da Path.cwd()": str(relativo.resolve()),
        "relativo dalla cartella del sorgente": str((sorgente / relativo).resolve()),
        "CORSO_UTENTE (default: ospite)": os.getenv("CORSO_UTENTE", "ospite"),
    }


def riepilogo_percorso(percorso):
    """Descrive i fatti osservabili di un percorso, senza aprirlo.

    Il risultato è un dizionario nuovo con il testo ricevuto, la forma
    assoluta, l'esistenza, la natura di file o directory, il nome e il
    suffisso. Un percorso inesistente ha comunque forma assoluta e nome:
    `esiste` è `False` e gli altri due controlli pure.
    """
    percorso = Path(percorso)
    return {
        "testo": str(percorso),
        "assoluto": str(percorso.resolve()),
        "esiste": percorso.exists(),
        "e_file": percorso.is_file(),
        "e_directory": percorso.is_dir(),
        "nome": percorso.name,
        "suffisso": percorso.suffix,
    }


def leggi_con_iterazione(percorso):
    """Legge le righe con un ciclo `for` e le restituisce come lista.

    Ogni riga conserva il proprio terminatore, tranne l'ultima quando il file
    non lo prevede. L'iterazione si ferma da sola alla fine del file.
    """
    righe = []
    with open(percorso, "r", encoding="utf-8") as sorgente:
        for riga in sorgente:
            righe.append(riga)
    return righe


def leggi_con_readline(percorso):
    """Legge le righe con `readline()` fino al valore di fine file.

    Il risultato è la coppia `(righe, ultima_terminata)`: la lista delle righe
    lette e un booleano che dice se l'ultima riga restituita termina con
    `\\n`. Il valore `""` restituito da `readline()` segnala la fine del file e
    non viene incluso fra le righe; una riga `\\n` è invece una riga vuota del
    file ed è un dato.
    """
    righe = []
    with open(percorso, "r", encoding="utf-8") as sorgente:
        riga = sorgente.readline()
        while riga != "":
            righe.append(riga)
            riga = sorgente.readline()
    ultima_terminata = bool(righe) and righe[-1].endswith("\n")
    return righe, ultima_terminata


def leggi_con_readlines(percorso):
    """Legge tutto con `readlines()` e restituisce la lista delle righe.

    `readlines()` legge il file intero prima di restituire: comodo sui file
    piccoli, ma la lista finale cresce con il file. Le righe sono nelle stesse
    forme dell'iterazione, terminatore compreso.
    """
    with open(percorso, "r", encoding="utf-8") as sorgente:
        return sorgente.readlines()


def esperimento_modalita(cartella):
    """Scrive un file di prova con `w`, `a` e `x` e descrive gli effetti.

    `cartella` è una cartella **di lavoro**: il file `prova_modalita.txt` viene
    creato, esteso, riscritto e lasciato al suo posto. Il risultato è una
    lista di coppie `(passo, effetto)` nell'ordine in cui gli effetti si
    producono: la modalità `w` crea il file se manca e **lo tronca** se
    esiste, `a` aggiunge in fondo, `x` crea soltanto se il nome è ancora
    libero e rifiuta altrimenti senza toccare il contenuto.
    """
    prova = Path(cartella) / "prova_modalita.txt"
    osservazioni = []

    with open(prova, "w", encoding="utf-8") as destinazione:
        destinazione.write("prima riga\n")
    osservazioni.append(("w su file assente: crea", repr(prova.read_text(encoding="utf-8"))))

    with open(prova, "a", encoding="utf-8") as destinazione:
        destinazione.write("seconda riga\n")
    osservazioni.append(("a su file esistente: aggiunge in fondo", repr(prova.read_text(encoding="utf-8"))))

    with open(prova, "w", encoding="utf-8") as destinazione:
        destinazione.write("riscrittura\n")
    osservazioni.append(("w su file esistente: tronca e riscrive", repr(prova.read_text(encoding="utf-8"))))

    try:
        with open(prova, "x", encoding="utf-8"):
            pass
    except FileExistsError:
        osservazioni.append(("x su file esistente: rifiuta", "FileExistsError, contenuto invariato"))
    osservazioni.append(("contenuto finale di prova_modalita.txt", repr(prova.read_text(encoding="utf-8"))))

    nuovo = Path(cartella) / "secondo_prova.txt"
    with open(nuovo, "x", encoding="utf-8") as destinazione:
        destinazione.write("creato da x\n")
    osservazioni.append(("x su nome libero: crea", repr(nuovo.read_text(encoding="utf-8"))))
    return osservazioni


def byte_iniziali(percorso, quantita=6):
    """Restituisce i primi `quantita` byte del file senza decodificarli.

    La lettura è **binaria** (`rb`): serve a osservare la firma UTF-8
    `EF BB BF` come sequenza di byte, prima di qualunque interpretazione come
    testo. L'accesso per posizione sui file binari è argomento del cap. PY-21.
    """
    with open(percorso, "rb") as sorgente:
        return sorgente.read(quantita)


def prova_apertura(percorso):
    """Prova l'apertura in lettura e descrive l'esito con la sola classe.

    Il risultato è la stringa `apertura riuscita` oppure `apertura non
    riuscita: <classe>`. Il messaggio del sistema non viene riportato perché
    cambia fra sistemi operativi e versioni. La funzione **apre e chiude**
    senza leggere: un file con byte non decodificabili supera l'apertura e
    fallisce più tardi, alla prima lettura.
    """
    try:
        with open(percorso, "r", encoding="utf-8"):
            pass
    except OSError as errore:
        return f"apertura non riuscita: {type(errore).__name__}"
    return "apertura riuscita"


if __name__ == "__main__":
    import tempfile

    canonico = CARTELLA_DATI / "analisi_canonica.txt"
    senza_terminatore = CARTELLA_DATI / "analisi_no_newline.txt"
    con_bom = CARTELLA_DATI / "analisi_con_bom.txt"

    print("=== A. Fatti di un percorso ===")
    for chiave, valore in riepilogo_percorso(canonico).items():
        print(f"{chiave}: {valore}")

    print()
    print("=== B. Radici di lavoro e ambiente ===")
    for chiave, valore in radici_di_lavoro().items():
        print(f"{chiave}: {valore}")

    print()
    print("=== D. Modalità ed effetti (cartella temporanea) ===")
    with tempfile.TemporaryDirectory() as cartella:
        for passo, effetto in esperimento_modalita(cartella):
            print(f"{passo} -> {effetto}")

    print()
    print("=== E. Righe, terminatore ed EOF ===")
    for nome in (canonico, senza_terminatore):
        righe, ultima_terminata = leggi_con_readline(nome)
        print(f"{nome.name}: righe={righe!r}")
        print(f"{nome.name}: ultima riga terminata = {ultima_terminata}")
        print(f"{nome.name}: iterazione = {leggi_con_iterazione(nome)!r}")
        print(f"{nome.name}: readlines = {leggi_con_readlines(nome)!r}")

    print()
    print("=== F. I primi byte, prima della decodifica ===")
    print(f"{con_bom.name}: {byte_iniziali(con_bom).hex(' ').upper()}")
    vuota = CARTELLA_DATI / "analisi_vuota.txt"
    print(f"{vuota.name}: {byte_iniziali(vuota).hex(' ') or '(nessun byte)'}")

    print()
    print("=== H. Diagnosi delle aperture ===")
    for caso in (
        CARTELLA_DATI / "non_esiste.txt",
        CARTELLA_DATI,
        CARTELLA_DATI / "byte_incompatibili.txt",
    ):
        print(f"{caso.name}: {prova_apertura(caso)}")
