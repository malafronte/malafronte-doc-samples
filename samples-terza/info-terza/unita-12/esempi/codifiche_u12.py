"""Byte, Unicode e codifiche: confronti in memoria, senza file.

Questo modulo ragiona su **sequenze di byte in memoria**: non apre file e non
scrive nulla. Ogni esperimento usa letterali `bytes` o `bytearray`, così il
dato e il suo atteso si leggono nello stesso listato. Le stesse verifiche sui
file reali si fanno con l'API dei file, spiegata nei capitoli successivi
dell'Unità 12.

Nuclei:

- `sommario_testo(testo)` - codepoint, byte UTF-8 e loro forma
  esadecimale, per contare `str` e `bytes` senza confonderli;
- `decodifiche_con_firma(dati)` - la stessa sequenza decodificata con `utf-8`
  e con `utf-8-sig`, per osservare che cosa succede al BOM iniziale;
- `confronto_bytearray()` - `bytes` immutabile contro `bytearray` modificabile;
- `BOM_UTF8` - i tre byte `EF BB BF` della firma UTF-8.

Ambiente: CPython sul computer. Nessuna lettura da tastiera, nessuna stampa.
"""

BOM_UTF8 = b"\xef\xbb\xbf"


def sommario_testo(testo):
    """Restituisce codepoint e byte UTF-8 del testo ricevuto.

    Il risultato è un dizionario nuovo con:
    - `testo`: il testo ricevuto, invariato;
    - `punti_codice`: quanti codepoint contiene (`len(testo)`);
    - `punti`: i codepoint come interi, nell'ordine del testo;
    - `byte_utf8`: la sequenza `bytes` della codifica UTF-8;
    - `byte_hex`: gli stessi byte in cifre esadecimali maiuscole, separati da
      uno spazio (per esempio `"C3 A8"`).
    """
    byte_utf8 = testo.encode("utf-8")
    return {
        "testo": testo,
        "punti_codice": len(testo),
        "punti": [ord(carattere) for carattere in testo],
        "byte_utf8": byte_utf8,
        "byte_hex": " ".join(f"{byte:02X}" for byte in byte_utf8),
    }


def decodifiche_con_firma(dati):
    """Decodifica la stessa sequenza di byte con `utf-8` e con `utf-8-sig`.

    Con `utf-8` un eventuale BOM iniziale diventa il carattere U+FEFF, che
    compare come primo codepoint della stringa. Con `utf-8-sig` la firma
    iniziale viene omessa e il testo è quello «pulito». Una U+FEFF interna o
    non iniziale **resta** in entrambi i casi: i due codec differiscono solo
    sull'inizio della sequenza.
    """
    return {
        "utf8": dati.decode("utf-8"),
        "utf8_sig": dati.decode("utf-8-sig"),
    }


def confronto_bytearray():
    """Restituisce un registro dell'esperimento fra `bytes` e `bytearray`.

    Il registro contiene la sequenza immutabile prima e dopo il tentativo di
    modifica per via indiretta, la sequenza modificabile prima e dopo
    l'assegnamento a un indice, e i due tipi risultanti. `bytes` non accetta
    assegnamenti per indice; `bytearray` sì, e i suoi byte si ottengono di
    nuovo come `bytes` con `bytes(...)`.
    """
    sequenza = b"ABCD"
    provata = sequenza
    esito = "assegnamento riuscito"
    try:
        provata[0] = 90
    except TypeError as errore:
        esito = f"TypeError: {errore}"
    modificabile = bytearray(b"ABCD")
    modificabile[0] = 90
    return {
        "bytes_originale": sequenza,
        "bytes_dopo": provata,
        "esito_assegnamento": esito,
        "bytearray_dopo": bytes(modificabile),
        "tipo_finale": type(modificabile).__name__,
    }


def main():
    """Stampa i confronti canonici del capitolo su byte e codifiche."""
    print("Il codepoint e i suoi byte UTF-8")
    for testo, etichetta in (("è", "precomposta"), ("e\u0300", "combinante"), ("", "vuota")):
        sommario = sommario_testo(testo)
        print(f"{etichetta:12} testo={testo!r:12} punti={sommario['punti_codice']}"
              f" byte={len(sommario['byte_utf8'])} hex={sommario['byte_hex'] or '(nessuno)'}")

    print()
    print("La firma UTF-8 all'inizio della sequenza")
    senza_firma = "sole".encode("utf-8")
    con_firma = BOM_UTF8 + senza_firma
    print(f"senza BOM: {senza_firma!r} -> {decodifiche_con_firma(senza_firma)}")
    print(f"con BOM:   {con_firma!r}")
    per_codec = decodifiche_con_firma(con_firma)
    for codec, testo in per_codec.items():
        print(f"  {codec:9} -> {testo!r}  punti={[hex(ord(c)) for c in testo]}")

    interno = "a\ufeffb".encode("utf-8")
    print(f"U+FEFF interna: {interno!r} -> {decodifiche_con_firma(interno)}")

    print()
    print("bytes e bytearray")
    for nome, valore in confronto_bytearray().items():
        print(f"{nome:20} {valore!r}")


if __name__ == "__main__":
    main()
