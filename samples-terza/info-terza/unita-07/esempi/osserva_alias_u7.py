"""Osservare l'alias e le copie con il debugger (Unità 7).

Collocare il file in `programmi/osserva_alias_u7.py` della raccolta dello
studente. È il programma di osservazione canonico della guida agli
strumenti di sviluppo: un elenco LINEARE di passi numerati, senza
funzioni, da eseguire in traccia passo passo con il debugger.

Prima di ogni punto di osservazione una riga `MISURA:` descrive lo stato
che ci si aspetta: nomi definiti, oggetti distinti o condivisi, dimensioni.
Le stampe sono volute: questo è il programma che OSSERVA, non una libreria
di funzioni da verificare.

Esecuzione: uv run python programmi/osserva_alias_u7.py
"""

# ===========================================================================
# Programma di osservazione. Eseguire i passi in ordine e fermarsi sulle
# righe indicate dai commenti MISURA per leggere lo stato nel debugger.
# ===========================================================================

if __name__ == "__main__":
    # ---------------------------------------------------------------------
    # PASSO 1 — costruzione della matrice 2x2 di partenza.
    # ---------------------------------------------------------------------
    originale = [[1, 2], [3, 4]]
    # MISURA (dopo l'assegnamento, prima di append): esiste il nome
    # `originale`, che indica una lista di due righe; ogni riga è una lista
    # di due interi. Nessun altro nome è ancora definito.
    print("PASSO 1 — originale =", originale)
    print("  id(originale) =", id(originale))
    print("  id(originale[0]) =", id(originale[0]), " id(originale[1]) =", id(originale[1]))
    print("  numero di righe:", len(originale))

    # ---------------------------------------------------------------------
    # PASSO 2 — alias: un secondo nome per lo STESSO oggetto.
    # ---------------------------------------------------------------------
    alias = originale
    # MISURA (dopo l'assegnamento): `alias` e `originale` indicano lo stesso
    # oggetto, quindi `alias is originale` vale True e `id(alias)` coincide
    # con `id(originale)`. Non è stata creata alcuna lista nuova.
    print("PASSO 2 — alias =", alias)
    print("  alias is originale:", alias is originale)
    print("  id(alias) =", id(alias), "-> coincide con id(originale)")

    # ---------------------------------------------------------------------
    # PASSO 3 — copia superficiale: lista esterna nuova, righe condivise.
    # ---------------------------------------------------------------------
    copia = originale.copy()
    # MISURA (dopo la copia): `copia` è una lista NUOVA (`copia is not
    # originale`), ma le sue due righe sono le STESSE liste di `originale`
    # (`copia[0] is originale[0]` vale True). Sono quindi tre i nomi
    # definiti e due gli oggetti lista interni.
    print("PASSO 3 — copia =", copia)
    print("  copia is not originale:", copia is not originale)
    print("  id(copia) =", id(copia), "-> diverso da id(originale)")
    print("  copia[0] is originale[0]:", copia[0] is originale[0], "-> riga condivisa")

    # ---------------------------------------------------------------------
    # PASSO 4 — mutazione interna attraverso la copia.
    # ---------------------------------------------------------------------
    copia[0][0] = 99
    # MISURA (dopo la mutazione interna): il valore 99 è scritto nella riga
    # condivisa, quindi appare in `copia`, in `originale` e in `alias`.
    # Nessuna lista esterna è stata sostituita: sono gli stessi oggetti di
    # prima, con un elemento cambiato.
    print("PASSO 4 — copia[0][0] = 99")
    print("  copia    =", copia, "-> vede 99")
    print("  originale=", originale, "-> vede 99 (riga condivisa)")
    print("  alias    =", alias, "-> vede 99 (stessa matrice)")

    # ---------------------------------------------------------------------
    # PASSO 5 — mutazione della sola lista esterna di `originale`.
    # ---------------------------------------------------------------------
    # MISURA (prima di append): `originale` e `alias` hanno 2 righe, `copia`
    # ha 2 righe; tutti e tre i nomi condividono la prima riga.
    originale.append([5, 6])
    # MISURA (dopo la mutazione esterna): `originale` e `alias` hanno 3 righe,
    # perché indicano la stessa lista esterna; `copia` resta a 2 righe,
    # perché la lista esterna è propria e la copia non la vede.
    print("PASSO 5 — originale.append([5, 6])")
    print("  originale=", originale, "-> righe:", len(originale))
    print("  alias    =", alias, "-> righe:", len(alias))
    print("  copia    =", copia, "-> righe:", len(copia))

    # ---------------------------------------------------------------------
    # PASSO 6 — riepilogo degli oggetti e dei nomi.
    # ---------------------------------------------------------------------
    # MISURA (riepilogo): i nomi sono quattro, gli oggetti lista esterni
    # sono due (`originale`/`alias` condividono l'uno, `copia` ha l'altro) e
    # la prima riga è un unico oggetto indicato da tutti e tre i nomi.
    print("PASSO 6 — riepilogo")
    print("  nomi definiti: originale, alias, copia")
    print("  id(originale) =", id(originale))
    print("  id(alias)     =", id(alias), "-> stesso oggetto di originale")
    print("  id(copia)     =", id(copia), "-> oggetto proprio")
    print("  id(originale[0]) =", id(originale[0]))
    print("  id(copia[0])     =", id(copia[0]), "-> stessa riga di originale[0]")
    print("  lunghezze -> originale:", len(originale), "alias:", len(alias), "copia:", len(copia))
