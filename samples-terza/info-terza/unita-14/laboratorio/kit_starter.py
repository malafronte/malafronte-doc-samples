"""Starter del LAB-PY-U14 — Prestiti e disponibilità di kit (da completare).

Questo starter **non è un programma completo**: dichiara i contratti pubblici
del laboratorio e lascia alle fasi L02-L07 le parti significative. Le firme
e i docstring sono leggibili così come sono; i punti da realizzare sono
marcati con `TODO` e `NotImplementedError`.

Contratto pubblico (dichiarato, non da scoprire tramite i test):

- `Kit` — `codice` testo non vuoto senza spazi agli estremi, `descrizione`
  con almeno un carattere non bianco, `dotazione` intera non booleana non
  negativa. Valore senza modifiche arbitrarie.
- `Prestito` — `identificatore` univoco, `codice_kit` di un kit del
  catalogo, `gruppo` testo non vuoto, `unita` intere non booleane positive.
- `GestorePrestiti` — catalogo di kit validi con codici univoci e raccolta
  propria dei prestiti attivi. Due gestori non condividono il contenitore
  dei prestiti.
- `disponibile(codice_kit)` — dotazione meno la somma delle unità dei
  prestiti attivi per quel kit; mai negativa.
- `presta(identificatore, codice_kit, gruppo, unita)` — `None` sul
  successo; `ValueError` per argomenti fuori dominio; `ErrorePrestito` per
  kit assente, identificatore duplicato o indisponibilità; nessuna
  modifica in caso di errore o rifiuto.
- `restituisci(identificatore)` — `True` se chiuso, `False` se assente.
- `riepilogo()` — snapshot con politica di copia dichiarata.

Ambiente: CPython sul computer. Le istruzioni operative complete sono
nella scheda del laboratorio, sul sito del corso.
"""


class ErrorePrestito(Exception):
    """Richiesta valida ma non accettabile: kit assente, duplicato o indisponibile."""


def _valida_testo_non_vuoto(valore, nome):
    """Controlla un campo testuale. Già completa: si può riusare."""
    if not isinstance(valore, str):
        raise ValueError(f"campo '{nome}': atteso testo, ricevuto {type(valore).__name__}")
    if valore == "":
        raise ValueError(f"campo '{nome}': non può essere vuoto")
    if valore != valore.strip():
        raise ValueError(
            f"campo '{nome}': spazi iniziali o finali non ammessi, ricevuto {valore!r}"
        )
    return None


def _valida_intero(valore, nome, minimo):
    """Controlla un intero non booleano con il minimo dichiarato.

    TODO (fase L02): da completare, sul modello dei validatori del corso.
    """
    raise NotImplementedError("validatore dell'intero da completare")


def crea_kit(codice, descrizione, dotazione):
    """Costruisce il valore `Kit` dopo i controlli. TODO (fase L02)."""
    raise NotImplementedError("costruzione del kit da completare")


def crea_prestito(identificatore, codice_kit, gruppo, unita):
    """Costruisce il valore `Prestito` dopo i controlli. TODO (fase L02)."""
    raise NotImplementedError("costruzione del prestito da completare")


class GestorePrestiti:
    """Catalogo dei kit e raccolta dei prestiti attivi.

    TODO (fase L03): scegliere la rappresentazione interna di catalogo e
    prestiti, senza contenitori sulla classe. TODO (fase L04-L05):
    realizzare le operazioni dichiarate nei docstring.
    """

    def __init__(self, kit=None):
        """Crea il gestore con il catalogo ricevuto (lista di `Kit`).

        Il catalogo è una copia difensiva: nessun alias esterno di un kit
        può mutare lo stato interno. TODO (fase L03).
        """
        raise NotImplementedError("costruzione del gestore da completare")

    def disponibile(self, codice_kit):
        """Unità disponibili del kit. Mai negativa.

        TODO (fase L04): calcolo esplicito a ogni chiamata, senza duplicare
        il dato né mantenerlo coerente a mano.
        """
        raise NotImplementedError("disponibile da completare")

    def presta(self, identificatore, codice_kit, gruppo, unita):
        """Registra un prestito. `None` sul successo.

        Rifiuti: `ValueError` per argomenti fuori dominio; `ErrorePrestito`
        per kit assente, identificatore già attivo o unità non disponibili.
        Ogni rifiuto lascia lo stato invariato. TODO (fase L04).
        """
        raise NotImplementedError("presta da completare")

    def restituisci(self, identificatore):
        """Chiude il prestito. `True` se chiuso, `False` se assente.

        TODO (fase L05): la restituzione parziale è un'estensione separata,
        non richiesta qui.
        """
        raise NotImplementedError("restituisci da completare")

    def riepilogo(self):
        """Snapshot con politica di copia dichiarata. TODO (fase L05).

        Requisito: modificare il risultato non modifica il gestore; la
        politica di copia va dichiarata e poi verificata con un test.
        """
        raise NotImplementedError("riepilogo da completare")


def catalogo_pubblico():
    """Il dataset sintetico del laboratorio: tre kit, nessun nome personale."""
    return [
        crea_kit("K01", "Kit misure", 3),
        crea_kit("K02", "Kit logica", 2),
        crea_kit("K03", "Kit riserva", 0),
    ]


def dimostrazione():
    """Dimostrazione non risolutiva: mostra il contratto, non la soluzione.

    Si limita a costruire due gestori e a stampare i riepiloghi **vuoti**:
    tutto il resto è lavoro delle fasi. Eseguirla richiede che le fasi L02
    e L03 siano state completate.
    """
    primo = GestorePrestiti(catalogo_pubblico())
    secondo = GestorePrestiti(catalogo_pubblico())
    print("primo:", primo.riepilogo())
    print("secondo:", secondo.riepilogo())


if __name__ == "__main__":
    dimostrazione()
