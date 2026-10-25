from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path

import pandas as pd

from .config import settings

SMS_SPAM_MEMBER = "SMSSpamCollection"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prepare_sms_spam(zip_path: Path, destination: Path) -> Path:
    """Extrae el SMS Spam Collection (texto separado por tabulador, sin
    cabecera) del .zip oficial de UCI y lo guarda como CSV con columnas
    ``label,text`` en ``destination``. No depende de rutas absolutas."""
    with zipfile.ZipFile(zip_path) as archive:
        with archive.open(SMS_SPAM_MEMBER) as member:
            frame = pd.read_csv(
                member,
                sep="\t",
                header=None,
                names=["label", "text"],
                quoting=3,
                encoding="utf-8",
            )
    destination.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(destination, index=False)
    return destination


def load_dataset(path: Path | None = None) -> pd.DataFrame:
    selected = path or settings.dataset_path
    if not selected.exists():
        raise FileNotFoundError(f"Dataset no encontrado: {selected}")
    return pd.read_csv(selected)


def validate_dataframe(df: pd.DataFrame, text_column: str, target_column: str) -> None:
    missing = {text_column, target_column} - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {sorted(missing)}")
    if df.empty:
        raise ValueError("El dataset está vacío")
    if df[text_column].fillna("").astype(str).str.strip().eq("").any():
        raise ValueError("Existen textos vacíos")
    if df[target_column].nunique(dropna=True) < 2:
        raise ValueError("Se requieren al menos dos clases")
