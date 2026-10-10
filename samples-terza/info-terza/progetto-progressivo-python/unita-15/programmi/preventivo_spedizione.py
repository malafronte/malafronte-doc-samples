"""Preventivo di spedizione di kit didattici (tappa U3).

Listino fittizio e didattico, non un'offerta commerciale. Dati di ingresso:
peso intero da 1 a 10000 g, destinazione `locale` oppure `nazionale`,
urgenza `s` oppure `n`. Un valore non ammesso produce un solo messaggio,
secondo la priorità peso -> destinazione -> urgenza, e nessuna riga di costo.

Si esegue dalla root del progetto con: uv run python programmi/preventivo_spedizione.py
"""

# Acquisizione: prima i tre testi, poi la conversione del peso.
peso_testo = input("Peso del kit in grammi interi (da 1 a 10000): ")
destinazione = input("Destinazione (locale o nazionale): ")
urgenza = input("Urgenza (s o n): ")
peso_g = int(peso_testo)

# Validazione con priorità peso -> destinazione -> urgenza.
if peso_g < 1 or peso_g > 10000:
    print("Peso non ammesso")
elif destinazione != "locale" and destinazione != "nazionale":
    print("Destinazione non ammessa")
elif urgenza != "s" and urgenza != "n":
    print("Urgenza non ammessa")
else:
    # Composizione: fasce di peso esclusive, supplementi indipendenti.
    if peso_g <= 500:
        costo_base = 3
    elif peso_g <= 2000:
        costo_base = 5
    else:
        costo_base = 8

    if destinazione == "nazionale":
        supplemento_dest = 4
    else:
        supplemento_dest = 0

    if urgenza == "s":
        supplemento_urg = 2
    else:
        supplemento_urg = 0

    totale = costo_base + supplemento_dest + supplemento_urg

    # Presentazione: riepilogo e quattro righe etichettate, due decimali ed euro.
    print(f"Peso: {peso_g} g")
    print(f"Destinazione: {destinazione}")
    print(f"Urgenza: {urgenza}")
    print(f"Costo base: {costo_base:.2f} euro")
    print(f"Supplemento destinazione: {supplemento_dest:.2f} euro")
    print(f"Supplemento urgenza: {supplemento_urg:.2f} euro")
    print(f"Totale: {totale:.2f} euro")
