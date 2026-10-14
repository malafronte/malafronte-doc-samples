"""Palette deterministiche e legenda (da completare, tappa FR-M5).

Contratto: `colora_esito` traduce un esito in tripla RGB con componenti in
`0..255`, distinguendo `None` (fuga non rilevata, colore interno dedicato)
dall'indice `0` (primo colore di fuga) con il controllo `is None`;
`legenda_palette` dichiara il significato dei colori (requisito FR-06).
"""

PALETTE_AMMESSE = ("binaria", "bande", "gradiente")


def colora_esito(indice_fuga: object, limite_iterazioni: object, nome_palette: object):
    """Restituisce la tripla RGB dell'esito (da completare, FR-M5)."""
    raise NotImplementedError("FR-M5: is None per l'interno, tabella o gradiente per fuga.")


def legenda_palette(nome_palette: object, limite_iterazioni: object):
    """Restituisce la legenda testuale della palette (da completare, FR-M5)."""
    raise NotImplementedError("FR-M5: significato di interno, bande e indice massimo.")
