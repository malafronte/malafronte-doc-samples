# Esperimenti sui costi PY-42 — Mandelbrot sulla vista iniziale

Vista: centro `-0.5 + 0j`, ampiezza orizzontale `3.5`. Hardware e ambiente:
`Windows 11 (AMD64)`,
CPython `3.14.7`, Tk non richiesto. I tempi coprono il
solo doppio ciclo di campionamento e classificazione; la preparazione resta
fuori dalla regione cronometrata. I valori documentano ordini di grandezza
sulla macchina usata, non soglie universali per i test.

| Risoluzione | N | K (lavoro effettivo) | W·H·N (limite) | K per pixel | Secondi |
|---|---|---|---|---|---|
| `160×120` | `25` | `146160` | `480000` | `7.6` | `0.06` |
| `160×120` | `100` | `394342` | `1920000` | `20.5` | `0.19` |
| `320×240` | `25` | `585020` | `1920000` | `7.6` | `0.21` |
| `320×240` | `100` | `1577550` | `7680000` | `20.5` | `0.45` |

Lettura: il raddoppio di risoluzione quadruplica pixel, limite superiore e
lavoro di campionamento `W·H`; il raddoppio di `N` alza il limite superiore
ma il lavoro effettivo cresce meno, perché i pixel esterni fuggono presto.
La colorazione dalla matrice costerebbe `Theta(W·H)` senza ricalcolare le
orbite; il salvataggio JSON dei soli parametri resta indipendente dai pixel.
