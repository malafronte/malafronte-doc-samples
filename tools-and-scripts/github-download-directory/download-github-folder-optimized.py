#!/usr/bin/env python3
# ruff: noqa: T201
"""Download a specific subfolder from GitHub.

Script Ottimizzato per scaricare una specifica sottocartella da GitHub
Usa git sparse-checkout per scaricare solo i file necessari (non l'intero repo)

Vantaggi:
- Scarica solo i metadati del repository (pochi KB/MB)
- Scarica solo i file nella cartella richiesta
- Molto più veloce per repository grandi

Esempio di utilizzo:
    python download-github-folder-optimized.py https://github.com/malafronte/malafronte-doc-samples/tree/main/samples-quarta/api_client_server_demos/mock-server-tutorial
"""

from __future__ import annotations

import contextlib
import os
import re
import shutil
import stat
import subprocess
import sys
import time
from collections.abc import Callable  # noqa: TC003
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from subprocess import CompletedProcess


def print_info(message: str) -> None:
    """Stampa un messaggio informativo."""
    print(f"📋 {message}")


def print_success(message: str) -> None:
    """Stampa un messaggio di successo."""
    print(f"✅ {message}")


def print_error(message: str) -> None:
    """Stampa un messaggio di errore."""
    print(f"❌ {message}")


def print_download(message: str) -> None:
    """Stampa un messaggio di download."""
    print(f"📥 {message}")


# Git version requirements for sparse-checkout support
GIT_REQUIRED_MAJOR_VERSION = 2
GIT_REQUIRED_MINOR_VERSION = 19

# Costanti per calcoli di dimensione
BYTES_PER_KB = 1024
BYTES_PER_MB = 1024 * 1024

# Indici per argomenti da riga di comando
URL_ARG_INDEX = 1
OUTPUT_DIR_ARG_INDEX = 2
TOKEN_ARG_INDEX = 3
MIN_ARGS_FOR_OUTPUT_DIR = 3
MIN_ARGS_FOR_TOKEN = 4
MIN_REQUIRED_ARGS = 2

# Nome variabile d'ambiente per il token
GITHUB_TOKEN_ENV_VAR = "GITHUB_TOKEN"

# Messaggi di errore
MSG_GIT_TOO_OLD = "Git versione {} è troppo vecchia. Richiesto Git {}.{} o superiore."
MSG_GIT_NOT_INSTALLED = (
    "Git non è installato. Installa Git {}.{} "
    "o superiore per usare questo script ottimizzato."
)


class GitNotInstalledError(Exception):
    """Eccezione sollevata quando Git non è installato o è troppo vecchio."""

    def __init__(self: GitNotInstalledError, message: str) -> None:
        """Inizializza l'eccezione con un messaggio."""
        super().__init__(message)
        self.message = message


class InvalidGitHubUrlError(Exception):
    """Eccezione sollevata quando l'URL GitHub non è valido."""

    def __init__(self: InvalidGitHubUrlError) -> None:
        """Inizializza l'eccezione con il messaggio predefinito."""
        super().__init__(
            "URL non valido. Il formato deve essere: "
            "https://github.com/owner/repo/tree/branch/path/to/folder",
        )


def _is_git_version_compatible(version_str: str) -> bool:
    """Verifica se la versione di Git è compatibile."""
    version_parts = version_str.rsplit(maxsplit=1)[-1].split(".")
    major, minor = int(version_parts[0]), int(version_parts[1])
    if major > GIT_REQUIRED_MAJOR_VERSION:
        return True
    return major == GIT_REQUIRED_MAJOR_VERSION and minor >= GIT_REQUIRED_MINOR_VERSION


def check_git_installed() -> bool:
    """Verifica se Git è installato."""
    git_path = shutil.which("git")
    if git_path is None:
        msg = MSG_GIT_NOT_INSTALLED.format(
            GIT_REQUIRED_MAJOR_VERSION,
            GIT_REQUIRED_MINOR_VERSION,
        )
        raise GitNotInstalledError(msg)

    try:
        result = subprocess.run(  # noqa: S603
            [git_path, "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        version_str = result.stdout.strip()
        if _is_git_version_compatible(version_str):
            return True
        msg = MSG_GIT_TOO_OLD.format(
            version_str,
            GIT_REQUIRED_MAJOR_VERSION,
            GIT_REQUIRED_MINOR_VERSION,
        )
        raise GitNotInstalledError(msg)
    except subprocess.CalledProcessError as e:
        msg = MSG_GIT_NOT_INSTALLED.format(
            GIT_REQUIRED_MAJOR_VERSION,
            GIT_REQUIRED_MINOR_VERSION,
        )
        raise GitNotInstalledError(msg) from e
    except FileNotFoundError as e:
        msg = MSG_GIT_NOT_INSTALLED.format(
            GIT_REQUIRED_MAJOR_VERSION,
            GIT_REQUIRED_MINOR_VERSION,
        )
        raise GitNotInstalledError(msg) from e
    except IndexError as e:
        msg = MSG_GIT_NOT_INSTALLED.format(
            GIT_REQUIRED_MAJOR_VERSION,
            GIT_REQUIRED_MINOR_VERSION,
        )
        raise GitNotInstalledError(msg) from e


def parse_github_folder_url(url: str) -> dict[str, str]:
    """Parsa un URL di cartella GitHub ed estrae le informazioni necessarie.

    Args:
        url: URL della cartella GitHub

    Returns:
        dict: Contiene owner, repo, branch, folder_path

    """
    # Pattern per URL GitHub: https://github.com/owner/repo/tree/branch/path/to/folder
    pattern = r"https://github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.+)"
    match = re.match(pattern, url)

    if not match:
        raise InvalidGitHubUrlError

    return {
        "owner": match.group(1),
        "repo": match.group(2),
        "branch": match.group(3),
        "folder_path": match.group(4),
    }


def run_command(
    command: list[str],
    cwd: str | Path | None = None,
    check: bool = True,  # noqa: FBT001, FBT002
) -> CompletedProcess[str]:
    """Esegue un comando subprocess e restituisce il risultato.

    Args:
        command: Lista con il comando e gli argomenti
        cwd: Directory di lavoro
        check: Se True, solleva un'eccezione se il comando fallisce

    Returns:
        subprocess.CompletedProcess

    """
    try:
        return subprocess.run(  # noqa: S603
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=check,
        )
    except subprocess.CalledProcessError as e:
        print_error(f"Errore durante l'esecuzione del comando: {' '.join(command)}")
        if e.stderr:
            print_error(f"Dettagli: {e.stderr.strip()}")
        raise


def copy_folder_contents(source: Path, destination: Path) -> None:
    """Copia il contenuto di una cartella in un'altra.

    Args:
        source: Percorso della cartella sorgente
        destination: Percorso della cartella di destinazione

    """
    for item in source.iterdir():
        if item.is_file():
            shutil.copy2(item, destination / item.name)
        elif item.is_dir():
            shutil.copytree(item, destination / item.name, dirs_exist_ok=True)


def _format_size(total_size: int) -> str:
    """Formatta la dimensione in formato leggibile."""
    size_kb = total_size / BYTES_PER_KB
    if size_kb < BYTES_PER_KB:
        return f"{size_kb:.0f}K"
    return f"{size_kb / BYTES_PER_KB:.1f}M"


def print_download_stats(extract_path: Path) -> None:
    """Stampa le statistiche del download.

    Args:
        extract_path: Percorso della cartella scaricata

    """
    file_count = sum(1 for _ in extract_path.rglob("*") if _.is_file())
    total_size = sum(f.stat().st_size for f in extract_path.rglob("*") if f.is_file())
    size_str = _format_size(total_size)

    print("\n🎉 Cartella scaricata con successo!")
    print(f"📍 Posizione: {extract_path.absolute()}")
    print(f"📊 File scaricati: {file_count}")
    print(f"💾 Dimensione: {size_str}")


def _print_repo_info(info: dict[str, str]) -> None:
    """Stampa le informazioni del repository."""
    print("\n📋 Informazioni Repository:")
    print(f"   Owner: {info['owner']}")
    print(f"   Repository: {info['repo']}")
    print(f"   Branch: {info['branch']}")
    print(f"   Cartella: {info['folder_path']}")
    print()


def _print_mode_info() -> None:
    """Stampa le informazioni sulla modalità di download."""
    print_info("Modalità Ottimizzata con Git Sparse-Checkout")
    print(
        "   Questo script userà git sparse-checkout per "
        "scaricare solo i file necessari.",
    )
    print()


def _build_authenticated_url(git_repo_url: str, token: str | None) -> str:
    """Costruisce l'URL del repository con autenticazione token.

    Args:
        git_repo_url: URL originale del repository
        token: Token di accesso GitHub (opzionale)

    Returns:
        str: URL con token incorporato se fornito

    """
    if not token:
        return git_repo_url

    # Inserisce il token nell'URL: https://<token>@github.com/owner/repo.git
    if git_repo_url.startswith("https://"):
        return git_repo_url.replace("https://", f"https://{token}@")

    return git_repo_url


def _clone_repository(
    git_repo_url: str,
    work_dir: Path,
    output_path: Path,
    token: str | None = None,
) -> None:
    """Clona il repository con filtro blob:none (solo metadati).

    Args:
        git_repo_url: URL del repository
        work_dir: Directory di lavoro
        output_path: Directory di output
        token: Token di accesso GitHub (opzionale)

    """
    print_download("Clone parziale del repository (solo metadati)...")

    # Usa URL autenticato se token è presente
    auth_url = _build_authenticated_url(git_repo_url, token)

    run_command(
        [
            "git",
            "clone",
            "--filter=blob:none",
            "--no-checkout",
            auth_url,
            str(work_dir),
        ],
        cwd=str(output_path),
        check=True,
    )
    print_success("Clone parziale completato (solo metadati scaricati)")


def _setup_sparse_checkout(work_dir: Path, folder_path: str) -> None:
    """Configura sparse-checkout per scaricare solo la cartella richiesta."""
    print_info("Configurazione sparse-checkout...")
    run_command(
        ["git", "sparse-checkout", "init", "--cone"],
        cwd=str(work_dir),
        check=True,
    )
    print_success("Sparse-checkout inizializzato")

    print_info(f"Impostazione cartella da scaricare: {folder_path}")
    run_command(
        ["git", "sparse-checkout", "set", folder_path],
        cwd=str(work_dir),
        check=True,
    )
    print_success("Cartella impostata")


def _checkout_files(work_dir: Path) -> None:
    """Esegue il checkout dei file richiesti."""
    print_download("Download dei file nella cartella richiesta...")
    run_command(["git", "checkout"], cwd=str(work_dir), check=True)
    print_success("File scaricati con successo")


def _copy_downloaded_files(
    work_dir: Path,
    output_path: Path,
    folder_path: str,
) -> Path:
    """Copia i file scaricati nella directory di output."""
    extract_path = output_path / Path(folder_path).name
    print_info("Copia dei file nella directory di output...")

    extract_path.mkdir(parents=True, exist_ok=True)
    source_folder = work_dir / folder_path
    copy_folder_contents(source_folder, extract_path)

    print_success(f"Copia completata: {extract_path}")
    return extract_path


def _remove_readonly(
    func: Callable[[str], None],
    path: str,
    _excinfo: tuple,
) -> None:
    """Gestore di errori per rimuovere file/directory read-only (Windows).

    Args:
        func: Funzione che ha generato l'errore
        path: Percorso del file/directory
        _excinfo: Informazioni sull'eccezione (non usato)

    """
    # Prova più volte con ritardo (utile se Git ha ancora handle aperti)
    for _ in range(3):
        try:
            # Rimuovi l'attributo read-only
            Path(path).chmod(stat.S_IWRITE)
            func(path)
        except OSError:  # noqa: PERF203
            time.sleep(0.2)  # Breve attesa prima di riprovare
        else:
            return


def _cleanup_work_dir(work_dir: Path) -> None:
    """Pulisce la directory temporanea di lavoro.

    Gestisce anche i file read-only creati da Git su Windows.

    """
    if not work_dir.exists():
        return

    # Attendi brevemente per dare tempo a Git di rilasciare gli handle
    time.sleep(0.3)

    # Primo tentativo: rmtree con gestione errori per file read-only
    with contextlib.suppress(PermissionError, OSError):
        shutil.rmtree(work_dir, onerror=_remove_readonly)

    # Secondo tentativo: rmtree con ignore_errors=True
    if work_dir.exists():
        with contextlib.suppress(PermissionError, OSError):
            shutil.rmtree(work_dir, ignore_errors=True)

    # Terzo tentativo: rimozione manuale ricorsiva con ritardo
    if work_dir.exists():
        _force_remove_directory(work_dir)

    if work_dir.exists():
        print(
            "\n⚠️  Attenzione: Impossibile rimuovere "
            "completamente la directory temporanea.",
        )
        print(f"   {work_dir}")
        print("   Puoi rimuoverla manualmente se necessario.")
    else:
        print("\n🧹 Pulizia completata")


def _force_remove_directory(path: Path) -> None:
    """Forza la rimozione di una directory e tutto il suo contenuto.

    Args:
        path: Percorso della directory da rimuovere

    """
    for item in path.rglob("*"):
        with contextlib.suppress(PermissionError, OSError):
            # Rimuovi attributi read-only e nascosti
            item.chmod(stat.S_IWRITE)
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                item.rmdir()

    # Prova a rimuovere la directory stessa
    for _ in range(3):
        try:
            path.rmdir()
        except (PermissionError, OSError):  # noqa: PERF203
            time.sleep(0.2)
        else:
            return


def _handle_download_error(error: Exception) -> None:
    """Gestisce gli errori durante il download."""
    print_error(f"\nErrore durante il download: {error}")
    sys.exit(1)


def download_github_folder_optimized(
    folder_url: str,
    output_dir: str = ".",
    token: str | None = None,
) -> Path | None:
    """Funzione principale ottimizzata per scaricare una cartella da GitHub.

    Args:
        folder_url: URL della cartella GitHub
        output_dir: Directory dove salvare la cartella (default: directory corrente)
        token: Token di accesso GitHub (opzionale)

    """
    output_path = Path(output_dir).absolute()
    output_path.mkdir(parents=True, exist_ok=True)

    info = parse_github_folder_url(folder_url)
    _print_repo_info(info)
    _print_mode_info()

    # Mostra info su autenticazione
    if token:
        print_info("Autenticazione con token GitHub")
    elif os.environ.get(GITHUB_TOKEN_ENV_VAR):
        print_info("Autenticazione con token da variabile d'ambiente")

    temp_repo_name = f"{info['repo']}_temp_clone"
    work_dir = output_path / temp_repo_name
    git_repo_url = f"https://github.com/{info['owner']}/{info['repo']}.git"

    try:
        _clone_repository(git_repo_url, work_dir, output_path, token)
        _setup_sparse_checkout(work_dir, info["folder_path"])
        _checkout_files(work_dir)
        extract_path = _copy_downloaded_files(
            work_dir,
            output_path,
            info["folder_path"],
        )
        print_download_stats(extract_path)
        return extract_path  # noqa: TRY300

    except (subprocess.CalledProcessError, shutil.Error, OSError) as e:
        _handle_download_error(e)
    finally:
        _cleanup_work_dir(work_dir)

    return None


def _print_usage() -> None:
    """Stampa le istruzioni di utilizzo."""
    print("\nUtilizzo:")
    print(
        "  python download-github-folder-optimized.py "
        "<URL_CARTELLA> [DIRECTORY_OUTPUT] [TOKEN]",
    )
    print("\nAutenticazione (per repository privati):")
    print(f"  1. Variabile d'ambiente: ${GITHUB_TOKEN_ENV_VAR}=<token>")
    print("  2. Parametro: <URL> [OUTPUT] <token>")
    print("\nEsempi:")
    print(
        "  python download-github-folder-optimized.py "
        "https://github.com/malafronte/malafronte-doc-samples/"
        "tree/main/samples-quarta/api_client_server_demos/"
        "mock-server-tutorial",
    )
    print("  python download-github-folder-optimized.py <URL> ./output")
    print(
        f"  {GITHUB_TOKEN_ENV_VAR}=ghp_xxx python download-github-folder-optimized.py "
        "<URL>",
    )
    print("  python download-github-folder-optimized.py <URL> ./output ghp_xxx")


def _parse_args(args: list[str]) -> tuple[str, str, str | None]:
    """Parsa gli argomenti da riga di comando.

    Args:
        args: Lista degli argomenti (sys.argv)

    Returns:
        tuple: (folder_url, output_dir, token)

    """
    if len(args) < MIN_REQUIRED_ARGS:
        print_error("URL della cartella non specificato")
        _print_usage()
        sys.exit(1)

    folder_url = args[URL_ARG_INDEX]
    output_dir = "."
    token = None

    # Cerca token in variabile d'ambiente
    env_token = os.environ.get(GITHUB_TOKEN_ENV_VAR)

    if len(args) >= MIN_ARGS_FOR_TOKEN:
        # Formato: <URL> <output> <token>
        output_dir = args[OUTPUT_DIR_ARG_INDEX]
        token = args[TOKEN_ARG_INDEX]
    elif len(args) >= MIN_ARGS_FOR_OUTPUT_DIR:
        # Controlla se l'argomento 2 è un token (inizia con ghp_, github_pat_, ecc.)
        # o una directory
        arg2 = args[OUTPUT_DIR_ARG_INDEX]
        if arg2.startswith(("ghp_", "github_pat_", "gho_", "ghu_", "ghs_")):
            token = arg2
        else:
            output_dir = arg2

    # Usa token da variabile d'ambiente se non passato come argomento
    if not token and env_token:
        token = env_token

    return folder_url, output_dir, token


def main() -> None:
    """Funzione principale con gestione argomenti da riga di comando."""
    try:
        if not check_git_installed():
            sys.exit(1)
    except GitNotInstalledError as e:
        print_error(str(e))
        print("Oppure usa la versione non ottimizzata che non richiede Git.")
        sys.exit(1)

    folder_url, output_dir, token = _parse_args(sys.argv)

    download_github_folder_optimized(folder_url, output_dir, token)


if __name__ == "__main__":
    main()
