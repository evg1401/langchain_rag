import requests
from app.config import QDRANT_URL

url = f"{QDRANT_URL}/collections/b2b_center_doc/points/search"

def retrieve(vector: list[int]):
    payload = {
        "vector": vector,
        "limit": 7,
        "with_payload": True,
        "score_threshold": 0.45
    }

    response = requests.post(url, json=payload)

    response.raise_for_status()

    data = response.json()

    # сортировка по номеру страницы, внутри одной страницы - по номеру чанка для llm (чтобы видела продолжение текста)
    data["result"].sort(
        key=lambda item: (
            item["payload"]["metadata"]["page"],
            int(item["payload"]["chunk_id"].split("-")[1])
        )
    )

    return data
