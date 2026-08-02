from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil

from scripts.rag_pipeline import generate_legal_answer
from qdrant_client import QdrantClient


# ==================================================
# APP CONFIGURATION
# ==================================================

app = FastAPI(
    title="Ethiopian Legal AI Assistant API"
)


# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================================================
# CHAT MODEL
# ==================================================

class ChatRequest(BaseModel):
    question: str


# ==================================================
# QDRANT CONFIG
# ==================================================

COLLECTION_NAME = "legal_documents"

qdrant_client = QdrantClient(
    host="localhost",
    port=6333
)

DOCUMENT_FOLDER = "data/documents"

os.makedirs(
    DOCUMENT_FOLDER,
    exist_ok=True
)


# ==================================================
# ROOT
# ==================================================

@app.get("/")
def root():

    return {
        "message": "Ethiopian Legal AI API Running"
    }


# ==================================================
# CHAT RAG API
# ==================================================

@app.post("/chat")
def chat(request: ChatRequest):

    try:

        answer = generate_legal_answer(
            request.question
        )

        return {
            "question": request.question,
            "result": answer
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# ==================================================
# ADMIN DASHBOARD STATISTICS
# ==================================================

@app.get("/admin/stats")
def dashboard():

    try:

        collection = qdrant_client.get_collection(
            COLLECTION_NAME
        )

        vectors = collection.points_count

        documents = len(
            os.listdir(DOCUMENT_FOLDER)
        )

        return {

            "documents": documents,

            "chunks": vectors,

            "embeddings": vectors,

            "qdrant": "Connected"

        }

    except Exception:

        return {

            "documents": 0,

            "chunks": 0,

            "embeddings": 0,

            "qdrant": "Offline"

        }


# ==================================================
# UPLOAD PDF DOCUMENT
# ==================================================

@app.post("/admin/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    try:

        file_path = os.path.join(
            DOCUMENT_FOLDER,
            file.filename
        )

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        return {

            "message":
            f"{file.filename} uploaded successfully"

        }

    except Exception as e:

        return {

            "message":
            str(e)

        }


# ==================================================
# PROCESS DOCUMENTS
# ==================================================

@app.post("/admin/process")
def process_documents():

    try:

        # Connect ingest.py here
        # Example:
        # subprocess.run(["python", "scripts/ingest.py"])

        return {

            "message":
            "Document processing completed"

        }

    except Exception as e:

        return {

            "message":
            str(e)

        }
# ==================================================
# GENERATE EMBEDDINGS
# ==================================================

@app.post("/admin/embeddings")
def create_embeddings():

    try:

        # Connect your embedding generation script here
        #
        # Example:
        # subprocess.run(
        #     ["python", "scripts/create_embeddings.py"]
        # )

        return {
            "message": "Embedding generation completed"
        }


    except Exception as e:

        return {
            "message": str(e)
        }



# ==================================================
# QDRANT INSERT / CONNECTION
# ==================================================

@app.post("/admin/qdrant")
def insert_qdrant():

    try:

        # Connect your Qdrant insertion pipeline here
        #
        # Example:
        # subprocess.run(
        #     ["python", "scripts/vector_store.py"]
        # )


        return {

            "message":
            "Documents inserted into Qdrant successfully"

        }


    except Exception as e:


        return {

            "message":
            str(e)

        }




# ==================================================
# QDRANT STATUS
# ==================================================

@app.get("/admin/qdrant")
def qdrant_status():

    try:

        collection = qdrant_client.get_collection(
            COLLECTION_NAME
        )


        return {

            "status":
            "Connected",

            "collection":
            COLLECTION_NAME,

            "vectors":
            collection.points_count

        }


    except Exception:


        return {

            "status":
            "Offline"

        }




# ==================================================
# RESET QDRANT COLLECTION
# ==================================================

@app.delete("/admin/reset")
def reset_qdrant():

    try:


        qdrant_client.delete_collection(
            collection_name=COLLECTION_NAME
        )


        return {

            "message":
            "Qdrant collection deleted successfully"

        }



    except Exception as e:


        return {

            "message":
            str(e)

        }




# ==================================================
# LOGOUT SUPPORT
# ==================================================

@app.post("/admin/logout")
def logout():

    return {

        "message":
        "Logout successful"

    }



# ==================================================
# RUN SERVER
# ==================================================

# Run:
# uvicorn main:app --reload
