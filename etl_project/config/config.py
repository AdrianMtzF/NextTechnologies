from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def _req(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"Falta la variable de entorno: {name}")
    return v

ROOT = Path(__file__).resolve().parents[1]

@dataclass(frozen=True)
class Settings:
    DB_URL: str = _req("DB_URL")
    INPUT_CSV: str = _req("INPUT_CSV")

    def csv_path(self) -> Path:
        p = Path(self.INPUT_CSV)
        return p if p.is_absolute() else (ROOT / p)

settings = Settings()
