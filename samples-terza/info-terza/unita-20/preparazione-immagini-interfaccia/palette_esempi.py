"""Palette deterministiche per gli esiti del kernel di fuga — Unità 20 (L5).

Il modulo implementa gli esempi preparatori del nucleo C del capitolo PY-40
(*Immagini dei frattali: pixel, coordinate e colori*):

- il contratto `colora_esito(indice_fuga, limite_iterazioni, nome_palette)`,
  che traduce un esito matematico in una tripla RGB con componenti intere in
  `0..255`;
- le tre strategie canoniche `"binaria"`, `"bande"` e `"gradiente"`, con le
  tabelle cromatiche condivise dal contratto L1 (`contratti_raster_json.py`);
- la distinzione obbligatoria fra esito `None` (fuga non rilevata entro il
  limite, colore interno dedicato) e indice `0` (fuga immediata, primo colore
  valido di fuga), controllata sempre con `is None`;
- la legenda testuale di una palette, che dichiara il significato dei colori
  senza affidarlo alla sola percezione visiva.

La colorazione non ricalcola le orbite: riceve la matrice degli esiti già
calcolata dal kernel. Una variazione di palette modifica l'immagine ma
conserva gli esiti matematici quando i parametri restano gli stessi.

Ambiente: CPython 3.14 sul computer. Il modulo non esegue operazioni di I/O
né apre finestre grafiche all'importazione.
"""

from contratti_raster_json import (
    COLORE_ESTERNO_BINARIA,
    COLORE_GRADIENTE_FINE,
    COLORE_GRADIENTE_INIZIO,
    COLORE_INTERNO_BANDE,
    COLORE_INTERNO_BINARIA,
    COLORE_INTERNO_GRADIENTE,
    PALETTE_AMMESSE,
    TABELLA_BANDE_FUGA,
)

type ColoreRGB = tuple[int, int, int]


def valida_limite_iterazioni(valore: object) -> int:
    """Verifica che `valore` sia un intero non booleano maggiore o uguale a 1."""
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise TypeError("Il parametro 'limite_iterazioni' richiede un intero non booleano.")
    if valore < 1:
        raise ValueError("Il parametro 'limite_iterazioni' richiede un valore >= 1.")
    return valore


def valida_colore_rgb(valore: object, nome_parametro: str) -> ColoreRGB:
    """Verifica che `valore` sia una tripla RGB con canali interi in `0..255`."""
    if not isinstance(valore, (tuple, list)) or len(valore) != 3:
        raise TypeError(f"Il parametro '{nome_parametro}' richiede una tripla (r, g, b).")
    canali: list[int] = []
    for i, canale in enumerate(valore):
        if isinstance(canale, bool) or not isinstance(canale, int):
            raise TypeError(f"Il canale '{nome_parametro}[{i}]' richiede un intero non booleano.")
        if not (0 <= canale <= 255):
            raise ValueError(f"Il canale '{nome_parametro}[{i}]' richiede un valore in 0..255.")
        canali.append(canale)
    return (canali[0], canali[1], canali[2])


def colora_esito(
    indice_fuga: int | None,
    limite_iterazioni: object,
    nome_palette: object = "bande",
) -> ColoreRGB:
    """Restituisce la tripla RGB deterministica associata a un esito del kernel.

    La regola del contratto distingue prima l'esito `None` con il controllo
    `is None` (mai con la sola falsità, perché l'indice `0` è falsificabile ma
    valido): `None` riceve il colore interno dedicato alla fuga non rilevata,
    ogni indice `0 <= n <= N` riceve un colore di fuga. La palette `"binaria"`
    usa un solo colore per tutti gli indici; `"bande"` sceglie nella tabella
    con `n % 8`; `"gradiente"` interpola linearmente fra il colore iniziale
    (per `n = 0`) e quello finale (per `n = N`).
    """
    n_max = valida_limite_iterazioni(limite_iterazioni)
    if not isinstance(nome_palette, str) or nome_palette not in PALETTE_AMMESSE:
        raise ValueError(f"Palette '{nome_palette}' non riconosciuta; ammesse: {PALETTE_AMMESSE}.")

    if indice_fuga is None:
        if nome_palette == "binaria":
            return COLORE_INTERNO_BINARIA
        if nome_palette == "bande":
            return COLORE_INTERNO_BANDE
        return COLORE_INTERNO_GRADIENTE

    if isinstance(indice_fuga, bool) or not isinstance(indice_fuga, int):
        raise TypeError("Il parametro 'indice_fuga' richiede un intero non booleano o None.")
    if not (0 <= indice_fuga <= n_max):
        raise ValueError(f"L'indice di fuga ({indice_fuga}) richiede un valore in 0..{n_max}.")

    if nome_palette == "binaria":
        return COLORE_ESTERNO_BINARIA
    if nome_palette == "bande":
        return TABELLA_BANDE_FUGA[indice_fuga % len(TABELLA_BANDE_FUGA)]

    frazione = indice_fuga / n_max
    r = round(
        COLORE_GRADIENTE_INIZIO[0]
        + frazione * (COLORE_GRADIENTE_FINE[0] - COLORE_GRADIENTE_INIZIO[0])
    )
    g = round(
        COLORE_GRADIENTE_INIZIO[1]
        + frazione * (COLORE_GRADIENTE_FINE[1] - COLORE_GRADIENTE_INIZIO[1])
    )
    b = round(
        COLORE_GRADIENTE_INIZIO[2]
        + frazione * (COLORE_GRADIENTE_FINE[2] - COLORE_GRADIENTE_INIZIO[2])
    )
    return (r, g, b)


def legenda_palette(nome_palette: object, limite_iterazioni: object) -> str:
    """Restituisce la legenda testuale di una palette per un limite `N` dichiarato.

    La legenda dichiara il colore degli esiti `None` (fuga non rilevata entro
    `N` iterazioni, senza affermare l'appartenenza a un insieme), il colore
    della fuga immediata all'indice `0` e quello della fuga all'ultimo passo
    `N`. Il numero di iterazioni si legge nei dati, così il colore accompagna
    una spiegazione esplicita.
    """
    n_max = valida_limite_iterazioni(limite_iterazioni)
    if not isinstance(nome_palette, str) or nome_palette not in PALETTE_AMMESSE:
        raise ValueError(f"Palette '{nome_palette}' non riconosciuta; ammesse: {PALETTE_AMMESSE}.")
    interno = colora_esito(None, n_max, nome_palette)
    primo = colora_esito(0, n_max, nome_palette)
    ultimo = colora_esito(n_max, n_max, nome_palette)
    return (
        f"Palette '{nome_palette}' con limite N = {n_max}:\n"
        f"- fuga non rilevata entro {n_max} iterazioni (None): RGB{interno};\n"
        f"- fuga immediata all'indice 0: RGB{primo};\n"
        f"- fuga all'ultimo passo N = {n_max}: RGB{ultimo}."
    )


if __name__ == "__main__":
    for nome in PALETTE_AMMESSE:
        print(legenda_palette(nome, 100))
