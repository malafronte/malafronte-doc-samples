"""Interazione a riga di comando del modello robusto del registro (U14).

Responsabilità del modulo: leggere i comandi, presentare gli esiti e le
diagnosi di dominio, tenere il conto delle modifiche pendenti. Il modello è
`registro_modello_u14.py`, la persistenza resta `registro_persistenza.py`:
la CLI è il confine che traduce le eccezioni di dominio in messaggi per chi
usa il programma — nessun `except` indiscriminato, ciascuna eccezione ha la
propria diagnosi.

Comandi e comportamenti di sessione sono quelli già verificati —
inizializzazione con `carica`, modifiche pendenti, salvataggio esplicito,
EOF gestito — per rendere confrontabili le tre CLI della raccolta.

Esecuzione, dalla root del progetto:

    uv run python programmi/registro_cli_u14.py
"""
from pathlib import Path

from registro_dominio import formatta_euro
from registro_modello_u14 import (
    CodiceAssente,
    CodiceDuplicato,
    DatoNonAmmesso,
    RegistroPreventivi,
    record_da_preventivo,
)
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
        f"{formatta_euro(sessione.totale_complessivo_cent)} euro"
    )
    return "\n".join(righe)


def comanda_cerca(sessione: RegistroPreventivi, codice: str) -> str:
    """Restituisce il testo della consultazione per codice."""
    preventivo = sessione.per_codice(codice)
    if preventivo is None:
        return f"Nessun record con codice {codice!r}."
    return riga_record(record_da_preventivo(preventivo))


def comanda_inserisci(
    sessione: RegistroPreventivi, codice: str, destinazione: str, totale_cent: int
):
    """Tenta l'inserimento; restituisce (messaggio, modifica_avvenuta)."""
    try:
        sessione.inserisci(codice, destinazione, totale_cent)
    except (DatoNonAmmesso, CodiceDuplicato) as problema:
        return f"Inserimento rifiutato: {problema}", False
    return "Record inserito.", True


def comanda_aggiorna(
    sessione: RegistroPreventivi, codice: str, destinazione: str, totale_cent: int
):
    """Tenta l'aggiornamento; restituisce (messaggio, modifica_avvenuta)."""
    try:
        sessione.aggiorna(codice, destinazione, totale_cent)
    except (DatoNonAmmesso, CodiceAssente) as problema:
        return f"Aggiornamento rifiutato: {problema}", False
    return "Record aggiornato.", True


def comanda_elimina(sessione: RegistroPreventivi, codice: str):
    """Tenta l'eliminazione; restituisce (messaggio, modifica_avvenuta)."""
    try:
        sessione.elimina(codice)
    except CodiceAssente as problema:
        return f"Eliminazione rifiutata: {problema}", False
    return "Record eliminato.", True


def leggi_riga(prompt: str):
    """Legge una riga dall'input; restituisce None se l'input termina (EOF)."""
    try:
        return input(prompt)
    except EOFError:
        return None


def leggi_dati():
    """Legge codice, destinazione e totale per un record.

    Restituisce `(dati, esito)` con esito `"ok"` oppure `"eof"` se l'input
    termina, oppure `"importo"` se il totale non è convertibile: in
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
    """Sessione di interazione sul modello robusto, salvataggio esplicito."""
    # La sessione None distingue una CLI non inizializzata da una raccolta
    # vuota valida: prima di ogni comando occorre eseguire `carica`.
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
            print(f"Archivio caricato: {sessione.numero} record.")
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
