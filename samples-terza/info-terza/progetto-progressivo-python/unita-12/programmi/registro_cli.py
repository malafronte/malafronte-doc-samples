"""Interazione a riga di comando del registro dei preventivi (U12).

Responsabilità del modulo: leggere i comandi, mostrare gli esiti e tenere il
conto delle modifiche pendenti. La logica è in `registro_dominio.py` e la
persistenza in `registro_persistenza.py`: le dipendenze vanno in una sola
direzione, dall'interazione verso il dominio e la persistenza.

Comandi: `carica`, `elenco`, `cerca`, `inserisci`, `aggiorna`, `elimina`,
`salva`, `esporta`, `esci`. Comportamenti dichiarati:

- **modifiche pendenti**: ogni inserimento, aggiornamento ed eliminazione
  rende pendente il salvataggio; `esci` con modifiche pendenti chiede
  conferma e non salva in silenzio;
- **salvataggio esplicito**: il messaggio di successo compare solo quando il
  file è stato sostituito; un guasto lascia il file precedente invariato;
- **EOF**: la fine dell'input termina la sessione con un messaggio, senza
  salvataggio automatico; le modifiche non salvate restano solo in memoria;
- **import del modulo**: nessuna domanda, nessuna stampa, nessuna scrittura.

Esecuzione, dalla root del progetto:

    uv run python programmi/registro_cli.py
"""
from pathlib import Path

from registro_dominio import (
    aggiorna_record,
    cerca_preventivo,
    elimina_record,
    formatta_euro,
    inserisci_record,
    riepilogo_per_destinazione,
)
from registro_persistenza import carica_archivio, esporta_csv, salva_archivio

PERCORSO_PREDEFINITO = Path("dati") / "unita-12" / "archivio.json"
PERCORSO_CSV = Path("dati") / "unita-12" / "esportazione.csv"
INTESTAZIONE = (
    "Comandi: carica, elenco, cerca, inserisci, aggiorna, elimina, salva, "
    "esporta, esci"
)


def riga_record(record: dict) -> str:
    """Restituisce la riga di presentazione di un record, importo in euro."""
    return (
        f"{record['codice']} | {record['destinazione']} | "
        f"{formatta_euro(record['totale_cent'])} euro "
        f"({record['totale_cent']} centesimi)"
    )


def comanda_elenco(registro: list) -> str:
    """Restituisce il testo dell'elenco dei record, con il riepilogo."""
    righe = []
    for record in registro:
        righe.append(riga_record(record))
    riepilogo = riepilogo_per_destinazione(registro)
    righe.append(
        f"locale: {riepilogo['locale']['conteggio']} preventivi, "
        f"{formatta_euro(riepilogo['locale']['totale_cent'])} euro"
    )
    righe.append(
        f"nazionale: {riepilogo['nazionale']['conteggio']} preventivi, "
        f"{formatta_euro(riepilogo['nazionale']['totale_cent'])} euro"
    )
    return "\n".join(righe)


def comanda_cerca(registro: list, codice: str) -> str:
    """Restituisce il testo della consultazione per codice."""
    record = cerca_preventivo(registro, codice)
    if record is None:
        return f"Nessun record con codice {codice!r}."
    return riga_record(record)


def comanda_inserisci(registro: list, codice: str, destinazione: str, totale_cent: int):
    """Tenta l'inserimento; restituisce (messaggio, modifica_avvenuta)."""
    if inserisci_record(registro, codice, destinazione, totale_cent):
        return "Record inserito.", True
    return "Inserimento rifiutato: codice già presente oppure dati non ammessi.", False


def comanda_aggiorna(registro: list, codice: str, destinazione: str, totale_cent: int):
    """Tenta l'aggiornamento; restituisce (messaggio, modifica_avvenuta)."""
    if aggiorna_record(registro, codice, destinazione, totale_cent):
        return "Record aggiornato.", True
    return "Aggiornamento rifiutato: codice assente oppure dati non ammessi.", False


def comanda_elimina(registro: list, codice: str):
    """Tenta l'eliminazione; restituisce (messaggio, modifica_avvenuta)."""
    if elimina_record(registro, codice):
        return "Record eliminato.", True
    return "Eliminazione rifiutata: nessun record con questo codice.", False


def leggi_riga(prompt: str):
    """Legge una riga dall'input; restituisce None se l'input termina (EOF).

    La fine dell'input non è un comando: ogni punto di lettura la riconosce e
    la tratta come fine della sessione, senza salvataggio automatico.
    """
    try:
        return input(prompt)
    except EOFError:
        return None


def main() -> None:
    """Sessione di interazione sul registro, con salvataggio esplicito."""
    registro = []
    percorso_archivio = PERCORSO_PREDEFINITO
    modifiche_pendenti = False

    print(INTESTAZIONE)
    while True:
        comando = leggi_riga("registro> ")
        if comando is None:
            print("Input terminato: le modifiche non salvate restano solo in memoria.")
            return
        comando = comando.strip()

        if comando == "carica":
            caricato, esito, dettaglio = carica_archivio(percorso_archivio)
            if esito != "":
                print(f"Caricamento non riuscito ({esito}): {dettaglio}")
                continue
            registro = caricato
            modifiche_pendenti = False
            print(f"Archivio caricato: {len(registro)} record.")
        elif comando == "elenco":
            print(comanda_elenco(registro))
        elif comando == "cerca":
            codice = leggi_riga("codice: ")
            if codice is None:
                print("Input terminato: le modifiche non salvate restano solo in memoria.")
                return
            print(comanda_cerca(registro, codice))
        elif comando == "inserisci":
            dati, esito = leggi_dati()
            if esito == "eof":
                print("Input terminato: le modifiche non salvate restano solo in memoria.")
                return
            if esito == "importo":
                continue
            codice, destinazione, totale_cent = dati
            messaggio, avvenuta = comanda_inserisci(
                registro, codice, destinazione, totale_cent
            )
            print(messaggio)
            modifiche_pendenti = modifiche_pendenti or avvenuta
        elif comando == "aggiorna":
            dati, esito = leggi_dati()
            if esito == "eof":
                print("Input terminato: le modifiche non salvate restano solo in memoria.")
                return
            if esito == "importo":
                continue
            codice, destinazione, totale_cent = dati
            messaggio, avvenuta = comanda_aggiorna(
                registro, codice, destinazione, totale_cent
            )
            print(messaggio)
            modifiche_pendenti = modifiche_pendenti or avvenuta
        elif comando == "elimina":
            codice = leggi_riga("codice: ")
            if codice is None:
                print("Input terminato: le modifiche non salvate restano solo in memoria.")
                return
            messaggio, avvenuta = comanda_elimina(registro, codice)
            print(messaggio)
            modifiche_pendenti = modifiche_pendenti or avvenuta
        elif comando == "salva":
            if salva_archivio(percorso_archivio, registro):
                modifiche_pendenti = False
                print("Archivio salvato.")
            else:
                print("Salvataggio non riuscito: il file precedente è invariato.")
        elif comando == "esporta":
            if esporta_csv(PERCORSO_CSV, registro):
                print(f"Esportazione CSV scritta in {PERCORSO_CSV}.")
            else:
                print("Esportazione non riuscita.")
        elif comando == "esci":
            if modifiche_pendenti:
                conferma = leggi_riga("Ci sono modifiche non salvate. Uscire comunque? (s/n): ")
                if conferma is None:
                    print("Input terminato: le modifiche non salvate restano solo in memoria.")
                    return
                if conferma.strip() != "s":
                    print("Uscita annullata.")
                    continue
            print("Sessione terminata.")
            return
        elif comando == "":
            continue
        else:
            print("Comando non riconosciuto.")


def leggi_dati():
    """Legge codice, destinazione e totale per un record.

    Restituisce `(dati, esito)` con esito `"ok"` e dati
    `(codice, destinazione, totale_cent)`, oppure esito `"eof"` se l'input
    termina, oppure esito `"importo"` se il totale non è convertibile: in
    quest'ultimo caso nessun dato viene usato e la modifica non parte.
    """
    codice = leggi_riga("codice: ")
    if codice is None:
        return None, "eof"
    destinazione = leggi_riga("destinazione: ")
    if destinazione is None:
        return None, "eof"
    testo_totale = leggi_riga("totale in centesimi: ")
    if testo_totale is None:
        return None, "eof"
    try:
        totale_cent = int(testo_totale)
    except ValueError:
        print("Importo non valido: serve un intero in centesimi.")
        return None, "importo"
    return (codice, destinazione, totale_cent), "ok"


if __name__ == "__main__":
    main()
