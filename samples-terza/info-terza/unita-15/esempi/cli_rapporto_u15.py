"""CLI circoscritta: dataset sintetico già acquisito, scelta del formato."""

from pathlib import Path

from esportatori_u15 import EsportatoreCSV, EsportatoreJSON
from rilevazioni_u15 import dataset
from servizio_rapporto_u15 import ServizioRapporto


def main():
    formato = input("formato (csv/json)> ").strip()
    match formato:
        case "csv":
            esportatore = EsportatoreCSV()
        case "json":
            esportatore = EsportatoreJSON()
        case _:
            print("formato non ammesso: scegliere csv oppure json")
            return 1
    percorso = Path(input("percorso di destinazione> "))
    servizio = ServizioRapporto(esportatore)
    try:
        quantita = servizio.genera(dataset(), percorso)
    except (ValueError, OSError) as errore:
        print(f"esportazione fallita: {errore}")
        return 1
    print(f"rilevazioni esportate: {quantita}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
