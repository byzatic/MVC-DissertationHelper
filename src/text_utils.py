from src.patterns import WORD_PATTERN


def get_context(text: str, start: int, end: int):
    before_words = WORD_PATTERN.findall(text[:start])
    after_words = WORD_PATTERN.findall(text[end:])

    return " ".join(before_words[-3:]), " ".join(after_words[:3])