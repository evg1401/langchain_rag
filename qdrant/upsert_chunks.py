from typing import Any
from uuid import uuid4
import requests
from app.config import QDRANT_URL

def point_from_chunk(
    chunk: dict[str, Any],
    document: dict[str, Any],
) -> tuple[dict[str, Any], bool]:

    chunk_id = chunk.get("chunk_id")

    if not isinstance(chunk_id, str):
        raise ValueError(
            f"chunk_id должен быть строкой: {chunk_id!r}"
        )

    if not chunk_id:
        raise ValueError("пустой chunk_id")

    embedding = chunk.get("embedding")

    # Если embedding отсутствует — этот chunk не отправляем.
    if embedding is None:
        return {}, False

    if not isinstance(embedding, list):
        raise ValueError(
            f"embedding для chunk {chunk_id!r} "
            "должен быть списком"
        )

    if not embedding:
        raise ValueError(
            f"пустой embedding для chunk {chunk_id!r}"
        )

    # Проверяем, что embedding состоит из чисел.
    if not all(
        isinstance(value, (int, float))
        for value in embedding
    ):
        raise ValueError(
            f"embedding для chunk {chunk_id!r} "
            "содержит нечисловые значения"
        )

    # Payload Qdrant.
    payload = {
        "chunk_id": chunk_id,
        "text": chunk.get("text", ""),
        "metadata": chunk.get("metadata", {}),
    }

    # Дополнительные данные документа.
    payload["document_id"] = document.get("document_id")
    payload["filename"] = document.get("filename")

    point = {
        "id": str(uuid4()),
        "payload": payload,
        "vector": embedding,
    }

    return point, True


def upsert_chunks(
    document: dict[str, Any],
    collection: str,
) -> None:
    qdrant_url = QDRANT_URL + f"/collections/{collection}/points"
    
    if not isinstance(document, dict):
        raise TypeError(
            "document должен быть словарём"
        )

    pages = document.get("pages")

    if not isinstance(pages, list):
        raise ValueError(
            "document['pages'] должен быть списком"
        )

    points = []

    for page in pages:

        if not isinstance(page, dict):
            raise ValueError(
                "элемент pages должен быть словарём"
            )

        chunks = page.get("chunks", [])

        if not isinstance(chunks, list):
            raise ValueError(
                "page['chunks'] должен быть списком"
            )

        for chunk in chunks:

            if not isinstance(chunk, dict):
                raise ValueError(
                    "chunk должен быть словарём"
                )

            point, ok = point_from_chunk(
                chunk,
                document,
            )

            if ok:
                points.append(point)

    if not points:
        raise ValueError(
            "в документе не найдено chunks с embedding"
        )

    body = {
        "points": points
    }

    try:
        response = requests.put(
            qdrant_url,
            json=body,
            headers={
                "Content-Type": "application/json",
            },
            timeout=60,
        )

    except requests.RequestException as e:
        raise RuntimeError(
            f"ошибка отправки запроса в Qdrant: {e}"
        ) from e

    if not 200 <= response.status_code < 300:
        raise RuntimeError(
            f"Qdrant returned {response.status_code}: "
            f"{response.text[:4096]}"
        )

    print(
        f"загружено {len(points)} chunks в Qdrant"
    )