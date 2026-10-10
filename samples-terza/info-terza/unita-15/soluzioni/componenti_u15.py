"""Soluzioni formative T03, T07, X01, X03, T10, X04 e X05."""

from pathlib import Path

from esportatori_u15 import scrivi_atomico
from politiche_duck_u15 import valida_intero, valida_valori
from rilevazioni_u15 import proiezioni, rilevazione_da_record
from soglia_algoritmi_u15 import valida_ingressi


class PoliticaMultipli:
    def __init__(self, divisore):
        valida_intero(divisore)
        if divisore <= 0:
            raise ValueError("divisore: atteso intero positivo")
        self._divisore = divisore

    def ammette(self, valore):
        valida_intero(valore)
        return valore % self._divisore == 0


def primo_ammesso(valori, politica):
    valida_valori(valori)
    for indice, valore in enumerate(valori):
        ammesso = politica.ammette(valore)
        if type(ammesso) is not bool:
            raise TypeError("ammette: atteso bool")
        if ammesso:
            return indice
    return None


class PoliticaCongiunzione:
    def __init__(self, prima, seconda):
        self._prima = prima
        self._seconda = seconda

    def ammette(self, valore):
        valida_intero(valore)
        uno = self._prima.ammette(valore)
        due = self._seconda.ammette(valore)
        if type(uno) is not bool or type(due) is not bool:
            raise TypeError("criteri: attesi bool")
        return uno and due


def seleziona_con_funzione(valori, criterio):
    valida_valori(valori)
    risultato = []
    for valore in valori:
        ammesso = criterio(valore)
        if type(ammesso) is not bool:
            raise TypeError("criterio: atteso bool")
        if ammesso:
            risultato.append(valore)
    return risultato


class EsportatoreTSV:
    def esporta(self, rilevazioni, percorso: Path):
        import csv

        record = proiezioni(rilevazioni)

        def scrivi(stream):
            writer = csv.DictWriter(
                stream,
                fieldnames=["codice", "valore", "unita"],
                delimiter="\t",
            )
            writer.writeheader()
            writer.writerows(record)

        scrivi_atomico(percorso, scrivi)
        return None


def leggi_tsv(percorso):
    import csv

    with percorso.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        if reader.fieldnames != ["codice", "valore", "unita"]:
            raise ValueError("TSV: intestazione invalida")
        risultato = []
        for record in reader:
            if set(record) != {"codice", "valore", "unita"} or None in record.values():
                raise ValueError("TSV: numero di campi invalido")
            record["valore"] = int(record["valore"])
            risultato.append(rilevazione_da_record(record))
        return risultato


class VistaEtichettata:
    def __init__(self, orologio, etichetta):
        if not isinstance(etichetta, str) or not etichetta.strip():
            raise ValueError("etichetta: atteso testo non vuoto")
        self._orologio = orologio
        self._etichetta = etichetta.strip()

    def imposta(self, ore, minuti):
        return self._orologio.imposta(ore, minuti)

    def avanza(self, minuti_trascorsi):
        return self._orologio.avanza(minuti_trascorsi)

    def leggi(self):
        return self._orologio.leggi()

    def testo(self):
        return self._orologio.testo()

    def descrizione(self):
        return f"{self._etichetta} — {self.testo()}"


def primo_uguale_lineare(valori_ordinati, cercato):
    valida_ingressi(valori_ordinati, cercato)
    for indice, valore in enumerate(valori_ordinati):
        if valore == cercato:
            return indice
    return None


def primo_uguale_dicotomico(valori_ordinati, cercato):
    valida_ingressi(valori_ordinati, cercato)
    sinistra, destra = 0, len(valori_ordinati)
    while sinistra < destra:
        centro = (sinistra + destra) // 2
        if valori_ordinati[centro] < cercato:
            sinistra = centro + 1
        else:
            destra = centro
    if sinistra < len(valori_ordinati) and valori_ordinati[sinistra] == cercato:
        return sinistra
    return None
