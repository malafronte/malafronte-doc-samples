"""Controllo autoriale: estrae le fence Python delle raccolte in test temporanei.

Non è una dipendenza dello studente. Le pagine e la directory di uscita sono
argomenti espliciti; nessun percorso assoluto di produzione è incorporato.
I test generati si eseguono dalla radice U15 con la configurazione di pytest.
"""

import argparse
import ast
import json
import re
from pathlib import Path


def estrai(pagina, uscita):
    testo = pagina.read_text(encoding="utf-8")
    resoconto = []
    for numero, fence in enumerate(re.finditer(r"^```python[^\n]*\n(.*?)^```", testo, re.M | re.S)):
        codice = fence.group(1)
        albero = ast.parse(codice)
        prima = testo[: fence.start()]
        ancore = re.findall(r'<span id="([^"]+)"', prima)
        ancora = ancore[-1] if ancore else "apertura"
        riga = testo.count("\n", 0, fence.start()) + 1
        nome = f"test_{pagina.stem.replace('-', '_')}_{numero:02d}.py"
        # L'errore intenzionale di E01 e il metodo da inserire in T02 richiedono contesto.
        if ancora == "py-u15-e01":
            contenuto = (
                "import pytest\n\ndef test_errore_intenzionale():\n"
                f"    with pytest.raises(AttributeError):\n        exec({codice!r}, {{}})\n"
            )
        elif ancora == "soluzione-py-u15-t02":
            contenuto = (
                "from orologi_base_u15 import OrologioDigitale\n\n"
                "class OrologioDiAula(OrologioDigitale):\n"
                "    def __init__(self, ore, minuti, aula):\n"
                "        super().__init__(ore, minuti)\n        self.aula = aula\n"
                + "\n".join("    " + r for r in codice.splitlines())
                + "\n\ndef test_estratto_integrato():\n"
                "    orologio = OrologioDiAula(8, 15, 'B12')\n"
                "    assert orologio.descrizione() == 'Ora 08:15; aula B12'\n"
                "    assert orologio.testo() == '08:15'\n"
            )
        elif any(
            isinstance(n, ast.FunctionDef) and n.name.startswith("test_") for n in albero.body
        ):
            contenuto = codice
        else:
            contenuto = f"def test_blocco():\n    exec({codice!r}, {{'__name__': 'verifica'}})\n"
        (uscita / nome).write_text(contenuto, encoding="utf-8")
        resoconto.append({"pagina": str(pagina), "riga": riga, "ancora": ancora, "test": nome})
    return resoconto


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--uscita", type=Path, required=True)
    parser.add_argument("pagine", nargs="+", type=Path)
    argomenti = parser.parse_args()
    # Una directory nuova impedisce di sovrascrivere altre verifiche o lavoro preesistente.
    argomenti.uscita.mkdir(parents=True, exist_ok=False)
    resoconto = []
    for pagina in argomenti.pagine:
        resoconto.extend(estrai(pagina, argomenti.uscita))
    (argomenti.uscita / "manifest.json").write_text(
        json.dumps(resoconto, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Fence compilate e preparate: {len(resoconto)}; uscita: {argomenti.uscita}")


if __name__ == "__main__":
    main()
