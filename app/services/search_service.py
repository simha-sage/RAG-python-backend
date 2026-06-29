

from annotated_types import doc

from app.database.mongodb import db
from app.services.embedding_service import generate_embedding

def search(question: str):

    query_embedding = generate_embedding(question)

    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 100,
                "limit": 5
            }
        }
    ]

    results = list(db.documents.aggregate(pipeline))
    for doc in results:
        doc.pop("_id", None)
        doc.pop("embedding", None)
    return results

def retrieve_context(question: str):

    results = search(question)

    context = ""

    for chunk in results:
        context += chunk["text"] + "\n\n"

    return context, results