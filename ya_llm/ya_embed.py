from qdrant.retriever import retrieve
import requests
from app.config import YC_API_KEY, YC_FOLDER_ID

DOC_URI = f"emb://{YC_FOLDER_ID}/text-embeddings-v2-doc/latest"
EMBED_URL = "https://ai.api.cloud.yandex.net:443/foundationModels/v1/textEmbedding"
HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {YC_API_KEY}", "x-folder-id": f"{YC_FOLDER_ID}"}

def getQueryEmbeddings(text: str):
    query_data = {
        "modelUri": DOC_URI,
        "text": text,
    }

    vector = requests.post(EMBED_URL, json=query_data, headers=HEADERS).json()["embedding"]
    return retrieve(vector)["result"]

def getEmbeddings(text: str):
    query_data = {
        "modelUri": DOC_URI,
        "text": text,
    }

    return requests.post(EMBED_URL, json=query_data, headers=HEADERS).json()["embedding"]
