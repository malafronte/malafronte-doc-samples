"""Gioco a tentativi con numero assegnato (tappa U4).

Il numero da trovare è assegnato nel sorgente: le prove sono riproducibili e
chi esegue il collaudo conosce il segreto. Dominio 1-20; 0 annulla la partita
senza consumare una richiesta; ogni altra risposta numerica consuma una
richiesta anche se fuori intervallo, mentre solo gli interi validi
incrementano i tentativi validi.

Si esegue dalla root del progetto con: uv run python programmi/indovina_numero.py
"""

segreto = 7
minimo = 1
massimo = 20
limite_richieste = 4

richieste = 0
tentativi_validi = 0
esito = ""

while True:
    testo = input(
        f"Numero da {minimo} a {massimo} (massimo {limite_richieste} richieste), "
        "0 per annullare: "
    )
    valore = int(testo)
    if valore == 0:
        esito = "Annullamento: partita terminata su richiesta."
        break
    richieste = richieste + 1
    if valore < minimo or valore > massimo:
        print("Valore fuori intervallo.")
    else:
        tentativi_validi = tentativi_validi + 1
        if valore == segreto:
            esito = "Vittoria: il numero da trovare è stato indovinato."
            break
        if valore < segreto:
            print("Il numero da trovare è maggiore.")
        else:
            print("Il numero da trovare è minore.")
    if richieste == limite_richieste:
        esito = "Richieste esaurite: il numero non è stato trovato."
        break

print(esito)
print(f"Richieste usate: {richieste}")
print(f"Tentativi validi: {tentativi_validi}")
