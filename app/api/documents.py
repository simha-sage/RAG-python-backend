from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil

from app.database.mongodb import db
from app.services.embedding_service import generate_embedding
from app.services.rag_service import ingest_document

router = APIRouter()


@router.delete("/all")
def delete_all_documents():
    result = db.documents.delete_many({})
    return {
        "message": "All documents deleted successfully",
        "deleted_count": result.deleted_count
    }


@router.delete("/{filename}")
def delete_document(filename: str):
    result = db.documents.delete_many({
        "filename": filename
    })
    return {
        "deleted": result.deleted_count
    }


@router.get("/")
def get_documents():
    docs = list(db.documents.find({}, {"_id": 0}))
    return docs


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    total_chunks = ingest_document(
        file_path=file_path,
        filename=file.filename
    )

    return {
        "message": "Document Indexed Successfully",
        "chunks": total_chunks
    }


@router.get("/embedding-test")
def embedding_test():
    embedding = generate_embedding("Python is awesome")

    return {
        "dimension": len(embedding),
        "preview": embedding[:5]
    }