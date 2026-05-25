from typing import Protocol


class AiService(Protocol):
    """Contract for model-backed text and JSON generation."""

    def generate_json(
        self,
        instructions: str,
        prompt: str,
        schema: dict,
    ) -> dict:
        """Generates a JSON object using a language model.

        Args:
            instructions: System or developer instructions for the model.
            prompt: User prompt.
            schema: JSON schema the response must follow.

        Returns:
            Generated JSON object.
        """
        ...
