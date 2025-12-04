from lexer.token import TokenType


OPERATORS_2 = {
    "==": TokenType.EQ,
    "!=": TokenType.NE,
    "<=": TokenType.LE,
    ">=": TokenType.GE,
    "++": TokenType.INC,
    "--": TokenType.DEC,
    "+=": TokenType.COMPOST_SUM,
    "-=": TokenType.COMPOST_SUB,
    "*=": TokenType.COMPOST_MUL,
    "/=": TokenType.COMPOST_DIV,
    "&&": TokenType.AND,
    "||": TokenType.OR,
}
# operadores simples (1 char)
OPERATORS_1 = {
    "=": TokenType.ASSIGN,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,
    "<": TokenType.LT,
    ">": TokenType.GT,
    "%": TokenType.MOD,
    "&": TokenType.ADDRESS_OF,
}
# delimitadores (pontuação)
DELIMS = {
    ";": TokenType.SEMI,
    ",": TokenType.COMMA,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    "[": TokenType.LBRACK,
    "]": TokenType.RBRACK
}