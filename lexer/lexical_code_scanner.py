from lexer.scanner import Scanner
from lexer.operators import OPERATORS_2, OPERATORS_1, DELIMS
from lexer.keywords import KEYWORDS
from lexer.token import TokenType, Token
from typing import List, Dict
from lexer.operators import DELIMS, OPERATORS_1, OPERATORS_2

class LexicalCodeScanner(Scanner):
    def __init__(self, text: str):
        super().__init__(text)
        self.tokens: List[Token] = []
        self.symbols: Dict[str, Dict[str, int]] = {}
        self._next_sym_id = 1
        self._delimiter_stack = []

        # >>> ADICIONADO <<<
        self.line = 1
        self.col = 1

    # >>> ADICIONADO: atualizar linha/col por caractere <<<
    def _advance(self):
        ch = self.text[self.i]

        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1

        self.i += 1
        return ch

    @staticmethod
    def _is_identifier_start(ch: str) -> bool:
        return ch.isalpha() or ch == "_"

    @staticmethod
    def _is_ident_part(ch: str) -> bool:
        return ch.isalnum() or ch == "_"

    def _emit_identifier_incremental_id(self, name: str, line: int, col: int):
        if name not in self.symbols:
            self.symbols[name] = {
                "id": self._next_sym_id,
                "count": 1
            }
            self._next_sym_id += 1
        else:
            self.symbols[name]["count"] += 1

        self.tokens.append(Token(TokenType.ID, name, line, col))

    def _is_string_start(self, ch: str) -> bool:
        return ch == '"' or ch == "'"

    def _handle_string_values(self):
        start_line = self.line
        start_col = self.col

        if self._peek() == '"':
            lex = ""
            self.i += 1
            self.col += 1

            while True:
                current = self._advance()
                if current == '"':
                    self.tokens.append(Token(TokenType.STR_VALUE, lex, start_line, start_col))
                    break
                if current == "\n" or current == "\0":
                    self.tokens.append(Token(TokenType.ERRO, lex, start_line, start_col))
                    break
                lex += current

        elif self._peek() == "'":
            lex = ""
            self.i += 1
            self.col += 1

            while True:
                current = self._advance()
                if current == "'":
                    self.tokens.append(Token(TokenType.STR_VALUE, lex, start_line, start_col))
                    break
                if current == "\n" or current == "\0":
                    self.tokens.append(Token(TokenType.ERRO, lex, start_line, start_col))
                    break
                lex += current

    def _handle_space(self):
        self._advance()

    def _handle_identifier(self):
        start_line = self.line
        start_col = self.col

        lex = self._advance()
        while self._is_ident_part(self._peek()):
            lex += self._advance()

        if lex in KEYWORDS:
            self.tokens.append(Token(KEYWORDS[lex], lex, start_line, start_col))
        else:
            self._emit_identifier_incremental_id(lex, start_line, start_col)

    def _handle_number_values(self):
        start_line = self.line
        start_col = self.col

        lex = self._advance()
        while self._peek().isdigit():
            lex += self._advance()

        nextTwoChars = self._peek2()
        isFloat = nextTwoChars[0] == "." and nextTwoChars[1].isdigit()
        if (isFloat):
            lex += self._advance()
            while self._peek().isdigit():
                lex += self._advance()

        isFloatWithComma = nextTwoChars[0] == "," and nextTwoChars[1].isdigit()
        if (isFloatWithComma):
            lex += self._advance()
            while self._peek().isdigit():
                lex += self._advance()
            self.tokens.append(Token(TokenType.ERRO, lex, start_line, start_col))
            return

        if self._is_ident_part(self._peek()):
            while self._is_ident_part(self._peek()):
                lex += self._advance()
            self.tokens.append(Token(TokenType.ERRO, lex, start_line, start_col))
        else:
            self.tokens.append(Token(TokenType.NUM, lex, start_line, start_col))

    def _is_comment_start(self, chars: str) -> bool:
        return chars == "//" or chars == "/*"

    def _handle_comment(self):
        start_line = self.line
        start_col = self.col

        isLineComment = self._peek2() == "//"
        if (isLineComment):
            while True:
                current = self._advance()
                if current == "\n" or current == "\0":
                    break
        else:
            while True:
                if self._peek2() == "*/":
                    self.i += 2
                    self.col += 2
                    break
                if self._peek() == "\0":
                    break
                self.i += 1
                self.col += 1

    def _is_preprocessor_directive_start(self, ch: str) -> bool:
        return ch == "#"

    def _handle_preprocessor_directive(self):
        start_line = self.line
        start_col = self.col

        lex = ""
        while True:
            current = self._advance()
            if current == "\n" or current == "\0":
                self.tokens.append(Token(TokenType.PP_DIRECTIVE, lex, start_line, start_col))
                break
            lex += current

    def _is_single_operator(self, ch: str) -> bool:
        return ch in OPERATORS_1

    def _is_double_operator(self, chars: str) -> bool:
        return chars in OPERATORS_2

    def _handle_single_operator(self, ch: str):
        start_line = self.line
        start_col = self.col
        lex = self._advance()
        self.tokens.append(Token(OPERATORS_1[ch], lex, start_line, start_col))

    def _handle_double_operator(self, chars: str):
        start_line = self.line
        start_col = self.col
        self.i += 2
        self.col += 2
        self.tokens.append(Token(OPERATORS_2[chars], chars, start_line, start_col))

    def _is_delimiter(self, ch: str) -> bool:
        return ch in DELIMS

    def _handle_delimiter(self, ch: str):
        start_line = self.line
        start_col = self.col

        PAIRS = {")": "(", "]": "[", "}": "{"}
        if ch in PAIRS.values():
            self._delimiter_stack.append(ch)
        elif ch in PAIRS:
            if not self._delimiter_stack:
                self.tokens.append(Token(TokenType.ERRO, self._advance(), start_line, start_col))
                return

            last_stack_value = self._delimiter_stack[-1]
            if last_stack_value != PAIRS[ch]:
                self.tokens.append(Token(TokenType.ERRO, self._advance(), start_line, start_col))
            else:
                self._delimiter_stack.pop()

        lex = self._advance()
        self.tokens.append(Token(DELIMS[ch], lex, start_line, start_col))

    def scan_all(self) -> List[Token]:
        while self.i < len(self.text):
            ch = self._peek()
            match True:
                case _ if self._is_string_start(ch):
                    self._handle_string_values()
                case _ if ch.isspace():
                    self._handle_space()
                case _ if self._is_identifier_start(ch):
                    self._handle_identifier()
                case _ if ch.isdigit():
                    self._handle_number_values()
                case _ if self._is_comment_start(self._peek2()):
                    self._handle_comment()
                case _ if self._is_preprocessor_directive_start(ch):
                    self._handle_preprocessor_directive()
                case _ if self._is_double_operator(self._peek2()):
                    self._handle_double_operator(self._peek2())
                case _ if self._is_single_operator(ch):
                    self._handle_single_operator(ch)
                case _ if self._is_delimiter(ch):
                    self._handle_delimiter(ch)
                case _:
                    start_line = self.line
                    start_col = self.col
                    self.tokens.append(Token(TokenType.ERRO, self._advance(), start_line, start_col))

        # fim de arquivo
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.col))
        return self.tokens

    def get_tokens(self) -> List[Token]:
        return self.tokens
