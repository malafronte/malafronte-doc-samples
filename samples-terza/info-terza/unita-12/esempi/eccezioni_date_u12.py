"""Eccezioni, propagazione e date: funzioni pure e coordinatore espliciti.

Le funzioni di questo modulo sono **pure**: ricevono dati e restituiscono
risultati oppure sollevano l'eccezione prevista dal proprio contratto. Non
leggono input, non stampano e non decidono se ripresentare una domanda: la
decisione spetta al coordinatore `main`, che è l'unico punto interattivo.

Nuclei:

- `valida_quantita(testo)` - conversione e dominio come controlli **separati**;
- `prezzo_totale(testo_quantita, prezzo_centesimi)` - propagazione su due
  chiamate (`main` -> `prezzo_totale` -> `valida_quantita`);
- `prova_conversione(testo)` - registro dei passaggi di
  `try`/`except`/`else`/`finally`;
- `giorni_tra(inizio, fine)` - differenza fra date ISO con `timedelta`;
- `eta_anni(nascita, riferimento)` - anni compiuti, con il compleanno del
  29 febbraio convenzionalmente fissato al 1° marzo negli anni non bisestili;
- `data_da_formato(testo, formato)` - parsing con `datetime.strptime` e
  formato esplicito;
- `main()` - coordinatore con gestori mirati, recupero della domanda ed EOF.

Ambiente: CPython sul computer. Esecuzione dalla cartella `esempi/`.
"""

from datetime import date, datetime


def valida_quantita(testo):
    """Converte e controlla una quantità: intero maggiore o uguale a zero.

    I due controlli sono separati e producono diagnosi diverse:
    - la **conversione** con `int(testo)` solleva `ValueError` se il formato
      non è quello di un intero (per esempio `"tre"`, `""`, `"3.5"`);
    - il **dominio** rifiuta con `ValueError` gli interi negativi, con un
      messaggio che nomina il valore.

    Zero è un dato **valido**. Un argomento che non è una stringa non è un
    dato sbagliato ma un uso sbagliato della funzione: non viene convertito in
    `ValueError` e il difetto resta visibile.
    """
    valore = int(testo)  # ValueError se il formato non è convertibile
    if valore < 0:
        raise ValueError(f"quantità negativa: {valore}")
    return valore


def prezzo_totale(testo_quantita, prezzo_centesimi):
    """Restituisce quantità per prezzo, in centesimi.

    Chiama `valida_quantita` senza intercettarne le eccezioni: una quantità non
    valida si propaga al chiamante di questa funzione. Il contratto prevede
    `prezzo_centesimi` intero non negativo, come per il magazzino del cap. PY-16.
    """
    quantita = valida_quantita(testo_quantita)
    return quantita * prezzo_centesimi


def prova_conversione(testo):
    """Restituisce il registro dei passaggi di try/except/else/finally.

    Il registro è una lista di stringhe nell'ordine in cui i passaggi vengono
    eseguiti: mostra che il corpo del `finally` è sempre eseguito, mentre
    quello dell'`else` è eseguito solo quando il blocco protetto termina senza
    eccezioni.
    """
    passaggi = []
    try:
        passaggi.append("try: provo la conversione")
        valore = int(testo)
    except ValueError:
        passaggi.append("except: il testo non è un intero")
    else:
        passaggi.append(f"else: conversione riuscita, valore {valore}")
    finally:
        passaggi.append("finally: sempre eseguito")
    return passaggi


def giorni_tra(inizio, fine):
    """Restituisce i giorni fra due date in formato ISO `AAAA-MM-GG`.

    Il secondo giorno non può precedere il primo: in quel caso la funzione
    solleva `ValueError` nominando le due date. Un formato non valido viene
    rifiutato dalla conversione `date.fromisoformat`, che solleva `ValueError`.
    Lo stesso giorno dà 0; la differenza è di calendario, non di 24 ore.
    """
    data_inizio = date.fromisoformat(inizio)
    data_fine = date.fromisoformat(fine)
    if data_fine < data_inizio:
        raise ValueError(f"la seconda data precede la prima: {fine} < {inizio}")
    return (data_fine - data_inizio).days


def compleanno_anno(data_nascita, anno):
    """Restituisce la ricorrenza del compleanno nell'anno indicato.

    Convenzione del corso: chi è nato il **29 febbraio** festeggia il **1°
    marzo** negli anni non bisestili, mentre negli anni bisestili la ricorrenza
    resta il 29 febbraio. La funzione riceve un oggetto `date` e restituisce
    un oggetto `date`.
    """
    if data_nascita.month == 2 and data_nascita.day == 29:
        try:
            return date(anno, 2, 29)  # anno bisestile: la ricorrenza resta il 29 febbraio
        except ValueError:
            return date(anno, 3, 1)  # anno non bisestile: convenzione del 1° marzo
    return date(anno, data_nascita.month, data_nascita.day)


def eta_anni(nascita, riferimento):
    """Restituisce gli anni compiuti alla data di riferimento, entrambe ISO.

    La nascita non può essere successiva al riferimento: in quel caso la
    funzione solleva `ValueError`. Gli anni compiuti non si ottengono dividendo
    i giorni per 365: si confronta la ricorrenza del compleanno nell'anno del
    riferimento e, se non è ancora trascorsa, si sottrae un anno.
    """
    data_nascita = date.fromisoformat(nascita)
    data_riferimento = date.fromisoformat(riferimento)
    if data_nascita > data_riferimento:
        raise ValueError(f"la nascita è successiva al riferimento: {nascita} > {riferimento}")
    anni = data_riferimento.year - data_nascita.year
    if compleanno_anno(data_nascita, data_riferimento.year) > data_riferimento:
        anni -= 1
    return anni


def data_da_formato(testo, formato):
    """Converte una data scritta in un formato esplicito, per esempio `%d/%m/%Y`.

    Il formato è parte dell'accordo: `datetime.strptime` solleva `ValueError`
    quando il testo non corrisponde. La funzione restituisce un oggetto `date`.
    """
    return datetime.strptime(testo, formato).date()


def main():
    """Coordina la sessione dimostrativa con gestori mirati e recupero."""
    print("1. Propagazione su due chiamate: main -> prezzo_totale -> valida_quantita")
    try:
        totale = prezzo_totale("tre", 250)
    except ValueError as errore:
        print(f"   il gestore di main intercetta ValueError: {errore}")
    else:
        print(f"   nessuna eccezione: il totale è {totale} centesimi")

    print("2. else e finally sulla conversione")
    for testo in ("42", "quarantadue"):
        print(f"   ingresso {testo!r}")
        for passaggio in prova_conversione(testo):
            print(f"     {passaggio}")

    print("3. Date con riferimenti fissi, senza il giorno di oggi")
    print(f"   giorni_tra('2024-02-28', '2024-03-01') = {giorni_tra('2024-02-28', '2024-03-01')}")
    print(f"   eta_anni('2012-02-29', '2026-02-28') = {eta_anni('2012-02-29', '2026-02-28')}")
    print(f"   eta_anni('2012-02-29', '2026-03-01') = {eta_anni('2012-02-29', '2026-03-01')}")
    print(f"   data_da_formato('20/10/2010', '%d/%m/%Y') = {data_da_formato('20/10/2010', '%d/%m/%Y')}")

    print("4. Domanda con recupero; la sessione termina anche senza dati in arrivo")
    while True:
        try:
            testo = input("   Inserisci una quantità (chiudi l'input per terminare): ")
        except EOFError:
            print("   EOFError: nessun dato in arrivo, sessione terminata")
            return
        try:
            quantita = valida_quantita(testo)
        except ValueError as errore:
            print(f"   valore rifiutato: {errore}; la domanda viene riproposta")
            continue
        print(f"   quantità accettata: {quantita}")
        return


if __name__ == "__main__":
    main()
