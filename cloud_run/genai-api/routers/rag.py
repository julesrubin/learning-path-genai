from fastapi import APIRouter, HTTPException

from models.rag import RagQueryRequest, RagQueryResponse
from services.rag import RagClient

router = APIRouter()
rag_client = RagClient()


@router.post("/rag", response_model=RagQueryResponse)
def rag(request: RagQueryRequest) -> RagQueryResponse:
    """Grounded Q&A over StyleCo's knowledge base via Vertex AI RAG Engine."""
    try:
        return rag_client.query(request.question)
    except LookupError as e:
        raise HTTPException(status_code=503, detail=str(e))
