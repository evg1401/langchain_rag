import json
from typing import Dict, List

def extract_json_object(raw_text: str) -> Dict[str, object]:
    text = raw_text.strip()
    if text.startswith("```"):
        text = text.strip("`").strip()
        if text.lower().startswith("json"):
            text = text[4:].strip()

    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            payload, _ = decoder.raw_decode(text[index:])
            if isinstance(payload, dict):
                return payload
        except json.JSONDecodeError:
            continue

    return {}

def extract_json_array(raw_text: str) -> List[str]:
    text = raw_text.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()

        if text.lower().startswith("json"):
            text = text[4:].strip()

    decoder = json.JSONDecoder()

    for i, ch in enumerate(text):
        if ch != "[":
            continue

        try:
            payload, _ = decoder.raw_decode(text[i:])
            if isinstance(payload, list):
                return payload
        except json.JSONDecodeError:
            pass

    return []

def buildContext(results: list) -> str:
    context = []

    for i, item in enumerate(results, start=1):
        payload = item["payload"]
        meta = payload["metadata"]

        block = f"""
        === Источник {i} ===

        Документ: {meta["filename"]}
        Страница: {meta["page"]}

        Краткое описание:
        {meta["summary"]}

        Текст:
        {payload["text"]}
        """

        context.append(block.strip())

    return "\n\n".join(context)