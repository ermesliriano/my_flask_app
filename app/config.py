# app/config.py
import os
from pathlib import Path

def _default_sqlite_uri() -> str:
    # Fallback robusto: SQLite persistente en /data/app.db
    data_dir = Path(os.environ.get("APP_DATA_DIR", "/data"))
    data_dir.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{data_dir / 'app.db'}"

def _resolve_db_uri() -> str:
    # Prioridad: SQLALCHEMY_DATABASE_URI > DATABASE_URI > SQLite
    return (
        os.environ.get("SQLALCHEMY_DATABASE_URI")
        or os.environ.get("DATABASE_URI")
        or _default_sqlite_uri()
    )

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-in-prod")
    # OJO: evaluar en runtime dentro de create_app (ver __init__.py), no te fíes solo de esto.
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
