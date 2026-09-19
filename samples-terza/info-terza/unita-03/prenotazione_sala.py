durata_testo = input("Durata in minuti interi (da 1 a 240): ")
durata_min = int(durata_testo)

if durata_min < 1 or durata_min > 240:
    print("Durata non ammessa: indicare un intero da 1 a 240.")
else:
    if durata_min <= 60:
        costo_euro = 2
    elif durata_min <= 120:
        costo_euro = 3
    else:
        costo_euro = 5
    print(f"Costo complessivo: {costo_euro:.2f} euro")
