from pathlib import Path

INPUT_FILE = Path("/Users/svyatvlasso/Desktop/Диссертация/COMMON/v1r13_диссертация.docx")
OUTPUT_FILE = Path("/Users/svyatvlasso/Desktop/Диссертация/COMMON/v1r00_диссертация.docx")

# Сдвиг литературных ссылок вида [160], [160-162], [160, 164]
START_FROM = 160
SHIFT = 0

# Отдельный сдвиг номеров рисунков в тексте:
# "рисунок 17", "рисунке 17", "Рисунок 17" и т.п.
FIGURE_START_FROM = 30
FIGURE_SHIFT = -1

LOG_ENABLED = True

XML_FILES = [
    "word/document.xml",
    "word/footnotes.xml",
    "word/endnotes.xml",
    "word/comments.xml",
]

CHECK_SEQUENCE_ONLY_IN = "word/document.xml"
