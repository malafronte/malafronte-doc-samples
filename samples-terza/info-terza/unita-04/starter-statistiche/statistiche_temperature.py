# Starter: statistiche su temperature simulate (da completare)
# Copiare in programmi/statistiche_temperature.py dentro la raccolta esistente.
# Questo file si avvia e si presenta, ma non calcola ancora alcuna statistica:
# un avvio riuscito non costituisce successo del laboratorio.
# Completare le parti indicate, senza aggiungere liste o funzioni.
# La gestione strutturata delle eccezioni non è richiesta nel percorso essenziale.

print("Statistiche delle temperature: programma da completare (U4).")

# 1. Quantità dei dati validi
# - Leggere la quantità come testo, con prompt che dichiara il dominio 0..20.
# - Convertire il testo con int in un nome dedicato (per esempio quantita).
# TODO: ripetere la richiesta con while finché la quantità risulta fuori 0..20.
# TODO: stampare un messaggio di quantità non ammessa e richiedere di nuovo.
quantita_testo = input("Quantità di temperature intere (da 0 a 20): ")
quantita = int(quantita_testo)

# 2. Caso senza dati
# TODO: se quantita è 0, stampare "Dati: 0" e "Nessun dato",
# TODO: senza chiedere temperature e senza leggere nomi degli estremi.

# 3. Scansione dei dati accettati
# - Per quantità positiva acquisire esattamente quel numero di temperature valide.
# - Ogni prompt indica quale dato valido si sta acquisendo, da 1 a quantità.
# - Dominio di ciascuna temperatura: intero da -30 a 50 inclusi.
# TODO: usare for per le posizioni previste e while interno per ripetere
# TODO: la lettura della stessa posizione dopo un rifiuto fuori dominio.
# TODO: accumulare conteggio, somma e numero di temperature sotto zero.
# TODO: riconoscere il primo dato valido per inizializzare minimo e massimo,
# TODO: poi confrontare ogni altro dato valido con i due estremi.
# TODO: i rifiuti non modificano conteggio, somma, estremi o contatore sotto zero.

# 4. Riepilogo dopo l'ultimo dato valido
# - Stampare Dati, Somma, Media con due decimali, Minimo, Massimo, Sotto zero.
# TODO: proteggere il riepilogo nel caso vuoto; la media non esiste senza dati.
# TODO: lo zero è valido e non è sotto zero; i valori uguali contano separatamente.

print("Attività da completare")
