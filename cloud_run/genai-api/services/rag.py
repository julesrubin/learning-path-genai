import vertexai
from google import genai
from google.genai import types
from vertexai import rag

from config import settings
from models.rag import Citation, RagQueryResponse


class RagCorpusNotFoundError(RuntimeError):
    """Raised when no corpus matching `rag_corpus_display_name` exists."""


_SYSTEM_INSTRUCTION = (
    "You are StyleCo's customer service assistant. Answer using only the "
    "provided context from StyleCo documents. If the answer is not in the "
    "context, say so clearly instead of guessing."
)


class RagClient:
    """
    Grounded Q&A on the StyleCo knowledge base via Vertex AI RAG Engine.

    The corpus itself is created out-of-band by the bootstrap script in
    `iac/scripts/bootstrap_rag_corpus.py`. This client uses google-genai for
    grounded generation; the only `vertexai` call is `rag.list_corpora()` to
    resolve the corpus by display name — google-genai has no corpus
    management API.
    """

    def __init__(self):
        self.client = genai.Client(
            vertexai=True,
            project=settings.google_cloud_project,
            location=settings.google_cloud_location,
        )
        vertexai.init(
            project=settings.google_cloud_project,
            location=settings.google_cloud_location,
        )
        self._corpus_resource_name: str | None = None

    @property
    def corpus_resource_name(self) -> str:
        if self._corpus_resource_name is None:
            self._corpus_resource_name = self._resolve_corpus()
        return self._corpus_resource_name

    def _resolve_corpus(self) -> str:
        for corpus in rag.list_corpora():
            if corpus.display_name == settings.rag_corpus_display_name:
                return corpus.name
        raise RagCorpusNotFoundError(
            f"No RAG corpus with display_name='{settings.rag_corpus_display_name}'. "
            "Run `just bootstrap-rag` from the iac/ directory to create it."
        )

    def query(self, question: str) -> RagQueryResponse:
        retrieval_tool = types.Tool(
            retrieval=types.Retrieval(
                vertex_rag_store=types.VertexRagStore(
                    rag_resources=[
                        types.VertexRagStoreRagResource(
                            rag_corpus=self.corpus_resource_name,
                        )
                    ],
                    similarity_top_k=settings.rag_top_k,
                )
            )
        )

        response = self.client.models.generate_content(
            model=settings.gemini_model_name,
            contents=question,
            config=types.GenerateContentConfig(
                system_instruction=_SYSTEM_INSTRUCTION,
                tools=[retrieval_tool],
            ),
        )

        citations: list[Citation] = []
        grounding = (
            response.candidates[0].grounding_metadata if response.candidates else None
        )
        if grounding and grounding.grounding_chunks:
            for chunk in grounding.grounding_chunks:
                ctx = chunk.retrieved_context
                if ctx is None:
                    continue
                citations.append(
                    Citation(
                        source=ctx.uri or ctx.title or "unknown",
                        snippet=ctx.text or "",
                    )
                )

        return RagQueryResponse(answer=response.text, citations=citations)
