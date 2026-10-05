"""Input validation and response safety helpers for the BFSI assistant."""

from collections.abc import Mapping


ALLOWED_CATEGORIES = {
    "account", "card", "credit", "deposits", "digital_banking",
    "insurance", "investment", "loan", "payments", "security", "support",
}
MAX_QUESTION_LENGTH = 10000


def validate_category(category: str) -> bool:
    return isinstance(category, str) and category in ALLOWED_CATEGORIES


def validate_question(question_data: Mapping | None) -> bool:
    if not isinstance(question_data, Mapping):
        return False
    question = question_data.get("question")
    return (
        validate_category(question_data.get("category"))
        and isinstance(question, str)
        and 0 < len(question.strip()) <= MAX_QUESTION_LENGTH
    )


def safe_response(response: str | None) -> str:
    if not isinstance(response, str) or not response.strip():
        return "I couldn't prepare a reliable answer. Please contact customer support."
    return response.strip()
