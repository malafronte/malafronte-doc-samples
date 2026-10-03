"""Immagini con Pillow: apertura, conversione RGB, inversione dei pixel.

Applicazione della libreria **Pillow** - distribuzione `pillow`, package
importabile `PIL` - dell'Unità 12. La trasformazione è **punto per punto**:
ogni pixel nuovo dipende soltanto dal pixel corrispondente dell'originale. Un
filtro spaziale, che legge anche i pixel vicini, è un passo successivo e qui
non è trattato.

Contratti:

- `crea_immagine_sintetica(percorso, lato=4)` → genera un'immagine RGB di
  `lato × lato` pixel con valori noti e la salva in PNG; restituisce la tupla
  `(larghezza, altezza)`; `lato` è un intero fra 1 e 6 inclusi.
- `carica_rgb(percorso)` → apre il file con `Image.open` e lo converte in
  modalità `RGB`; restituisce l'immagine. Il file sorgente resta apribile e
  invariato.
- `inverti_pixel(immagine)` → restituisce un'immagine **nuova** in cui ogni
  canale `c` diventa `255 - c`; l'immagine ricevuta non è modificata.
- `confronta_imageops(immagine)` → restituisce `True` se l'inversione manuale
  coincide con `ImageOps.invert(immagine)` su tutti i pixel.
- `salva_png(immagine, percorso, sorgente=None)` → salva in un file distinto
  dalla sorgente dichiarata; se i due percorsi identificano lo stesso file,
  rifiuta la scrittura. L'originale non va sovrascritto dalla trasformazione.

Errori: `TypeError` per argomenti di tipo sbagliato, `ValueError` per i dati
fuori dominio o per la destinazione coincidente con la sorgente. Le classi
d'errore di I/O (`FileNotFoundError`, `PIL.UnidentifiedImageError`) si
propagano dal livello che apre il file.

Ambiente: CPython nel progetto `applicazioni-librerie` con `pillow` installato
in modo esplicito; nessuna installazione globale. Si importa `PIL`, non
`pillow`: il nome della distribuzione e quello del package non coincidono.
"""

from pathlib import Path

from PIL import Image
from PIL import ImageOps


def crea_immagine_sintetica(percorso, lato=4):
    """Genera e salva un'immagine RGB quadrata con valori di pixel noti.

    Il pixel alla posizione `(x, y)` ha canali `(16 + 40 * x, 16 + 40 * y,
    128)`: il valore si ricostruisce dalla posizione e permette di verificare
    ogni trasformazione senza un editor di immagini. Il lato è limitato a
    1-6: all'indice 5 i canali valgono 216; all'indice 6 varrebbero 256,
    oltre il massimo 255 di un canale RGB a 8 bit.
    """
    if isinstance(lato, bool) or not isinstance(lato, int):
        raise TypeError(f"lato: atteso un intero, ricevuto {type(lato).__name__}")
    if not 1 <= lato <= 6:
        raise ValueError(f"lato: deve essere fra 1 e 6, ricevuto {lato}")
    immagine = Image.new("RGB", (lato, lato))
    for y in range(lato):
        for x in range(lato):
            immagine.putpixel((x, y), (16 + 40 * x, 16 + 40 * y, 128))
    immagine.save(percorso, format="PNG")
    return (lato, lato)


def carica_rgb(percorso):
    """Apre il file immagine e lo converte in modalità RGB."""
    with Image.open(percorso) as aperta:
        return aperta.convert("RGB")


def inverti_pixel(immagine):
    """Restituisce un'immagine nuova con ogni canale `c` trasformato in `255 - c`."""
    if not isinstance(immagine, Image.Image):
        raise TypeError("immagine: attesa un'immagine PIL")
    larghezza, altezza = immagine.size
    invertita = Image.new("RGB", (larghezza, altezza))
    for y in range(altezza):
        for x in range(larghezza):
            rosso, verde, blu = immagine.getpixel((x, y))
            invertita.putpixel((x, y), (255 - rosso, 255 - verde, 255 - blu))
    return invertita


def confronta_imageops(immagine):
    """Verifica che l'inversione manuale coincida con `ImageOps.invert`."""
    manuale = inverti_pixel(immagine)
    con_libre = ImageOps.invert(immagine)
    larghezza, altezza = immagine.size
    for y in range(altezza):
        for x in range(larghezza):
            if manuale.getpixel((x, y)) != con_libre.getpixel((x, y)):
                return False
    return True


def salva_png(immagine, percorso, sorgente=None):
    """Salva l'immagine in PNG su un percorso diverso dalla sorgente."""
    if not isinstance(immagine, Image.Image):
        raise TypeError("immagine: attesa un'immagine PIL")
    if sorgente is not None:
        destinazione = Path(percorso)
        origine = Path(sorgente)
        # resolve confronta percorsi relativi/assoluti e collegamenti simbolici.
        coincidente = destinazione.resolve() == origine.resolve()
        # Due nomi già esistenti possono anche essere collegamenti fisici
        # allo stesso file: samefile confronta l'identità nel file system.
        if not coincidente and destinazione.exists() and origine.exists():
            coincidente = destinazione.samefile(origine)
        if coincidente:
            raise ValueError("destinazione coincidente con la sorgente: l'originale non si sovrascrive")
    immagine.save(percorso, format="PNG")
    return percorso


if __name__ == "__main__":
    # Dimostrazione sotto guardia: immagine sintetica, apertura, trasformazione
    # e salvataggio in file nuovi nella cartella `output` accanto al sorgente.
    uscita = Path(__file__).with_name("output")
    uscita.mkdir(exist_ok=True)
    originale = uscita / "pillow-originale.png"

    dimensioni = crea_immagine_sintetica(originale)
    print(f"immagine sintetica {dimensioni[0]}x{dimensioni[1]} salvata in {originale}")

    aperta = carica_rgb(originale)
    print(f"modalita dopo la conversione: {aperta.mode}, dimensioni: {aperta.size}")
    print(f"pixel (0, 0): {aperta.getpixel((0, 0))}")

    invertita = inverti_pixel(aperta)
    print(f"pixel (0, 0) dopo l'inversione: {invertita.getpixel((0, 0))}")
    print(f"inversione manuale uguale a ImageOps.invert: {confronta_imageops(aperta)}")

    salva_png(invertita, uscita / "pillow-invertita.png", sorgente=originale)
    di_nuovo = carica_rgb(originale)
    print(f"originale dopo il salvataggio: {di_nuovo.getpixel((0, 0))}")
