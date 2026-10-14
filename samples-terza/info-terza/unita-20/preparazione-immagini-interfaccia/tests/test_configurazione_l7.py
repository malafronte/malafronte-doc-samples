"""Verifica del modello a componenti, della persistenza e dei costi — Unità 20 (L7).

La suite verifica `configurazione_esempio.py` senza aprire finestre
grafiche e senza creare immagini:

- l'importazione non carica né `tkinter` né `PIL` (sottoprocesso fresco);
- oggetti di valore con validazione, rifiuto di booleani e non finiti;
- classificatori di Mandelbrot e Julia contro i casi canonici
  discriminanti (budget finito, fuga all'indice `0`, raggio sicuro);
- produttori di Koch e Sierpiński con vertici, conteggi e centrale escluso;
- sostituibilità di classificatori, produttori e colorazioni attraverso
  i contratti (`Protocol`);
- round-trip delle quattro famiglie e accordo degli esiti dopo il
  caricamento;
- documenti invalidi con eccezioni dedicate, inclusi booleani nei campi
  interi e costanti non finite nel testo JSON;
- salvataggio atomico con file precedente preservato e caricamento
  fallito senza perdita della configurazione corrente;
- costi dichiarati contro i contatori implementati e accordo con le
  statistiche del modulo `griglia_pillow`.
"""

import json
import math
import subprocess
import sys
from pathlib import Path

import pytest

from configurazione_esempio import (
    ArchivioConfigurazioni,
    ClassificatoreJulia,
    ClassificatoreMandelbrot,
    ColorazioneBande,
    ColorazioneBinaria,
    ColorazioneGradiente,
    ConfigurazioneFrattale,
    ErroreConfigurazione,
    LimiteOperativoSuperato,
    ParametriImmagine,
    ParametriJulia,
    ParametriKoch,
    ParametriMandelbrot,
    ParametriSierpinski,
    ProduttoreKoch,
    ProduttoreSierpinski,
    TipoNonSupportato,
    VersioneNonSupportata,
    VistaComplessa,
    classifica_punti,
    colora_riga_esiti,
    complesso_a_oggetto,
    elementi_geometrici,
    lavoro_effettivo_da_matrice,
    misura_classificazione,
    oggetto_a_complesso,
    stima_budget_aggiornamenti,
)
from palette_esempi import colora_esito


def test_import_senza_tkinter_e_pil_nel_processo_fresco() -> None:
    processo = subprocess.run(
        [
            sys.executable,
            "-c",
            "import configurazione_esempio, sys; "
            "print('tkinter' in sys.modules, 'PIL' in sys.modules)",
        ],
        cwd=Path(__file__).resolve().parent.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    assert processo.returncode == 0, processo.stderr
    assert processo.stdout.strip() == "False False"


def test_sorgente_senza_import_grafici() -> None:
    sorgente = (
        Path(__file__)
        .resolve()
        .parent.parent.joinpath("configurazione_esempio.py")
        .read_text(encoding="utf-8")
    )
    assert "import tkinter" not in sorgente
    assert "import PIL" not in sorgente and "from PIL" not in sorgente


def test_vista_valida_e_rifiuto_dei_fuori_dominio() -> None:
    vista = VistaComplessa(centro_reale=-0.5, centro_immaginaria=0.0, ampiezza_orizzontale=3.5)
    assert vista.centro_reale == -0.5
    with pytest.raises(ErroreConfigurazione, match="ampiezza_orizzontale"):
        VistaComplessa(centro_reale=0.0, centro_immaginaria=0.0, ampiezza_orizzontale=0.0)
    with pytest.raises(ErroreConfigurazione, match="centro_reale"):
        VistaComplessa(centro_reale=200.0, centro_immaginaria=0.0, ampiezza_orizzontale=3.5)
    with pytest.raises(ValueError, match="NaN o infinito"):
        VistaComplessa(centro_reale=math.nan, centro_immaginaria=0.0, ampiezza_orizzontale=3.5)
    with pytest.raises(TypeError):
        VistaComplessa(centro_reale=True, centro_immaginaria=0.0, ampiezza_orizzontale=3.5)


def test_parametri_rifiutano_bool_e_limiti() -> None:
    with pytest.raises(TypeError):
        ParametriKoch(livello=True, variante="curva", lato_iniziale=3.0)
    with pytest.raises(LimiteOperativoSuperato, match="Livello di Koch"):
        ProduttoreKoch(livello=7, variante="curva", lato_iniziale=3.0)
    with pytest.raises(LimiteOperativoSuperato, match="Sierpi"):
        ProduttoreSierpinski(livello=8, stile="pieno", lato_iniziale=4.0)
    with pytest.raises(TipoNonSupportato):
        ParametriKoch(livello=1, variante="albero", lato_iniziale=3.0)
    with pytest.raises(LimiteOperativoSuperato):
        ParametriJulia(limite_iterazioni=100, c_reale=20.0, c_immaginaria=0.0)
    with pytest.raises(TypeError):
        ClassificatoreJulia(limite_iterazioni=100, c="non-complesso")


def test_classificatore_mandelbrot_casi_discriminanti() -> None:
    due = ClassificatoreMandelbrot(limite_iterazioni=2)
    tre = ClassificatoreMandelbrot(limite_iterazioni=3)
    # c = 1: con N = 2 vale |z_2| = 2 senza fuga; con N = 3 fuga all'indice 3
    assert due.classifica(complex(1.0, 0.0)) is None
    assert tre.classifica(complex(1.0, 0.0)) == 3
    # c = -2: soglia stretta, |z| = 2 non è fuga
    dieci = ClassificatoreMandelbrot(limite_iterazioni=10)
    assert dieci.classifica(complex(-2.0, 0.0)) is None
    assert dieci.classifica(complex(0.0, 0.0)) is None
    # c = 3: fuga immediata già sul seme all'indice 1 (|3| > 2 dopo un passo? no:
    # il controllo iniziale su z_0 = 0 non fugge, z_1 = 3 fugge all'indice 1)
    assert dieci.classifica(complex(3.0, 0.0)) == 1
    with pytest.raises(TypeError):
        dieci.classifica("non-complesso")


def test_classificatore_julia_raggio_sicuro() -> None:
    julia_zero = ClassificatoreJulia(limite_iterazioni=10, c=complex(0.0, 0.0))
    assert julia_zero.classifica(complex(1.0, 0.0)) is None
    # z_0 = 3 con c = 0 fugge subito all'indice 0
    assert julia_zero.classifica(complex(3.0, 0.0)) == 0
    # z_0 = 3 con c = -6 è punto fisso con raggio 6: nessuna fuga rilevata
    julia_meno_sei = ClassificatoreJulia(limite_iterazioni=10, c=complex(-6.0, 0.0))
    assert julia_meno_sei.classifica(complex(3.0, 0.0)) is None


def test_classificatori_sostituibili_sugli_stessi_punti() -> None:
    punti = (complex(0.0, 0.0), complex(1.0, 0.0), complex(3.0, 0.0))
    mandelbrot = ClassificatoreMandelbrot(limite_iterazioni=3)
    julia = ClassificatoreJulia(limite_iterazioni=3, c=complex(0.0, 0.0))
    esiti_mandelbrot = classifica_punti(mandelbrot, punti)
    esiti_julia = classifica_punti(julia, punti)
    # Stesso contratto, famiglie diverse: con c = 3 Mandelbrot fugge al
    # passo 1, mentre con c = 0 Julia considera 0 e 1 punti interni
    assert esiti_mandelbrot == (None, 3, 1)
    assert esiti_julia == (None, None, 0)
    with pytest.raises(TypeError, match="ClassificatoreQuadratico"):
        classifica_punti("non-classificatore", punti)


def test_produttore_koch_curva_livello_0_e_1() -> None:
    base = ProduttoreKoch(livello=0, variante="curva", lato_iniziale=3.0)
    assert base.conta_elementi() == 1
    assert elementi_geometrici(base) == (((0.0, 0.0), (3.0, 0.0)),)
    primo = ProduttoreKoch(livello=1, variante="curva", lato_iniziale=3.0)
    assert primo.conta_elementi() == 4
    radice_3_mezzi = math.sqrt(3.0) / 2.0
    assert elementi_geometrici(primo) == (
        ((0.0, 0.0), (1.0, 0.0)),
        ((1.0, 0.0), (1.5, radice_3_mezzi)),
        ((1.5, radice_3_mezzi), (2.0, 0.0)),
        ((2.0, 0.0), (3.0, 0.0)),
    )
    assert ProduttoreKoch(livello=2, variante="curva").conta_elementi() == 16
    assert ProduttoreKoch(livello=1, variante="fiocco").conta_elementi() == 12


def test_produttore_sierpinski_livello_0_e_1_con_centrale_escluso() -> None:
    base = ProduttoreSierpinski(livello=0, stile="pieno", lato_iniziale=4.0)
    assert base.conta_elementi() == 1
    radice_3 = math.sqrt(3.0)
    assert elementi_geometrici(base) == (((0.0, 0.0), (4.0, 0.0), (2.0, 2.0 * radice_3)),)
    primo = ProduttoreSierpinski(livello=1, stile="pieno", lato_iniziale=4.0)
    assert primo.conta_elementi() == 3
    triangoli = elementi_geometrici(primo)
    assert triangoli == (
        ((0.0, 0.0), (2.0, 0.0), (1.0, radice_3)),
        ((2.0, 0.0), (4.0, 0.0), (3.0, radice_3)),
        ((1.0, radice_3), (3.0, radice_3), (2.0, 2.0 * radice_3)),
    )
    # Il triangolo centrale ((2,0),(3,√3),(1,√3)) è escluso dai tre d'angolo
    centrale = ((2.0, 0.0), (3.0, radice_3), (1.0, radice_3))
    assert centrale not in triangoli
    assert ProduttoreSierpinski(livello=2, stile="contorno").conta_elementi() == 9
    with pytest.raises(TypeError, match="ProduttoreGeometrico"):
        elementi_geometrici("non-produttore")


def test_colorazioni_sostituibili_con_none_e_zero_distinti() -> None:
    riga = (None, 0, 1, 2)
    for colorazione in (
        ColorazioneBinaria(),
        ColorazioneBande(),
        ColorazioneGradiente(),
    ):
        colori = colora_riga_esiti(colorazione, riga, 6)
        assert len(colori) == 4
        # `None` e `0` ricevono colori diversi in ogni strategia
        assert colori[0] != colori[1]
        assert colori == tuple(colora_esito(esito, 6, colorazione.nome) for esito in riga)
    # La stessa matrice cambia veste senza ricalcolare gli esiti
    assert colora_riga_esiti(ColorazioneBinaria(), riga, 6) != colora_riga_esiti(
        ColorazioneBande(), riga, 6
    )
    with pytest.raises(TypeError, match="Colorazione"):
        colora_riga_esiti("non-colorazione", riga, 6)


def test_complesso_oggetto_round_trip_e_rifiuti() -> None:
    oggetto = complesso_a_oggetto(complex(-0.8, 0.156))
    assert oggetto == {"reale": -0.8, "immaginaria": 0.156}
    assert oggetto_a_complesso(oggetto, "parametri.c", -10.0, 10.0) == complex(-0.8, 0.156)
    with pytest.raises(TypeError):
        oggetto_a_complesso([1.0, 2.0], "parametri.c", -10.0, 10.0)
    with pytest.raises(ValueError, match="esattamente"):
        oggetto_a_complesso({"reale": 1.0}, "parametri.c", -10.0, 10.0)
    with pytest.raises(ErroreConfigurazione, match="\\[-10.0, 10.0\\]"):
        oggetto_a_complesso({"reale": 20.0, "immaginaria": 0.0}, "parametri.c", -10.0, 10.0)
    with pytest.raises(ValueError, match="NaN o infin"):
        complesso_a_oggetto(complex(math.nan, 0.0))


def _configurazioni_quattro_famiglie() -> dict[str, ConfigurazioneFrattale]:
    vista_mandelbrot = VistaComplessa(
        centro_reale=-0.5, centro_immaginaria=0.0, ampiezza_orizzontale=3.5
    )
    vista_julia = VistaComplessa(centro_reale=0.0, centro_immaginaria=0.0, ampiezza_orizzontale=3.5)
    vista_geom = VistaComplessa(
        centro_reale=1.5, centro_immaginaria=0.8660254037844386, ampiezza_orizzontale=4.0
    )
    piccola = ParametriImmagine(larghezza=8, altezza=6, palette="bande")
    return {
        "mandelbrot": ConfigurazioneFrattale(
            tipo_frattale="mandelbrot",
            vista=vista_mandelbrot,
            immagine=piccola,
            parametri=ParametriMandelbrot(limite_iterazioni=10),
        ),
        "julia": ConfigurazioneFrattale(
            tipo_frattale="julia",
            vista=vista_julia,
            immagine=piccola,
            parametri=ParametriJulia(limite_iterazioni=10, c_reale=-0.8, c_immaginaria=0.156),
        ),
        "koch": ConfigurazioneFrattale(
            tipo_frattale="koch",
            vista=vista_geom,
            immagine=ParametriImmagine(larghezza=8, altezza=6, palette="binaria"),
            parametri=ParametriKoch(livello=1, variante="curva", lato_iniziale=3.0),
        ),
        "sierpinski": ConfigurazioneFrattale(
            tipo_frattale="sierpinski",
            vista=vista_geom,
            immagine=ParametriImmagine(larghezza=8, altezza=6, palette="binaria"),
            parametri=ParametriSierpinski(livello=1, stile="pieno", lato_iniziale=4.0),
        ),
    }


def test_round_trip_quattro_famiglie_con_esiti_conservati() -> None:
    archivio = ArchivioConfigurazioni()
    for famiglia, configurazione in _configurazioni_quattro_famiglie().items():
        testo = archivio.a_testo_json(configurazione)
        documento = json.loads(testo)
        assert documento["versione_schema"] == 1
        assert documento["tipo_frattale"] == famiglia
        ricaricata = archivio.da_testo_json(testo)
        assert ricaricata == configurazione
        assert "palette" in ricaricata.riepilogo()
    # Gli esiti numerici restano gli stessi dopo il round-trip
    originale = _configurazioni_quattro_famiglie()["julia"]
    ricaricata = ArchivioConfigurazioni().da_testo_json(
        ArchivioConfigurazioni().a_testo_json(originale)
    )
    assert isinstance(ricaricata.parametri, ParametriJulia)
    prima = ClassificatoreJulia(
        limite_iterazioni=originale.parametri.limite_iterazioni,
        c=complex(originale.parametri.c_reale, originale.parametri.c_immaginaria),
    ).classifica(complex(0.5, 0.25))
    dopo = ClassificatoreJulia(
        limite_iterazioni=ricaricata.parametri.limite_iterazioni,
        c=complex(ricaricata.parametri.c_reale, ricaricata.parametri.c_immaginaria),
    ).classifica(complex(0.5, 0.25))
    assert prima == dopo


def test_documenti_invalidi_con_eccezioni_dedicate() -> None:
    archivio = ArchivioConfigurazioni()
    base = _configurazioni_quattro_famiglie()["mandelbrot"].a_dizionario()

    documento = dict(base, versione_schema=2)
    with pytest.raises(VersioneNonSupportata, match="Versione schema"):
        ConfigurazioneFrattale.da_dizionario(documento)

    documento = dict(base, tipo_frattale="albero")
    with pytest.raises(TipoNonSupportato, match="non supportato"):
        ConfigurazioneFrattale.da_dizionario(documento)

    documento = dict(base)
    documento["immagine"] = dict(base["immagine"], palette="arcobaleno")
    with pytest.raises(TipoNonSupportato):
        ConfigurazioneFrattale.da_dizionario(documento)

    documento = dict(base)
    del documento["vista"]
    with pytest.raises(ErroreConfigurazione, match="mancanti"):
        ConfigurazioneFrattale.da_dizionario(documento)

    documento = dict(base)
    documento["immagine"] = dict(base["immagine"], larghezza=True)
    with pytest.raises(TypeError, match="non booleano"):
        ConfigurazioneFrattale.da_dizionario(documento)

    with pytest.raises(ErroreConfigurazione, match="non finita"):
        archivio.da_testo_json('{"versione_schema": 1, "x": NaN}')

    with pytest.raises(ErroreConfigurazione, match="malformato"):
        archivio.da_testo_json('{"versione_schema": 1,')

    # Budget 800×600×500 oltre il limite operativo con messaggio operativo
    documento = dict(base)
    documento["immagine"] = dict(base["immagine"], larghezza=800, altezza=600)
    documento["parametri"] = {"limite_iterazioni": 500}
    with pytest.raises(LimiteOperativoSuperato, match="ridurre risoluzione o N"):
        ConfigurazioneFrattale.da_dizionario(documento)

    # Parametri incoerenti con la famiglia dichiarata
    with pytest.raises(ErroreConfigurazione, match="richiede parametri"):
        ConfigurazioneFrattale(
            tipo_frattale="julia",
            vista=VistaComplessa(
                centro_reale=0.0, centro_immaginaria=0.0, ampiezza_orizzontale=3.5
            ),
            immagine=ParametriImmagine(larghezza=8, altezza=6, palette="bande"),
            parametri=ParametriMandelbrot(limite_iterazioni=10),
        )


def test_salvataggio_atomico_e_stato_preservato(tmp_path, monkeypatch) -> None:
    archivio = ArchivioConfigurazioni()
    configurazione = _configurazioni_quattro_famiglie()["mandelbrot"]
    destinazione = tmp_path / "sottocartella" / "mandelbrot.json"
    restituito = archivio.salva(destinazione, configurazione)
    assert restituito == destinazione
    assert archivio.carica(destinazione) == configurazione
    assert json.loads(destinazione.read_text(encoding="utf-8"))["versione_schema"] == 1

    # Sovrascrittura con una configurazione diversa la sostituisce
    archivio.salva(destinazione, _configurazioni_quattro_famiglie()["julia"])
    assert archivio.carica(destinazione).tipo_frattale == "julia"

    # Salvataggio fallito: il file precedente resta preservato senza residui
    destinazione.write_text("ORIGINALE", encoding="utf-8")
    corrente = _configurazioni_quattro_famiglie()["mandelbrot"]

    def _serializzazione_guasto(*args, **kwargs):
        raise RuntimeError("disco non disponibile")

    monkeypatch.setattr("json.dumps", _serializzazione_guasto)
    with pytest.raises(RuntimeError, match="disco non disponibile"):
        archivio.salva(destinazione, corrente)
    assert destinazione.read_text(encoding="utf-8") == "ORIGINALE"
    assert list(tmp_path.rglob("*.tmp")) == []

    # Caricamento fallito: la configurazione corrente resta invariata
    errata = tmp_path / "errata.json"
    errata.write_text('{"versione_schema": 1,', encoding="utf-8")
    with pytest.raises(ErroreConfigurazione):
        archivio.carica(errata)
    assert corrente == _configurazioni_quattro_famiglie()["mandelbrot"]
    with pytest.raises(ErroreConfigurazione, match="non trovato"):
        archivio.carica(tmp_path / "assente.json")


def test_costi_dichiarati_contro_conteggi_e_statistiche() -> None:
    assert stima_budget_aggiornamenti(320, 240, 100) == 7_680_000
    with pytest.raises(LimiteOperativoSuperato):
        stima_budget_aggiornamenti(800, 600, 500)
    # `None` costa N aggiornamenti, l'indice 0 ne costa zero
    assert lavoro_effettivo_da_matrice(((None, 0), (1, 2)), 6) == 6 + 0 + 1 + 2
    assert ProduttoreKoch(livello=3, variante="fiocco").conta_elementi() == 3 * 4**3
    assert ProduttoreSierpinski(livello=4).conta_elementi() == 3**4

    # Accordo con le statistiche del modulo Pillow sulla stessa matrice
    from griglia_pillow import statistiche_matrice

    esito = misura_classificazione(
        ClassificatoreMandelbrot(limite_iterazioni=5).classifica,
        8,
        6,
        complex(-0.5, 0.0),
        3.5,
        5,
    )
    assert esito["limite_superiore"] == 8 * 6 * 5
    assert esito["lavoro_effettivo"] <= esito["limite_superiore"]
    assert esito["secondi"] >= 0.0
    statistiche = statistiche_matrice(esito["matrice"], 5)
    assert statistiche.aggiornamenti_totali == esito["lavoro_effettivo"]
    assert statistiche.limite_superiore == esito["limite_superiore"]
