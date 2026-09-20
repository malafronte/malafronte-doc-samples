risposta = input("Confermare (s/n): ")

match risposta:
    case "s":
        print("Richiesta confermata")
    case "n":
        print("Richiesta rifiutata")
    case _:
        print("Risposta non ammessa: indicare s oppure n.")
