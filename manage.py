# manage.py
import os

from app import create_app, db
from app.models import Data

env_name = os.getenv("FLASK_ENV", "development")
init_db_flag = os.getenv("INIT_DB", "0")  # "1" => inicializa

# Solo permite inicializar en desarrollo o si lo fuerzas explícitamente
if not (env_name == "development" or init_db_flag == "1"):
    print("manage.py: saltado (no es entorno de desarrollo y INIT_DB != 1)")
else:
    app = create_app(env_name)
    with app.app_context():
        db.create_all()
        # Semilla de ejemplo SOLO si no existe (evitar duplicados)
        if not Data.query.filter_by(name="SQL Test User").first():
            sample_data = Data(name="SQL Test User")
            db.session.add(sample_data)
            db.session.commit()
        print("Database tables ensured (create_all).")
