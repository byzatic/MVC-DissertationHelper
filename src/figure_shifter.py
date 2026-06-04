from config import FIGURE_START_FROM, FIGURE_SHIFT


class FigureShifter:
    def shift_number(self, value: int) -> int:
        if value >= FIGURE_START_FROM:
            return value + FIGURE_SHIFT
        return value

    def process_figure_number(self, number_text: str) -> str:
        old = int(number_text)
        new = self.shift_number(old)
        return str(new)
