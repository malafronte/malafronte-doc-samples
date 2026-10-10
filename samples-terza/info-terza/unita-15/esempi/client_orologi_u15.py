"""Un client comune; la stampa appartiene alla dimostrazione."""

from orologi_base_u15 import OrologioDigitale
from orologi_derivati_u15 import OrologioConEtichetta, OrologioConSveglia


def descrizioni(orologi):
    risultato = []
    for orologio in orologi:
        risultato.append(orologio.descrizione())
    return risultato


if __name__ == "__main__":
    orologi = [
        OrologioDigitale(8, 15),
        OrologioConEtichetta(8, 15, "Laboratorio"),
        OrologioConSveglia(8, 15, 7, 0),
    ]
    for testo in descrizioni(orologi):
        print(testo)
