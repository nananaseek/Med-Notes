import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    TOKEN: str = os.environ.get('TOKEN')

    DEBUG: bool = os.environ.get('DEBUG')

    PROJECT_ROOT: str = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    BASE_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
    LOGS_ROOT: str = os.path.join(BASE_DIR, "logs")
    TEMP_FOLDER: str = f"{BASE_DIR}/temp/"

    DB_USERNAME: str = os.environ.get('DB_USERNAME')
    DB_PASSWORD: str = os.environ.get('DB_PASSWORD')
    DB_HOST: str = os.environ.get('DB_HOST')
    DB_PORT: str = os.environ.get('DB_PORT')
    DB_NAME: str = os.environ.get('DB_NAME')

    DB_URL: str = f"postgres://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    MODELS: dict[str, list] = {
        'models': [
            'app.database.model'
        ]
    }


settings = Settings()
