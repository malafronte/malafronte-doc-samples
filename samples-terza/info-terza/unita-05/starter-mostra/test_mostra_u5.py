"""Starter del file di test della mostra (LAB-PY-U5).

Questo file diventa eseguibile SOLO dopo che lo studente ha creato
programmi/mostra_u5.py con le funzioni errore_dati_mostra, categoria_mostra e
costo_mostra. Prima di allora l'import fallisce: è normale e non è un difetto
del programma della mostra.

Contiene UN solo caso completo, come modello della forma (preparazione, azione,
verifica). Gli altri casi vanno scritti dallo studente a partire dalla matrice
L01-L19, una funzione di test per caso. I casi mancanti NON sono presenti come
funzioni vuote: non si usano pass o puntini di sospensione, così il conteggio
della discovery riflette i test realmente scritti.

Comando dalla root della raccolta:
    uv run pytest -q programmi/test_mostra_u5.py
"""

from mostra_u5 import categoria_mostra, costo_mostra, errore_dati_mostra


def test_diciotto_anni_senza_tessera_ordinario() -> None:
    # L05: tre asserzioni coerenti sullo stesso scenario.
    assert errore_dati_mostra(18, "n") == ""
    assert categoria_mostra(18) == "Ordinario"
    assert costo_mostra(18, "n") == 7


# Da completare (una funzione di test per caso, con nome descrittivo):
#   L01: 0 / "n"   -> "", Gratuito, 0
#   L02: 5 / "s"   -> "", Gratuito, 0
#   L03: 6 / "n"   -> "", Ridotto, 4
#   L04: 17 / "s"  -> "", Ridotto, 4
#   L06: 18 / "s"  -> "", Ordinario, 5
#   L07: 64 / "n"  -> "", Ordinario, 7
#   L08: 64 / "s"  -> "", Ordinario, 5
#   L09: 65 / "n"  -> "", Senior, 5
#   L10: 65 / "s"  -> "", Senior, 5
#   L11: 120 / "n" -> "", Senior, 5
#   L12: 30 / "n"  -> "", Ordinario, 7
#   L13: 30 / "s"  -> "", Ordinario, 5
#   L14: -1 / "n"  -> "Età non ammessa" (solo validatore)
#   L15: 121 / "s" -> "Età non ammessa" (solo validatore)
#   L16: 30 / "S"  -> "Risposta tessera non ammessa" (solo validatore)
#   L17: 30 / ""   -> "Risposta tessera non ammessa" (solo validatore)
#   L18: -1 / "forse" -> "Età non ammessa" (solo validatore)
#   L19: 30 / " "  -> "Risposta tessera non ammessa" (solo validatore)
