import pytest

from factory_ereditata_u15 import Contatore, ContatoreEtichettato
from mro_cooperativa_u15 import Base, Derivata, Destra, Invertita, Sinistra


def test_mro():
    assert Derivata.__mro__ == (Derivata, Sinistra, Destra, Base, object)
    assert Derivata().passaggi() == ["Derivata", "Sinistra", "Destra", "Base"]
    assert Sinistra().passaggi() == ["Sinistra", "Base"]
    assert Invertita().passaggi() == ["Invertita", "Destra", "Sinistra", "Base"]


def test_factory():
    uno = ContatoreEtichettato.zero()
    due = ContatoreEtichettato.zero()
    assert type(uno) is ContatoreEtichettato
    assert uno.valore == 0
    assert uno.etichetta == "Conteggio"
    assert uno is not due

    class Incompatibile(Contatore):
        def __init__(self, valore, etichetta):
            super().__init__(valore)
            self.etichetta = etichetta

    with pytest.raises(TypeError):
        Incompatibile.zero()
