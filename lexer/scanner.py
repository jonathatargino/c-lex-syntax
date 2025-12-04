class Scanner:
    def __init__(self, text: str):
        self.text = text
        self.i = 0 

    def _peek(self) -> str:
        return self.text[self.i] if self.i < len(self.text) else "\0"

    def _peek2(self) -> str:
        if self.i + 1 < len(self.text):
            return self.text[self.i] + self.text[self.i + 1]
        return "\0\0"

    def _advance(self) -> str:
        ch = self._peek()
        self.i += 1
        return ch