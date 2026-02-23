#!/usr/bin/env python3
"""Script per scaricare una specifica sottocartella da un repository GitHub.

Supporta URL di cartelle GitHub e scarica solo la cartella richiesta come ZIP.

Esempio di utilizzo:
    python download-github-folder.py https://github.com/malafronte/malafronte-doc-samples/tree/main/samples-quarta/api_client_server_demos/mock-server-tutorial
"""

import re
import shutil
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

# Costanti
ARGUMENT_COUNT_ERROR = 2
EXIT_ERROR = 1


def parse_github_folder_url(url: str) -> dict[str, str]:
    """Parsa un URL di cartella GitHub ed estrae le informazioni necessarie.

    Args:
        url: URL della cartella GitHub.

    Returns:
        Dict: Contiene owner, repo, branch, folder_path.

    """
    # Pattern per URL GitHub: https://github.com/owner/repo/tree/branch/path/to/folder
    pattern = r"https://github\.com/([^/]+)/([^/]+)/tree/([^/]+)/(.+)"
    match = re.match(pattern, url)

    if not match:
        msg = (
            "URL non valido. Il formato deve essere: "
            "https://github.com/owner/repo/tree/branch/path/to/folder"
        )
        raise ValueError(msg)

    return {
        "owner": match.group(1),
        "repo": match.group(2),
        "branch": match.group(3),
        "folder_path": match.group(4),
    }


def download_repository_zip(
    owner: str,
    repo: str,
    branch: str,
    temp_dir: Path,
) -> Path:
    """Scarica il repository completo come file ZIP.

    Args:
        owner: Proprietario del repository.
        repo: Nome del repository.
        branch: Branch da scaricare.
        temp_dir: Directory temporanea.

    Returns:
        Path: Percorso del file ZIP scaricato.

    """
    zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"
    zip_path = Path(temp_dir) / f"{repo}-{branch}.zip"

    print(f"📥 Download del repository da: {zip_url}")  # noqa: T201

    try:
        with (
            urllib.request.urlopen(zip_url) as response,  # noqa: S310
            Path.open(zip_path, "wb") as out_file,
        ):
            shutil.copyfileobj(response, out_file)
    except urllib.error.URLError as e:
        msg = f"Errore durante il download: {e}"
        raise ConnectionError(msg) from e
    else:
        print(f"✅ Download completato: {zip_path}")  # noqa: T201
        return zip_path


def _ensure_dir(path: Path) -> None:
    """Crea la directory, rimuovendo eventuali file con lo stesso nome.

    Args:
        path: Percorso della directory da creare.

    """
    # Se esiste un file con questo nome, rimuovilo
    if path.exists() and path.is_file():
        path.unlink()
    # Se non esiste, crealo (e le parent se necessario)
    if not path.exists():
        # Prima assicurati che le parent siano directory (non file)
        for parent in path.parents:
            if parent.exists() and parent.is_file():
                parent.unlink()
                break  # Solo il primo file trovato va rimosso
        path.mkdir(parents=True, exist_ok=True)


def extract_folder_from_zip(
    zip_path: Path,
    repo_name: str,
    branch: str,
    folder_path: str,
    output_dir: Path,
) -> Path:
    """Estrae solo la cartella specificata dal file ZIP.

    Args:
        zip_path: Percorso del file ZIP.
        repo_name: Nome del repository.
        branch: Branch del repository.
        folder_path: Percorso della cartella da estrarre.
        output_dir: Directory di output.

    Returns:
        Path: Percorso della cartella estratta.

    """
    # Il ZIP contiene una cartella root con formato repo-branch
    zip_root = f"{repo_name}-{branch}"
    full_folder_path = f"{zip_root}/{folder_path}"

    # Nome della cartella finale (solo l'ultimo componente)
    folder_name = Path(folder_path).name
    extract_path = Path(output_dir) / folder_name

    print(f"📦 Estrazione della cartella: {folder_path}")  # noqa: T201

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            # Trova tutti i file e directory nella cartella specificata
            entries_to_extract = [
                f
                for f in zip_ref.namelist()
                if f.startswith(full_folder_path) and f != full_folder_path + "/"
            ]

            if not entries_to_extract:
                msg = f"Cartella '{folder_path}' non trovata nel repository"
                raise FileNotFoundError(msg)

            # Estrae i file e le directory rimuovendo il prefisso zip_root
            for entry in entries_to_extract:
                # Nuovo percorso relativo (senza zip_root e folder_path)
                relative_path = entry[len(full_folder_path) :].lstrip("/")
                output_path = extract_path / relative_path

                # Se è una directory (termina con /), creala e continua
                if entry.endswith("/"):
                    _ensure_dir(output_path)
                    continue

                # Assicurati che la directory parent esista
                _ensure_dir(output_path.parent)

                # Estrae il file
                with (
                    zip_ref.open(entry) as source,
                    Path.open(output_path, "wb") as target,
                ):
                    shutil.copyfileobj(source, target)

    except zipfile.BadZipFile as e:
        msg = f"Errore durante l'estrazione: {e}"
        raise ValueError(msg) from e
    else:
        print(f"✅ Estrazione completata: {extract_path}")  # noqa: T201
        return extract_path


def download_github_folder(
    folder_url: str,
    output_dir: str | Path = ".",
) -> Path | None:
    """Funzione principale per scaricare una cartella da GitHub.

    Args:
        folder_url: URL della cartella GitHub.
        output_dir: Directory dove salvare la cartella (default: directory corrente).

    Returns:
        Path: Percorso della cartella scaricata, o None se fallisce.

    """
    output_path = Path(output_dir)
    # Crea directory temporanea
    temp_dir = output_path / ".temp_github_download"
    temp_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Parse dell'URL
        info = parse_github_folder_url(folder_url)
        print("\n📋 Informazioni Repository:")  # noqa: T201
        print(f"   Owner: {info['owner']}")  # noqa: T201
        print(f"   Repository: {info['repo']}")  # noqa: T201
        print(f"   Branch: {info['branch']}")  # noqa: T201
        print(f"   Cartella: {info['folder_path']}")  # noqa: T201
        print()  # noqa: T201

        # Download del ZIP
        zip_path = download_repository_zip(
            info["owner"],
            info["repo"],
            info["branch"],
            temp_dir,
        )

        # Estrazione della cartella
        result_path = extract_folder_from_zip(
            zip_path,
            info["repo"],
            info["branch"],
            info["folder_path"],
            output_path,
        )

    except (ValueError, ConnectionError, FileNotFoundError, OSError) as e:
        print(f"\n❌ Errore: {e}")  # noqa: T201
        sys.exit(EXIT_ERROR)
    else:
        print("\n🎉 Cartella scaricata con successo!")  # noqa: T201
        print(f"📍 Posizione: {result_path.absolute()}")  # noqa: T201
        return result_path
    finally:
        # Pulizia directory temporanea
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            print("\n🧹 Pulizia completata")  # noqa: T201


def main() -> None:
    """Funzione principale con gestione argomenti da riga di comando."""
    if len(sys.argv) < ARGUMENT_COUNT_ERROR:
        print("❌ Errore: URL della cartella non specificato")  # noqa: T201
        print("\nUtilizzo:")  # noqa: T201
        print("  python download-github-folder.py <URL_CARTELLA> [DIRECTORY_OUTPUT]")  # noqa: T201
        print("\nEsempio:")  # noqa: T201
        print(  # noqa: T201
            "  python download-github-folder.py https://github.com/malafronte/malafronte-doc-samples/tree/main/samples-quarta/api_client_server_demos/mock-server-tutorial",
        )
        print("  python download-github-folder.py <URL> ./output")  # noqa: T201
        sys.exit(EXIT_ERROR)

    folder_url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > ARGUMENT_COUNT_ERROR else "."

    download_github_folder(folder_url, output_dir)


if __name__ == "__main__":
    main()
