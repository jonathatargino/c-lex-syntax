# lexer/token.py
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional

# ------------------------------
# Enum para tipos de tokens
# ------------------------------
class TokenType(Enum):
    # categorias gerais
    ID = auto()       # identificadores (variáveis, funções)
    KEYWORD = auto()  # palavras reservadas (int, if, while, etc.)
    NUM = auto()      # números inteiros
    EOL = auto()      # fim de linha
    EOF = auto()      # fim de arquivo
    ERRO = auto()     # sequência inválida (ex.: "8a")
    STR_VALUE = auto()
    PP_DIRECTIVE = auto()

    LET = auto()      # palavra reservada 'let'
    IF = auto()       # palavra reservada 'if'
    ELSE = auto()     # palavra reservada 'else'
    FOR = auto()      # palavra reservada 'for'
    WHILE = auto()    # palavra reservada 'while'
    RETURN = auto()   # palavra reservada 'return'

    # operadores de 2 caracteres
    EQUAL = auto()       # ==
    NE = auto()       # !=
    LE = auto()       # <=
    GE = auto()       # >=
    COMPOST_SUM = auto()  # +=
    COMPOST_SUB = auto()  # -=
    COMPOST_MUL = auto()  # *=
    COMPOST_DIV = auto()  # /=
    DEC = auto()      # --
    INC = auto()      # ++
    AND = auto()      # &&
    OR = auto()       # ||

    # operadores de 1 caractere
    ASSIGN = auto()   # =
    PLUS = auto()     # +
    MINUS = auto()    # -
    STAR = auto()     # *
    SLASH = auto()    # /
    LT = auto()       # <
    GT = auto()       # >
    MOD = auto()      # %
    ADDRESS_OF = auto()  # &

    # delimitadores
    SEMI = auto()     # ;
    COMMA = auto()    # ,
    LPAREN = auto()   # (
    RPAREN = auto()   # )
    LBRACE = auto()   # {
    RBRACE = auto()   # }
    LBRACK = auto()   # [
    RBRACK = auto()   # ]

# ------------------------------
# Classe Token
# ------------------------------
@dataclass
class Token:
    type: str
    lex: str
    line: int
    col: int

    def __repr__(self) -> str:
        return f"<{self.type}, {self.lex}>"