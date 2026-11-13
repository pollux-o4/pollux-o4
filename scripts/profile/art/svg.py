"""SVG 문자열 조립 도구. 그림 모듈은 모두 이것만으로 SVG를 만든다."""
from ..style import SVG_SANS


def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>'


def write(out, name, svg):
    with open(f"{out}/{name}.svg", "w", encoding="utf-8") as f:
        f.write(svg)


def text(x, y, s, fill, size, family=SVG_SANS, weight=400, anchor="start", spacing=0):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" letter-spacing="{spacing}">{s}</text>')
