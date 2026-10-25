from __future__ import annotations

import sys
from pathlib import Path

import requests

from inf8239_u02.config import ROOT, settings
from inf8239_u02.data import prepare_sms_spam, sha256


def main() -> int:
    output = ROOT / "data/raw/dataset.csv"
    if settings.data_source == "local":
        if output.exists():
            print(f"Modo local. Archivo ya presente: {output}")
            print(f"SHA-256: {sha256(output)}")
            return 0
        print(
            f"No existe {output}. Configure DATA_SOURCE=url en .env para "
            "descargarlo, o coloque el archivo manualmente.",
            file=sys.stderr,
        )
        return 2
    if settings.data_source != "url" or not settings.dataset_url:
        print("Configure DATA_SOURCE=url y DATASET_URL en .env", file=sys.stderr)
        return 2

    output.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(settings.dataset_url, timeout=60)
    response.raise_for_status()
    zip_path = output.parent / "_sms_spam_collection.zip"
    zip_path.write_bytes(response.content)
    prepare_sms_spam(zip_path, output)
    zip_path.unlink()
    print(f"Guardado: {output}")
    print(f"SHA-256: {sha256(output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
