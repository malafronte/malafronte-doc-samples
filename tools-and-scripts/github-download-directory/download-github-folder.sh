#!/bin/bash

################################################################################
# Script per scaricare una specifica sottocartella da un repository GitHub
# Supporta URL di cartelle GitHub e scarica solo la cartella richiesta
#
# Esempio di utilizzo:
#   ./download-github-folder.sh https://github.com/malafronte/malafronte-doc-samples/tree/main/samples-quarta/api_client_server_demos/mock-server-tutorial
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
    echo "  $0 <URL_CARTELLA> [DIRECTORY_OUTPUT]"
    echo ""
    echo "Esempio:"
    echo "  $0 https://github.com/malafronte/malafronte-doc-samples/tree/main/samples-quarta/api_client_server_demos/mock-server-tutorial"
    echo "  $0 <URL> ./output"
    exit 1
}

# Verifica argomenti
if [ $# -lt 1 ]; then
    print_error "URL della cartella non specificato"
    echo ""
    show_usage
fi

FOLDER_URL="$1"
OUTPUT_DIR="${2:-.}"

# Directory temporanea
TEMP_DIR="${OUTPUT_DIR}/.temp_github_download"
mkdir -p "$TEMP_DIR"

# Funzione di pulizia
# NOTA PER GLI STUDENTI:
# Questa funzione rimuove la directory temporanea creata durante l'esecuzione.
# Non viene chiamata direttamente nel codice, ma è registrata con 'trap' qui sotto.
# shellcheck disable=SC2329
cleanup() {
    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
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

echo ""
print_info "Informazioni Repository:"
echo "   Owner: $OWNER"
echo "   Repository: $REPO"
echo "   Branch: $BRANCH"
echo "   Cartella: $FOLDER_PATH"
echo ""

# Costruisci URL del ZIP del repository
ZIP_URL="https://github.com/${OWNER}/${REPO}/archive/refs/heads/${BRANCH}.zip"
ZIP_FILE="${TEMP_DIR}/${REPO}-${BRANCH}.zip"

# Scarica il repository
print_download "Download del repository da: $ZIP_URL"
if ! curl -L -o "$ZIP_FILE" "$ZIP_URL"; then
    print_error "Errore durante il download del repository"
    exit 1
fi
print_success "Download completato: $ZIP_FILE"

# Crea directory di output
EXTRACT_PATH="${OUTPUT_DIR}/${FOLDER_NAME}"
mkdir -p "$EXTRACT_PATH"

# Estrai solo la cartella specificata
ZIP_ROOT="${REPO}-${BRANCH}"
FULL_FOLDER_PATH="${ZIP_ROOT}/${FOLDER_PATH}"

print_info "Estrazione della cartella: $FOLDER_PATH"

# Usa unzip per estrarre solo i file nella cartella specificata
if ! unzip -o "$ZIP_FILE" "${FULL_FOLDER_PATH}/*" -d "$TEMP_DIR" 2>/dev/null; then
    # Fallback: estrai e poi sposta i file
    print_info "Tentativo alternativo di estrazione..."
    unzip -q -o "$ZIP_FILE" -d "$TEMP_DIR" || {
        print_error "Errore durante l'estrazione"
        exit 1
    }
fi

# Verifica che la cartella esista
EXTRACTED_FOLDER="${TEMP_DIR}/${FULL_FOLDER_PATH}"
if [ ! -d "$EXTRACTED_FOLDER" ]; then
    print_error "Cartella '$FOLDER_PATH' non trovata nel repository"
    exit 1
fi

# Sposta i file nella directory di output
print_info "Copia dei file nella directory di output..."
cp -r "${EXTRACTED_FOLDER}"/* "$EXTRACT_PATH/"

print_success "Estrazione completata: $EXTRACT_PATH"

# Mostra il percorso assoluto
ABSOLUTE_PATH=$(cd "$EXTRACT_PATH" && pwd)
echo ""
echo -e "${GREEN}🎉 Cartella scaricata con successo!${NC}"
echo -e "${BLUE}📍 Posizione: $ABSOLUTE_PATH${NC}"

exit 0