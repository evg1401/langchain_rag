import os

from dotenv import load_dotenv


load_dotenv()

env_vars = {
    "YC_API_KEY": os.getenv("YC_API_KEY"),
    "YC_FOLDER_ID": os.getenv("YC_FOLDER_ID"),
    "QDRANT_URL": os.getenv("QDRANT_URL", "http://qdrant_db:6333"),
    "QDRANT_COLLECTION": os.getenv("QDRANT_COLLECTION"),
    "DOC_PDF_PATH": os.getenv("DOC_PDF_PATH")
}

missing = [key for key, value in env_vars.items() if value is None]
if missing:
    raise ValueError(f"Отсутствует переменная окружения: {', '.join(missing)}")

YC_API_KEY, YC_FOLDER_ID, QDRANT_URL, QDRANT_COLLECTION, DOC_PDF_PATH = env_vars.values()