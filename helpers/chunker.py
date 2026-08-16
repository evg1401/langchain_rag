import json
from typing import Dict, List


def chunk_text(
    text: str,
    chunk_size: int = 500,
    # перекрытие соседних чанков
    overlap: int = 100
):
    """
    Разбивает текст на чанки.

    chunk_size — максимальное количество слов.
    overlap — сколько слов повторяется между чанками.
    """

    words = text.split()

    chunks = []

    step = chunk_size - overlap

    for i in range(0, len(words), step):

        chunk = words[i:i + chunk_size]

        if chunk:
            chunks.append(" ".join(chunk))

    return chunks