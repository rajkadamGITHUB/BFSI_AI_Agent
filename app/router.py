SUPPORTED_ROUTES = {"rag", "tool", "support"}


def route_question(question_data: dict) -> str:
    route = question_data.get("type")
    return route if route in SUPPORTED_ROUTES else "refuse"
