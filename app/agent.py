"""BFSI request orchestration with grounded answers and safe failure paths."""

import logging

from app.guardrails import safe_response, validate_question
from app.llm import generate_answer
from app.rag import retrieve_context
from app.router import route_question
from app.tools import get_account_balance, get_card_status, get_recent_transactions

FALLBACK_ANSWER = (
    "I couldn't prepare a reliable answer right now. Please try again or contact "
    "the institution's authorized customer support team."
)
logger = logging.getLogger(__name__)


def _run_tool(question_id: str) -> tuple[dict | None, str | None]:
    if question_id == "account_balance":
        result = get_account_balance()
        context = (
            f"Demo account ending {result['account']}: "
            f"{result['currency']} {result['balance']:,.2f}. "
            "This is sample data from a demonstration tool."
        )
    elif question_id == "transactions":
        result = get_recent_transactions()
        context = f"Demonstration transaction data: {result['transactions']}"
    elif question_id == "card_status":
        result = get_card_status()
        context = f"Demonstration card ending {result['card']}: {result['status']}"
    else:
        return None, None
    return result, context


def process_question(question_data: dict, history: list | None = None) -> dict:
    if not validate_question(question_data):
        return {
            "status": "rejected",
            "type": "guardrail",
            "answer": "I can only assist with supported BFSI questions.",
        }

    question = question_data["question"].strip()
    route = route_question(question_data)
    question_id = question_data["id"]

    if route == "support":
        return {
            "status": "escalated",
            "type": "support",
            "question_id": question_id,
            "answer": (
                "Please contact the institution's authorized customer support "
                "team through its official channels."
            ),
        }

    if route == "tool":
        _, context = _run_tool(question_id)
        if context is None:
            return {
                "status": "rejected", "type": "guardrail",
                "answer": "Unsupported banking operation.",
            }
    elif route == "rag":
        context = retrieve_context(question)
    else:
        return {
            "status": "rejected", "type": "guardrail",
            "answer": "I can only assist with supported BFSI questions.",
        }

    try:
        answer = safe_response(generate_answer(question, context, history))
    except Exception:
        # Provider errors and timeouts should not expose internals or break the API.
        logger.exception("BFSI answer generation failed")
        answer = FALLBACK_ANSWER

    return {
        "status": "success" if answer != FALLBACK_ANSWER else "unavailable",
        "type": route,
        "question_id": question_id,
        "answer": answer,
    }
