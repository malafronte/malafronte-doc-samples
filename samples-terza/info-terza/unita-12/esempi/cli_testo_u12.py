"""CLI dell'analisi di testo: apertura, presentazione e diagnosi.

Questo modulo è il **coordinatore** dell'analizzatore del cap. PY-19: riceve
il percorso del file da analizzare, chiama `analizza_file`, presenta il
risultato e traduce gli errori attesi in messaggi e codici di uscita. Il
calcolo resta in `analisi_testo_u12.py`; qui ci sono soltanto scelte di
presentazione e recupero.

Uso da un terminale, dalla cartella `unita-12/` del repository:

    uv run --python 3.14 python esempi/cli_testo_u12.py dati/testi/analisi_canonica.txt

Codici di uscita: `0` analisi completata, `1` percorso o contenuto non
ammesso, `2` argomenti di riga di comando non validi.

Ambiente: CPython sul computer. La guardia `if __name__ == "__main__"` è
l'unico avvio automatico: importare il modulo non stampa e non chiede nulla.
"""

import sys
from pathlib import Path

from analisi_testo_u12 import analizza_file


def righe_presentazione(risultato):
    """Restituisce le righe di testo che presentano un risultato d'analisi.

    Nessuna stampa: la funzione costruisce una lista di stringhe e il
    coordinatore decide come mostrarle. Il vuoto è dichiarato, non taciuto:
    quando non ci sono parole le due classifiche riportano `(vuota)`.
    """
    righe = [
        f"parole totali: {risultato['totale']}",
        f"parole distinte: {len(risultato['frequenze'])}",
        "",
        "classifica per frequenza crescente (parola crescente a parità):",
    ]
    righe.extend(_righe_classifica(risultato["classifica_crescente"]))
    righe.append("")
    righe.append("classifica per frequenza decrescente (parola crescente a parità):")
    righe.extend(_righe_classifica(risultato["classifica_decrescente"]))
    return righe


def _righe_classifica(classifica):
    if not classifica:
        return ["  (vuota)"]
    return [f"  {parola} {frequenza}" for parola, frequenza in classifica]


def main(argv=None):
    """Coordina apertura, presentazione e diagnosi; ritorna un codice d'uscita.

    Con un solo argomento - il percorso del file - l'analisi viene eseguita e
    presentata. Gli errori attesi ricevono ciascuno il proprio messaggio: il
    percorso assente, il percorso che non è un file leggibile e i byte che non
    sono UTF-8 non vengono mai presentati come un'analisi riuscita. I difetti
    di programmazione non vengono catturati.
    """
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) != 1:
        print("uso: python cli_testo_u12.py <percorso-del-file>")
        return 2

    percorso = Path(argv[0])
    try:
        risultato = analizza_file(percorso)
    except FileNotFoundError:
        print(f"file non trovato: {percorso}")
        return 1
    except (IsADirectoryError, PermissionError):
        print(f"percorso non leggibile come file (directory o permessi): {percorso}")
        return 1
    except UnicodeDecodeError as errore:
        print(f"byte non UTF-8 alla posizione {errore.start}: {percorso}")
        return 1

    for riga in righe_presentazione(risultato):
        print(riga)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
