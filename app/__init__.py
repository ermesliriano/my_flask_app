import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.config import config_dict, _default_sqlite_uri, _resolve_db_uri

db = SQLAlchemy()

def create_app(config_name: str | None = None) -> Flask:
    # 1) Determina entorno con fallback
    config_name = (config_name or os.getenv("FLASK_ENV", "production")).lower()
    config_cls = config_dict.get(config_name, config_dict["production"])

    app = Flask(__name__)
    app.config.from_object(config_cls)

    # 2) Fija SIEMPRE una URI válida ANTES de init_app
    uri = _resolve_db_uri()
    if not uri:
        uri = _default_sqlite_uri()
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    # 3) Inicializa extensiones
    db.init_app(app)

    # 4) Blueprints opcionales (no bloquea si aún no existen)
    try:
        from app.routes import data_routes
        app.register_blueprint(data_routes)
    except Exception:
        pass

    # 5) Health-check
    @app.get("/health")
    def health():
        return jsonify(status="ok"), 200

    return app
