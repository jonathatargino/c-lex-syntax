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

    @staticmethod
    def _is_identifier_start(ch: str) -> bool:
        return ch.isalpha() or ch == "_"

    @staticmethod
    def _is_ident_part(ch: str) -> bool:
        return ch.isalnum() or ch == "_"

    def _emit_identifier_incremental_id(self, name: str):
        if name not in self.symbols:
            self.symbols[name] = {
                "id": self._next_sym_id,
                "count": 1
            }
            self._next_sym_id += 1
        else:
            self.symbols[name]["count"] += 1

        sym_id = self.symbols[name]["id"]
        self.tokens.append(Token(TokenType.ID, lexema=name, atributo=f"id{sym_id}"))


    def _is_string_start(self, ch: str) -> bool:
        return ch == '"' or ch == "'"

    def _handle_string_values(self):
        if self._peek() == '"':
                lex = ""
                self.i += 1
                while True:
                    current = self._advance()
                    has_string_closed = current == '"'
                    if has_string_closed:
                        self.tokens.append(Token(TokenType.STR_VALUE, lex))
                        break

                    is_string_not_closed = current == "\n" or current == "\0"
                    if is_string_not_closed:
                        self.tokens.append(Token(TokenType.ERRO, lex))
                        break

                    lex += current

        elif  self._peek() == "'":
            lex = ""
            self.i += 1
            while True:
                current = self._advance()
                has_string_closed = current == "'"
                if has_string_closed:
                    self.tokens.append(Token(TokenType.STR_VALUE, lex))
                    break

                is_string_not_closed = current == "\n" or current == "\0"
                if is_string_not_closed:
                    self.tokens.append(Token(TokenType.ERRO, lex))
                    break
            
                lex += current


    def _handle_space(self):
        self._advance()

    def _handle_identifier(self):
        lex = self._advance()
        while self._is_ident_part(self._peek()):
            lex += self._advance()
        if lex in KEYWORDS:
            self.tokens.append(Token(TokenType.KEYWORD, lex))
        else:
            self._emit_identifier_incremental_id(lex)

    def _handle_number_values(self):
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
            self.tokens.append(Token(TokenType.ERRO, lex))
            return
            

        if self._is_ident_part(self._peek()):
            while self._is_ident_part(self._peek()):
                lex += self._advance()
            self.tokens.append(Token(TokenType.ERRO, lex))
        else:
            self.tokens.append(Token(TokenType.NUM, lex))

    def _is_comment_start(self, chars: str) -> bool:
        return chars == "//" or chars == "/*"
    
    def _handle_comment(self):
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
                    break

                if self._peek() == "\0":
                    break
                    
                self.i += 1

    def _is_preprocessor_directive_start(self, ch: str) -> bool:
        return ch == "#"
    
    def _handle_preprocessor_directive(self):
        lex = ""
        while True:
            current = self._advance()
            if current == "\n" or current == "\0":
                self.tokens.append(Token(TokenType.PP_DIRECTIVE, lex))
                break

            lex += current
    
    def _is_single_operator(self, ch: str) -> bool:
        return ch in OPERATORS_1
    
    def _is_double_operator(self, chars: str) -> bool:
        return chars in OPERATORS_2
    
    def _handle_single_operator(self, ch: str):
        self.tokens.append(Token(OPERATORS_1[ch], self._advance()))

    def _handle_double_operator(self, chars: str):  
        self.tokens.append(Token(OPERATORS_2[chars], chars))
        self.i += 2

    def _is_delimiter(self, ch: str) -> bool:
        return ch in DELIMS
    
    def _handle_delimiter(self, ch: str):
        PAIRS = {")": "(", "]": "[", "}": "{"}
        if ch in PAIRS.values():
            self._delimiter_stack.append(ch)
        elif ch in PAIRS:
            if not self._delimiter_stack:
                self.tokens.append(Token(TokenType.ERRO, self._advance()))
                return

            last_stack_value = self._delimiter_stack[-1]
            if last_stack_value != PAIRS[ch]:
                self.tokens.append(Token(TokenType.ERRO, self._advance()))
            else:
                self._delimiter_stack.pop()
        
        self.tokens.append(Token(DELIMS[ch], self._advance()))

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
                    self.tokens.append(Token(TokenType.ERRO, self._advance()))
    
        # fim de arquivo
        self.tokens.append(Token(TokenType.EOF, ""))
        return self.tokens

    def print_tokens(self):
        print("\n=== LISTA DE TOKENS ===")
        for t in self.tokens:
            print(f"{t.tipo.name:<7}  {t.lexema}  {t.atributo if t.atributo else ''}")

    def print_symbol_table(self, sort_by_name: bool = False):
        print("\n=== TABELA DE SÍMBOLOS ===")
        items = list(self.symbols.items())
        if sort_by_name:
            items.sort(key=lambda x: x[0])  # ordena alfabeticamente
        for name, data in items:
            print(f"id{data['id']:<3}  {name:<10}  ocorrências: {data['count']}")