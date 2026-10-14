"""Produttori di Koch e Sierpiński (da completare, tappa FR-M2).

Contratto: ogni funzione restituisce gli elementi finiti della costruzione
al livello richiesto con conteggio esatto (`4^d` per la curva di Koch,
`3 * 4^d` per il fiocco, `3^d` per Sierpiński) e vertici verificati sui
casi canonici (requisito FR-01).
"""


def produci_koch(livello: object, variante: object, lato_iniziale: object):
    """Restituisce i segmenti di Koch al livello (da completare, FR-M2)."""
    raise NotImplementedError("FR-M2: curva o fiocco orario con punte esterne.")


def produci_sierpinski(livello: object, stile: object, lato_iniziale: object):
    """Restituisce i triangoli di Sierpiński al livello (da completare, FR-M2)."""
    raise NotImplementedError("FR-M2: tre triangoli d'angolo, centrale escluso.")
