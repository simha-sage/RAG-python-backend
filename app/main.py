from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.documents import router as document_router
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
import os

load_dotenv()

client_url = os.getenv("CLIENT_URL")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[client_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

