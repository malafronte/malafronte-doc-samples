"""Conteggi dei cicli dell'Unità 9: formule esatte e confini.

Collocare il file in `programmi/conteggi_cicli.py` della raccolta dello
studente. Il modulo esegue i procedimenti della tabella dei cicli del
capitolo PY-13, parti I-II, e ne restituisce il conteggio esatto del corpo
del ciclo: attraversamenti, cicli indipendenti e annidati, coppie di indici,
cicli con interno fisso, dimezzamenti, raddoppiamenti e visita di una
matrice rettangolare.

Convenzione del conteggio: si conta quante volte si esegue il CORPO del
ciclo dichiarato. Il conteggio non include la valutazione finale falsa
della guardia, che non è un'esecuzione del corpo: per un ciclo `while`
quella valutazione avviene una volta in più, a lavoro finito. Se si vuole
contare anche quella serve una colonna distinta e una convenzione
esplicita.

Unità contata ed esempi: per i cicli che attraversano una sequenza il corpo
è la visita a un elemento; per le coppie `i < j` il corpo è la gestione di
una coppia; per il dimezzamento il corpo è il passo `m //= 2`. La base del
logaritmo incide sul conteggio esatto ma non sulla classe Θ(log n) per basi
costanti maggiori di 1.

L'import non chiede input e non stampa: la tabella dei conteggi si costruisce
in memoria e si presenta nel main protetto dalla guardia di avvio.
Esecuzione: uv run python programmi/conteggi_cicli.py
"""


# ---------------------------------------------------------------------------
# Attraversamenti e cicli indipendenti
# ---------------------------------------------------------------------------


def conta_attraversamento(n: int) -> int:
    """Restituisce le esecuzioni del corpo di un unico attraversamento.

    Dominio: n intero non negativo, numero degli elementi. Il corpo si
    esegue n volte: 0 per n = 0, 1 per n = 1, 4 per n = 4.
    """
    contatore = 0
    for _indice in range(n):
        contatore += 1
    return contatore


def conta_due_consecutivi(n: int) -> int:
    """Restituisce le esecuzioni del corpo di due attraversamenti in sequenza.

    Dominio: n intero non negativo. I due cicli sono consecutivi e
    indipendenti l'uno dall'altro: il secondo riparte da capo e il totale
    è 2n. Per n = 0/1/4 il totale è 0/2/8.
    """
    contatore = 0
    for _indice in range(n):
        contatore += 1
    for _indice in range(n):
        contatore += 1
    return contatore


def conta_due_indipendenti(n: int) -> int:
    """Restituisce le esecuzioni del corpo di due cicli annidati indipendenti.

    Struttura: `range(n)` dentro `range(n)`. Ogni giro del ciclo esterno
    avvia un attraversamento completo di n elementi: il totale è n², che
    per n = 0/1/4 vale 0/1/16. La presenza di due cicli annidati non basta
    da sola a dichiarare un andamento quadratico: qui lo diventa perché
    entrambi dipendono da n.
    """
    contatore = 0
    for _esterno in range(n):
        for _interno in range(n):
            contatore += 1
    return contatore


def conta_coppie_i_j(n: int) -> int:
    """Restituisce le esecuzioni del corpo sulle coppie di indici i < j.

    Struttura: `i in range(n)` e `j in range(i + 1, n)`. Le coppie
    considerate hanno gli indici strettamente crescenti: escludono la
    diagonale con i = j e le coppie invertite, quindi ogni coppia distinta
    viene visitata una volta sola. Il totale è n(n-1)/2: 0 per n = 0 e
    n = 1, 6 per n = 4.
    """
    contatore = 0
    for i in range(n):
        for j in range(i + 1, n):
            contatore += 1
    return contatore


def conta_interno_fisso(n: int) -> int:
    """Restituisce le esecuzioni del corpo con interno a tre giri fissi.

    Struttura: ciclo esterno su n giri e ciclo interno sempre di 3 giri.
    L'interno non dipende da n: il totale è 3n e non n². Per n = 0/1/4 il
    totale è 0/3/12.
    """
    contatore = 0
    for _esterno in range(n):
        for _interno in range(3):
            contatore += 1
    return contatore


# ---------------------------------------------------------------------------
# Dimezzamenti e raddoppiamenti
# ---------------------------------------------------------------------------


def conta_dimezzamenti(n: int) -> int:
    """Restituisce i giri del dimezzamento `while m > 1: m //= 2` da m = n.

    Dominio: n intero. Per n >= 1 il totale è floor(log2(n)): 0 per n = 1,
    2 per n = 7, 3 per n = 8 e n = 9, 4 per n = 20. Per n = 0 la guardia
    `m > 1` è subito falsa e il totale è 0: non si scrive log2(0), si
    dichiara il comportamento del ramo. Il conteggio non include la
    valutazione finale falsa della guardia. Il conteggio esatto dipende
    dalla guardia adottata: con `m > 0` il valore che raggiunge 1 eseguebbe
    un giro in più.
    """
    contatore = 0
    m = n
    while m > 1:
        m //= 2
        contatore += 1
    return contatore


def conta_raddoppiamenti(n: int) -> int:
    """Restituisce i giri del raddoppio `while m < n: m *= 2` da m = 1.

    Dominio: n intero. Per n >= 1 il totale è ceil(log2(n)), con il
    soffitto perché basta raggiungere o superare n: 0 per n = 1, 3 per
    n = 7 e n = 8, 4 per n = 9, 5 per n = 20. Per n = 0 la guardia `m < n`
    è subito falsa e il totale è 0. Il conteggio non include la valutazione
    finale falsa della guardia.
    """
    contatore = 0
    m = 1
    while m < n:
        m *= 2
        contatore += 1
    return contatore


def conta_n_dimezzamenti(n: int) -> int:
    """Restituisce i dimezzamenti totali di n ripetizioni indipendenti.

    Struttura: per ciascuno dei n elementi si riparte da m = n e si esegue
    `while m > 1: m //= 2`. L'unità contata è il passo di dimezzamento: il
    giro del ciclo esterno che riparte da m = n non è incluso nel conteggio
    dichiarato. Per n >= 1 il totale è n * floor(log2(n)) e per n = 8 vale
    24; per n = 0 il ciclo esterno non ha giri e il totale è 0. Il modello
    n·log2(n) deriva da questa ripetizione indipendente e non richiede
    algoritmi di ordinamento.
    """
    contatore = 0
    for _elemento in range(n):
        m = n
        while m > 1:
            m //= 2
            contatore += 1
    return contatore


# ---------------------------------------------------------------------------
# Matrice rettangolare
# ---------------------------------------------------------------------------


def conta_visite_matrice(righe: int, colonne: int) -> int:
    """Restituisce le visite alle celle di una matrice rettangolare r x c.

    Dominio: `righe` e `colonne` interi non negativi; la matrice ha righe
    di uguale lunghezza. L'unità contata è la visita a una cella del doppio
    attraversamento riga per riga; la costruzione della matrice interna non
    rientra nel conteggio dichiarato. Il totale è r*c: 6 per 2x3, 9 per
    3x3; se una delle due dimensioni è 0 il totale è 0. Il lavoro è
    quadratico rispetto al lato solo quando r = c = n: in termini di celle
    totali N = r*c resta lineare rispetto a N.
    """
    matrice = [[10 * riga + colonna for colonna in range(colonne)] for riga in range(righe)]
    contatore = 0
    for riga in matrice:
        for _valore in riga:
            contatore += 1
    return contatore


# ---------------------------------------------------------------------------
# Tabella dei conteggi
# ---------------------------------------------------------------------------


def tabella_dei_conteggi() -> list[dict]:
    """Restituisce la tabella dei conteggi come lista di righe in memoria.

    Ogni riga ha le chiavi `chiave`, `procedimento`, `formula`, `dominio` e
    `casi`. `chiave` è il nome della funzione che produce il conteggio;
    `formula` è la regola generale ricavata dal modello; `casi` è la lista
    di coppie `(parametri, conteggio)` calcolate eseguendo le funzioni sui
    casi di riferimento. Per la matrice i parametri sono la coppia
    `(righe, colonne)`, per tutti gli altri procedimenti il singolo n.
    La funzione non stampa: la presentazione testuale sta nel main.
    """
    return [
        {
            "chiave": "conta_attraversamento",
            "procedimento": "Un attraversamento completo",
            "formula": "n",
            "dominio": "n >= 0",
            "casi": [(n, conta_attraversamento(n)) for n in (0, 1, 4)],
        },
        {
            "chiave": "conta_due_consecutivi",
            "procedimento": "Due attraversamenti consecutivi",
            "formula": "2n",
            "dominio": "n >= 0",
            "casi": [(n, conta_due_consecutivi(n)) for n in (0, 1, 4)],
        },
        {
            "chiave": "conta_due_indipendenti",
            "procedimento": "Due cicli indipendenti di lunghezza n",
            "formula": "n^2",
            "dominio": "n >= 0",
            "casi": [(n, conta_due_indipendenti(n)) for n in (0, 1, 4)],
        },
        {
            "chiave": "conta_coppie_i_j",
            "procedimento": "Coppie i < j, j in range(i + 1, n)",
            "formula": "n(n-1)/2",
            "dominio": "n >= 0",
            "casi": [(n, conta_coppie_i_j(n)) for n in (0, 1, 4)],
        },
        {
            "chiave": "conta_interno_fisso",
            "procedimento": "Ciclo esterno n, interno 3 giri",
            "formula": "3n",
            "dominio": "n >= 0",
            "casi": [(n, conta_interno_fisso(n)) for n in (0, 1, 4)],
        },
        {
            "chiave": "conta_dimezzamenti",
            "procedimento": "Dimezzamento while m > 1 da m = n",
            "formula": "floor(log2(n))",
            "dominio": "n >= 1 (n = 0 ha ramo con 0 giri)",
            "casi": [(n, conta_dimezzamenti(n)) for n in (1, 7, 8, 9, 20)],
        },
        {
            "chiave": "conta_raddoppiamenti",
            "procedimento": "Raddoppio while m < n da m = 1",
            "formula": "ceil(log2(n))",
            "dominio": "n >= 1 (n = 0 ha ramo con 0 giri)",
            "casi": [(n, conta_raddoppiamenti(n)) for n in (1, 7, 8, 9, 20)],
        },
        {
            "chiave": "conta_n_dimezzamenti",
            "procedimento": "n ripetizioni indipendenti del dimezzamento",
            "formula": "n * floor(log2(n))",
            "dominio": "n >= 1 (n = 0 ha ramo con 0 iterazioni)",
            "casi": [(0, conta_n_dimezzamenti(0)), (8, conta_n_dimezzamenti(8))],
        },
        {
            "chiave": "conta_visite_matrice",
            "procedimento": "Matrice rettangolare r x c",
            "formula": "r * c",
            "dominio": "r, c >= 0",
            "casi": [
                ((2, 3), conta_visite_matrice(2, 3)),
                ((3, 3), conta_visite_matrice(3, 3)),
            ],
        },
    ]


if __name__ == "__main__":
    # Le uniche stampe del modulo stanno qui: la tabella si costruisce
    # in memoria e la funzione sopra non scrive nulla.
    print("Tabella dei conteggi — corpo del ciclo, senza la guardia finale")
    for riga in tabella_dei_conteggi():
        print(f"\n{riga['procedimento']}  [{riga['formula']}]  dominio {riga['dominio']}")
        for parametri, conteggio in riga["casi"]:
            print(f"  {parametri}  ->  {conteggio}")
