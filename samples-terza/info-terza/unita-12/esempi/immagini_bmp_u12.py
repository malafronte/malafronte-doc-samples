"""Lettura mirata di un'immagine BMP e trasformazioni semplici sui pixel.

Un'immagine è anch'essa un file binario, e questo modulo la tratta come il
cap. PY-21 tratta i record: intestazione letta campo per campo, pixel a
**posizione calcolata**, trasformazioni che toccano soltanto i byte previsti.
Il sottoinsieme di formato qui usato è dichiarato e non si estende:

- BMP a **24 bit non compresso** (BITMAPINFOHEADER da 40 byte, totale 54 byte
  di intestazione);
- ogni pixel occupa tre byte nell'ordine **BGR** - blu, verde, rosso -, come
  impone il formato;
- le righe sono scritte **dal basso verso l'alto** e allineate a multipli di
  quattro byte: se la riga di pixel non è già un multiplo di quattro, il
  formato inserisce byte di riempimento in fondo a ogni riga.

Le due trasformazioni sono filtri RGB elementari: l'inversione di colore
sostituisce ogni componente `c` con `255 - c`; lo scambio blu/rosso scambia il
primo e il terzo byte di ogni pixel e rende visibile l'ordine BGR del file.
Nessuna delle due è un'elaborazione d'immagine completa: formati compressi -
PNG, JPEG - e varianti del BMP richiedono una libreria come Pillow, che
conosce la struttura per intero.

Ambiente: CPython sul computer, sola libreria standard. Le immagini di
prova sono **copie di lavoro**: la funzione di scrittura rifiuta una
destinazione coincidente con la sorgente.
"""

from pathlib import Path

LUNGHEZZA_INTESTAZIONE = 54
BYTE_PER_PIXEL = 3


def _campi_intestazione(contenuto):
    """Legge dall'header i campi usati da questo modulo, in ordine di offset.

    I valori sono interi little-endian letti con `int.from_bytes`: la firma è
    l'unica coppia di byte interpretata come testo. Solleva `ValueError` se
    l'header è più corto di 54 byte.
    """
    if len(contenuto) < LUNGHEZZA_INTESTAZIONE:
        raise ValueError(f"intestazione incompleta: {len(contenuto)} byte su {LUNGHEZZA_INTESTAZIONE}")
    return {
        "firma": contenuto[0:2].decode("ascii", errors="replace"),
        "dimensione_dichiarata": int.from_bytes(contenuto[2:6], "little"),
        "offset_pixel": int.from_bytes(contenuto[10:14], "little"),
        "larghezza": int.from_bytes(contenuto[18:22], "little"),
        "altezza": int.from_bytes(contenuto[22:26], "little"),
        "bit_per_pixel": int.from_bytes(contenuto[28:30], "little"),
    }


def intestazione_bmp(percorso):
    """Restituisce i campi dell'intestazione BMP con la verifica di completezza.

    Il risultato è un dizionario con `firma`, `dimensione_dichiarata`,
    `dimensione_effettiva`, `offset_pixel`, `larghezza`, `altezza`,
    `bit_per_pixel` e `completo`. Il campo `completo` confronta la dimensione
    **dichiarata** nell'header con quella **effettiva** del file: è la verifica
    semplice che scopre i file troncati, di cui la firma iniziale non dice
    nulla. L'ordine dei pixel nel file non è controllato qui: BMP conserva le
    righe dal basso verso l'alto.
    """
    percorso = Path(percorso)
    contenuto = percorso.read_bytes()
    campi = _campi_intestazione(contenuto)
    campi["dimensione_effettiva"] = len(contenuto)
    campi["completo"] = campi["dimensione_dichiarata"] == len(contenuto)
    return campi


def _offset_pixel(campi, indice):
    """Calcola l'offset del pixel di indice `indice` nella sequenza del file.

    L'indice attraversa i pixel da sinistra a destra e dalla prima riga del
    file - che per BMP è la riga **bassa** dell'immagine. L'offset tiene conto
    dell'allineamento di riga: `larghezza * 3` byte di pixel più il
    riempimento che porta la riga al multiplo di quattro successivo.
    """
    numero_pixel = campi["larghezza"] * campi["altezza"]
    if isinstance(indice, bool) or not isinstance(indice, int):
        raise TypeError(f"indice: atteso un intero, ricevuto {type(indice).__name__}")
    if indice < 0:
        raise ValueError(f"indice {indice}: negativo, gli indici partono da 0")
    if indice >= numero_pixel:
        raise ValueError(f"indice {indice}: fuori intervallo, l'immagine contiene {numero_pixel} pixel")
    riga_pixel = campi["larghezza"] * BYTE_PER_PIXEL
    riga_allineata = (riga_pixel + 3) // 4 * 4
    riga = indice // campi["larghezza"]
    colonna = indice % campi["larghezza"]
    return campi["offset_pixel"] + riga * riga_allineata + colonna * BYTE_PER_PIXEL


def leggi_pixel(percorso, indice):
    """Restituisce la terna `(blu, verde, rosso)` del pixel di indice `indice`.

    I tre valori sono interi 0-255 nell'ordine in cui il file li conserva, che
    per BMP è BGR. Un pixel incompleto produce `ValueError`: nessun colore
    sintetico viene restituito per il byte mancante.
    """
    percorso = Path(percorso)
    contenuto = percorso.read_bytes()
    campi = _campi_intestazione(contenuto)
    offset = _offset_pixel(campi, indice)
    byte_pixel = contenuto[offset:offset + BYTE_PER_PIXEL]
    if len(byte_pixel) != BYTE_PER_PIXEL:
        raise ValueError(f"pixel {indice}: incompleto, {len(byte_pixel)} byte disponibili su {BYTE_PER_PIXEL}")
    return byte_pixel[0], byte_pixel[1], byte_pixel[2]


def _trasforma_immagine(percorso, destinazione, trasforma_pixela):
    """Copia l'immagine applicando `trasforma_pixela` a ogni pixel della riga.

    `trasforma_pixela(blu, verde, rosso)` restituisce la terna da scrivere.
    L'header e i byte di riempimento di riga restano invariati; il file di
    partenza non viene toccato. Restituisce il numero di pixel trasformati.
    """
    percorso = Path(percorso)
    destinazione = Path(destinazione)
    if destinazione.resolve() == percorso.resolve():
        raise ValueError("la destinazione coincide con la sorgente: usare una copia di lavoro")
    contenuto = bytearray(percorso.read_bytes())
    campi = _campi_intestazione(contenuto)
    riga_pixel = campi["larghezza"] * BYTE_PER_PIXEL
    riga_allineata = (riga_pixel + 3) // 4 * 4
    trasformati = 0
    for riga in range(campi["altezza"]):
        inizio = campi["offset_pixel"] + riga * riga_allineata
        for colonna in range(campi["larghezza"]):
            offset = inizio + colonna * BYTE_PER_PIXEL
            blu, verde, rosso = contenuto[offset:offset + BYTE_PER_PIXEL]
            nuovo_blu, nuovo_verde, nuovo_rosso = trasforma_pixela(blu, verde, rosso)
            contenuto[offset:offset + BYTE_PER_PIXEL] = bytes((nuovo_blu, nuovo_verde, nuovo_rosso))
            trasformati += 1
    destinazione.write_bytes(bytes(contenuto))
    return trasformati


def inverti_colori(percorso, destinazione):
    """Scrive una copia con ogni componente del colore sostituita da `255 - c`.

    Filtro RGB elementare: il bianco diventa nero, i colori diventano i
    complementari. Header e allineamenti restano invariati.
    """
    return _trasforma_immagine(percorso, destinazione, lambda blu, verde, rosso: (255 - blu, 255 - verde, 255 - rosso))


def scambia_blu_rosso(percorso, destinazione):
    """Scrive una copia con il primo e il terzo byte di ogni pixel scambiati.

    Poiché BMP conserva i canali nell'ordine BGR, questo filtro mostra il
    rosso dove il file ha il blu e viceversa: è il modo più diretto per
    osservare che l'ordine dei byte, sui colori, è parte del formato.
    """
    return _trasforma_immagine(percorso, destinazione, lambda blu, verde, rosso: (rosso, verde, blu))


if __name__ == "__main__":
    # Dimostrazione sulla fixture, con le copie in una cartella temporanea.
    import tempfile

    originale = Path("dati/immagini/immagine_originale.bmp")
    print("== intestazione ==")
    for nome, valore in intestazione_bmp(originale).items():
        print(f"{nome}: {valore}")
    print("== primo pixel (indice 0, in fondo a sinistra nell'immagine) ==")
    print("BGR:", leggi_pixel(originale, 0))
    with tempfile.TemporaryDirectory() as cartella:
        invertita = Path(cartella) / "invertita.bmp"
        scambiata = Path(cartella) / "scambiata.bmp"
        print("== inversione dei colori ==")
        print("pixel trasformati:", inverti_colori(originale, invertita))
        print("primo pixel dopo:", leggi_pixel(invertita, 0))
        print("lunghezza invariata:", invertita.stat().st_size == originale.stat().st_size)
        print("== scambio blu/rosso ==")
        print("pixel trasformati:", scambia_blu_rosso(originale, scambiata))
        print("primo pixel dopo:", leggi_pixel(scambiata, 0))
