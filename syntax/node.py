from dataclasses import dataclass
from typing import List, Any, Union

NodeLike = Union[
    "ProgramNode", "LetNode", "AssignNode", "IfNode", "WhileNode",
    "ReturnNode", "BlockNode", "CallNode", "IndexNode", "BinOpNode",
    "IdentifierNode", "LiteralNode"
]


@dataclass
class Node: pass

@dataclass
class ProgramNode(Node):
    body: List[Node]
    line: int
    col: int

@dataclass
class LetNode(Node):
    lhs: Any
    init: Any
    line: int
    col: int

@dataclass
class AssignNode(Node):
    target: Any
    value: Any
    line: int
    col: int

@dataclass
class IfNode(Node):
    test: Any
    then: Any
    otherwise: Any
    line: int
    col: int

@dataclass
class WhileNode(Node):
    test: Any
    body: Any
    line: int
    col: int

@dataclass
class ReturnNode(Node):
    value: Any
    line: int
    col: int

@dataclass
class BlockNode(Node):
    body: List[Any]
    line: int
    col: int

@dataclass
class CallNode(Node):
    callee: Any
    args: List[Any]
    line: int
    col: int

@dataclass
class IndexNode(Node):
    target: Any
    index: Any
    line: int
    col: int

@dataclass
class BinOpNode(Node):
    left: Any
    right: Any
    op: str
    line: int
    col: int

@dataclass
class IdentifierNode(Node):
    name: str
    line: int
    col: int

@dataclass
class LiteralNode(Node):
    value: Any
    line: int
    col: int

NodeLike = Any

def node_label(n: NodeLike) -> str:
    tname = type(n).__name__
    if tname == "ProgramNode": return "Program"
    if tname == "LetNode":     return "Let"
    if tname == "AssignNode":  return "Assign"
    if tname == "IfNode":      return "If"
    if tname == "WhileNode":   return "While"
    if tname == "ReturnNode":  return "Return"
    if tname == "BlockNode":   return "Block"
    if tname == "CallNode":    return "Call"
    if tname == "IndexNode":   return "Index"
    if tname == "BinOpNode":   return f"BinOp('{getattr(n, 'op', '?')}')"
    if tname == "VarNode":     return f"Id({getattr(n, 'name', '?')})"
    if tname == "NumNode":     return f"Num({getattr(n, 'value', '?')})"
    if tname == "BoolNode":
        v = getattr(n, "value", None)
        return f"Bool({str(v).lower()})" if isinstance(v, bool) else "Bool(?)"

    return tname