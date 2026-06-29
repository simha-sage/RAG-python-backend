from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.documents import router as document_router

app = FastAPI()

app.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"]
)

@app.get("/")
def root():
    return {
        "message":"Backend Running"
    }

app.include_router(
    document_router,
    prefix="/documents",
    tags=["Documents"]
)

