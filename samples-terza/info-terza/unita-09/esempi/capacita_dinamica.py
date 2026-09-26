"""Capacità dinamica dell'Unità 9: modello didattico del costo ammortizzato.

Collocare il file in `programmi/capacita_dinamica.py` della raccolta dello
studente. Il modulo SIMULA il modello didattico della sequenza a capacità
dinamica del capitolo PY-13, parte III, e ne conta le operazioni: non è una
implementazione di lista Python e non descrive la formula di crescita di
CPython, che adotta dettagli propri.

Ipotesi del modello, da dichiarare ogni volta che se ne parla:
- la sequenza parte VUOTA con capacità 1;
- ogni inserimento scrive un riferimento nella prima cella libera e costa 1;
- se la sequenza è piena, la capacità RADDOPPIA e tutti i riferimenti
  presenti vengono copiati nella nuova area, con un'unità di costo per copia;
- si contano copie e scritture, non byte né tempi reali di allocazione.

Nella simulazione non si conservano gli elementi: restano soltanto la
lunghezza, la capacità e i conteggi. Un singolo passo può costare Θ(n),
cioè lineare nel numero di riferimenti presenti; il limite vale sull'intera
sequenza di m accodamenti ed è questa la ragione del costo ammortizzato
costante per accodamento. Misurare i picchi di otto `append` reali non
dimostrebbe l'analisi.

L'import non chiede input e non stampa: le tabelle si costruiscono in
memoria e si presentano nel main protetto dalla guardia di avvio.
Esecuzione: uv run python programmi/capacita_dinamica.py
"""


def simula_accodamenti(inserimenti: int) -> list[dict]:
    """Restituisce una riga per ogni inserimento del modello didattico.

    PRECONDIZIONE: `inserimenti` è un intero non negativo; m = `inserimenti`
    è il numero di accodamenti simulati. Ogni riga ha le chiavi
    `inserimento`, `capacita_dopo`, `copie`, `scrittura_nuova`,
    `costo_passo` e `cumulativo`. La scrittura nuova è sempre 1; il costo
    del passo è `copie + scrittura_nuova`; il cumulativo somma i costi dei
    passi precedenti incluso quello corrente. Per `inserimenti = 0` il
    risultato è la lista vuota.

    Sugli otto primi accodamenti la tabella del capitolo è: capacità dopo
    1/2/4/4/8/8/8/8, copie 0/1/2/0/4/0/0/0, costo del passo 1/2/3/1/5/1/1/1
    e cumulativo 1/3/6/7/12/13/14/15.
    """
    righe = []
    capacita = 1
    lunghezza = 0
    cumulativo = 0
    for inserimento in range(1, inserimenti + 1):
        copie = 0
        if lunghezza == capacita:
            capacita *= 2
            copie = lunghezza
        lunghezza += 1
        costo_passo = copie + 1
        cumulativo += costo_passo
        righe.append(
            {
                "inserimento": inserimento,
                "capacita_dopo": capacita,
                "copie": copie,
                "scrittura_nuova": 1,
                "costo_passo": costo_passo,
                "cumulativo": cumulativo,
            }
        )
    return righe


def riepilogo_ammortizzato(inserimenti: int) -> dict:
    """Restituisce copie totali, scritture e costo totale di m accodamenti.

    PRECONDIZIONE: `inserimenti` è un intero non negativo; m = `inserimenti`.
    Il risultato ha le chiavi `inserimenti`, `copie_totali`,
    `scritture_totali`, `costo_totale`, `capacita_finale`, `limite_copie` e
    `limite_costo`. I totali derivano dalla simulazione di
    `simula_accodamenti`, non da una formula ripetuta: la formula serve a
    descriverli e a dimostrarne i limiti.

    DIMOSTRAZIONE. Le copie avvengono soltanto quando la capacità è piena,
    cioè agli inserimenti 2, 3, 5, 9, ... = 2^k + 1, e ammontano a
    1, 2, 4, ..., 2^k riferimenti. La somma delle copie fino a m accodamenti
    è quindi la somma geometrica 1 + 2 + 4 + ... + 2^K = 2^(K+1) - 1, con
    2^K < m: ne segue `copie_totali` < 2 * m. Aggiungendo le m scritture
    nuove si ottiene `costo_totale` = m + `copie_totali` < 3 * m per m >= 1;
    per m = 0 entrambi i totali sono nulli. Il costo ammortizzato per
    accodamento è dunque costante: si ricava da un limite sull'intera
    sequenza, non da un limite sul singolo passo.
    """
    righe = simula_accodamenti(inserimenti)
    copie_totali = sum(riga["copie"] for riga in righe)
    scritture_totali = sum(riga["scrittura_nuova"] for riga in righe)
    capacita_finale = righe[-1]["capacita_dopo"] if righe else 1
    return {
        "inserimenti": inserimenti,
        "copie_totali": copie_totali,
        "scritture_totali": scritture_totali,
        "costo_totale": copie_totali + scritture_totali,
        "capacita_finale": capacita_finale,
        "limite_copie": 2 * inserimenti,
        "limite_costo": 3 * inserimenti,
    }


if __name__ == "__main__":
    # Le uniche stampe del modulo stanno qui: le funzioni sopra costruiscono
    # liste e dizionari e non scrivono nulla.
    print("Modello didattico — otto accodamenti")
    print("ins  capacita  copie  scrittura  costo  cumulativo")
    for riga in simula_accodamenti(8):
        print(
            f"{riga['inserimento']:<4} {riga['capacita_dopo']:<9} {riga['copie']:<6} "
            f"{riga['scrittura_nuova']:<10} {riga['costo_passo']:<6} {riga['cumulativo']}"
        )

    print()
    print("Totali per m accodamenti, con i limiti del modello")
    print("m     copie  < 2m   costo  < 3m   capacita finale")
    for m in (0, 1, 2, 3, 5, 8, 16, 32, 128):
        riepilogo = riepilogo_ammortizzato(m)
        print(
            f"{m:<5} {riepilogo['copie_totali']:<6} {riepilogo['limite_copie']:<6} "
            f"{riepilogo['costo_totale']:<6} {riepilogo['limite_costo']:<6} "
            f"{riepilogo['capacita_finale']}"
        )
