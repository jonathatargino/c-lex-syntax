from dataclasses import dataclass
from typing import List, Optional, Any
from syntax.node import NodeLike, IdentifierNode, LiteralNode, IndexNode, BinOpNode
from syntax.node import ProgramNode, LetNode, AssignNode, IfNode, WhileNode, ReturnNode, BlockNode, CallNode
from lexer.token import Token, TokenType


@dataclass
class Token:
    type: str
    lex: str
    line: int
    col: int

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.errors: List[str] = []

    def peek(self) -> Token:
        if self.pos >= len(self.tokens):
            return Token("EOL", "", -1, -1)
        return self.tokens[self.pos]

    def lookahead(self, k: int) -> Token:
        idx = self.pos + k
        if idx >= len(self.tokens):
            return Token("EOL", "", -1, -1)
        return self.tokens[idx]

    def emit_error(self, msg: str):
        self.errors.append(msg)

    def consume(self, expected: Optional[TokenType] = None) -> Token:
        if self.pos >= len(self.tokens):
            return Token("EOL", "", -1, -1)
        tok = self.tokens[self.pos]
        if expected:
            if tok.type == expected:
                self.pos += 1
                return tok
            self.emit_error(f"[ERRO] Esperado {expected}, obtido {tok.type} na linha {tok.line}")
            self.pos += 1
            return Token(expected, "", tok.line, tok.col)
        self.pos += 1
        return tok

    def match(self, *types: str) -> bool:
        return self.peek().type in types

    def synchronize(self):
        sync_tokens = {"SEMI", "RBRACE", "EOL"}
        first_stmt = {"LET", "IF", "WHILE", "RETURN", "LBRACE", "ID", "NUM"}
        while self.pos < len(self.tokens):
            if self.tokens[self.pos].type in sync_tokens:
                self.pos += 1
                return
            if self.tokens[self.pos].type in first_stmt:
                return
            self.pos += 1

    def starts_assignment(self) -> bool:
        if not self.match(TokenType.ID):
            return False
        if self.lookahead(1).type == TokenType.ASSIGN:
            return True
        if self.lookahead(1).type == TokenType.LBRACK:
            depth = 0
            i = self.pos + 1

            ## While garante que os colchetes se fechem e o conteúdo dentro deles possa ter um tamanho ilimitado
            while i < len(self.tokens):
                t = self.tokens[i]
                if t.type == "LBRACK":
                    depth += 1
                elif t.type == "RBRACK":
                    depth -= 1
                    if depth == 0:
                        if i + 1 < len(self.tokens) and self.tokens[i + 1].type == "EQUAL":
                            return True
                        break
                i += 1
        return False

    def parse_program(self) -> ProgramNode:
        body = []
        while self.pos < len(self.tokens):
            if self.match(TokenType.EOL):
                self.consume(TokenType.EOL)
                continue
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        return ProgramNode(body=body, line=1, col=1)

    def parse_statement(self):
        if self.match(TokenType.LET):
            return self.parse_let_statement()
        elif self.match(TokenType.IF):
            return self.parse_if_statement()
        elif self.match(TokenType.WHILE):
            return self.parse_while_statement()
        elif self.match(TokenType.RETURN):
            return self.parse_return_statement()
        elif self.match(TokenType.LBRACE):
            return self.parse_block()
        elif self.match(TokenType.ELSE):
            tok = self.consume(TokenType.ELSE)
            self.emit_error(f"[ERRO] 'else' sem 'if' correspondente na linha {tok.line}")
            self.synchronize()
            return None
        elif self.starts_assignment():
            return self.parse_assignment_statement()
        elif self.match(TokenType.ID, TokenType.NUM, TokenType.LPAREN):
            return self.parse_expression_statement()
        elif self.match(TokenType.PP_DIRECTIVE):
            self.consume(TokenType.PP_DIRECTIVE)
            return None
        elif self.match(TokenType.EOF):
            self.consume(TokenType.EOF)
            return None
        else:
            tok = self.peek()
            self.emit_error(f"[ERRO] Token inesperado {tok.type} na linha {tok.line}")
            self.synchronize()
            return None

    def parse_let_statement(self) -> LetNode:
        let_token = self.consume(TokenType.LET)
        id_token = self.consume(TokenType.ID)
        left_hand_side = IdentifierNode(id_token.lex, line=id_token.line, col=id_token.col)
        equal_token = self.consume(TokenType.ASSIGN)
        init = None

        if self.match(TokenType.NUM, TokenType.ID, TokenType.LPAREN, TokenType.STR_VALUE):
            init = self.parse_expression()
        else:
            self.emit_error(f"[ERRO] Esperado expressão após '=', obtido {self.peek().type} na linha {self.peek().line}")

        if self.match(TokenType.SEMI):
            self.consume(TokenType.SEMI)
        return LetNode(lhs=left_hand_side, init=init, line=let_token.line, col=let_token.col)

    def parse_assignment_statement(self) -> AssignNode:
        id_token = self.consume(TokenType.ID)
        target: NodeLike = IdentifierNode(id_token.lex, line=id_token.line, col=id_token.col)

        # assignment em um index específico
        while self.match(TokenType.LBRACK):
            lbr = self.consume(TokenType.LBRACK)
            idx = self.parse_expression()
            if self.match(TokenType.RBRACK):
                self.consume(TokenType.RBRACK)
            else:
                self.emit_error(f"[ERRO] Esperado RBRACK, obtido {self.peek().type} na linha {self.peek().line}")
                self.synchronize()
                break
            target = IndexNode(target=target, index=idx, line=lbr.line, col=lbr.col)

        self.consume(TokenType.ASSIGN)
        value = self.parse_expression()
        if self.match(TokenType.SEMI):
            self.consume(TokenType.SEMI)
        return AssignNode(target=target, value=value, line=id_token.line, col=id_token.col)

    def parse_if_statement(self) -> IfNode:
        if_token = self.consume(TokenType.IF)
        self.consume(TokenType.LPAREN)
        test = self.parse_expression()
        if not self.match(TokenType.RPAREN):
            self.emit_error(f"[ERRO] Esperado RPAREN, obtido {self.peek().type} na linha {self.peek().line}")
            self.synchronize()
        else:
            self.consume(TokenType.RPAREN)
        then = self.parse_statement()
        otherwise = None
        if self.match(TokenType.ELSE):
            self.consume(TokenType.ELSE)
            otherwise = self.parse_statement()
        return IfNode(test=test, then=then, otherwise=otherwise, line=if_token.line, col=if_token.col)

    def parse_while_statement(self) -> WhileNode:
        while_token = self.consume(TokenType.WHILE)
        self.consume(TokenType.LPAREN)
        test = self.parse_expression()
        if not self.match(TokenType.RPAREN):
            self.emit_error(f"[ERRO] Esperado RPAREN, obtido {self.peek().type} na linha {self.peek().line}")
            self.synchronize()
        else:
            self.consume(TokenType.RPAREN)
        body = self.parse_statement()
        return WhileNode(test=test, body=body, line=while_token.line, col=while_token.col)

    def parse_return_statement(self) -> ReturnNode:
        return_token = self.consume(TokenType.RETURN)
        value = None
        if not self.match(TokenType.SEMI):
            value = self.parse_expression()
        if self.match(TokenType.SEMI):
            self.consume(TokenType.SEMI)
        return ReturnNode(value=value, line=return_token.line, col=return_token.col)

    def parse_block(self) -> BlockNode:
        lbrace = self.consume(TokenType.LBRACE)
        body = []
        while not self.match(TokenType.RBRACE) and self.pos < len(self.tokens):
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        if self.match(TokenType.RBRACE):
            self.consume(TokenType.RBRACE)
        else:
            self.emit_error(f"[ERRO] Esperado RBRACE, obtido EOF na linha {lbrace.line}")
        return BlockNode(body=body, line=lbrace.line, col=lbrace.col)

    def parse_expression(self) -> Any:
        return self.parse_and_operator()

    def parse_and_operator(self):
        node = self.parse_equality_operator()
        while self.match(TokenType.AND):
            op = self.consume()
            right = self.parse_equality_operator()
            node = BinOpNode(left=node, right=right, op=op.lex, line=op.line, col=op.col)
        return node

    def parse_equality_operator(self) -> Any:
        node = self.parse_relational_operator()
        while self.match(TokenType.EQUAL, TokenType.NE):
            op = self.consume()
            right = self.parse_relational_operator()
            node = BinOpNode(left=node, right=right, op=op.lex, line=op.line, col=op.col)
        return node

    def parse_relational_operator(self) -> Any:
        node = self.parse_additive_operator()
        while self.match(TokenType.LT, TokenType.GT, TokenType.LE, TokenType.GE):
            op = self.consume()
            right = self.parse_additive_operator()
            node = BinOpNode(left=node, right=right, op=op.lex, line=op.line, col=op.col)
        return node

    def parse_additive_operator(self) -> Any:
        node = self.parse_term_operator()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.consume()
            right = self.parse_term_operator()
            node = BinOpNode(left=node, right=right, op=op.lex, line=op.line, col=op.col)
        return node

    def parse_term_operator(self) -> Any:
        node = self.parse_factor_operator()
        while self.match(TokenType.STAR, TokenType.SLASH):
            op = self.consume()
            right = self.parse_factor_operator()
            node = BinOpNode(left=node, right=right, op=op.lex, line=op.line, col=op.col)
        return node

    def parse_factor_operator(self) -> Any:
        node = self.parse_literal_or_parenthesis()
        while self.match(TokenType.LPAREN, TokenType.LBRACK):
            if self.match(TokenType.LPAREN):
                lparen = self.consume(TokenType.LPAREN)
                args = []
                if not self.match(TokenType.RPAREN):
                    args.append(self.parse_expression())
                    while self.match(TokenType.COMMA):
                        self.consume(TokenType.COMMA)
                        args.append(self.parse_expression())
                if self.match(TokenType.RPAREN):
                    self.consume(TokenType.RPAREN)
                else:
                    self.emit_error(f"[ERRO] Esperado RPAREN na chamada de função, obtido {self.peek().type} na linha {self.peek().line}")
                    self.synchronize()
                node = CallNode(callee=node, args=args, line=lparen.line, col=lparen.col)
            elif self.match(TokenType.LBRACK):
                lbrack = self.consume(TokenType.LBRACK)
                index = self.parse_expression()
                if self.match(TokenType.RBRACK):
                    self.consume(TokenType.RBRACK)
                else:
                    self.emit_error(f"[ERRO] Esperado RBRACK, obtido {self.peek().type} na linha {self.peek().line}")
                    self.synchronize()
                node = IndexNode(target=node, index=index, line=lbrack.line, col=lbrack.col)
        return node

    def parse_expression_statement(self):
        expr = self.parse_expression()
        if self.match(TokenType.SEMI):
            self.consume(TokenType.SEMI)
        return expr

    def parse_literal_or_parenthesis(self) -> Any:
        if self.pos >= len(self.tokens):
            return LiteralNode(value=0, line=-1, col=-1)
        tok = self.peek()
        if self.match(TokenType.NUM):
            t = self.consume(TokenType.NUM)
            return LiteralNode(t.lex, line=t.line, col=t.col)
        if self.match(TokenType.ID):
            t = self.consume(TokenType.ID)
            return IdentifierNode(name=t.lex, line=t.line, col=t.col)
        if self.match(TokenType.LPAREN):
            self.consume(TokenType.LPAREN)
            expr = self.parse_expression()
            if self.match(TokenType.RPAREN):
                self.consume(TokenType.RPAREN)
            else:
                self.emit_error(f"[ERRO] Esperado RPAREN, obtido {self.peek().type} na linha {self.peek().line}")
                self.synchronize()
            return expr
        if self.match(TokenType.STR_VALUE):
            t = self.consume(TokenType.STR_VALUE)
            return LiteralNode(value=t.lex, line=t.line, col=t.col)
        if tok.type in {TokenType.SEMI, TokenType.EOL, TokenType.RBRACE}:
            return LiteralNode(value=0, line=tok.line, col=tok.col)


        self.emit_error(f"[ERRO] Token inesperado {tok.type} na linha {tok.line}")
        self.consume()
        return LiteralNode(value=0, line=tok.line, col=tok.col)
