"""Dimostrazione canonica delle tracce del capitolo — Unità 18.

Il programma riproduce con i moduli degli esempi le tracce dei dati canonici:
sequenza base del concatenamento, ricerche con conteggi, crescita da cinque a
dieci bucket, hash dei codici testuali e sondaggio con marcatore. L'output è
il riferimento verificato delle tabelle e delle figure del capitolo.

Esecuzione dalla cartella `unita-18`:

```powershell
uv run python esempi/dimostrazione_hash_u18.py
```
"""

from __future__ import annotations

from confronto_indici_u18 import confronta_strategie
from hash_chiavi_u18 import indice_per, traccia_accumulatore
from tabella_hash_u18 import TabellaHashConcatenata, hash_didattico
from tracce_sondaggio_u18 import traccia_canonica


def stato_base():
    """Costruisce la tabella con le quattro associazioni canoniche."""
    tabella = TabellaHashConcatenata(5)
    tabella.assegna(12, "A")
    tabella.assegna(7, "B")
    tabella.assegna(22, "C")
    tabella.assegna(17, "D")
    return tabella


def main():
    """Stampa le tracce canoniche del capitolo."""
    print("== sequenza base del concatenamento (m = 5) ==")
    tabella = TabellaHashConcatenata(5)
    for chiave, valore in [(12, "A"), (7, "B"), (22, "C"), (17, "D")]:
        tabella.assegna(chiave, valore)
        print(f"assegna({chiave}, {valore!r}): indice {indice_per(chiave, 5)}, n = {len(tabella)}")
    tabella.assegna(7, "B2")
    print(f"assegna(7, 'B2'): aggiornamento, n = {len(tabella)}, carico = {tabella.fattore_carico}")
    print(f"catena del bucket 2: {[(n.chiave, n.valore) for n in _catena(tabella, 2)]}")

    print("== ricerche con conteggi ==")
    for query in (17, 7, 12, 27, 4):
        try:
            esito = tabella.cerca(query)
        except KeyError:
            esito = "KeyError"
        print(f"cerca({query}): {esito}, confronti = {tabella.confronti_per(query)}")

    print("== crescita da cinque a dieci bucket ==")
    crescita = TabellaHashConcatenata(5)
    for chiave in (12, 7, 22, 17, 3, 8):
        crescita.assegna(chiave, f"V{chiave}")
        print(f"chiave {chiave}: n = {len(crescita)}, m = {crescita.capacita}")
    print(f"carico finale: {crescita.fattore_carico}")
    print(f"lunghezze dei bucket: {crescita.lunghezze_bucket()}")

    print("== codici testuali ==")
    for codice in ("007", "012", "003", "017", "7", ""):
        indice = indice_per(codice, 5)
        print(f"{codice!r}: hash = {hash_didattico(codice)}, indice (m = 5) = {indice}")
    print("traccia dell'accumulatore per '007':")
    for carattere, codice_punto, accumulatore in traccia_accumulatore("007"):
        print(f"  {carattere!r} ord = {codice_punto}: h = {accumulatore}")

    print("== sondaggio lineare con marcatore (m = 7) ==")
    traccia = traccia_canonica()
    print(f"posizioni dopo 5, 12, 19: {traccia['dopo_inserimenti']}")
    print(f"sonde per 19: {traccia['sonde_19']}")
    print(f"posizioni dopo la rimozione di 12: {traccia['dopo_cancellazione']}")
    print(f"cerca(19) oltre il marcatore: {traccia['valore_19_oltre_marcatore']!r}")

    print("== confronto delle strategie ==")
    coppie = [(12, "A"), (7, "B"), (22, "C"), (17, "D")]
    for riga in confronta_strategie(coppie, [7, 27], 5):
        print(
            f"{riga['strategia']}: query {riga['query']!r}, trovato = {riga['trovato']}, "
            f"confronti = {riga['confronti']}"
        )


def _catena(tabella, posizione):
    """Restituisce i nodi della catena di `posizione` dalla testa."""
    nodi = []
    corrente = tabella._bucket[posizione]
    while corrente is not None:
        nodi.append(corrente)
        corrente = corrente.successivo
    return nodi


if __name__ == "__main__":
    main()
