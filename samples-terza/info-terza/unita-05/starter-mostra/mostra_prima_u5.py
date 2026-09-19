"""Baseline monolitica della tariffa della mostra, conforme a U3.

Questo file è il punto di partenza del laboratorio LAB-PY-U5: funziona, ma
mescola lettura, conversione, validazione, classificazione, calcolo e stampa.
Non contiene la decomposizione in funzioni: è compito dello studente estrarla
senza cambiare il comportamento pubblico.

Collocare il file in programmi/mostra_prima_u5.py e, dopo la rifattorizzazione,
creare programmi/mostra_u5.py con le funzioni richieste.
Eseguire con: uv run python programmi/mostra_prima_u5.py
"""

eta_testo = input("Età in anni interi (da 0 a 120): ")
tessera = input("Tessera ridotta (s oppure n): ")
eta = int(eta_testo)

if eta < 0 or eta > 120:
    print("Età non ammessa")
elif tessera != "s" and tessera != "n":
    print("Risposta tessera non ammessa")
else:
    if eta <= 5:
        categoria = "Gratuito"
        costo_euro = 0
    elif eta <= 17:
        categoria = "Ridotto"
        costo_euro = 4
    elif eta <= 64:
        categoria = "Ordinario"
        costo_euro = 7
        if tessera == "s":
            costo_euro = costo_euro - 2
    else:
        categoria = "Senior"
        costo_euro = 5
    print(f"Categoria: {categoria}")
    print(f"Costo: {costo_euro:.2f} euro")
