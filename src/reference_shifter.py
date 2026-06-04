import re

from config import START_FROM, SHIFT


class ReferenceShifter:
    def shift_number(self, value: int) -> int:
        if value >= START_FROM:
            return value + SHIFT
        return value

    def process_token(self, token: str, replacements: list[str]) -> str:
        token = token.strip()

        if "-" in token:
            left, right = re.split(r"\s*-\s*", token, maxsplit=1)

            left_old = int(left)
            right_old = int(right)

            left_new = self.shift_number(left_old)
            right_new = self.shift_number(right_old)

            if left_old != left_new:
                replacements.append(f"{left_old} -> {left_new}")

            if right_old != right_new:
                replacements.append(f"{right_old} -> {right_new}")

            return f"{left_new}-{right_new}"

        old = int(token)
        new = self.shift_number(old)

        if old != new:
            replacements.append(f"{old} -> {new}")

        return str(new)

    def process_reference_text(self, ref_text: str, replacements: list[str]) -> str:
        inner = ref_text[1:-1]
        tokens = inner.split(",")

        updated = [
            self.process_token(token, replacements)
            for token in tokens
        ]

        return "[" + ", ".join(updated) + "]"

    def extract_numbers_from_reference(self, ref_text: str) -> set[int]:
        inner = ref_text[1:-1]
        tokens = inner.split(",")

        numbers = set()

        for token in tokens:
            token = token.strip()

            if "-" in token:
                left, right = re.split(r"\s*-\s*", token, maxsplit=1)

                left_num = int(left)
                right_num = int(right)

                start = min(left_num, right_num)
                end = max(left_num, right_num)

                numbers.update(range(start, end + 1))
            else:
                numbers.add(int(token))

        return numbers