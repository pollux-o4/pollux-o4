"""연도표 아래 대표 기술. 네 분류 = 네 칸, 칸마다 공식 로고 + 이름.
배지 대신 직접 그려 다른 섹션과 같은 축·헤어라인·서체를 유지한다. 표식 규칙은 marks."""
from ..content import STACK
from ..style import SVG_MONO, THEMES, axis
from .marks import mark
from .svg import svg, text, write

W, TOP, ROW, ICON = 1000, 34, 34, 18
X0 = axis(W)


def stack(t):
    cw = (W - X0 * 2) / len(STACK)
    out = [text(X0, 14, "STACK", t["sub"], 11, SVG_MONO, 500, spacing=1.2)]
    for i, (group, items) in enumerate(STACK):
        x = X0 + i * cw
        out.append(f'<line x1="{x}" y1="{TOP}" x2="{x + cw - 28}" y2="{TOP}" stroke="{t["rule"]}"/>')
        out.append(text(x, TOP + 24, group, t["sub"], 12, weight=500))
        for j, (name, slug) in enumerate(items):
            y = TOP + 44 + j * ROW
            out.append(mark(slug, x, y, t, ICON))
            out.append(text(x + ICON + 10, y + 14, name, t["ink"], 13.5, weight=500))
    rows = max(len(items) for _, items in STACK)
    return svg(W, TOP + 44 + rows * ROW, "".join(out))


def render(out):
    for name, t in THEMES.items():
        write(out, f"stack-{name}", stack(t))
