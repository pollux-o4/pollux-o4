"""히어로 아래 오른쪽 프로필 링크(Portfolio·LinkedIn). 아이콘 + 이름 + ↗ 한 칸씩.
아이콘은 marks 레지스트리(공식 로고 또는 선 기호)이라 페이지 전체가 한 벌로 읽힌다."""
from ..content import PERSON
from ..style import SVG_SANS, THEMES, font
from .marks import mark
from .svg import svg, text, write

H, ICON = 32, 18


def width(name):
    """아이콘(18) + 간격(8) + 실제 글자 폭 + 간격(8) + 화살표(8). 글자 폭은 렌더 서체로 잰다."""
    return round(26 + font("medium", 14).getlength(name) + 16)


def bar(name, slug, t):
    w = width(name)
    return svg(w, H, f'<g transform="translate(0,7)">{mark(slug, 0, 0, t, ICON)}</g>'
               + text(26, 21, name, t["ink"], 14, SVG_SANS, 500)
               + f'<path d="M{w - 9},{H / 2 + 4} l7,-7 M{w - 7},{H / 2 - 3} h5 v5" fill="none" '
                 f'stroke="{t["acc"]}" stroke-width="1.6" stroke-linecap="round"/>')


def render(out):
    for name, t in THEMES.items():
        for key, label, _, slug in PERSON["links"]:
            write(out, f"profile-{key}-{name}", bar(label, slug, t))
