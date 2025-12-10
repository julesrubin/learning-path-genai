from fastapi import APIRouter

from models.gemini import (
    PromptRequest,
    PromptResponse,
    TemperatureRequest,
    TemperatureResponse,
    TemperatureResponseItem,
    TokenAnalysisResponse,
)
from services.gemini import GeminiClient

router = APIRouter()
gemini_client = GeminiClient()


@router.post("/hello_gemini", response_model=PromptResponse)
def hello_gemini(request: PromptRequest) -> PromptResponse:
    """
    Simple endpoint that accepts a prompt and returns Gemini's response.
    """
    response_text = gemini_client.generate_simple_response(request.prompt)
    return PromptResponse(response=response_text)


@router.post("/styleco_assistant", response_model=PromptResponse)
def styleco_assistant(request: PromptRequest) -> PromptResponse:
    """
    StyleCo customer service assistant powered by a system prompt.
    """
    response_text = gemini_client.generate_styleco_response(request.prompt)
    return PromptResponse(response=response_text)


@router.post("/styleco_assistant_temperature", response_model=TemperatureResponse)
def styleco_assistant_temperature(request: TemperatureRequest) -> TemperatureResponse:
    """
    Test the same prompt with different temperature settings.
    """
    responses = gemini_client.generate_temperature_responses(
        request.prompt, request.temperatures
    )
    response_items = [
        TemperatureResponseItem(temperature=r["temperature"], response=r["response"])
        for r in responses
    ]
    return TemperatureResponse(prompt=request.prompt, responses=response_items)


@router.post("/token_analysis", response_model=TokenAnalysisResponse)
def token_analysis(request: PromptRequest) -> TokenAnalysisResponse:
    """
    Analyze token usage, estimated cost, and context window for a given prompt.
    """
    response = gemini_client.token_analysis(
        request.prompt
    )
    return TokenAnalysisResponse(**response)
