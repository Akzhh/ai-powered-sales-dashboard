import sys
import os
from pathlib import Path

# Manually load .env for local script execution
env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value.strip('"\'')

# Ensure dummy SECRET_KEY if not in .env
if "SECRET_KEY" not in os.environ:
    os.environ["SECRET_KEY"] = "init-script-dummy-key"

sys.path.insert(0, str(Path(__file__).resolve().parent / "api"))
from _services.database import init_db

if __name__ == "__main__":
    print("Initializing Supabase database...")
    init_db()
    print("Database tables initialized successfully!")
