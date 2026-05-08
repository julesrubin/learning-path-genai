from google import genai

from config import settings
from prompts import load_prompt


class GeminiClient:
    """
    Client for interacting with Google's Gemini API via Vertex AI.
    Handles initialization, prompt generation, and token analysis.
    """

    def __init__(self):
        """Initialize the Gemini client with Vertex AI configuration."""
        self.client = genai.Client(
            vertexai=True,
            project=settings.google_cloud_project,
            location=settings.google_cloud_location,
        )
        self.model_name = settings.gemini_model_name

    def generate_simple_response(self, prompt: str) -> str:
        """
        Generate a simple response from Gemini for a given prompt.

        Args:
            prompt: The user's prompt

        Returns:
            Generated text response
        """
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        return response.text

    def generate_styleco_response(self, prompt: str) -> str:
        """
        Generate a StyleCo customer service response using the system prompt.

        Args:
            prompt: The user's prompt

        Returns:
            Generated text response with StyleCo context
        """
        system_prompt = load_prompt("styleco_customer_service")
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={"system_instruction": system_prompt},
        )
        return response.text

    def generate_temperature_responses(
        self, prompt: str, temperatures: list[float]
    ) -> list[dict[str, str | float]]:
        """
        Generate multiple responses using different temperature settings.

        Args:
            prompt: The user's prompt
            temperatures: List of temperature values to test

        Returns:
            List of dicts containing temperature and response
        """
        system_prompt = load_prompt("styleco_customer_service")
        responses = []

        for temp in temperatures:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={"system_instruction": system_prompt, "temperature": temp},
            )
            responses.append({"temperature": temp, "response": response.text})

        return responses

    def token_analysis(self, prompt: str) -> dict[str, int | float | list[str]]:
        """
        Analyze token usage, estimated cost, and context window for a given prompt.

        Args:
            prompt: The text to analyze

        Returns:
            Dictionary with token count, estimated cost, context usage percent, and warnings
        """
        token_count = self.client.models.count_tokens(
            model=self.model_name, contents=prompt
        ).total_tokens

        estimated_cost = (
            token_count / 1_000_000
        ) * settings.gemini_input_price_per_million
        context_usage_percent = (token_count / settings.gemini_context_window) * 100

        warnings = []
        if context_usage_percent > 80:
            warnings.append("Approaching context limit (>80%)")
        if context_usage_percent > 95:
            warnings.append("Critical: Very close to context limit (>95%)")

        return {
            "token_count": token_count,
            "estimated_cost_usd": round(estimated_cost, 6),
            "context_usage_percent": round(context_usage_percent, 2),
            "warnings": warnings,
        }
