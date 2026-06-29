from app.services.pdf_service import extract_text
from app.services.chunk_service import chunk_text
from app.services.embedding_service import generate_embedding
from app.database.mongodb import db


def ingest_document(file_path: str, filename: str):

    text = extract_text(file_path)

    chunks = chunk_text(text)

    documents = []

    for index, chunk in enumerate(chunks):

        embedding = generate_embedding(chunk)

        documents.append({
            "filename": filename,
            "chunk_index": index,
            "text": chunk,
            "embedding": embedding
        })

    db.documents.insert_many(documents)

    return len(documents)