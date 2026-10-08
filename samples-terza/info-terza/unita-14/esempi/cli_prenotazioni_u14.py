"""CLI delle prenotazioni: menu, acquisizione e presentazione (OOP-04, sez. G).

Applicazione **circoscritta**: quattro moduli con dipendenze in una sola
direzione — `intervalli_u14` (valore), `prenotazioni_u14` (dominio),
`csv_prenotazioni_u14` (persistenza) e questo modulo (confine). La sessione
lavora **in memoria**: non esiste un archivio di avvio né un autosalvataggio.
L'importazione legge un CSV scelto di volta in volta; l'esportazione scrive
il file richiesto. Prima di uscire il programma **dichiara** che i dati non
esportati restano solo nella sessione: la voce "0" non afferma di salvare.

Menu: `1` riepilogo, `2` registrazione, `3` annullamento, `4` modifica,
`5` importazione CSV, `6` esportazione CSV, `0` uscita.

Gli orari si digitano nel formato `HH:MM`, con **due cifre** per parte:
`09:30` è ammesso, `9:30` no. `24:00` è ammesso solo come confine finale
dell'intervallo. Il convertitore appartiene a questo confine: il dominio
riceve minuti interi e i test lo provano anche direttamente sui numeri.

La CLI gestisce **solo gli errori attesi** del proprio dominio: rifiuti
(`ValueError`, `CodiceDuplicato`, `ConflittoPrenotazione`) e guasti di I/O
(`FileNotFoundError`, `OSError`, `csv.Error`, `UnicodeDecodeError`). Ogni
altro errore è un difetto di programmazione e deve fermare il programma,
non essere trasformato in un messaggio di successo.

Codici di uscita: 0 uscita con la voce "0", 1 interruzione per fine
dell'input, 2 argomenti non validi.

Ambiente: CPython sul computer. La guardia `if __name__ == "__main__"` è
l'unico punto che avvia il menu.
"""

import csv
import sys

from csv_prenotazioni_u14 import esporta_registro, importa_lotto
from intervalli_u14 import Intervallo
from prenotazioni_u14 import (
    CodiceDuplicato,
    ConflittoPrenotazione,
    Prenotazione,
    RegistroPrenotazioni,
)

MENU = """\
1 - riepilogo
2 - registrazione
3 - annullamento
4 - modifica
5 - importazione CSV
6 - esportazione CSV
0 - uscita"""

ERRORI_ATTESI = (ValueError, CodiceDuplicato, ConflittoPrenotazione)


def minuti_in_testo(minuti):
    """Formatta i minuti da mezzanotte come `HH:MM`. Funzione pura."""
    return f"{minuti // 60:02d}:{minuti % 60:02d}"


def testo_in_minuti(testo, estremo_finale=False):
    """Converte `HH:MM` in minuti da mezzanotte, con controlli di dominio.

    Le due parti hanno esattamente due cifre. Gli orari vanno da `00:00` a
    `23:59`; `24:00` è ammesso **solo** quando `estremo_finale` è `True`,
    perché rappresenta il confine di fine giornata, non un orario di inizio.
    Solleva `ValueError` con la diagnosi del motivo.
    """
    if not isinstance(testo, str) or len(testo) != 5 or testo[2] != ":":
        raise ValueError(f"orario {testo!r}: atteso il formato HH:MM")
    parte_ore = testo[:2]
    parte_minuti = testo[3:]
    if not (parte_ore.isdigit() and parte_minuti.isdigit()):
        raise ValueError(f"orario {testo!r}: attese due cifre per parte")
    ore = int(parte_ore)
    minuti = int(parte_minuti)
    if ore == 24 and minuti == 0 and estremo_finale:
        return 1440
    if not (0 <= ore <= 23 and 0 <= minuti <= 59):
        raise ValueError(f"orario {testo!r}: fuori dal dominio della giornata")
    return ore * 60 + minuti


def leggi_orario(prompt, estremo_finale=False):
    """Legge un orario e restituisce i minuti. Ripete finché non è valido."""
    while True:
        testo = input(prompt).strip()
        try:
            return testo_in_minuti(testo, estremo_finale)
        except ValueError as errore:
            print(f"dato non valido: {errore}")


def leggi_intero_positivo(prompt):
    """Legge un intero positivo. Ripete finché non è valido."""
    while True:
        testo = input(prompt).strip()
        try:
            valore = int(testo)
        except ValueError:
            print(f"dato non valido: {testo!r} non è un intero")
            continue
        if valore <= 0:
            print(f"dato non valido: {valore}: atteso un intero positivo")
            continue
        return valore


def leggi_intervallo():
    """Legge inizio e fine e costruisce l'`Intervallo`, con i suoi rifiuti."""
    while True:
        inizio_min = leggi_orario("ora di inizio (HH:MM)> ")
        fine_min = leggi_orario("ora di fine (HH:MM)> ", estremo_finale=True)
        try:
            return Intervallo(inizio_min, fine_min)
        except ValueError as errore:
            print(f"intervallo rifiutato: {errore}")


def riga_prenotazione(prenotazione):
    """Riga di presentazione con gli orari formattati. Non stampa."""
    intervallo = prenotazione.intervallo
    inizio = minuti_in_testo(intervallo.inizio_min)
    fine = minuti_in_testo(intervallo.fine_min)
    durata = intervallo.durata_min
    return (
        f"{prenotazione.codice} - aula {prenotazione.aula} - "
        f"{inizio}-{fine} ({durata} min) - {prenotazione.partecipanti} partecipanti"
    )


def mostra_riepilogo(registro):
    """Presenta i totali e l'elenco. Non muta il registro."""
    totale = registro.riepilogo()
    print(f"prenotazioni: {totale['numero_prenotazioni']}")
    print(f"minuti di occupazione complessivi: {totale['durata_totale_min']}")
    print(f"partecipazioni complessive: {totale['partecipanti_totali']}")
    if not totale["prenotazioni"]:
        print("(nessuna prenotazione)")
    for record in totale["prenotazioni"]:
        inizio = minuti_in_testo(record["inizio_min"])
        fine = minuti_in_testo(record["fine_min"])
        durata = record["fine_min"] - record["inizio_min"]
        print(
            f"{record['codice']} - aula {record['aula']} - "
            f"{inizio}-{fine} ({durata} min) - {record['partecipanti']} partecipanti"
        )
    return None


def chiedi_conferma(domanda):
    """Chiede conferma e restituisce `True` solo per una "s" esplicita."""
    risposta = input(domanda).strip().casefold()
    return risposta == "s"


def main(argv=None):
    """Coordina menu, acquisizione e presentazione della sessione in memoria."""
    if argv is None:
        argv = sys.argv[1:]
    if argv:
        print("uso: python cli_prenotazioni_u14.py")
        print("la sessione lavora in memoria; nessun archivio di avvio")
        return 2

    registro = RegistroPrenotazioni()
    while True:
        print(MENU)
        try:
            scelta = input("scelta> ").strip()
            match scelta:
                case "1":
                    mostra_riepilogo(registro)
                case "2":
                    try:
                        codice = input("codice> ").strip()
                        aula = input("aula> ").strip()
                        intervallo = leggi_intervallo()
                        partecipanti = leggi_intero_positivo("partecipanti> ")
                        registro.registra(Prenotazione(codice, aula, intervallo, partecipanti))
                    except ERRORI_ATTESI as errore:
                        print(f"registrazione rifiutata: {errore}")
                    else:
                        print(f"prenotazione {codice!r} registrata")
                case "3":
                    codice = input("codice> ").strip()
                    try:
                        rimosso = registro.annulla(codice)
                    except ValueError as errore:
                        print(f"annullamento rifiutato: {errore}")
                    else:
                        if rimosso:
                            print(f"prenotazione {codice!r} annullata")
                        else:
                            print(f"nessuna prenotazione con codice {codice!r}")
                case "4":
                    try:
                        codice = input("codice> ").strip()
                        aula = input("nuova aula> ").strip()
                        intervallo = leggi_intervallo()
                        partecipanti = leggi_intero_positivo("partecipanti> ")
                        applicato = registro.modifica(codice, aula, intervallo, partecipanti)
                    except ERRORI_ATTESI as errore:
                        print(f"modifica rifiutata: {errore}")
                    else:
                        if applicato:
                            print(f"prenotazione {codice!r} modificata")
                        else:
                            print(f"nessuna prenotazione con codice {codice!r}")
                case "5":
                    percorso = input("file da importare> ").strip()
                    try:
                        importa_lotto(percorso, registro)
                    except FileNotFoundError:
                        print(f"file assente: {percorso!r}")
                    except UnicodeDecodeError as errore:
                        print(f"file non leggibile come UTF-8: {errore}")
                    except csv.Error as errore:
                        print(f"file CSV malformato: {errore}")
                    except ERRORI_ATTESI as errore:
                        print(f"importazione rifiutata: {errore}")
                        print("il registro conserva lo stato precedente")
                    except OSError as errore:
                        print(f"errore di accesso al file: {errore}")
                    else:
                        print(f"importazione completata: {percorso}")
                case "6":
                    percorso = input("file di destinazione> ").strip()
                    try:
                        esporta_registro(percorso, registro)
                    except (OSError, csv.Error) as errore:
                        print(f"esportazione non riuscita: {errore}")
                        print("il file precedente, se esisteva, resta invariato")
                    else:
                        print(f"registro esportato: {percorso}")
                case "0":
                    print("i dati non esportati restano solo in questa sessione")
                    return 0
                case _:
                    print(f"comando non riconosciuto: {scelta!r}")
        except EOFError:
            print("sessione interrotta: l'input è terminato")
            print("i dati non esportati restano solo in questa sessione")
            return 1


if __name__ == "__main__":
    raise SystemExit(main())
