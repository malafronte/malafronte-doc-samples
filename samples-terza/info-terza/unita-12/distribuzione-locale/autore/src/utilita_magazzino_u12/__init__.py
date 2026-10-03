"""`utilita_magazzino_u12`: piccola libreria personale di calcoli di magazzino.

Il package espone tre funzioni pubbliche, definite nel modulo `calcoli`:

- `valore_magazzino(articoli)` - valore complessivo di un inventario, in centesimi;
- `formatta_centesimi(centesimi)` - importo in centesimi come stringa `"euro,cc €"`;
- `normalizza_codice(testo)` - codice senza spazi iniziali e finali.

L'`__init__` ha il solo compito di comporre l'**API pubblica**: chi importa il
package ottiene i tre nomi senza conoscere la struttura interna. La versione
del package è dichiarata qui e coerente con `pyproject.toml`.
"""

from utilita_magazzino_u12.calcoli import formatta_centesimi
from utilita_magazzino_u12.calcoli import normalizza_codice
from utilita_magazzino_u12.calcoli import valore_magazzino

__all__ = ["valore_magazzino", "formatta_centesimi", "normalizza_codice"]
__version__ = "0.1.0"
