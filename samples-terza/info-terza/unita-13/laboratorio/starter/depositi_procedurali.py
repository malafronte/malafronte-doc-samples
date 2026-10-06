"""Depositi di kit didattici in forma procedurale: record e funzioni.

Questo modulo è la **versione procedurale di partenza** del laboratorio
LAB-PY-U13. Funziona ed è completa: va eseguita, letta e capita prima di
scrivere qualunque classe.

Dominio: un deposito contiene **kit didattici**. Ogni deposito ha
un'`etichetta` che lo identifica nella sessione, una `capacita` che indica il
numero massimo di kit che può contenere e una `quantita` che conta i kit
**contenuti** — non i posti liberi.

| Campo | Tipo | Regola |
|---|---|---|
| `etichetta` | `str` | non vuota, senza spazi agli estremi |
| `capacita` | `int` | intero non booleano >= 0 |
| `quantita` | `int` | intero non booleano, da 0 a `capacita` |

Invariante del deposito: `0 <= quantita <= capacita` per ogni stato
osservabile.

Contratto delle operazioni:

| Operazione | Contratto |
|---|---|
| `nuovo_deposito(...)` | record nuovo; fuori contratto: `ValueError` |
| `carica(deposito, unita)` | `True` se entrano, `False` se superano la capacità |
| `preleva(deposito, unita)` | `True` se bastano, `False` se non bastano |
| `spazio_libero(deposito)` | posti liberi; nessuna modifica |
| `situazione(deposito)` | nuovo dizionario con i tre campi |

Sul rifiuto lo stato resta invariato. La quantità zero è un'operazione valida
e restituisce `True`. Un valore di carico o prelievo negativo, non intero o
booleano è un **errore di input** e solleva `ValueError`: non viene tradotto
in un rifiuto.

Ambiente: CPython sul computer. Dipende soltanto dal linguaggio.
"""


def _valida_unita(unita):
    """Controlla che `unita` sia un intero non booleano non negativo."""
    if isinstance(unita, bool) or not isinstance(unita, int):
        raise ValueError(f"unita: atteso un intero, ricevuto {type(unita).__name__}")
    if unita < 0:
        raise ValueError(
            f"unita: atteso un valore maggiore o uguale a zero, ricevuto {unita}"
        )
    return None


def _valida_deposito(etichetta, capacita, quantita):
    """Controlla etichetta, capacità e quantità secondo lo schema."""
    if not isinstance(etichetta, str):
        raise ValueError(
            f"campo 'etichetta': atteso testo, ricevuto {type(etichetta).__name__}"
        )
    if etichetta == "":
        raise ValueError("campo 'etichetta': non può essere vuota")
    if etichetta != etichetta.strip():
        raise ValueError(
            f"campo 'etichetta': spazi iniziali o finali non ammessi, "
            f"ricevuta {etichetta!r}"
        )
    for valore, nome in ((capacita, "capacita"), (quantita, "quantita")):
        if isinstance(valore, bool) or not isinstance(valore, int):
            raise ValueError(
                f"campo '{nome}': atteso un intero, ricevuto {type(valore).__name__}"
            )
        if valore < 0:
            raise ValueError(
                f"campo '{nome}': atteso un valore maggiore o uguale a zero, "
                f"ricevuto {valore}"
            )
    if quantita > capacita:
        raise ValueError(
            f"coppia ({capacita}, {quantita}): la quantita {quantita} "
            f"supera la capacita {capacita}"
        )
    return None


def nuovo_deposito(etichetta, capacita, quantita=0):
    """Restituisce il record del deposito. Fuori contratto: `ValueError`."""
    _valida_deposito(etichetta, capacita, quantita)
    return {"etichetta": etichetta, "capacita": capacita, "quantita": quantita}


def carica(deposito, unita):
    """Aggiunge kit al deposito. `True` se applicato, `False` se non entrano."""
    _valida_unita(unita)
    if deposito["quantita"] + unita > deposito["capacita"]:
        return False
    deposito["quantita"] = deposito["quantita"] + unita
    return True


def preleva(deposito, unita):
    """Preleva kit dal deposito. `True` se applicato, `False` se non bastano."""
    _valida_unita(unita)
    if unita > deposito["quantita"]:
        return False
    deposito["quantita"] = deposito["quantita"] - unita
    return True


def spazio_libero(deposito):
    """Restituisce i posti liberi del deposito. Nessuna modifica."""
    return deposito["capacita"] - deposito["quantita"]


def situazione(deposito):
    """Restituisce un nuovo dizionario con i tre campi del deposito."""
    return {
        "etichetta": deposito["etichetta"],
        "capacita": deposito["capacita"],
        "quantita": deposito["quantita"],
    }


def descrizione(deposito):
    """Restituisce la riga di presentazione del deposito. Non stampa."""
    return (
        f"{deposito['etichetta']}: {deposito['quantita']} kit "
        f"su {deposito['capacita']} posti, liberi {spazio_libero(deposito)}"
    )


def confronta_sessioni(prima, seconda):
    """Restituisce il confronto fra due sessioni di depositi.

    Una **sessione** è una lista di depositi indipendente dalle altre: due
    sessioni non condividono alcun record e le operazioni su una non si vedono
    sull'altra. Il risultato elenca, per ogni deposito di ogni sessione,
    etichetta, quantità e spazio libero.
    """
    return {
        "prima": [situazione(deposito) for deposito in prima],
        "seconda": [situazione(deposito) for deposito in seconda],
    }
