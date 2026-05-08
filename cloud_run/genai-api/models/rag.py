from pydantic import BaseModel, Field


class RagQueryRequest(BaseModel):
    question: str = Field(
        ...,
        examples=["What is your return policy?"],
        description="Customer question to answer using StyleCo's knowledge base.",
    )


class Citation(BaseModel):
    source: str = Field(..., description="Source document path or filename.")
    snippet: str = Field(..., description="Retrieved chunk text used as evidence.")


class RagQueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
