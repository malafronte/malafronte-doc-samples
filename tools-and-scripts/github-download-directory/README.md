# Script per Scaricare Sottocartelle da GitHub

Questi script permettono di scaricare una specifica sottocartella da un repository GitHub, simile a [download-directory.github.io](https://download-directory.github.io), ma eseguibili localmente senza dipendenze da servizi esterni.

## Caratteristiche

- 📥 Scarica solo la cartella richiesta (non l'intero repository)
- 🎯 Funziona con qualsiasi repository GitHub **pubblico** (tutti gli script)
- 🔐 Supporta repository **privati** con GitHub Token (solo script ottimizzati)
- 🛡️ Gestione automatica degli errori
- 🧹 Pulizia automatica dei file temporanei
- 📊 Output dettagliato con messaggi colorati

## Script Disponibili

### 1. Script Python (`download-github-folder.py`) - Versione Non Ottimizzata

> ⚠️ **Nota:** Questa versione **non supporta l'autenticazione** e funziona solo con repository **pubblici**.

**Requisiti:**

- Python 3.6 o superiore
- **Nessuna dipendenza esterna** (usa solo librerie standard: `re`, `shutil`, `urllib`, `zipfile`, `pathlib`)

**Utilizzo:**

```bash
# Download nella directory corrente
python download-github-folder.py https://github.com/malafronte/malafronte-doc-samples/tree/main/samples-quarta/api_client_server_demos/mock-server-tutorial

# Download in una directory specifica
python download-github-folder.py <URL> ./output
```

### 2. Script Bash (`download-github-folder.sh`) - Versione Non Ottimizzata

> ⚠️ **Nota:** Questa versione **non supporta l'autenticazione** e funziona solo con repository **pubblici**.

**Requisiti:**

- Bash shell
- **`curl`** - per il download del repository
- **`unzip`** - per l'estrazione dei file

**Installazione delle dipendenze:**

<details>
<summary>Windows (Git Bash)</summary>

Git Bash include già `curl` e `unzip`. Se non sono disponibili, reinstalla Git per Windows con l'opzione "Git Bash".

</details>

<details>
<summary>Windows (WSL)</summary>

```bash
sudo apt update
sudo apt install curl unzip
```

</details>

<details>
<summary>macOS</summary>

`curl` è preinstallato. Per `unzip` (di solito già presente):

```bash
# Con Homebrew
brew install unzip
```

</details>

<details>
<summary>Linux (Debian/Ubuntu)</summary>

```bash
sudo apt update
sudo apt install curl unzip
```

</details>

**Utilizzo:**

```bash
# Rendi lo script eseguibile (su Linux/Mac)
chmod +x download-github-folder.sh

# Download nella directory corrente
./download-github-folder.sh https://github.com/malafronte/malafronte-doc-samples/tree/main/samples-quarta/api_client_server_demos/mock-server-tutorial

# Download in una directory specifica
./download-github-folder.sh <URL> ./output
```

**Su Windows (Git Bash o WSL):**

```bash
bash download-github-folder.sh https://github.com/malafronte/malafronte-doc-samples/tree/main/samples-quarta/api_client_server_demos/mock-server-tutorial
```

### 3. Script Bash Ottimizzato (`download-github-folder-optimized.sh`) ⭐ CONSIGLIATO

**Requisiti:**

- Bash shell
- **`git`** 2.19 o superiore (per `git sparse-checkout`)

**Installazione di Git:**

<details>
<summary>Windows (Git Bash)</summary>

Scarica e installa Git per Windows da [git-scm.com](https://git-scm.com/download/win)

</details>

<details>
<summary>Windows (WSL)</summary>

```bash
sudo apt update
sudo apt install git
```

</details>

<details>
<summary>macOS</summary>

```bash
# Con Homebrew
brew install git

# Oppure scarica il pacchetto da git-scm.com
```

</details>

<details>
<summary>Linux (Debian/Ubuntu)</summary>

```bash
sudo apt update
sudo apt install git
```

</details>

**Verifica versione Git:**

```bash
git --version  # Deve essere 2.19 o superiore
```

**Utilizzo:**

```bash
# Rendi lo script eseguibile (su Linux/Mac)
chmod +x download-github-folder-optimized.sh

# Download nella directory corrente
./download-github-folder-optimized.sh https://github.com/malafronte/malafronte-doc-samples/tree/main/samples-quarta/api_client_server_demos/mock-server-tutorial

# Download in una directory specifica
./download-github-folder-optimized.sh <URL> ./output
```

**Su Windows (Git Bash o WSL):**

```bash
bash download-github-folder-optimized.sh https://github.com/malafronte/malafronte-doc-samples/tree/main/samples-quarta/api_client_server_demos/mock-server-tutorial
```

### 4. Script Python Ottimizzato (`download-github-folder-optimized.py`) ⭐ CONSIGLIATO

**Requisiti:**

- Python 3.6 o superiore
- **`git`** 2.19 o superiore installato nel sistema (per `git sparse-checkout`)
- **Nessuna dipendenza Python esterna** (usa solo librerie standard)

**Installazione di Git:**

Vedi le istruzioni di installazione Git nella sezione dello [Script Bash Ottimizzato](#3-script-bash-ottimizzato-download-github-folder-optimizedsh--consigliato) sopra.

**Verifica versione Git:**

```bash
git --version  # Deve essere 2.19 o superiore
```

**Utilizzo:**

```bash
# Download nella directory corrente
python download-github-folder-optimized.py https://github.com/malafronte/malafronte-doc-samples/tree/main/samples-quarta/api_client_server_demos/mock-server-tutorial

# Download in una directory specifica
python download-github-folder-optimized.py <URL> ./output
```

## Autenticazione con GitHub Token

Gli script **ottimizzati** supportano l'autenticazione tramite GitHub Personal Access Token per accedere a **repository privati**. Gli script non ottimizzati **non supportano** l'autenticazione e funzionano solo con repository pubblici.

### Differenza tra Script Ottimizzati e Non Ottimizzati

| Caratteristica | Script Non Ottimizzati | Script Ottimizzati |
| ---------------- | ------------------------ | ------------------- |
| **Repository pubblici** | ✅ Funzionano | ✅ Funzionano |
| **Repository privati** | ❌ Non supportati | ✅ Supportati con token |
| **Metodo di autenticazione** | Nessuno | Token GitHub |

### Come Creare un GitHub Personal Access Token

1. **Accedi a GitHub** e vai su **Settings** (click sull'avatar in alto a destra → Settings)
2. Nel menu a sinistra, scorri fino a **Developer settings** → **Personal access tokens** → **Tokens (classic)**
3. Click su **Generate new token** → **Generate new token (classic)**
4. Dai un nome al token (es. "Download GitHub Folders")
5. Seleziona lo scopo **expiration** (scadenza) a tua scelta
6. Nella sezione **Select scopes**, seleziona almeno:
   - ✅ `repo` - Accesso completo ai repository privati
7. Click su **Generate token** in fondo alla pagina
8. **Copia subito il token** (verrà mostrato solo una volta!)

> ⚠️ **Importante:** Conserva il token in modo sicuro. Non condividerlo mai in pubblico o nel codice.

### Come Usare il Token con gli Script Ottimizzati

#### Script Python Ottimizzato

**Metodo 1: Variabile d'ambiente (consigliato):**

```bash
# Windows (PowerShell)
$env:GITHUB_TOKEN="ghp_tuotokenqui"
python download-github-folder-optimized.py https://github.com/owner/private-repo/tree/main/folder

# Windows (CMD)
set GITHUB_TOKEN=ghp_tuotokenqui
python download-github-folder-optimized.py https://github.com/owner/private-repo/tree/main/folder

# Linux/macOS/Git Bash
export GITHUB_TOKEN=ghp_tuotokenqui
python download-github-folder-optimized.py https://github.com/owner/private-repo/tree/main/folder
```

**Metodo 2: Parametro da riga di comando:**

```bash
python download-github-folder-optimized.py https://github.com/owner/private-repo/tree/main/folder ./output ghp_tuotokenqui
```

**Metodo 3: File di configurazione:**

Crea un file `~/.github_token` (senza estensione) nella tua home directory con il token:

```bash
# Linux/macOS
echo "ghp_tuotokenqui" > ~/.github_token

# Windows (PowerShell)
"ghp_tuotokenqui" | Out-File -FilePath $env:USERPROFILE\.github_token -NoNewline
```

#### Script Bash Ottimizzato

**Metodo 1: Variabile d'ambiente (consigliato):**

```bash
# Linux/macOS/Git Bash/WSL
export GITHUB_TOKEN=ghp_tuotokenqui
./download-github-folder-optimized.sh https://github.com/owner/private-repo/tree/main/folder

# Oppure in un solo comando
GITHUB_TOKEN=ghp_tuotokenqui ./download-github-folder-optimized.sh https://github.com/owner/private-repo/tree/main/folder
```

**Metodo 2: Parametro da riga di comando:**

```bash
./download-github-folder-optimized.sh https://github.com/owner/private-repo/tree/main/folder ./output ghp_tuotokenqui
```

**Metodo 3: File di configurazione:**

Crea un file `~/.github_token` nella tua home directory:

```bash
echo "ghp_tuotokenqui" > ~/.github_token
chmod 600 ~/.github_token  # Imposta permessi sicuri (solo proprietario può leggere)
./download-github-folder-optimized.sh https://github.com/owner/private-repo/tree/main/folder
```

### Priorità dei Metodi di Autenticazione

Se specificati più metodi, viene usato il primo disponibile in questo ordine:

1. **Parametro da riga di comando** (più alto priorità)
2. **Variabile d'ambiente** `GITHUB_TOKEN`
3. **File `~/.github_token`**
4. **Nessuna autenticazione** (solo repository pubblici)

## Formato dell'URL

Lo script accetta URL di cartelle GitHub nel seguente formato:

```text
https://github.com/OWNER/REPO/tree/BRANCH/path/to/folder
```

**Esempi validi:**

- `https://github.com/malafronte/malafronte-doc-samples/tree/main/samples-quarta/api_client_server_demos/mock-server-tutorial`
- `https://github.com/facebook/react/tree/main/packages/react`
- `https://github.com/python/cpython/tree/main/Lib/xml`

## Confronto Prestazioni: Versione Ottimizzata vs Non Ottimizzata

### Test Eseguito su Repository: `malafronte/malafronte-doc-samples`

| Metrica | Versione Non Ottimizzata | Versione Ottimizzata | Risparmio |
| --------- | ------------------------- | ---------------------- | ----------- |
| **Dati scaricati** | 268 MB | 29 KB | **99.99%** |
| **Dimensione file finali** | 124 KB | 124 KB | - |
| **Tempo di download** | ~11 secondi | ~3 secondi | **~73% più veloce** |
| **Requisiti** | Python/curl/unzip | Git 2.19+ | - |
| **Repository privati** | ❌ Non supportati | ✅ Supportati con token | - |
| **Autenticazione** | Nessuna | GitHub Token | - |

### Perché la differenza è così enorme?

**Versione Non Ottimizzata (Python/Bash):**

1. Scarica l'**intero repository** come ZIP (268 MB nel nostro esempio)
2. Estrae solo la cartella richiesta (124 KB)
3. Elimina il resto

**Versione Ottimizzata (Git Sparse-Checkout):**

1. Clona solo i **metadati** del repository (qualche KB)
2. Scarica **solo i file** nella cartella richiesta usando `git sparse-checkout`
3. Risultato: scaricato solo ciò che serve!

### Quando usare quale versione?

🚀 **Usa la versione ottimizzata quando:**

- Git è installato (versione 2.19+)
- Il repository è grande (decine/centinaia di MB o più)
- Vuoi il massimo risparmio di banda e tempo
- Hai una connessione internet lenta o limitata
- Preferisci Python: usa `download-github-folder-optimized.py`
- Preferisci Bash: usa `download-github-folder-optimized.sh`

📦 **Usa la versione non ottimizzata quando:**

- Git non è installato e non vuoi installarlo
- Il repository è piccolo (< 10 MB)
- Hai solo Python o curl/unzip disponibili
- Preferisci Python: usa `download-github-folder.py`
- Preferisci Bash: usa `download-github-folder.sh`

## Come Funzionano

### Versione Non Ottimizzata (Python/Bash)

Gli script seguono questi passaggi:

1. **Parse dell'URL:** Estrae owner, repo, branch e percorso della cartella dall'URL
2. **Download:** Scarica l'intero repository come file ZIP dal branch specificato
3. **Estrazione selettiva:** Estrae solo i file nella cartella richiesta
4. **Pulizia:** Rimuove automaticamente i file temporanei

### Versione Ottimizzata (Git Sparse-Checkout)

Lo script segue questi passaggi:

1. **Clone parziale:** Clona solo i metadati del repository con `--filter=blob:none --no-checkout`
2. **Inizializza sparse-checkout:** Configura Git per scaricare solo cartelle specifiche
3. **Imposta cartella target:** Specifica quale cartella scaricare
4. **Checkout selettivo:** Scarica solo i file nella cartella richiesta
5. **Copia e pulizia:** Copia i file nella directory di output e pulisce

## Vantaggi rispetto ad altri metodi

### vs `git clone --sparse`

- ✅ Non richiede configurazione manuale multipla
- ✅ Più semplice da usare per utenti non tecnici
- ✅ Scarica solo una cartella specifica con un singolo comando

### vs Download manuale da GitHub

- ✅ GitHub non permette il download diretto di singole cartelle
- ✅ Automatizza il processo di estrazione selettiva
- ✅ Evita di scaricare l'intero repository manualmente

### vs Servizi online (download-directory.github.io)

- ✅ Funziona offline dopo il primo download
- ✅ Nessuna dipendenza da servizi di terze parti
- ✅ Maggiore privacy (nessun URL inviato a servizi esterni)
- ✅ Versione ottimizzata con risparmio di banda >99%

## Esempio di Output

### Output Versione Ottimizzata

```bash
📋 Informazioni Repository:
   Owner: malafronte
   Repository: malafronte-doc-samples
   Branch: main
   Cartella: samples-quarta/api_client_server_demos/mock-server-tutorial

📋 Modalità Ottimizzata con Git Sparse-Checkout
   Questo script userà git sparse-checkout per scaricare solo i file necessari.

📥 Clone parziale del repository (solo metadati)...
✅ Clone parziale completato (solo metadati scaricati)
📋 Configurazione sparse-checkout...
✅ Sparse-checkout inizializzato
📋 Impostazione cartella da scaricare: samples-quarta/api_client_server_demos/mock-server-tutorial
✅ Cartella impostata
📥 Download dei file nella cartella richiesta...
remote: Total 8 (delta 0), reused 1 (delta 0), pack-reused 5 (from 1)
Receiving objects: 100% (8/8), 29.23 KiB | 2.25 MiB/s, done.
✅ File scaricati con successo
📋 Copia dei file nella directory di output...
✅ Copia completata: /path/to/output/mock-server-tutorial

🎉 Cartella scaricata con successo!
📍 Posizione: /path/to/output/mock-server-tutorial
📊 File scaricati: 4
💾 Dimensione: 124K
🧹 Pulizia completata
```

## FAQ - Domande Frequenti

### Qual è la differenza tra gli script ottimizzati e quelli non ottimizzati?

| Aspetto | Script Non Ottimizzati | Script Ottimizzati |
| --------- | ------------------------ | ------------------- |
| **Metodo** | Download ZIP intero + estrazione | Git sparse-checkout |
| **Velocità** | Più lento per repo grandi | Molto più veloce |
| **Repository privati** | ❌ Non supportati | ✅ Supportati con token |
| **Autenticazione** | Nessuna | GitHub Personal Access Token |
| **Requisiti** | Python/curl/unzip | Git 2.19+ |

### Posso usare gli script con repository privati?

- **Script non ottimizzati:** ❌ No, funzionano solo con repository pubblici.
- **Script ottimizzati:** ✅ Sì, è necessario un GitHub Personal Access Token. Vedi la sezione [Autenticazione con GitHub Token](#autenticazione-con-github-token) per istruzioni dettagliate.

### Dove devo salvare il token GitHub?

Puoi usare uno di questi metodi (in ordine di priorità):

1. **Parametro da riga di comando** (più sicuro per uso occasionale)
2. **Variabile d'ambiente `GITHUB_TOKEN`** (consigliata per uso frequente)
3. **File `~/.github_token`** (comodo ma meno sicuro)

> ⚠️ **Mai salvare il token nel codice o condividerlo!**

### Lo script dice "Authentication failed" - cosa fare?

1. Verifica che il token sia valido su GitHub → Settings → Developer settings → Personal access tokens
2. Assicurati che il token abbia il permesso `repo` per accedere ai repository privati
3. Controlla che il token non sia scaduto
4. Verifica di aver copiato l'intero token (inizia con `ghp_`, `github_pat_`, etc.)

### Posso usare lo stesso token su più computer?

Sì, ma è consigliato creare un token separato per ogni dispositivo per motivi di sicurezza. Se un dispositivo viene compromesso, puoi revocare solo quel token senza influenzare gli altri.

### Quanto è sicuro usare il token con questi script?

- Il token viene usato solo per l'autenticazione con GitHub
- Non viene mai salvato nei log degli script (viene mascherato)
- Se usato come variabile d'ambiente, esiste solo per la sessione corrente
- Se salvato in `~/.github_token`, assicurati di impostare permessi restrittivi: `chmod 600 ~/.github_token`

## Risoluzione dei Problemi

### Errore: "URL non valido"

Assicurati che l'URL sia nel formato corretto e punti a una **cartella** (non un file) di GitHub.

### Errore: "Cartella non trovata nel repository"

Verifica che:

- L'URL sia corretto
- Il branch esista
- Il percorso della cartella sia giusto (controlla le maiuscole/minuscole)

### Errore: "Git non è installato" (solo versione ottimizzata)

Installa Git o usa la versione non ottimizzata che non richiede Git.

### Errore di download

Controlla la tua connessione internet e assicurati che il repository sia pubblico.

## Note

- Gli script funzionano solo con repository **pubblici**
- I repository privati richiedono autenticazione aggiuntiva
- I file temporanei vengono salvati in una cartella nascosta `.temp_github_download` (versione non ottimizzata) o `REPO_temp_clone` (versione ottimizzata)
- La cartella scaricata prende il nome dell'ultima sottocartella nell'URL
- La versione ottimizzata richiede Git 2.19 o superiore per supportare `git sparse-checkout`

## Licenza

Questi script sono forniti con licenza MIT.
