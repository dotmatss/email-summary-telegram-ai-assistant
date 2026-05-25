from src.schemas.meeting import (
    MeetingBriefRequest,
    MeetingBriefResponse,
    MeetingSummaryRequest,
    MeetingSummaryResponse,
)


class MeetingAgent:
    """Handles meeting summaries and pre-meeting briefs."""

    def summarize(self, request: MeetingSummaryRequest) -> MeetingSummaryResponse:
        """Summarizes a meeting transcript.

        Args:
            request: Meeting summary request.

        Returns:
            Meeting summary response.
        """
        transcript_preview = request.transcript.strip().replace("\n", " ")[:240]
        action_items = self._extract_action_items(request.transcript)
        return MeetingSummaryResponse(
            title=request.title,
            summary=f"Summary draft: {transcript_preview}",
            action_items=action_items,
        )

    def create_brief(self, request: MeetingBriefRequest) -> MeetingBriefResponse:
        """Creates a pre-meeting brief.

        Args:
            request: Meeting brief request.

        Returns:
            Meeting brief response.
        """
        attendee_count = len(request.attendee_emails)
        agenda = request.agenda or "No agenda was provided."
        return MeetingBriefResponse(
            title=request.title,
            brief=(
                f"Prepare for {request.title} with {attendee_count} attendee(s). "
                f"Agenda context: {agenda}"
            ),
            suggested_questions=[
                "What decision should this meeting produce?",
                "Are there blockers that need executive input?",
                "What follow-ups should be captured before the meeting ends?",
            ],
        )

    @staticmethod
    def _extract_action_items(transcript: str) -> list[str]:
        """Extracts action items from transcript lines.

        Args:
            transcript: Meeting transcript text.

        Returns:
            Extracted action items or a fallback review item.
        """
        lines = [line.strip("- ").strip() for line in transcript.splitlines()]
        candidates = [
            line
            for line in lines
            if line.lower().startswith(("action:", "todo:", "next step:"))
        ]
        return candidates or ["Review transcript and confirm action items."]
