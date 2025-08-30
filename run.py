import os
from app import create_app

# Usar FLASK_ENV para decidir la configuración (development/production)
env_name = os.getenv("FLASK_ENV", "development")
app = create_app(env_name)

if __name__ == "__main__":
    # En contenedor solemos escuchar en 0.0.0.0
    debug = env_name == "development"
    app.run(debug=debug, host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
