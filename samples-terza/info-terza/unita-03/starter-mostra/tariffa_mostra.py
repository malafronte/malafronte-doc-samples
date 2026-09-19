# Starter: tariffa della mostra (da completare)
# Copiare in programmi/tariffa_mostra.py dentro la raccolta esistente.
# Questo file si avvia e si presenta, ma non calcola ancora alcuna tariffa:
# un avvio riuscito non costituisce successo del laboratorio.
# Completare le quattro parti indicate, senza aggiungere cicli o funzioni.

print("Tariffa della mostra: programma da completare (U3).")

# 1. Lettura e conversione
# - Leggere eta e tessera come testo, con prompt che dichiarano i vincoli.
# - I prompt dichiarano: eta intera da 0 a 120; tessera esattamente s oppure n.
# - Convertire il testo dell'eta con int in un nome dedicato (per esempio eta).
# - La tessera resta stringa: non richiede conversione.

# 2. Validazione dopo conversione riuscita
# - Prima l'eta (intero da 0 a 120 inclusi), poi la tessera (s oppure n).
# - Se entrambi i valori risultano non ammessi, prevale l'errore sull'eta.
# - Su input non ammesso si stampa il solo messaggio di rifiuto,
#   senza alcuna riga di categoria o di costo.

# 3. Fasce e riduzione subordinata
# - Fasce da costruire con una catena di selezione (dati nella pagina del laboratorio):
#   gratuito, ridotto, ordinario e senior, ciascuna con il proprio prezzo base.
# - La riduzione di 2 euro con tessera vale soltanto per la categoria ordinario.
# - Le riduzioni non si sommano: le altre categorie mantengono il prezzo base.

# 4. Presentazione e verifica
# - Nel solo ramo valido si stampano categoria e costo con due decimali.
# - Provare i casi della pagina del laboratorio e registrare atteso e osservato.
