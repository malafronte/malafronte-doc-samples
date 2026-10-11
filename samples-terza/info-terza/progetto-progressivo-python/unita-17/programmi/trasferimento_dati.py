"""Calcolatore del tempo di trasferimento (tappa U2).

Modello semplificato a velocità costante. Dati di ingresso: dimensione in MB
interi (milioni di byte), velocità in MB/s con punto decimale, preparazione in
secondi interi. Il programma accetta input conformi e non intercetta quelli
non conformi: domini e limiti sono in documentazione/unita-02/specifica.md.

Si esegue dalla root del progetto con: uv run python programmi/trasferimento_dati.py
"""

# Acquisizione: tre testi nell'ordine della consegna.
dimensione_testo = input("Dimensione in MB interi, zero ammesso: ")
velocita_testo = input("Velocità in MB/s, punto decimale, minimo 0.01: ")
preparazione_testo = input("Preparazione in secondi interi, zero ammesso: ")

# Conversioni motivate dal tipo dei dati: interi dove il dato è intero,
# float dove il dato ammette il punto decimale.
dimensione_mb = int(dimensione_testo)
velocita_mb_s = float(velocita_testo)
preparazione_s = int(preparazione_testo)

# Calcolo sui valori convertiti: nessun arrotondamento intermedio.
trasferimento_s = dimensione_mb / velocita_mb_s
totale_s = trasferimento_s + preparazione_s
totale_min = totale_s / 60

# Presentazione: due cifre decimali solo nelle stringhe finali.
print(f"Dimensione: {dimensione_mb} MB")
print(f"Velocità: {velocita_mb_s} MB/s")
print(f"Preparazione: {preparazione_s} secondi")
print(f"Tempo di trasferimento: {trasferimento_s:.2f} secondi")
print(f"Tempo totale: {totale_s:.2f} secondi")
print(f"Tempo totale: {totale_min:.2f} minuti")
