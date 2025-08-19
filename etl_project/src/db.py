from __future__ import annotations
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from typing import Optional
from etl_project.src.config import settings

_engine: Optional[Engine] = None

def get_engine() -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(
            settings.DB_URL,
            pool_pre_ping=True,
            future=True,
        )
    return _engine

def ping() -> None:
    with get_engine().connect() as conn:
        conn.execute(text("SELECT 1"))
