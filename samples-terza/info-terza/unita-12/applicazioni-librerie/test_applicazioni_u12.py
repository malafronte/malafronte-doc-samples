"""Regressione delle applicazioni U12, senza finestre e senza dipendenze di test.

Esecuzione dalla cartella del progetto: `uv run python -m unittest -v`.
I PNG di prova e gli alias di file vivono soltanto in cartelle temporanee.
Questa suite non certifica la resa o l'interazione delle finestre Tk.
"""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

import grafico_frequenze_u12 as grafici
import immagini_u12 as immagini
from penna_di_prova_u12 import crea_penna_di_prova
import tkinter_u12 as interfaccia
import turtle_u12 as disegni


class TestImmagini(unittest.TestCase):
    def setUp(self):
        self.cartella = tempfile.TemporaryDirectory()
        self.addCleanup(self.cartella.cleanup)
        self.originale = Path(self.cartella.name) / "originale.png"
        immagini.crea_immagine_sintetica(self.originale)
        self.prima = self.originale.read_bytes()
        self.aperta = immagini.carica_rgb(self.originale)
        self.invertita = immagini.inverti_pixel(self.aperta)

    def test_pixel_noti_a_ogni_dimensione_ammessa(self):
        for lato in range(1, 7):
            with self.subTest(lato=lato):
                immagini.crea_immagine_sintetica(self.originale, lato=lato)
                aperta = immagini.carica_rgb(self.originale)
                self.assertEqual(aperta.size, (lato, lato))
                self.assertEqual(
                    aperta.getpixel((lato - 1, lato - 1)),
                    (16 + 40 * (lato - 1), 16 + 40 * (lato - 1), 128),
                )

    def test_lato_fuori_dominio_non_scrive(self):
        for lato in (0, 7):
            with self.subTest(lato=lato):
                with self.assertRaises(ValueError):
                    immagini.crea_immagine_sintetica(self.originale, lato=lato)
                self.assertEqual(self.originale.read_bytes(), self.prima)

    def test_lato_di_tipo_errato_non_scrive(self):
        for lato in (True, 4.0, "4"):
            with self.subTest(lato=lato):
                with self.assertRaises(TypeError):
                    immagini.crea_immagine_sintetica(self.originale, lato=lato)
                self.assertEqual(self.originale.read_bytes(), self.prima)

    def test_destinazioni_equivalenti_non_sovrascrivono(self):
        for destinazione in (
            self.originale,
            str(self.originale),
            str(self.originale.parent) + "/./originale.png",
            os.path.relpath(self.originale),
        ):
            with self.subTest(destinazione=str(destinazione)):
                with self.assertRaisesRegex(ValueError, "coincidente"):
                    immagini.salva_png(self.invertita, destinazione, sorgente=self.originale)
                self.assertEqual(self.originale.read_bytes(), self.prima)

    def test_collegamento_fisico_non_sovrascrive(self):
        alias = self.originale.with_name("alias.png")
        try:
            os.link(self.originale, alias)
        except OSError as errore:
            self.skipTest(f"collegamenti fisici non disponibili: {errore}")
        with self.assertRaisesRegex(ValueError, "coincidente"):
            immagini.salva_png(self.invertita, alias, sorgente=self.originale)
        self.assertEqual(self.originale.read_bytes(), self.prima)

    def test_inversione_e_salvataggio_distinto_preservano_originale(self):
        self.assertEqual(self.aperta.getpixel((0, 0)), (16, 16, 128))
        self.assertEqual(self.invertita.getpixel((0, 0)), (239, 239, 127))
        self.assertTrue(immagini.confronta_imageops(self.aperta))
        destinazione = self.originale.with_name("invertita.png")
        immagini.salva_png(self.invertita, destinazione, sorgente=self.originale)
        self.assertEqual(self.originale.read_bytes(), self.prima)
        self.assertEqual(immagini.carica_rgb(destinazione).getpixel((0, 0)), (239, 239, 127))


class TestGrafici(unittest.TestCase):
    def test_pareggio_discrimina_la_sola_frequenza(self):
        frequenze = {"sole": 2, "luna": 2, "mare": 1}
        prima = list(frequenze.items())
        self.assertEqual(grafici.ordina_per_grafico(frequenze), [("luna", 2), ("sole", 2), ("mare", 1)])
        self.assertEqual(list(frequenze.items()), prima)
        ingenuo = sorted(frequenze.items(), key=lambda coppia: -coppia[1])
        self.assertNotEqual(ingenuo, grafici.ordina_per_grafico(frequenze))

    def test_tabella_equivalente_contiene_tutte_le_coppie(self):
        righe = [("luna", 2), ("sole", 2), ("mare", 1)]
        self.assertEqual(grafici.tabella_equivalente(righe)[2:], ["luna | 2", "sole | 2", "mare | 1"])

    def test_png_barre_etichette_scala_intera_e_chiusura(self):
        with tempfile.TemporaryDirectory() as cartella:
            percorso = Path(cartella) / "grafico.png"
            with patch.object(grafici.plt, "close", wraps=grafici.plt.close) as chiusura:
                risultato = grafici.costruisci_grafico(
                    {"sole": 2, "luna": 2, "mare": 1}, percorso, massimo_y=4
                )
            self.assertEqual(risultato, percorso)
            figura = chiusura.call_args.args[0]
            assi = figura.axes[0]
            self.assertEqual([etichetta.get_text() for etichetta in assi.get_xticklabels()], ["luna", "sole", "mare"])
            self.assertEqual([barra.get_height() for barra in assi.patches], [2, 2, 1])
            self.assertEqual([etichetta.get_text() for etichetta in assi.texts], ["2", "2", "1"])
            self.assertEqual(assi.get_ylim(), (0, 4))
            self.assertTrue(all(tacca == int(tacca) for tacca in assi.get_yticks()))
            self.assertNotIn(figura.number, grafici.plt.get_fignums())
            with Image.open(percorso) as png:
                self.assertEqual(png.format, "PNG")
                self.assertEqual(png.size, (1280, 720))

    def test_dataset_vuoto_produce_png_e_tabella_vuota(self):
        with tempfile.TemporaryDirectory() as cartella:
            percorso = Path(cartella) / "vuoto.png"
            grafici.costruisci_grafico({}, percorso)
            self.assertTrue(percorso.exists())
        self.assertEqual(grafici.ordina_per_grafico({}), [])
        self.assertEqual(len(grafici.tabella_equivalente([])), 2)

    def test_scala_inadatta_viene_rifiutata(self):
        with tempfile.TemporaryDirectory() as cartella:
            percorso = Path(cartella) / "non-creato.png"
            with self.assertRaises(ValueError):
                grafici.costruisci_grafico({"sole": 3}, percorso, massimo_y=2)
            self.assertFalse(percorso.exists())


class TestDisegni(unittest.TestCase):
    def test_penna_fornita_registra_il_quadrato(self):
        penna = crea_penna_di_prova()
        self.assertIsNone(disegni.disegna_poligono(penna, 4, 10))
        self.assertEqual(penna.azioni, [("pendown",)] + [("forward", 10), ("left", 90.0)] * 4)

    def test_due_figure_restituiscono_none_e_separano_il_tratto(self):
        penna = crea_penna_di_prova()
        self.assertIsNone(disegni.disegna_due_figure(penna, 3, 60))
        self.assertIn(("forward", 132.0), penna.azioni)
        indice = penna.azioni.index(("forward", 132.0))
        self.assertEqual(penna.azioni[indice - 1], ("penup",))
        self.assertEqual(penna.azioni[indice + 1], ("pendown",))


class TestCalcoloInterfaccia(unittest.TestCase):
    def test_calcolo_noto_e_formatto(self):
        totale = interfaccia.valore_in_centesimi(4, 25)
        self.assertEqual(totale, 100)
        self.assertEqual(interfaccia.formatta_euro(totale), "1,00 €")

    def test_input_non_valido_distingue_formato_e_dominio(self):
        for testo, motivo in (("tre", "non è un intero"), ("", "campo vuoto"), ("-1", "negativo")):
            with self.subTest(testo=testo):
                with self.assertRaisesRegex(ValueError, motivo):
                    interfaccia.centesimi_da_testo(testo)


if __name__ == "__main__":
    unittest.main()
