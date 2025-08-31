# run.py
import os
from app import create_app

env_name = os.getenv("FLASK_ENV", "development")
app = create_app(env_name)

if __name__ == "__main__":
    debug = env_name.lower() == "development"
    app.run(debug=debug, host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
