from syntax.node import NodeLike, node_label
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass
import matplotlib.pyplot as plt

def children(n: NodeLike) -> List[NodeLike]:
    tname = type(n).__name__

    if tname == "ProgramNode": return list(getattr(n, "body", []))
    if tname == "LetNode":     return [getattr(n, "lhs", None), getattr(n, "init", None)]
    if tname == "AssignNode":  return [getattr(n, "target", None), getattr(n, "value", None)]
    if tname == "IfNode":
        lst = [getattr(n, "test", None), getattr(n, "then", None)]
        other = getattr(n, "otherwise", None)
        if other is not None: lst.append(other)
        return lst
    if tname == "WhileNode":   return [getattr(n, "test", None), getattr(n, "body", None)]
    if tname == "ReturnNode":
        v = getattr(n, "value", None)
        return [v] if v is not None else []
    if tname == "BlockNode":   return list(getattr(n, "body", []))
    if tname == "CallNode":    return [getattr(n, "callee", None)] + list(getattr(n, "args", []))
    if tname == "IndexNode":   return [getattr(n, "target", None), getattr(n, "index", None)]
    if tname == "BinOpNode":   return [getattr(n, "left", None), getattr(n, "right", None)]

    return []

def _compute_layout(n: NodeLike, x0=0.0, y0=0.0, y_spacing=1.6) -> Tuple[Dict[int,Tuple[float,float]], float]:
    ch = [c for c in children(n) if c is not None]
    if not ch:
        return ({id(n): (x0, y0)}, 1.0)

    pos: Dict[int,Tuple[float,float]] = {}
    widths: List[float] = []
    subs: List[NodeLike] = []

    for c in ch:
        subpos, w = _compute_layout(c, 0, 0, y_spacing)
        pos.update(subpos)
        widths.append(w)
        subs.append(c)

    total_w = sum(widths) + (len(widths)-1)*0.8
    cur_x = x0 - total_w/2.0

    def shift(node: NodeLike, dx: float, dy: float):
        x, y = pos[id(node)]
        pos[id(node)] = (x + dx, y + dy)
        for cc in children(node):
            if cc is not None:
                shift(cc, dx, dy)

    for c, w in zip(subs, widths):
        cx = cur_x + w/2.0
        shift(c, cx, y0 - y_spacing)
        cur_x += w + 0.8

    pos[id(n)] = (x0, y0)
    return pos, total_w

def draw_tree(root: NodeLike, filename: str, figsize=(10, 7), dpi: int = 160):
    pos, _ = _compute_layout(root, 0.0, 0.0)

    fig, ax = plt.subplots(figsize=figsize)
    ax.set_axis_off()

    def draw_edges(node: NodeLike):
        x, y = pos[id(node)]
        for c in children(node):
            if c is None:
                continue
            xc, yc = pos[id(c)]
            ax.plot([x, xc], [y-0.05, yc+0.05])
            draw_edges(c)

    def draw_nodes(node: NodeLike):
        x, y = pos[id(node)]
        bbox = dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1)
        ax.text(x, y, node_label(node), ha="center", va="center", bbox=bbox, fontsize=10)
        for c in children(node):
            if c is not None:
                draw_nodes(c)

    draw_edges(root)
    draw_nodes(root)

    xs = [xy[0] for xy in pos.values()]
    ys = [xy[1] for xy in pos.values()]
    pad = 1.2
    ax.set_xlim(min(xs)-pad, max(xs)+pad)
    ax.set_ylim(min(ys)-pad, max(ys)+pad)
    plt.tight_layout()
    plt.savefig(filename, dpi=dpi, bbox_inches="tight")
    plt.close(fig)