"""Grafico del confronto fra strategie di ordinamento (tappa U11).

Legge i campioni di `confronto_ordinamenti_u11.py` e disegna le mediane del
tempo di ordinamento per famiglia di input e dimensione. La tabella equivalente
è in `documentazione/unita-11/relazione-confronto.md`.

Comando, dalla root del progetto:

    uv run python programmi/grafico_ordinamenti_u11.py
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt

PERCORSO_RISULTATI = Path(__file__).resolve().parent.parent / "risultati" / "unita-11"
ETICHETTE = {
    "inserimento": "ordinamento per inserimento",
    "fusione": "MergeSort stabile",
    "sorted": "sorted (riferimento CPython)",
}


def main() -> None:
    """Costruisce il grafico dei tempi e lo salva in PNG, senza finestre."""
    file_campioni = PERCORSO_RISULTATI / "misure_u11.json"
    documento = json.loads(file_campioni.read_text(encoding="utf-8"))

    fig, assi = plt.subplots(figsize=(9, 5))
    for procedimento, etichetta in ETICHETTE.items():
        dimensioni = []
        mediane = []
        for campione in documento["ordinamenti"]:
            if campione["procedimento"] == procedimento and campione["famiglia"] == "pseudo_casuale":
                dimensioni.append(campione["n"])
                mediane.append(campione["mediana_s"] * 1000)
        assi.plot(dimensioni, mediane, marker="o", label=etichetta)

    assi.set_xlabel("numero di record (n), famiglia pseudo_casuale")
    assi.set_ylabel("mediana del tempo di ordinamento (ms)")
    assi.set_title("Inserimento, MergeSort e sorted sullo stesso criterio")
    assi.legend()
    assi.grid(True, alpha=0.3)
    fig.tight_layout()

    PERCORSO_RISULTATI.mkdir(parents=True, exist_ok=True)
    file_grafico = PERCORSO_RISULTATI / "confronto_u11.png"
    fig.savefig(file_grafico, dpi=120)
    print(f"Grafico salvato in: {file_grafico}")
    print("La tabella equivalente è nella relazione di confronto.")


if __name__ == "__main__":
    main()
