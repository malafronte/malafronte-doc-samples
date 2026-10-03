"""Supporto fornito per provare turtle senza aprire una finestra.

`crea_penna_di_prova()` restituisce un oggetto già pronto con i cinque metodi
richiesti dalle funzioni di disegno e una lista `azioni`. Ogni chiamata
aggiunge una tupla alla lista; nessun metodo disegna o apre una finestra.
Il supporto si usa così com'è: non richiede di definire classi proprie.
"""

from types import SimpleNamespace


def crea_penna_di_prova():
    """Restituisce una penna nuova e il suo registro inizialmente vuoto."""
    azioni = []

    def forward(distanza):
        azioni.append(("forward", distanza))

    def left(angolo):
        azioni.append(("left", angolo))

    def penup():
        azioni.append(("penup",))

    def pendown():
        azioni.append(("pendown",))

    def color(colore):
        azioni.append(("color", colore))

    return SimpleNamespace(
        azioni=azioni, forward=forward, left=left,
        penup=penup, pendown=pendown, color=color,
    )
