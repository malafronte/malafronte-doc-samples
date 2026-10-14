"""Matrice degli esiti, immagini RGB e file PNG con Pillow — Unità 20 (L5).

Il modulo implementa gli esempi preparatori dei nuclei C e D del capitolo
PY-40 (*Immagini dei frattali: pixel, coordinate e colori*):

- la matrice degli esiti `esiti[q][p]`, costruita con un doppio ciclo esplicito
  su righe e colonne: per ciascun pixel calcola il punto al centro della cella
  e lo classifica con il kernel ricevuto come funzione;
- le statistiche della matrice (punti con fuga rilevata, punti interni, indice
  massimo, aggiornamenti totali effettivi contro il limite superiore `W·H·N`);
- la traduzione della matrice in immagine RGB tramite una palette
  deterministica e il disegno delle figure geometriche con `ImageDraw`;
- il salvataggio in PNG e la riapertura con verifica di dimensioni, modalità
  e pixel scelti (un test sulla sola esistenza del file coprirebbe soltanto
  la creazione del file).

Il kernel di classificazione è un parametro (`classifica_punto`): il modulo
non importa i kernel dei frattali, così la stessa matrice funziona per
Mandelbrot, per Julia e per i classificatori dei test. Questa separazione fra
calcolo iniettato e rendering anticipa i componenti sostituibili di PY-42.

Ambiente: CPython 3.14 sul computer con la dipendenza `pillow` (bloccata nel
file `uv.lock`). Il modulo non apre finestre grafiche all'importazione.
"""

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw

from coordinate_esempi import (
    punto_da_pixel,
    valida_intero_non_booleano,
    valida_reale_finito,
)
from palette_esempi import colora_esito, valida_colore_rgb, valida_limite_iterazioni

type EsitoPixel = int | None
type MatriceEsiti = tuple[tuple[EsitoPixel, ...], ...]
type ClassificaPunto = Callable[[complex], EsitoPixel]


@dataclass(frozen=True)
class StatisticheRaster:
    """Conteggi osservati su una matrice di esiti con limite `N` dichiarato.

    Il campo `aggiornamenti_totali` somma gli aggiornamenti eseguiti sui pixel:
    un indice `n` contribuisce con `n` aggiornamenti, un esito `None` con `N`
    aggiornamenti. Il lavoro effettivo non supera mai il limite superiore
    `larghezza · altezza · N`. Il campo `byte_immagine_rgb` vale `W · H · 3`
    (tre byte per pixel); la matrice conserva inoltre un riferimento per esito.
    """

    larghezza: int
    altezza: int
    limite_iterazioni: int
    punti_totali: int
    punti_fuga: int
    punti_interni: int
    indice_massimo: int | None
    aggiornamenti_totali: int
    limite_superiore: int
    byte_immagine_rgb: int


def valida_matrice_esiti(valore: object) -> MatriceEsiti:
    """Verifica che `valore` sia una matrice rettangolare non vuota di esiti."""
    if not isinstance(valore, (tuple, list)) or len(valore) == 0:
        raise TypeError("Il parametro 'matrice_esiti' richiede una sequenza non vuota di righe.")
    righe: list[tuple[EsitoPixel, ...]] = []
    larghezza: int | None = None
    for q, riga in enumerate(valore):
        if not isinstance(riga, (tuple, list)) or len(riga) == 0:
            raise TypeError(f"La riga {q} della matrice richiede una sequenza non vuota di esiti.")
        if larghezza is None:
            larghezza = len(riga)
        elif len(riga) != larghezza:
            raise ValueError(
                f"La riga {q} ha {len(riga)} esiti contro {larghezza} della prima riga."
            )
        esiti: list[EsitoPixel] = []
        for p, esito in enumerate(riga):
            if esito is None:
                esiti.append(None)
            elif isinstance(esito, bool) or not isinstance(esito, int) or esito < 0:
                raise TypeError(f"L'esito ({p}, {q}) richiede un intero >= 0 oppure None.")
            else:
                esiti.append(esito)
        righe.append(tuple(esiti))
    return tuple(righe)


def costruisci_matrice_esiti(
    classifica_punto: ClassificaPunto,
    larghezza: object,
    altezza: object,
    centro_reale: object,
    centro_immaginaria: object,
    ampiezza_orizzontale: object,
    limite_iterazioni: object,
) -> MatriceEsiti:
    """Costruisce la matrice `H × W` degli esiti con un doppio ciclo su righe e colonne.

    Per ciascun pixel `(p, q)` calcola il punto al centro della cella con
    `punto_da_pixel` e lo classifica con `classifica_punto`, che restituisce
    l'indice di fuga oppure `None`. La matrice degli esiti matematici resta
    distinta dall'immagine RGB: la stessa matrice può essere colorata con
    palette diverse senza ricalcolare le orbite.
    """
    if not callable(classifica_punto):
        raise TypeError("Il parametro 'classifica_punto' richiede una funzione chiamabile.")
    w = valida_intero_non_booleano(larghezza, "larghezza", minimo=1)
    h = valida_intero_non_booleano(altezza, "altezza", minimo=1)
    x_c = valida_reale_finito(centro_reale, "centro_reale")
    y_c = valida_reale_finito(centro_immaginaria, "centro_immaginaria")
    s_x = valida_reale_finito(ampiezza_orizzontale, "ampiezza_orizzontale")
    if s_x <= 0.0:
        raise ValueError("Il parametro 'ampiezza_orizzontale' richiede un valore positivo.")
    n_max = valida_limite_iterazioni(limite_iterazioni)
    righe: list[tuple[EsitoPixel, ...]] = []
    for q in range(h):
        riga: list[EsitoPixel] = []
        for p in range(w):
            punto = punto_da_pixel(p, q, w, h, x_c, y_c, s_x)
            esito = classifica_punto(punto)
            if esito is None:
                riga.append(None)
            elif isinstance(esito, bool) or not isinstance(esito, int):
                raise TypeError(
                    f"Il classificatore ha restituito un esito non valido in ({p}, {q})."
                )
            elif not (0 <= esito <= n_max):
                raise ValueError(f"L'esito in ({p}, {q}) esce dall'intervallo 0..{n_max}.")
            else:
                riga.append(esito)
        righe.append(tuple(riga))
    return tuple(righe)


def statistiche_matrice(matrice_esiti: object, limite_iterazioni: object) -> StatisticheRaster:
    """Riassume una matrice di esiti: conteggi, indice massimo e lavoro effettivo.

    Il totale degli aggiornamenti distingue l'indice `0` (zero aggiornamenti
    su quel pixel) dall'esito `None` (`N` aggiornamenti su quel pixel): il
    controllo usa `is None`, mai la sola falsità.
    """
    matrice = valida_matrice_esiti(matrice_esiti)
    n_max = valida_limite_iterazioni(limite_iterazioni)
    altezza = len(matrice)
    larghezza = len(matrice[0])
    punti_fuga = 0
    aggiornamenti = 0
    indici: list[int] = []
    for riga in matrice:
        for esito in riga:
            if esito is None:
                aggiornamenti += n_max
            else:
                if esito > n_max:
                    raise ValueError(f"L'indice {esito} supera il limite {n_max}.")
                punti_fuga += 1
                aggiornamenti += esito
                indici.append(esito)
    punti_totali = larghezza * altezza
    return StatisticheRaster(
        larghezza=larghezza,
        altezza=altezza,
        limite_iterazioni=n_max,
        punti_totali=punti_totali,
        punti_fuga=punti_fuga,
        punti_interni=punti_totali - punti_fuga,
        indice_massimo=max(indici) if indici else None,
        aggiornamenti_totali=aggiornamenti,
        limite_superiore=punti_totali * n_max,
        byte_immagine_rgb=punti_totali * 3,
    )


def matrice_a_immagine(
    matrice_esiti: object,
    limite_iterazioni: object,
    nome_palette: object = "bande",
) -> Image.Image:
    """Traduce una matrice di esiti in un'immagine RGB `W × H` con Pillow.

    Ogni esito diventa un pixel tramite `colora_esito`; la colorazione costa
    `Theta(W·H)` senza ricalcolare le orbite. L'immagine risultante ha
    modalità `"RGB"` e le stesse dimensioni della matrice.
    """
    matrice = valida_matrice_esiti(matrice_esiti)
    n_max = valida_limite_iterazioni(limite_iterazioni)
    altezza = len(matrice)
    larghezza = len(matrice[0])
    pixel = [colora_esito(esito, n_max, nome_palette) for riga in matrice for esito in riga]
    immagine = Image.new("RGB", (larghezza, altezza))
    immagine.putdata(pixel)
    return immagine


def disegna_segmenti(
    larghezza: object,
    altezza: object,
    segmenti_pixel: object,
    colore_linea: object,
    colore_sfondo: object = (255, 255, 255),
    larghezza_linea: object = 1,
) -> Image.Image:
    """Disegna segmenti in coordinate pixel su una nuova immagine RGB.

    I segmenti provengono dall'adattamento geometrico (`adatta_geometria_a_raster`);
    Pillow disegna gli stessi dati prodotti dai generatori, senza ricalcolarli.
    """
    w = valida_intero_non_booleano(larghezza, "larghezza", minimo=1)
    h = valida_intero_non_booleano(altezza, "altezza", minimo=1)
    linea = valida_colore_rgb(colore_linea, "colore_linea")
    sfondo = valida_colore_rgb(colore_sfondo, "colore_sfondo")
    spessore = valida_intero_non_booleano(larghezza_linea, "larghezza_linea", minimo=1)
    if not isinstance(segmenti_pixel, (tuple, list)) or len(segmenti_pixel) == 0:
        raise ValueError("Il parametro 'segmenti_pixel' richiede una sequenza non vuota.")
    immagine = Image.new("RGB", (w, h), sfondo)
    disegno = ImageDraw.Draw(immagine)
    for i, segmento in enumerate(segmenti_pixel):
        if not isinstance(segmento, (tuple, list)) or len(segmento) != 2:
            raise TypeError(f"Il segmento {i} richiede una coppia di punti (A, B).")
        a = (float(segmento[0][0]), float(segmento[0][1]))
        b = (float(segmento[1][0]), float(segmento[1][1]))
        disegno.line([a, b], fill=linea, width=spessore)
    return immagine


def disegna_triangoli_pieni(
    larghezza: object,
    altezza: object,
    triangoli_pixel: object,
    colore_riempimento: object,
    colore_sfondo: object = (255, 255, 255),
    colore_contorno: object | None = None,
) -> Image.Image:
    """Disegna triangoli pieni in coordinate pixel su una nuova immagine RGB.

    Ogni triangolo è una tripla di punti `(A, B, C)` già adattati al canvas.
    Il contorno, quando dichiarato, usa lo stesso colore dedicato per tutti i
    triangoli della figura.
    """
    w = valida_intero_non_booleano(larghezza, "larghezza", minimo=1)
    h = valida_intero_non_booleano(altezza, "altezza", minimo=1)
    riempimento = valida_colore_rgb(colore_riempimento, "colore_riempimento")
    sfondo = valida_colore_rgb(colore_sfondo, "colore_sfondo")
    contorno = (
        None if colore_contorno is None else valida_colore_rgb(colore_contorno, "colore_contorno")
    )
    if not isinstance(triangoli_pixel, (tuple, list)) or len(triangoli_pixel) == 0:
        raise ValueError("Il parametro 'triangoli_pixel' richiede una sequenza non vuota.")
    immagine = Image.new("RGB", (w, h), sfondo)
    disegno = ImageDraw.Draw(immagine)
    for i, triangolo in enumerate(triangoli_pixel):
        if not isinstance(triangolo, (tuple, list)) or len(triangolo) != 3:
            raise TypeError(f"Il triangolo {i} richiede una tripla di punti (A, B, C).")
        vertici = [(float(p[0]), float(p[1])) for p in triangolo]
        disegno.polygon(vertici, fill=riempimento, outline=contorno)
    return immagine


def salva_png(immagine: object, percorso: object) -> Path:
    """Salva un'immagine RGB in formato PNG creando le directory genitrici.

    Restituisce il percorso del file scritto.
    """
    if not isinstance(immagine, Image.Image):
        raise TypeError("Il parametro 'immagine' richiede un'immagine Pillow.")
    if not isinstance(percorso, (str, Path)):
        raise TypeError("Il parametro 'percorso' richiede una stringa o un Path.")
    destinazione = Path(percorso)
    if destinazione.suffix.lower() != ".png":
        raise ValueError("Il percorso di esportazione richiede l'estensione '.png'.")
    destinazione.parent.mkdir(parents=True, exist_ok=True)
    immagine.save(destinazione, format="PNG")
    return destinazione


def riapri_png_verificato(
    percorso: object,
    larghezza_attesa: object,
    altezza_attesa: object,
) -> Image.Image:
    """Riapre un PNG e ne verifica dimensioni attese e modalità RGB.

    La verifica controlla il contenuto oltre l'esistenza del file: un percorso
    assente solleva `FileNotFoundError`, dimensioni o modalità diverse
    sollevano `ValueError`. Restituisce l'immagine riaperta in modalità RGB.
    """
    if not isinstance(percorso, (str, Path)):
        raise TypeError("Il parametro 'percorso' richiede una stringa o un Path.")
    w = valida_intero_non_booleano(larghezza_attesa, "larghezza_attesa", minimo=1)
    h = valida_intero_non_booleano(altezza_attesa, "altezza_attesa", minimo=1)
    origine = Path(percorso)
    if not origine.is_file():
        raise FileNotFoundError(f"Il file PNG '{origine}' non esiste.")
    with Image.open(origine) as candidata:
        candidata.load()
        immagine = candidata.convert("RGB")
    if immagine.size != (w, h):
        raise ValueError(f"Il PNG misura {immagine.size} contro ({w}, {h}) attesi.")
    return immagine
