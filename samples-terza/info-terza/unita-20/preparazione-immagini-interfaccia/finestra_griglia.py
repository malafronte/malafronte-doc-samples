"""Finestra Tkinter con rendering cooperativo a blocchi — Unità 20 (L6).

Il modulo implementa gli esempi preparatori del capitolo PY-41
(*Interfaccia grafica ed esplorazione reattiva*):

- il coordinatore puro `LavoroGriglia`, eseguibile a blocchi senza importare
  Tkinter: la libreria matematica offre lavoro eseguibile a blocchi, il
  coordinatore della GUI decide quando avanzare e visualizzare;
- gli stati `pronto`, `in_calcolo`, `annullato`, `completato` ed `errore`, la
  fotografia validata della configurazione acquisita all'avvio, gli
  identificatori di lavoro con invalidazione delle callback obsolete;
- la conversione e validazione dei campi di testo con messaggi che nominano
  campo, dominio ammesso e correzione;
- la conversione dalla posizione nel widget alla cella della griglia, con
  dimensioni e offset della zona dell'immagine conservati;
- la dimostrazione Tkinter (`avvia_dimostrazione`), con import pigro di
  `tkinter` dentro la funzione: l'importazione del modulo non apre finestre
  né richiede un display.

La griglia dimostrativa è artificiale e circoscritta: ogni cella riceve un
esito deterministico (`esito_artificiale`) colorato con le palette L5. Il
progetto autonomo trasferirà la tecnica ai frattali e integrerà tutti i casi
d'uso (L8).

Ambiente: CPython 3.14 sul computer con la dipendenza `pillow`. I test
`pytest` verificano il coordinatore senza aprire finestre grafiche; il
collaudo grafico è affidato allo script manuale `collaudo_gui_l6.py`.
"""

from collections.abc import Callable
from dataclasses import dataclass, field

from coordinate_esempi import valida_intero_non_booleano, valida_reale_finito
from palette_esempi import valida_limite_iterazioni

STATI_LAVORO: tuple[str, ...] = ("pronto", "in_calcolo", "annullato", "completato", "errore")

LARGHEZZA_MINIMA = 1
LARGHEZZA_MASSIMA = 800
ALTEZZA_MINIMA = 1
ALTEZZA_MASSIMA = 600
RIGHE_PER_BLOCCO_MINIME = 1
RIGHE_PER_BLOCCO_MASSIME = 600


@dataclass(frozen=True)
class ConfigurazioneGriglia:
    """Fotografia validata dei parametri di una griglia dimostrativa.

    La configurazione si acquisisce all'avvio del lavoro e resta invariata
    fino alla conclusione: i campi della finestra possono cambiare per il
    lavoro successivo senza alterare il lavoro in corso.
    """

    larghezza: int
    altezza: int
    righe_per_blocco: int
    limite_etichetta: int


@dataclass
class LavoroGriglia:
    """Stato mutabile di un rendering cooperativo con identificatore.

    Il campo `id_lavoro` distingue i lavori successivi: una callback che
    presenta un identificatore diverso da quello corrente viene ignorata,
    così annullamento e nuovo avvio non lasciano callback obsolete con
    effetti sul risultato.
    """

    configurazione: ConfigurazioneGriglia
    id_lavoro: int
    stato: str = "pronto"
    righe_completate: int = 0
    righe: list[tuple[int | None, ...]] = field(default_factory=list)
    errore: str | None = None


def nuova_configurazione(
    larghezza: object,
    altezza: object,
    righe_per_blocco: object,
    limite_etichetta: object = 7,
) -> ConfigurazioneGriglia:
    """Costruisce e valida la fotografia dei parametri della griglia."""
    w = valida_intero_non_booleano(larghezza, "larghezza")
    h = valida_intero_non_booleano(altezza, "altezza")
    blocco = valida_intero_non_booleano(righe_per_blocco, "righe_per_blocco")
    n_max = valida_limite_iterazioni(limite_etichetta)
    if not (LARGHEZZA_MINIMA <= w <= LARGHEZZA_MASSIMA):
        raise ValueError(
            f"Il parametro 'larghezza' richiede un valore in "
            f"{LARGHEZZA_MINIMA}..{LARGHEZZA_MASSIMA}."
        )
    if not (ALTEZZA_MINIMA <= h <= ALTEZZA_MASSIMA):
        raise ValueError(
            f"Il parametro 'altezza' richiede un valore in {ALTEZZA_MINIMA}..{ALTEZZA_MASSIMA}."
        )
    if not (RIGHE_PER_BLOCCO_MINIME <= blocco <= RIGHE_PER_BLOCCO_MASSIME):
        raise ValueError(
            f"Il parametro 'righe_per_blocco' richiede un valore in "
            f"{RIGHE_PER_BLOCCO_MINIME}..{RIGHE_PER_BLOCCO_MASSIME}."
        )
    return ConfigurazioneGriglia(
        larghezza=w, altezza=h, righe_per_blocco=blocco, limite_etichetta=n_max
    )


def valida_id_lavoro(valore: object) -> int:
    """Verifica che `valore` sia un identificatore di lavoro intero non booleano."""
    if isinstance(valore, bool) or not isinstance(valore, int):
        raise TypeError("Il parametro 'id_lavoro' richiede un intero non booleano.")
    return valore


def nuovo_lavoro(configurazione: ConfigurazioneGriglia, id_lavoro: object) -> LavoroGriglia:
    """Crea un lavoro in stato `pronto` con la fotografia acquisita."""
    if not isinstance(configurazione, ConfigurazioneGriglia):
        raise TypeError("Il parametro 'configurazione' richiede una ConfigurazioneGriglia.")
    return LavoroGriglia(configurazione=configurazione, id_lavoro=valida_id_lavoro(id_lavoro))


def avvia_lavoro(lavoro: LavoroGriglia) -> None:
    """Porta il lavoro in stato `in_calcolo`, azzerando righe ed errore."""
    if not isinstance(lavoro, LavoroGriglia):
        raise TypeError("Il parametro 'lavoro' richiede un LavoroGriglia.")
    lavoro.stato = "in_calcolo"
    lavoro.righe_completate = 0
    lavoro.righe = []
    lavoro.errore = None


def annulla_lavoro(lavoro: LavoroGriglia) -> bool:
    """Annulla un lavoro in calcolo, conservando il risultato parziale.

    Restituisce `True` se il lavoro era in calcolo e passa ad `annullato`;
    in ogni altro stato restituisce `False` senza modificare il lavoro.
    """
    if not isinstance(lavoro, LavoroGriglia):
        raise TypeError("Il parametro 'lavoro' richiede un LavoroGriglia.")
    if lavoro.stato != "in_calcolo":
        return False
    lavoro.stato = "annullato"
    return True


def esegui_blocco(
    lavoro: LavoroGriglia,
    id_atteso: object,
    calcola_riga: Callable[[int], tuple[int | None, ...]],
) -> bool:
    """Esegue un blocco di righe se lavoro e identificatore sono correnti.

    La callback non applica alcun effetto quando l'identificatore presentato
    differisce da quello del lavoro (callback di un lavoro precedente) oppure
    quando lo stato non è `in_calcolo` (annullato, completato, errore o
    finestra chiusa). Un'eccezione di `calcola_riga` porta il lavoro in stato
    `errore` con il messaggio conservato. Restituisce `True` se il blocco ha
    prodotto righe, `False` se è stato ignorato o ha registrato un errore.
    """
    if not isinstance(lavoro, LavoroGriglia):
        raise TypeError("Il parametro 'lavoro' richiede un LavoroGriglia.")
    id_corrente = valida_id_lavoro(id_atteso)
    if id_corrente != lavoro.id_lavoro or lavoro.stato != "in_calcolo":
        return False
    if not callable(calcola_riga):
        raise TypeError("Il parametro 'calcola_riga' richiede una funzione chiamabile.")
    configurazione = lavoro.configurazione
    ultima = min(lavoro.righe_completate + configurazione.righe_per_blocco, configurazione.altezza)
    try:
        for q in range(lavoro.righe_completate, ultima):
            riga = calcola_riga(q)
            if not isinstance(riga, (tuple, list)) or len(riga) != configurazione.larghezza:
                raise ValueError(f"La riga {q} richiede {configurazione.larghezza} esiti.")
            for p, esito in enumerate(riga):
                if esito is not None and (
                    isinstance(esito, bool) or not isinstance(esito, int) or esito < 0
                ):
                    raise TypeError(f"L'esito ({p}, {q}) richiede un intero >= 0 oppure None.")
            lavoro.righe.append(tuple(riga))
        lavoro.righe_completate = ultima
    except Exception as causa:  # noqa: BLE001 - il messaggio di dominio si conserva nel lavoro
        lavoro.stato = "errore"
        lavoro.errore = str(causa)
        return False
    if lavoro.righe_completate >= configurazione.altezza:
        lavoro.stato = "completato"
    return True


def frazione_completata(lavoro: LavoroGriglia) -> float:
    """Restituisce la frazione di righe completate in `[0.0, 1.0]`."""
    if not isinstance(lavoro, LavoroGriglia):
        raise TypeError("Il parametro 'lavoro' richiede un LavoroGriglia.")
    return lavoro.righe_completate / lavoro.configurazione.altezza


def etichetta_progresso(lavoro: LavoroGriglia) -> str:
    """Restituisce il testo del progresso con righe, percentuale e stato."""
    if not isinstance(lavoro, LavoroGriglia):
        raise TypeError("Il parametro 'lavoro' richiede un LavoroGriglia.")
    altezza = lavoro.configurazione.altezza
    percentuale = round(100.0 * lavoro.righe_completate / altezza)
    return (
        f"Riga {lavoro.righe_completate} di {altezza} — {percentuale}% "
        f"(lavoro {lavoro.id_lavoro}, {lavoro.stato})"
    )


def etichetta_risultato(lavoro: LavoroGriglia) -> str:
    """Dichiara se il risultato è completo, parziale o assente.

    Il progresso per righe non misura la frazione esatta delle operazioni,
    perché le celle richiedono quantità diverse di aggiornamenti; un
    risultato parziale resta etichettato come tale e l'esportazione ordinaria
    riguarda soltanto l'ultimo risultato completo.
    """
    if not isinstance(lavoro, LavoroGriglia):
        raise TypeError("Il parametro 'lavoro' richiede un LavoroGriglia.")
    if lavoro.stato == "completato":
        return f"Risultato completo del lavoro {lavoro.id_lavoro}."
    if lavoro.stato == "in_calcolo":
        return f"Risultato parziale del lavoro {lavoro.id_lavoro}: calcolo in corso."
    if lavoro.stato == "annullato":
        return f"Risultato parziale del lavoro {lavoro.id_lavoro}: calcolo annullato."
    if lavoro.stato == "errore":
        return f"Nessun risultato utilizzabile: errore nel lavoro {lavoro.id_lavoro}."
    return "Nessun risultato: lavoro non avviato."


def risultato_completo(lavoro: LavoroGriglia) -> bool:
    """Indica se il lavoro è completato e quindi esportabile."""
    if not isinstance(lavoro, LavoroGriglia):
        raise TypeError("Il parametro 'lavoro' richiede un LavoroGriglia.")
    return lavoro.stato == "completato"


def riepilogo_configurazione(configurazione: ConfigurazioneGriglia) -> str:
    """Restituisce il riepilogo testuale di una configurazione."""
    if not isinstance(configurazione, ConfigurazioneGriglia):
        raise TypeError("Il parametro 'configurazione' richiede una ConfigurazioneGriglia.")
    return (
        f"{configurazione.larghezza}x{configurazione.altezza}, "
        f"blocco di {configurazione.righe_per_blocco} righe, "
        f"etichetta N={configurazione.limite_etichetta}"
    )


def esito_artificiale(colonna_p: int, riga_q: int, limite: int) -> int | None:
    """Restituisce l'esito dimostrativo della cella `(p, q)` in `0..limite` o `None`.

    La funzione è deterministica e mescola esiti interni (`None` quando
    `(p + q)` è multiplo di `7`) e indici di fuga, incluso lo `0`: non
    descrive alcun frattale e serve soltanto a esercitare coordinamento,
    colorazione e annullamento su un dominio circoscritto.
    """
    if not isinstance(colonna_p, int) or not isinstance(riga_q, int):
        raise TypeError("Gli indici di cella richiedono interi.")
    n_max = valida_limite_iterazioni(limite)
    if (colonna_p + riga_q) % 7 == 0:
        return None
    return (colonna_p * 3 + riga_q) % (n_max + 1)


def converti_campo_intero(
    testo: object, nome_campo: object, minimo: object, massimo: object
) -> int:
    """Converte il testo di un campo in intero validato nell'intervallo.

    I dati digitati sono stringhe: lettura, conversione e validazione
    precedono la costruzione della configurazione. Il messaggio di errore
    identifica campo, dominio ammesso e correzione.
    """
    if not isinstance(nome_campo, str) or not nome_campo:
        raise TypeError("Il parametro 'nome_campo' richiede una stringa non vuota.")
    minimo_intero = valida_intero_non_booleano(minimo, "minimo")
    massimo_intero = valida_intero_non_booleano(massimo, "massimo")
    if minimo_intero > massimo_intero:
        raise ValueError("Il parametro 'minimo' non può superare 'massimo'.")
    if not isinstance(testo, str):
        raise TypeError(
            f"Il campo '{nome_campo}' richiede una stringa; "
            f"correggere con un intero fra {minimo_intero} e {massimo_intero}."
        )
    try:
        valore = int(testo.strip(), 10)
    except ValueError:
        raise ValueError(
            f"Il campo '{nome_campo}' richiede un intero fra {minimo_intero} "
            f"e {massimo_intero}; ricevuto '{testo}'. "
            f"Correggere con un numero intero nell'intervallo."
        ) from None
    if not (minimo_intero <= valore <= massimo_intero):
        raise ValueError(
            f"Il campo '{nome_campo}' richiede un intero fra {minimo_intero} "
            f"e {massimo_intero}; ricevuto '{testo}'. "
            f"Correggere con un numero intero nell'intervallo."
        )
    return valore


def posizione_widget_a_cella(
    x_widget: object,
    y_widget: object,
    offset_x: object,
    offset_y: object,
    scala_anteprima: object,
    larghezza: object,
    altezza: object,
) -> tuple[int, int] | None:
    """Converte la posizione nel widget nella cella `(p, q)` o `None` se esterna.

    La conversione attraversa due passi dichiarati: dalla posizione nel
    widget alla posizione nell'immagine (sottrazione dell'offset e divisione
    per la scala dell'anteprima), poi dall'immagine alla cella (parte intera,
    con controllo dei bordi). Le prove su centri e bordi identificano errori
    di traslazione, scala o inversione.
    """
    x = valida_reale_finito(x_widget, "x_widget")
    y = valida_reale_finito(y_widget, "y_widget")
    ox = valida_reale_finito(offset_x, "offset_x")
    oy = valida_reale_finito(offset_y, "offset_y")
    scala = valida_intero_non_booleano(scala_anteprima, "scala_anteprima", minimo=1)
    w = valida_intero_non_booleano(larghezza, "larghezza", minimo=1)
    h = valida_intero_non_booleano(altezza, "altezza", minimo=1)
    p = int((x - ox) // scala)
    q = int((y - oy) // scala)
    if 0 <= p < w and 0 <= q < h:
        return (p, q)
    return None


def avvia_dimostrazione(*, avvia_ciclo: bool = True):
    """Apre la finestra dimostrativa con griglia colorata annullabile.

    L'importazione di `tkinter` avviene dentro la funzione, così
    l'importazione del modulo non apre finestre né richiede un display. La
    finestra contiene campi validati, comandi Genera e Annulla, zoom
    dell'anteprima con ripristino, canvas con zona dell'immagine a dimensioni
    e offset conservati, avanzamento, messaggi e salvataggio del risultato
    completo. La chiusura durante il calcolo invalida il lavoro e impedisce
    aggiornamenti su widget distrutti.

    Con `avvia_ciclo=False` la funzione restituisce la dimostrazione senza
    avviare il ciclo degli eventi, per il collaudo guidato dello script
    `collaudo_gui_l6.py`.
    """
    import tkinter as tk
    from tkinter import filedialog, ttk

    from PIL import Image, ImageTk

    from palette_esempi import colora_esito

    ZONA_ANTEPRIMA = (320, 240)
    OFFSET_IMMAGINE = (8, 8)
    SCALE_ANTEPRIMA = (1, 2, 4)

    class DimostrazioneGriglia:
        """Finestra dimostrativa con rendering cooperativo tramite `after`."""

        def __init__(self, radice: tk.Tk) -> None:
            self.radice = radice
            self.radice.title("PY-41 — Griglia colorata annullabile")
            self.contatore_lavori = 0
            self.lavoro_corrente = nuovo_lavoro(nuova_configurazione(160, 120, 8, 7), 0)
            self.id_after: str | None = None
            self.finestra_valida = True
            self.scala_anteprima = 1
            self.immagine_calcolata: Image.Image | None = None
            self.anteprima: Image.Image | None = None
            self.riferimento_photo: ImageTk.PhotoImage | None = None
            self.durata_massima_blocco_ms = 0.0
            self._costruisci_widget()
            self.radice.protocol("WM_DELETE_WINDOW", self.chiudi)

        def _costruisci_widget(self) -> None:
            cornice = ttk.Frame(self.radice, padding=8)
            cornice.grid(row=0, column=0, sticky="nsew")
            self.radice.columnconfigure(0, weight=1)
            self.radice.rowconfigure(0, weight=1)

            ttk.Label(cornice, text="Larghezza (1..800):").grid(row=0, column=0, sticky="w")
            self.campo_larghezza = ttk.Entry(cornice, width=8)
            self.campo_larghezza.insert(0, "160")
            self.campo_larghezza.grid(row=0, column=1, sticky="w")

            ttk.Label(cornice, text="Altezza (1..600):").grid(row=1, column=0, sticky="w")
            self.campo_altezza = ttk.Entry(cornice, width=8)
            self.campo_altezza.insert(0, "120")
            self.campo_altezza.grid(row=1, column=1, sticky="w")

            ttk.Label(cornice, text="Righe per blocco (1..600):").grid(row=2, column=0, sticky="w")
            self.campo_blocco = ttk.Entry(cornice, width=8)
            self.campo_blocco.insert(0, "8")
            self.campo_blocco.grid(row=2, column=1, sticky="w")

            self.pulsante_genera = ttk.Button(cornice, text="Genera", command=self.genera)
            self.pulsante_genera.grid(row=3, column=0, sticky="ew", pady=4)
            self.pulsante_annulla = ttk.Button(cornice, text="Annulla", command=self.annulla)
            self.pulsante_annulla.grid(row=3, column=1, sticky="ew", pady=4)
            self.pulsante_zoom_avanti = ttk.Button(
                cornice, text="Zoom anteprima +", command=lambda: self.cambia_zoom(1)
            )
            self.pulsante_zoom_avanti.grid(row=4, column=0, sticky="ew")
            self.pulsante_zoom_indietro = ttk.Button(
                cornice, text="Zoom anteprima −", command=lambda: self.cambia_zoom(-1)
            )
            self.pulsante_zoom_indietro.grid(row=4, column=1, sticky="ew")
            self.pulsante_ripristina = ttk.Button(
                cornice, text="Ripristina anteprima", command=self.ripristina_anteprima
            )
            self.pulsante_ripristina.grid(row=5, column=0, columnspan=2, sticky="ew")
            self.pulsante_salva = ttk.Button(
                cornice, text="Salva PNG", command=self.salva_png, state="disabled"
            )
            self.pulsante_salva.grid(row=6, column=0, columnspan=2, sticky="ew")

            self.etichetta_stato = ttk.Label(cornice, text="Pronta: premere Genera.")
            self.etichetta_stato.grid(row=7, column=0, columnspan=2, sticky="w")
            self.etichetta_cella = ttk.Label(cornice, text="Cella: —")
            self.etichetta_cella.grid(row=8, column=0, columnspan=2, sticky="w")
            self.etichetta_messaggio = ttk.Label(cornice, text="", foreground="red")
            self.etichetta_messaggio.grid(row=9, column=0, columnspan=2, sticky="w")

            self.tela = tk.Canvas(
                cornice, width=ZONA_ANTEPRIMA[0], height=ZONA_ANTEPRIMA[1], bg="white"
            )
            self.tela.grid(row=0, column=2, rowspan=10, padx=(12, 0))
            self.tela.bind("<Button-1>", self.al_clic)
            self.id_immagine = self.tela.create_image(
                OFFSET_IMMAGINE[0], OFFSET_IMMAGINE[1], anchor="nw"
            )
            self.radice.bind("<Escape>", lambda _evento: self.annulla())
            self.pulsante_genera.focus_set()

        def _leggi_configurazione(self) -> ConfigurazioneGriglia | None:
            try:
                larghezza = converti_campo_intero(self.campo_larghezza.get(), "larghezza", 1, 800)
                altezza = converti_campo_intero(self.campo_altezza.get(), "altezza", 1, 600)
                blocco = converti_campo_intero(self.campo_blocco.get(), "righe per blocco", 1, 600)
                configurazione = nuova_configurazione(larghezza, altezza, blocco, 7)
            except (TypeError, ValueError) as causa:
                self.etichetta_messaggio.config(text=str(causa))
                return None
            self.etichetta_messaggio.config(text="")
            return configurazione

        def genera(self) -> None:
            """Avvia un nuovo lavoro con fotografia dei campi e invalida il precedente."""
            configurazione = self._leggi_configurazione()
            if configurazione is None:
                return
            self._cancella_callback_pendente()
            annulla_lavoro(self.lavoro_corrente)
            self.contatore_lavori += 1
            self.lavoro_corrente = nuovo_lavoro(configurazione, self.contatore_lavori)
            avvia_lavoro(self.lavoro_corrente)
            self.immagine_calcolata = Image.new(
                "RGB", (configurazione.larghezza, configurazione.altezza)
            )
            self.durata_massima_blocco_ms = 0.0
            self._imposta_campi_abilitati(False)
            self.pulsante_salva.config(state="disabled")
            self._programma_prossimo_blocco()

        def annulla(self) -> None:
            """Annulla il lavoro in corso; le callback obsolete restano senza effetti."""
            if annulla_lavoro(self.lavoro_corrente):
                self._cancella_callback_pendente()
                self._imposta_campi_abilitati(True)
                self.etichetta_stato.config(
                    text=etichetta_progresso(self.lavoro_corrente)
                    + " — "
                    + etichetta_risultato(self.lavoro_corrente)
                )

        def cambia_zoom(self, passo: int) -> None:
            """Varia la scala dell'anteprima senza ricalcolare l'immagine."""
            posizione = SCALE_ANTEPRIMA.index(self.scala_anteprima)
            nuova_posizione = min(max(posizione + passo, 0), len(SCALE_ANTEPRIMA) - 1)
            self.scala_anteprima = SCALE_ANTEPRIMA[nuova_posizione]
            self._ridisegna_anteprima()

        def ripristina_anteprima(self) -> None:
            """Riporta la scala dell'anteprima al valore iniziale."""
            self.scala_anteprima = 1
            self._ridisegna_anteprima()

        def salva_png(self) -> None:
            """Esporta l'ultimo risultato completo; rifiuta i risultati parziali."""
            if not risultato_completo(self.lavoro_corrente):
                self.etichetta_messaggio.config(
                    text="Esportazione non disponibile: "
                    + etichetta_risultato(self.lavoro_corrente)
                )
                return
            percorso = filedialog.asksaveasfilename(
                title="Esporta PNG del risultato completo",
                defaultextension=".png",
                filetypes=[("PNG", "*.png")],
            )
            if percorso and self.immagine_calcolata is not None:
                self.immagine_calcolata.save(percorso, format="PNG")

        def al_clic(self, evento: tk.Event) -> None:  # type: ignore[type-arg]
            """Mostra la cella corrispondente alla posizione del clic."""
            configurazione = self.lavoro_corrente.configurazione
            cella = posizione_widget_a_cella(
                float(evento.x),
                float(evento.y),
                float(OFFSET_IMMAGINE[0]),
                float(OFFSET_IMMAGINE[1]),
                self.scala_anteprima,
                configurazione.larghezza,
                configurazione.altezza,
            )
            if cella is None:
                self.etichetta_cella.config(text="Cella: fuori dall'immagine")
            else:
                self.etichetta_cella.config(text=f"Cella: colonna {cella[0]}, riga {cella[1]}")

        def chiudi(self) -> None:
            """Invalida il lavoro, cancella la callback pendente e distrugge la finestra."""
            annulla_lavoro(self.lavoro_corrente)
            self._cancella_callback_pendente()
            self.finestra_valida = False
            self.radice.destroy()

        def _imposta_campi_abilitati(self, abilitati: bool) -> None:
            stato = "normal" if abilitati else "disabled"
            self.campo_larghezza.config(state=stato)
            self.campo_altezza.config(state=stato)
            self.campo_blocco.config(state=stato)

        def _cancella_callback_pendente(self) -> None:
            if self.id_after is not None:
                try:
                    self.radice.after_cancel(self.id_after)
                except tk.TclError:
                    pass
                self.id_after = None

        def _programma_prossimo_blocco(self) -> None:
            if self.finestra_valida:
                self.id_after = self.radice.after(10, self._corpo_blocco)

        def _corpo_blocco(self) -> None:
            """Esegue un blocco con fotografia e identificatore, poi riprogramma.

            L'identificatore si fotografa alla programmazione: se nel frattempo
            è partito un nuovo lavoro o la finestra è stata chiusa, la callback
            non applica alcun effetto.
            """
            import time

            self.id_after = None
            id_fotografato = self.lavoro_corrente.id_lavoro
            configurazione = self.lavoro_corrente.configurazione
            limite = configurazione.limite_etichetta

            def calcola_riga(q: int) -> tuple[int | None, ...]:
                return tuple(
                    esito_artificiale(p, q, limite) for p in range(configurazione.larghezza)
                )

            inizio = time.perf_counter()
            avanzato = esegui_blocco(self.lavoro_corrente, id_fotografato, calcola_riga)
            durata_ms = (time.perf_counter() - inizio) * 1000.0
            if not avanzato or not self.finestra_valida:
                return
            self.durata_massima_blocco_ms = max(self.durata_massima_blocco_ms, durata_ms)
            self._aggiorna_immagine_parziale()
            self._ridisegna_anteprima()
            testo = etichetta_progresso(self.lavoro_corrente)
            testo += f" — blocco {durata_ms:.1f} ms (max {self.durata_massima_blocco_ms:.1f} ms)"
            if risultato_completo(self.lavoro_corrente):
                self._imposta_campi_abilitati(True)
                self.pulsante_salva.config(state="normal")
                testo += " — " + etichetta_risultato(self.lavoro_corrente)
            self.etichetta_stato.config(text=testo)
            if self.lavoro_corrente.stato == "in_calcolo":
                self._programma_prossimo_blocco()

        def _aggiorna_immagine_parziale(self) -> None:
            assert self.immagine_calcolata is not None
            lavoro = self.lavoro_corrente
            limite = lavoro.configurazione.limite_etichetta
            for q in range(len(lavoro.righe)):
                for p, esito in enumerate(lavoro.righe[q]):
                    self.immagine_calcolata.putpixel((p, q), colora_esito(esito, limite))

        def _ridisegna_anteprima(self) -> None:
            if self.immagine_calcolata is None:
                return
            w, h = self.immagine_calcolata.size
            self.anteprima = self.immagine_calcolata.resize(
                (w * self.scala_anteprima, h * self.scala_anteprima), Image.NEAREST
            )
            self.riferimento_photo = ImageTk.PhotoImage(self.anteprima, master=self.radice)
            if self.finestra_valida:
                self.tela.itemconfig(self.id_immagine, image=self.riferimento_photo)

    radice = tk.Tk()
    dimostrazione = DimostrazioneGriglia(radice)
    if avvia_ciclo:
        dimostrazione.radice.mainloop()
    return dimostrazione


if __name__ == "__main__":
    avvia_dimostrazione()
