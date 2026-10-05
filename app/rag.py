"""Lightweight, deterministic retrieval over the curated FAQ knowledge base."""

import re
from pathlib import Path

FAQ_FILE = Path(__file__).resolve().parent.parent / "data" / "banking_faq.txt"
_TOKEN_RE = re.compile(r"[a-z0-9]+")
_STOP_WORDS = {
    "a", "an", "and", "are", "can", "do", "for", "how", "i", "in",
    "is", "it", "me", "my", "of", "on", "or", "the", "to", "what",
    "when", "where", "which", "who", "with", "you", "your",
}
_SYNONYMS = {
    "atm": "cash", "charge": "fee", "charges": "fee", "cheque": "check",
    "debit": "card", "fraud": "scam", "lost": "block", "mobile": "digital",
    "rate": "interest", "rates": "interest", "stolen": "block", "upi": "payment",
}


def load_knowledge_base() -> str:
    return FAQ_FILE.read_text(encoding="utf-8")


def _terms(text: str) -> set[str]:
    terms = {word for word in _TOKEN_RE.findall(text.lower()) if len(word) > 2}
    expanded = set(terms)
    for word in terms:
        if word in _SYNONYMS:
            expanded.add(_SYNONYMS[word])
        expanded.update(key for key, value in _SYNONYMS.items() if value == word)
    return expanded - _STOP_WORDS


def retrieve_context(question: str, *, max_sections: int = 3) -> str:
    """Return only relevant FAQ sections; an empty result means no evidence."""
    if not isinstance(question, str) or not question.strip():
        return ""

    knowledge = load_knowledge_base()
    query_terms = _terms(question)
    if not query_terms:
        return ""

    sections = [
        part.strip()
        for part in re.split(r"(?=^## )", knowledge, flags=re.MULTILINE)
        if part.strip()
    ]
    scored = []
    for index, section in enumerate(sections):
        section_terms = _terms(section)
        overlap = query_terms & section_terms
        if overlap:
            # Prefer sections covering a greater share of the question's key terms.
            score = len(overlap) / len(query_terms)
            scored.append((score, len(overlap), -index, section))

    scored.sort(reverse=True)
    return "\n\n".join(row[3] for row in scored[:max_sections])
