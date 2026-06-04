from config import LOG_ENABLED

class ScriptLogger:
    def __init__(self):
        self.logs: list[str] = []
        self.check_logs: list[str] = []

    def log(self, message: str = ""):
        if LOG_ENABLED:
            self.logs.append(message)

    def check_log(self, message: str = ""):
        if LOG_ENABLED:
            self.check_logs.append(message)

    def separator(self):
        self.log("=" * 80)

    def check_separator(self):
        self.check_log("=" * 80)

    def flush(self):
        output = []

        output.extend(self.logs)

        if self.check_logs:
            output.append("=" * 80)
            output.append("Reference sequence check")
            output.extend(self.check_logs)

        if output:
            print("\n".join(output))