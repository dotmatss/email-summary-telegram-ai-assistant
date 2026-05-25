from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from src.config.config import settings
from src.integrations.ai_service import AiService


class LangChainOpenAiClient(AiService):
    """LangChain-backed OpenAI adapter for structured model outputs."""

    def generate_json(
        self,
        instructions: str,
        prompt: str,
        schema: dict,
    ) -> dict:
        """Generates a JSON object through LangChain structured output."""
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is required when AI_PROVIDER=openai.")

        model = ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.ai_model,
            temperature=0,
        )
        response_schema = dict(schema["schema"])
        response_schema.setdefault("title", schema["name"])
        structured_model = model.with_structured_output(
            response_schema,
            method="json_schema",
        )
        result = structured_model.invoke(
            [
                SystemMessage(content=instructions),
                HumanMessage(content=prompt),
            ]
        )
        return dict(result)
