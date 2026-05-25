from typing import Any

from src.agents.email_agent import EmailAgent
from src.workflows.nodes import EmailProcessingNodes


class EmailProcessingGraphBuilder:
    """Builds the LangGraph email processing workflow."""

    def __init__(self, email_agent: EmailAgent | None = None) -> None:
        """Initializes the graph builder.

        Args:
            email_agent: Optional email agent override.
        """
        self._nodes = EmailProcessingNodes(email_agent=email_agent)

    def build(self) -> Any:
        """Builds the email processing graph.

        Returns:
            Compiled LangGraph workflow, or None when LangGraph is unavailable.
        """
        try:
            from langgraph.graph import END, StateGraph
        except ImportError:
            return None

        graph = StateGraph(dict)
        graph.add_node("classify", self._nodes.classify)
        graph.set_entry_point("classify")
        graph.add_edge("classify", END)
        return graph.compile()
