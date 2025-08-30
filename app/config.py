import os
from pathlib import Path


def _default_sqlite_uri() -> str:
    """
    Construye una URI SQLite persistente en /data/app.db (o APP_DATA_DIR si se define).
    """
    data_dir = Path(os.environ.get("APP_DATA_DIR", "/data"))
    data_dir.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{data_dir / 'app.db'}"


def _resolve_db_uri() -> str:
    """
    Prioridad:
      1) SQLALCHEMY_DATABASE_URI
      2) DATABASE_URI
      3) SQLite por defecto (persistente)
    """
    return (
        os.environ.get("SQLALCHEMY_DATABASE_URI")
        or os.environ.get("DATABASE_URI")
        or _default_sqlite_uri()
    )


class Config:
    # Clave secreta (ajústala en producción via SECRET_KEY)
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-in-prod")

    # Base de datos
    SQLALCHEMY_DATABASE_URI = _resolve_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


# Map de entornos
config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
