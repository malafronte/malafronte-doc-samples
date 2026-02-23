#!/bin/bash

################################################################################
# Script Ottimizzato per scaricare una specifica sottocartella da GitHub
# Usa git sparse-checkout per scaricare solo i file necessari (non l'intero repo)
#
# Vantaggi:
# - Scarica solo i metadati del repository (pochi KB/MB)
# - Scarica solo i file nella cartella richiesta
# - Molto più veloce per repository grandi
#
# Esempio di utilizzo:
#   ./download-github-folder-optimized.sh https://github.com/malafronte/malafronte-doc-samples/tree/main/samples-quarta/api_client_server_demos/mock-server-tutorial
################################################################################

# Colori per l'output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funzione per stampare messaggi colorati
print_info() {
    echo -e "${BLUE}📋 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_download() {
    echo -e "${YELLOW}📥 $1${NC}"
}

# Funzione per mostrare l'uso dello script
show_usage() {
    echo "Utilizzo:"
    echo "  $0 <URL_CARTELLA> [DIRECTORY_OUTPUT] [TOKEN]"
    echo ""
    echo "Autenticazione (per repository privati):"
    echo "  1. Variabile d'ambiente: GITHUB_TOKEN=<token>"
    echo "  2. Parametro: <URL> [OUTPUT] <token>"
    echo "  3. File ~/.github_token (contenuto: token)"
    echo ""
    echo "Esempi:"
    echo "  $0 https://github.com/malafronte/malafronte-doc-samples/tree/main/samples-quarta/api_client_server_demos/mock-server-tutorial"
    echo "  $0 <URL> ./output"
    echo "  GITHUB_TOKEN=ghp_xxx $0 <URL>"
    echo "  $0 <URL> ./output ghp_xxx"
    exit 1
}

# Funzione per leggere token da file di configurazione
get_token_from_file() {
    local token_file="$HOME/.github_token"
    local line=""
    if [ -f "$token_file" ]; then
        # Leggi prima riga non vuota, rimuovi whitespace con parameter expansion
        while IFS= read -r line; do
            # Salta righe vuote (rimuovi tutti i whitespace e controlla)
            # shellcheck disable=SC2001
            [ -z "${line//[[:space:]]/}" ] && continue
            # Rimuovi tutti i whitespace
            echo "${line//[[:space:]]/}"
            return
        done < "$token_file"
    fi
}

# Funzione per costruire l'URL autenticato
build_authenticated_url() {
    local url="$1"
    local token="$2"

    if [ -n "$token" ]; then
        # Inserisce il token nell'URL: https://<token>@github.com/owner/repo.git
        echo "${url/https:\/\//https://${token}@}"
    else
        echo "$url"
    fi
}

# Verifica argomenti
if [ $# -lt 1 ]; then
    print_error "URL della cartella non specificato"
    echo ""
    show_usage
fi

FOLDER_URL="$1"
OUTPUT_DIR="."
TOKEN=""

# Leggi token da variabile d'ambiente GITHUB_TOKEN
ENV_TOKEN="${GITHUB_TOKEN}"

# Se non c'è in variabile d'ambiente, prova dal file
if [ -z "$ENV_TOKEN" ]; then
    ENV_TOKEN=$(get_token_from_file)
fi

if [ $# -ge 3 ]; then
    # Formato: <URL> <output> <token>
    OUTPUT_DIR="$2"
    TOKEN="$3"
elif [ $# -ge 2 ]; then
    # Controlla se l'argomento 2 è un token o una directory
    arg2="$2"
    case "$arg2" in
        ghp_*|github_pat_*|gho_*|ghu_*|ghs_*)
            TOKEN="$arg2"
            ;;
        *)
            OUTPUT_DIR="$arg2"
            ;;
    esac
fi

# Usa token da variabile d'ambiente se non passato come argomento
if [ -z "$TOKEN" ] && [ -n "$ENV_TOKEN" ]; then
    TOKEN="$ENV_TOKEN"
fi

# Converti OUTPUT_DIR in percorso assoluto
mkdir -p "$OUTPUT_DIR" 2>/dev/null
cd "$OUTPUT_DIR" || {
    print_error "Directory di output non valida: $OUTPUT_DIR"
    exit 1
}
ABSOLUTE_OUTPUT_DIR=$(pwd)
cd - > /dev/null || exit 1

# Verifica che git sia installato
if ! command -v git &> /dev/null; then
    print_error "Git non è installato. Installa Git per usare questo script ottimizzato."
    echo "Oppure usa la versione non ottimizzata che non richiede Git."
    exit 1
fi

# Parsa l'URL GitHub
# Pattern: https://github.com/owner/repo/tree/branch/path/to/folder
if [[ ! "$FOLDER_URL" =~ ^https://github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.+)$ ]]; then
    print_error "URL non valido"
    echo "Il formato deve essere: https://github.com/owner/repo/tree/branch/path/to/folder"
    exit 1
fi

OWNER="${BASH_REMATCH[1]}"
REPO="${BASH_REMATCH[2]}"
BRANCH="${BASH_REMATCH[3]}"
FOLDER_PATH="${BASH_REMATCH[4]}"

# Estrae il nome della cartella finale
FOLDER_NAME=$(basename "$FOLDER_PATH")

# Nome temporaneo del clone (percorso assoluto)
TEMP_REPO_NAME="${REPO}_temp_clone"
WORK_DIR="${ABSOLUTE_OUTPUT_DIR}/${TEMP_REPO_NAME}"

echo ""
print_info "Informazioni Repository:"
echo "   Owner: $OWNER"
echo "   Repository: $REPO"
echo "   Branch: $BRANCH"
echo "   Cartella: $FOLDER_PATH"
echo ""

print_info "Modalità Ottimizzata con Git Sparse-Checkout"
echo "   Questo script userà git sparse-checkout per scaricare solo i file necessari."
echo ""

if [ -n "$TOKEN" ]; then
    print_info "Autenticazione con token GitHub"
fi

# Crea directory di output
mkdir -p "$ABSOLUTE_OUTPUT_DIR"

# Funzione di pulizia
# NOTA PER GLI STUDENTI:
# Questa funzione rimuove la directory temporanea creata durante l'esecuzione.
# Non viene chiamata direttamente nel codice, ma è registrata con 'trap' qui sotto.
# shellcheck disable=SC2329
cleanup() {
    if [ -d "$WORK_DIR" ]; then
        rm -rf "$WORK_DIR"
        echo -e "\n${GREEN}🧹 Pulizia completata${NC}"
    fi
}

# NOTA - IL COMANDO TRAP:
# 'trap' è un meccanismo di Bash che cattura segnali ed eventi.
# 'trap cleanup EXIT' dice a Bash: "quando lo script termina (EXIT),
# esegui automaticamente la funzione cleanup()".
#
# Questo garantisce che:
# 1. La directory temporanea venga sempre rimossa, anche se lo script fallisce
# 2. Non serva chiamare cleanup() manualmente in ogni punto di uscita
# 3. Il sistema rimanga pulito anche in caso di errori imprevisti
#
# ShellCheck potrebbe segnalare che cleanup() "non viene invocata" -
# è un falso positivo perché non rileva l'invocazione indiretta tramite trap.
trap cleanup EXIT

# Step 1: Clone parziale (solo metadati)
print_download "Clone parziale del repository (solo metadati)..."
GIT_REPO_URL="https://github.com/${OWNER}/${REPO}.git"

# Usa URL autenticato se token è presente
AUTH_GIT_REPO_URL=$(build_authenticated_url "$GIT_REPO_URL" "$TOKEN")

if ! git clone --filter=blob:none --no-checkout "$AUTH_GIT_REPO_URL" "$WORK_DIR" 2>/dev/null; then
    print_error "Errore durante il clone del repository"
    exit 1
fi
print_success "Clone parziale completato (solo metadati scaricati)"

# Step 2: Configura sparse-checkout
cd "$WORK_DIR" || exit 1

print_info "Configurazione sparse-checkout..."

if ! git sparse-checkout init --cone; then
    print_error "Errore durante l'inizializzazione di sparse-checkout"
    exit 1
fi

print_success "Sparse-checkout inizializzato"

# Step 3: Imposta la cartella da scaricare
print_info "Impostazione cartella da scaricare: $FOLDER_PATH"

if ! git sparse-checkout set "$FOLDER_PATH"; then
    print_error "Errore durante l'impostazione della cartella"
    exit 1
fi

print_success "Cartella impostata"

# Step 4: Checkout dei file
print_download "Download dei file nella cartella richiesta..."

if ! git checkout; then
    print_error "Errore durante il checkout"
    exit 1
fi

print_success "File scaricati con successo"

# Step 5: Sposta i file nella directory di output
EXTRACT_PATH="${ABSOLUTE_OUTPUT_DIR}/${FOLDER_NAME}"
print_info "Copia dei file nella directory di output..."

# Copia la cartella usando percorsi assoluti
mkdir -p "$EXTRACT_PATH"
cp -r "${WORK_DIR}/${FOLDER_PATH}"/* "$EXTRACT_PATH/"

print_success "Copia completata: $EXTRACT_PATH"

# Mostra le statistiche
FILE_COUNT=$(find "$EXTRACT_PATH" -type f | wc -l)
DIR_SIZE=$(du -sh "$EXTRACT_PATH" | cut -f1)

echo ""
echo -e "${GREEN}🎉 Cartella scaricata con successo!${NC}"
echo -e "${BLUE}📍 Posizione: $EXTRACT_PATH${NC}"
echo -e "${BLUE}📊 File scaricati: $FILE_COUNT${NC}"
echo -e "${BLUE}💾 Dimensione: $DIR_SIZE${NC}"

exit 0