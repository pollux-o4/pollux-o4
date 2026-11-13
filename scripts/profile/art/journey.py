"""01 — WHAT I DO. 주장 세 칸이 왼쪽에서 오른쪽으로 이어져 한 문장이 된다:
모델을 학습시키고 → 서비스로 붙여 배포하고 → 개인 프로젝트로 운영까지.
칸마다 그 말의 실물인 대표 항목 아이콘 줄.
아이콘은 모두 24칸 격자·같은 선 두께라 셋이 한 벌로 읽힌다."""
from ..content import CLAIMS, CLAIMS_TITLE, SECTIONS
from ..style import SVG_MONO, SVG_SANS, THEMES, axis
from .marks import mark
from .svg import svg, text, write

W, TOP = 1000, 112
X0 = axis(W)


def item(x, y, key, name, note, t, accent):
    return mark(key, x, y, t, 24, ink=t["acc"] if accent else None, stroke=1.6) + text(x, y + 44, name, t["ink"], 12, weight=600) + text(x, y + 60, note, t["sub"], 10.5, SVG_MONO)


def claims(t):
    n, title, _ = SECTIONS["stack"]
    cw = (W - X0 * 2) / len(CLAIMS)
    out = [f'<line x1="0" y1="6" x2="{W}" y2="6" stroke="{t["rule"]}"/>',
           text(X0, 36, f"{n} — {title}", t["sub"], 11, SVG_MONO, 500, spacing=1.2),
           text(X0, 70, CLAIMS_TITLE, t["ink"], 20, weight=600, spacing=-.4)]
    for i, (claim, items) in enumerate(CLAIMS):
        x, last = X0 + i * cw, i == len(CLAIMS) - 1
        out.append(f'<line x1="{x}" y1="{TOP}" x2="{x + cw - 28}" y2="{TOP}" stroke="{t["acc"] if last else t["ink"]}" stroke-width="2"/>')
        if not last:  # 다음 칸으로 이어지는 화살
            out.append(f'<path d="M{x + cw - 34},{TOP - 5} L{x + cw - 28},{TOP} L{x + cw - 34},{TOP + 5}" fill="none" stroke="{t["ink"]}" stroke-width="2"/>')
        out.append(text(x, TOP + 30, claim, t["ink"], 15, weight=600))
        step = (cw - 28) / 4  # 네 칸 격자 — 항목이 셋이어도 같은 간격
        for j, (key, name, note) in enumerate(items):
            out.append(item(x + j * step, TOP + 52, key, name, note, t, last))
    return svg(W, TOP + 126, "".join(out))


def render(out):
    for name, t in THEMES.items():
        write(out, f"journey-{name}", claims(t))
