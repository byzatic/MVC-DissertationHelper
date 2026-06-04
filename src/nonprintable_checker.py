import unicodedata

from src.logger import ScriptLogger
from src.text_utils import get_context


class NonPrintableChecker:
    BAD_CHARS = {
        #0x00A0,  # NO-BREAK SPACE
        0x200B,  # ZERO WIDTH SPACE
        0x200C,  # ZERO WIDTH NON-JOINER
        0x200D,  # ZERO WIDTH JOINER
        0x202C,  # POP DIRECTIONAL FORMATTING
        0x202E,  # RIGHT-TO-LEFT OVERRIDE
        0x202F,  # NARROW NO-BREAK SPACE
        0x2060,  # WORD JOINER
        0xFEFF,  # BOM
    }

    def __init__(self, logger: ScriptLogger):
        self.logger = logger

    def check(self, text: str, file_name: str):
        found = False

        for i, ch in enumerate(text, 1):
            code = ord(ch)

            if code not in self.BAD_CHARS:
                continue

            found = True

            try:
                name = unicodedata.name(ch)
            except ValueError:
                name = "UNKNOWN"

            before, after = get_context(
                text,
                max(0, i - 1),
                min(len(text), i)
            )

            self.logger.check_separator()

            self.logger.check_log(
                f"Non-printable char in {file_name}"
            )

            self.logger.check_log(
                f"Position: {i}"
            )

            self.logger.check_log(
                f"Unicode: U+{code:04X}"
            )

            self.logger.check_log(
                f"Name: {name}"
            )

            self.logger.check_log(
                f"Context: ... {before} [{name}] {after} ..."
            )

        if not found:
            self.logger.check_separator()
            self.logger.check_log(
                f"No non-printable characters found in {file_name}"
            )