from pydantic import BaseModel


class PromptRequest(BaseModel):
    prompt: str


class PromptResponse(BaseModel):
    response: str


class TemperatureRequest(BaseModel):
    prompt: str
    temperatures: list[float] = [0.0, 0.5, 1.0]


class TemperatureResponseItem(BaseModel):
    temperature: float
    response: str


class TemperatureResponse(BaseModel):
    prompt: str
    responses: list[TemperatureResponseItem]


class TokenAnalysisResponse(BaseModel):
    token_count: int
    estimated_cost_usd: float | None = None
    context_usage_percent: float | None = None
    warnings: list[str] | None = None
