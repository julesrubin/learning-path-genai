import os
from pathlib import Path

from google import genai


class GeminiClient:
    """
    Client for interacting with Google's Gemini API via Vertex AI.
    Handles initialization, prompt generation, and token analysis.
    """

    def __init__(self):
        """Initialize the Gemini client with Vertex AI configuration."""
        self.client = self._initialize_client()
        self.prompts_dir = Path(__file__).parent.parent / "instructions"
        self.model_name = "gemini-2.5-flash"

    def _initialize_client(self) -> genai.Client:
        """
        Initialize and return a Gemini client configured for Vertex AI.

        Returns:
            Configured genai.Client instance
        """
        return genai.Client(
            vertexai=True,
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("GOOGLE_CLOUD_LOCATION", "europe-west1"),
        )

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
        system_prompt = (self.prompts_dir / "styleco_customer_service.txt").read_text()
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
        system_prompt = (self.prompts_dir / "styleco_customer_service.txt").read_text()
        responses = []

        for temp in temperatures:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={"system_instruction": system_prompt, "temperature": temp},
            )
            responses.append({"temperature": temp, "response": response.text})

        return responses

    def count_tokens(self, prompt: str, model_name: str | None = None) -> int:
        """
        Count the number of tokens in a prompt.

        Args:
            prompt: The text to analyze
            model_name: Optional model name (defaults to instance model)

        Returns:
            Total token count
        """
        model = model_name or self.model_name
        response = self.client.models.count_tokens(
            model=model,
            contents=prompt,
        )
        return response.total_tokens
