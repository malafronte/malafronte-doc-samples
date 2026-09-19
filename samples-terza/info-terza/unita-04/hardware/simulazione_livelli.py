# Simulazione dei livelli logici (Unità 4) — CPython sul computer.
# Nessuna lettura di GPIO: il testo assegnato rappresenta livelli simulati.
# Regola simulata del laboratorio: ogni 1 simulato produce 0, ogni 0 produce 1.

ingresso_simulato = "1100011"
uscite_simulate = ""
for simbolo in ingresso_simulato:
    if simbolo == "1":
        uscite_simulate = uscite_simulate + "0"
    else:
        uscite_simulate = uscite_simulate + "1"

print(f"Simulazione: ingresso simulato {ingresso_simulato}")
print(f"Simulazione: uscite simulate {uscite_simulate}")
