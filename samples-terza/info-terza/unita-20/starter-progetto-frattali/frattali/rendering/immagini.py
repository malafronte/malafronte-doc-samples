"""Matrice degli esiti, immagini RGB e file PNG (in parte da completare).

Stato dello starter:

- forniti: `salva_png` e `riapri_png_verificato` per scrittura e rilettura
  con controllo di dimensioni, modalità e pixel (tappa FR-M7);
- da completare: `costruisci_matrice_esiti` con classificatore iniettato,
  `statistiche_matrice` con il lavoro effettivo e `matrice_a_immagine` con
  la palette iniettata (tappe FR-M5 e FR-M7, requisiti FR-06 e FR-10).
"""

from pathlib import Path

from PIL import Image


def salva_png(immagine: object, percorso: object) -> Path:
    """Salva un'immagine RGB in PNG e restituisce il percorso (fornita, FR-M7)."""
    if not isinstance(immagine, Image.Image):
        raise TypeError("Il parametro 'immagine' richiede una PIL.Image.")
    if immagine.mode != "RGB":
        raise ValueError("Il parametro 'immagine' richiede il modo 'RGB'.")
    destinazione = Path(percorso)
    immagine.save(destinazione, format="PNG")
    return destinazione


def riapri_png_verificato(percorso: object, larghezza: object, altezza: object):
    """Riapre il PNG e ne verifica dimensioni e modo (fornita, FR-M7)."""
    if not isinstance(larghezza, int) or not isinstance(altezza, int):
        raise TypeError("Le dimensioni attese richiedono interi.")
    riaperta = Image.open(Path(percorso))
    riaperta.load()
    if riaperta.size != (larghezza, altezza):
        raise ValueError(f"Dimensioni {riaperta.size} contro attese {(larghezza, altezza)}.")
    if riaperta.mode != "RGB":
        raise ValueError(f"Modo {riaperta.mode} contro atteso 'RGB'.")
    return riaperta


def costruisci_matrice_esiti(configurazione: object, classifica_punto: object):
    """Costruisce la matrice degli esiti (da completare, FR-M5)."""
    raise NotImplementedError("FR-M5: campionare la vista e classificare ogni punto.")


def statistiche_matrice(matrice_esiti: object, configurazione: object):
    """Riassume esiti, indice massimo e lavoro (da completare, FR-M7/FR-M8)."""
    raise NotImplementedError("FR-M7: distinguere None (costo N) dall'indice n (costo n).")


def matrice_a_immagine(matrice_esiti: object, configurazione: object):
    """Traduce la matrice in immagine RGB (da completare, FR-M5)."""
    raise NotImplementedError("FR-M5: colorare ogni esito senza ricalcolare le orbite.")
