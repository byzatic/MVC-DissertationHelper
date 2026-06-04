from src.patterns import REFERENCE_PATTERN
from src.reference_shifter import ReferenceShifter
from src.logger import ScriptLogger


class ReferenceChecker:
    def __init__(self, shifter: ReferenceShifter, logger: ScriptLogger):
        self.shifter = shifter
        self.logger = logger

    def check_sequence(self, text: str, file_name: str):
        found_numbers = set()

        for match in REFERENCE_PATTERN.finditer(text):
            found_numbers.update(
                self.shifter.extract_numbers_from_reference(match.group(0))
            )

        if not found_numbers:
            return

        first = min(found_numbers)
        last = max(found_numbers)

        expected = set(range(first, last + 1))
        missing = sorted(expected - found_numbers)

        self.logger.check_separator()
        self.logger.check_log(f"Check references: {file_name}")
        self.logger.check_log(f"First number: {first}")
        self.logger.check_log(f"Last number: {last}")
        self.logger.check_log(f"Found unique numbers: {len(found_numbers)}")

        if missing:
            self.logger.check_log(f"Missing numbers: {missing}")
        else:
            self.logger.check_log("Missing numbers: none")