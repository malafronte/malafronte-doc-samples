"""Grafico delle durate misurate (tappa U9).

Legge i campioni prodotti da `analisi_costi_u9.py` e disegna le mediane delle
durate per dimensione del registro. Ogni serie del grafico ha la tabella
equivalente in `documentazione/unita-09/progetto/dossier-analisi.md`.

Comando, dalla root del progetto:

    uv run python programmi/grafico_costi_u9.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt

PERCORSO_RISULTATI = Path(__file__).resolve().parent.parent / "risultati" / "unita-09"
ETICHETTE = {
    "riepilogo_per_destinazione": "riepilogo per destinazione",
    "cerca_preventivo_ultima_posizione": "ricerca, ultima posizione",
    "cerca_preventivo_assente": "ricerca, codice assente",
}


def main() -> None:
    """Costruisce il grafico dei tempi e lo salva in PNG, senza finestre."""
    file_campioni = PERCORSO_RISULTATI / "misure_u9.json"
    documento = json.loads(file_campioni.read_text(encoding="utf-8"))

    fig, assi = plt.subplots(figsize=(8, 5))
    for operazione, etichetta in ETICHETTE.items():
        dimensioni = []
        mediane = []
        for campione in documento["campioni"]:
            if campione["operazione"] == operazione:
                dimensioni.append(campione["n"])
                mediane.append(campione["mediana_s"] * 1000)
        assi.plot(dimensioni, mediane, marker="o", label=etichetta)

    assi.set_xlabel("numero di record del registro (n)")
    assi.set_ylabel("mediana del tempo per chiamata (ms)")
    assi.set_title("Costo di riepilogo e consultazione al crescere di n")
    assi.legend()
    assi.grid(True, alpha=0.3)
    fig.tight_layout()

    PERCORSO_RISULTATI.mkdir(parents=True, exist_ok=True)
    file_grafico = PERCORSO_RISULTATI / "costi_u9.png"
    fig.savefig(file_grafico, dpi=120)
    print(f"Grafico salvato in: {file_grafico}")
    print("La tabella equivalente è nel dossier di analisi.")


if __name__ == "__main__":
    main()
