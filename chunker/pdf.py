import fitz
from helpers.chunker import chunk_text
from qdrant.upsert_chunks import upsert_chunks
from ya_llm.ya_embed import getEmbeddings
from ya_llm.ya_llm import generateQuestion, generateShortDescr, fetchKeywords
from app.config import DOC_PDF_PATH, QDRANT_COLLECTION

def chunk_pdf():
    doc = fitz.open(DOC_PDF_PATH)

    document = {
        "document_id": "doc-001",
        "filename": DOC_PDF_PATH.split('/')[-1],
        "metadata": doc.metadata,
        "pages": []
    }

    for page_num, page in enumerate(doc):

        document["pages"].append({
            "page": page_num + 1,
            "text": page.get_text()
        })

    # 116 страница
    # print(document["pages"][115])

    # page = doc[0]
    # blocks = page.get_text("blocks")
    # for block in blocks:
    #     x0, y0, x1, y1, text, *_ = block

    #     print(text)
    #     print((x0, y0, x1, y1))

    CHUNK_SIZE = 500
    OVERLAP = 100

    for page in document["pages"]:

        page["chunks"] = []

        chunks = chunk_text(page["text"], CHUNK_SIZE, OVERLAP)

        for i, chunk in enumerate(chunks):

            page["chunks"].append({
                "chunk_id": f'{page["page"]}-{i}',
                "text": chunk,
            })

    tokenStart = 0
    tokenEnd = CHUNK_SIZE
    for page in document["pages"]:
        if i > 0:
            tokenEnd - OVERLAP
            tokenStart += tokenEnd

        for chunk in page["chunks"]:

            chunk["metadata"] = {

                "document_id": document["document_id"],

                "filename": document["filename"],

                "page": page["page"],

                "author": document["metadata"].get("author"),

                "title": document["metadata"].get("title"),

                "token_start": tokenStart,
                
                "token_end": tokenEnd,
            }
            
            # генерация краткого описания
            summary = generateShortDescr(chunk["text"])
            chunk["metadata"]["summary"] = summary

            # генерация ключевых слов
            keywords = fetchKeywords(chunk["text"])
            chunk["metadata"]["keywords"] = keywords

            # генерация вопросов
            questions = generateQuestion(chunk["text"])
            chunk["metadata"]["questions"] = questions

            # конвертация в эмбединги
            embedding = getEmbeddings(chunk["text"])
            chunk["embedding"] = embedding


    upsert_chunks(document, QDRANT_COLLECTION)