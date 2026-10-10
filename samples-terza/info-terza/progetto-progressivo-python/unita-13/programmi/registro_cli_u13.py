"""Interazione a riga di comando della variante a oggetti del registro (U13).

Responsabilità del modulo: leggere i comandi, mostrare gli esiti e tenere il
conto delle modifiche pendenti. Lo stato della sessione vive nell'istanza di
`RegistroPreventivi`, la persistenza resta in `registro_persistenza.py`: la
CLI è il raccordo fra le due, mediante le conversioni esplicite `per_lista()`
e `sostituisci_da_lista()`. Le dipendenze vanno in una sola direzione,
dall'interazione verso il modello e la persistenza.

Comandi e comportamenti sono quelli già verificati della CLI U12 —
inizializzazione con `carica`, modifiche pendenti, salvataggio esplicito,
EOF gestito — per rendere confrontabile la sessione prima e dopo la
rifattorizzazione. L'unica differenza di interazione è la presentazione del
totale complessivo, aggiunto dalla modifica breve della tappa.

Esecuzione, dalla root del progetto:

    uv run python programmi/registro_cli_u13.py
"""
from pathlib import Path

from registro_dominio import formatta_euro
from registro_oggetti_u13 import RegistroPreventivi
from registro_persistenza import carica_archivio, esporta_csv, salva_archivio

PERCORSO_PREDEFINITO = Path("dati") / "unita-12" / "archivio.json"
PERCORSO_CSV = Path("dati") / "unita-12" / "esportazione.csv"
INTESTAZIONE = (
    "Comandi: carica, elenco, cerca, inserisci, aggiorna, elimina, salva, "
    "esporta, esci"
)
FINE_INPUT = "Input terminato: le modifiche non salvate restano solo in memoria."


def riga_record(record: dict) -> str:
    """Restituisce la riga di presentazione di un record, importo in euro."""
    return (
        f"{record['codice']} | {record['destinazione']} | "
        f"{formatta_euro(record['totale_cent'])} euro "
        f"({record['totale_cent']} centesimi)"
    )


def comanda_elenco(sessione: RegistroPreventivi) -> str:
    """Restituisce il testo dell'elenco dei record, con il riepilogo."""
    righe = []
    for record in sessione.per_lista():
        righe.append(riga_record(record))
    riepilogo = sessione.riepilogo_per_destinazione()
    righe.append(
        f"locale: {riepilogo['locale']['conteggio']} preventivi, "
        f"{formatta_euro(riepilogo['locale']['totale_cent'])} euro"
    )
    righe.append(
        f"nazionale: {riepilogo['nazionale']['conteggio']} preventivi, "
        f"{formatta_euro(riepilogo['nazionale']['totale_cent'])} euro"
    )
    righe.append(
        f"totale complessivo: "
        f"{formatta_euro(sessione.totale_complessivo_cent())} euro"
    )
    return "\n".join(righe)


def comanda_cerca(sessione: RegistroPreventivi, codice: str) -> str:
    """Restituisce il testo della consultazione per codice."""
    record = sessione.cerca(codice)
    if record is None:
        return f"Nessun record con codice {codice!r}."
    return riga_record(record)


def comanda_inserisci(
    sessione: RegistroPreventivi, codice: str, destinazione: str, totale_cent: int
):
    """Tenta l'inserimento; restituisce (messaggio, modifica_avvenuta)."""
    if sessione.inserisci(codice, destinazione, totale_cent):
        return "Record inserito.", True
    return "Inserimento rifiutato: codice già presente oppure dati non ammessi.", False


def comanda_aggiorna(
    sessione: RegistroPreventivi, codice: str, destinazione: str, totale_cent: int
):
    """Tenta l'aggiornamento; restituisce (messaggio, modifica_avvenuta)."""
    if sessione.aggiorna(codice, destinazione, totale_cent):
        return "Record aggiornato.", True
    return "Aggiornamento rifiutato: codice assente oppure dati non ammessi.", False


def comanda_elimina(sessione: RegistroPreventivi, codice: str):
    """Tenta l'eliminazione; restituisce (messaggio, modifica_avvenuta)."""
    if sessione.elimina(codice):
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


def main() -> None:
    """Sessione di interazione sul registro a oggetti, salvataggio esplicito."""
    # La sessione None distingue una CLI non inizializzata da un registro
    # vuoto valido: prima di ogni comando occorre eseguire `carica`.
    sessione = None
    percorso_archivio = PERCORSO_PREDEFINITO
    modifiche_pendenti = False

    print(INTESTAZIONE)
    while True:
        comando = leggi_riga("registro> ")
        if comando is None:
            print(FINE_INPUT)
            return
        comando = comando.strip()

        if sessione is None and comando in (
            "elenco", "cerca", "inserisci", "aggiorna", "elimina", "salva", "esporta"
        ):
            print("Registro non inizializzato: eseguire carica prima di usare il registro.")
            continue

        if comando == "carica":
            if modifiche_pendenti:
                print("Caricamento rifiutato: ci sono modifiche non salvate.")
                print("Salvare le modifiche oppure uscire confermandone la perdita.")
                continue
            caricato, esito, dettaglio = carica_archivio(percorso_archivio)
            if esito == "assente":
                sessione = RegistroPreventivi()
                print("Archivio assente: nuovo registro vuoto.")
                continue
            if esito != "":
                print(f"Caricamento non riuscito ({esito}): {dettaglio}")
                continue
            sessione = RegistroPreventivi()
            sessione.sostituisci_da_lista(caricato)
            modifiche_pendenti = False
            print(f"Archivio caricato: {sessione.numero()} record.")
        elif comando == "elenco":
            print(comanda_elenco(sessione))
        elif comando == "cerca":
            codice = leggi_riga("codice: ")
            if codice is None:
                print(FINE_INPUT)
                return
            print(comanda_cerca(sessione, codice))
        elif comando == "inserisci":
            dati, esito = leggi_dati()
            if esito == "eof":
                print(FINE_INPUT)
                return
            if esito == "importo":
                continue
            codice, destinazione, totale_cent = dati
            messaggio, avvenuta = comanda_inserisci(
                sessione, codice, destinazione, totale_cent
            )
            print(messaggio)
            modifiche_pendenti = modifiche_pendenti or avvenuta
        elif comando == "aggiorna":
            dati, esito = leggi_dati()
            if esito == "eof":
                print(FINE_INPUT)
                return
            if esito == "importo":
                continue
            codice, destinazione, totale_cent = dati
            messaggio, avvenuta = comanda_aggiorna(
                sessione, codice, destinazione, totale_cent
            )
            print(messaggio)
            modifiche_pendenti = modifiche_pendenti or avvenuta
        elif comando == "elimina":
            codice = leggi_riga("codice: ")
            if codice is None:
                print(FINE_INPUT)
                return
            messaggio, avvenuta = comanda_elimina(sessione, codice)
            print(messaggio)
            modifiche_pendenti = modifiche_pendenti or avvenuta
        elif comando == "salva":
            if salva_archivio(percorso_archivio, sessione.per_lista()):
                modifiche_pendenti = False
                print("Archivio salvato.")
            else:
                print("Salvataggio non riuscito: il file precedente è invariato.")
        elif comando == "esporta":
            if esporta_csv(PERCORSO_CSV, sessione.per_lista()):
                print(f"Esportazione CSV scritta in {PERCORSO_CSV}.")
            else:
                print("Esportazione non riuscita.")
        elif comando == "esci":
            if modifiche_pendenti:
                conferma = leggi_riga(
                    "Ci sono modifiche non salvate. Uscire comunque? (s/n): "
                )
                if conferma is None:
                    print(FINE_INPUT)
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


if __name__ == "__main__":
    main()
