import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.config import config_dict, _default_sqlite_uri

db = SQLAlchemy()


def create_app(config_name: str | None = None) -> Flask:
    """
    Crea la app usando FLASK_ENV (development/production) si no se especifica config_name.
    Garantiza que SQLALCHEMY_DATABASE_URI esté siempre definido (con fallback a SQLite).
    Registra un endpoint /health para checks en despliegue.
    """
    # Determinar el entorno
    if not config_name:
        config_name = os.getenv("FLASK_ENV", "production").lower()

    # Tomar la clase de config; fallback a 'production' si la clave no existe
    config_cls = config_dict.get(config_name, config_dict["production"])

    app = Flask(__name__)
    app.config.from_object(config_cls)

    # Cinturón y tirantes: si por cualquier motivo la URI no quedó definida, poner SQLite
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        app.config["SQLALCHEMY_DATABASE_URI"] = _default_sqlite_uri()

    # Desactivar track mods si no está presente
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    # Inicializar extensiones
    db.init_app(app)

    # Registrar blueprints/rutas de tu app
    try:
        from app.routes import data_routes  # si existe
        app.register_blueprint(data_routes)
    except Exception:
        # Si aún no tienes el blueprint, no bloquear el arranque
        pass

    # Health-check simple para despliegues
    @app.get("/health")
    def health():
        return jsonify(status="ok"), 200

    return app
