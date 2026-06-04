import re

REFERENCE_PATTERN = re.compile(
    r"\[((?:\d{1,3}(?:\s*-\s*\d{1,3})?)(?:\s*,\s*\d{1,3}(?:\s*-\s*\d{1,3})?)*)\]"
)

# Ищет ссылки на рисунки в обычном тексте: "рисунок 17", "рисунке 17".
# Группа number содержит только номер, чтобы менять его отдельно от слова.
FIGURE_PATTERN = re.compile(
    r"(?P<prefix>\bрисун(?:ок|к(?:е|а|у|ом|и|ов)?)\s+)(?P<number>\d{1,3})\b",
    re.IGNORECASE
)

WT_PATTERN = re.compile(
    r"(<w:t(?:\s[^>]*)?>)(.*?)(</w:t>)",
    re.DOTALL
)

WORD_PATTERN = re.compile(r"\S+")
