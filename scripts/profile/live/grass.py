"""요일 × 주 잔디. 도시와 같은 주 칸(CW)에 맞춰 언제 커밋했는지 평면으로 보여준다."""
from ..content import CONTRIB
from ..style import SVG_MONO, SVG_SANS
from .city import CW

HEIGHT = 186
CELL = 11
DAYS = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")  # GitHub 주 배열은 일요일부터
ROWS = (1, 2, 3, 4, 5, 6, 0)  # 월요일부터 보여 준다
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
LEVELS = (.07, .2, .35, .55)  # 무채색 단계, 맨 위 단계(상위 5%)는 강조색


def _label(x, y, s, t, family=SVG_MONO, anchor="start"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{family}" font-size="10" fill="{t["mute"]}">{s}</text>'


def _cell(x, y, fill, op=1):
    return f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="1.5" fill="{fill}" fill-opacity="{op}"/>'


def grass(cal, x0, w, top, t):
    acc = t["win"] or t["acc"]
    cuts = [cal.quantile(r) for r in (.25, .5, .75, .95)]
    gy = top + 38
    out = [f'<line x1="{x0}" y1="{top}" x2="{w - x0}" y2="{top}" stroke="{t["mute"]}" stroke-opacity=".35"/>']
    out += [_label(x0 + i * CW + 2, gy - 8, MONTHS[m - 1], t) for i, m in cal.month_starts()]
    for r, j in enumerate(ROWS):
        y = gy + r * 15
        if r % 2 == 0:
            out.append(_label(x0 - 8, y + 9.5, DAYS[j], t, SVG_SANS, "end"))
        for i, wk in enumerate(cal.weeks):
            if j < len(wk):
                lv = sum(wk[j] >= v for v in cuts) if wk[j] else 0
                out.append(_cell(x0 + i * CW + 2, y, acc) if lv == len(LEVELS) else _cell(x0 + i * CW + 2, y, t["fg"], LEVELS[lv]))
    ly = gy + 7 * 15 + 12
    out.append(_label(w - x0 - 128, ly + 9, CONTRIB["less"], t, anchor="end"))
    out += [_cell(w - x0 - 120 + k * 15, ly, t["fg"], op) for k, op in enumerate(LEVELS)]
    out += [_cell(w - x0 - 60, ly, acc), _label(w - x0 - 44, ly + 9, CONTRIB["more"], t)]
    return out
