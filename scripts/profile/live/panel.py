"""05 — CONSISTENCY 패널: 머리 수치 + 도시 + 잔디를 한 장의 SVG로 묶는다."""
from ..content import CONTRIB, SECTIONS
from ..style import SVG_MONO, SVG_SANS, THEMES, axis
from .calendar import Calendar
from .city import CW, DX, city, palette
from .grass import HEIGHT as GRASS_H, grass

BASE = 300
X0 = axis(1000)  # 다른 SVG 섹션(폭 1000)과 같은 축


def _sky(w, h, t):
    """야경은 자체 밤하늘을 가져 어느 페이지 테마에서도 한 장의 작품으로 보인다."""
    out = [f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["sky"][0]}"/>'
           f'<stop offset="1" stop-color="{t["sky"][1]}"/></linearGradient></defs>',
           f'<rect width="{w}" height="{h}" fill="url(#sky)"/>']
    for k in range(40):
        out.append(f'<circle cx="{(k * 97) % (w - 40) + 20}" cy="{(k * 53) % 120 + 14}" r="{.5 + (k % 3) * .3}" '
                   f'fill="#ffffff" fill-opacity="{.15 + (k % 4) * .08}"/>')
    return out


def _header(cal, w, t):
    n, title, _ = SECTIONS["contrib"]
    total = f"{cal.total:,}"
    out = [f'<text x="{X0}" y="36" font-family="{SVG_MONO}" font-size="11" letter-spacing="1.2" fill="{t["sub"]}">{n} — {title}</text>',
           f'<text x="{X0 - 3}" y="100" font-family="{SVG_SANS}" font-size="56" font-weight="300" fill="{t["fg"]}">{total}</text>',
           f'<text x="{X0 + 34 * len(total)}" y="100" font-family="{SVG_SANS}" font-size="15" fill="{t["sub"]}">{CONTRIB["unit"]}</text>']
    for i, (label, val) in enumerate(zip(CONTRIB["stats"], (cal.active_days, f"{cal.longest_streak}d"))):
        x = w - X0 - 160 * (1 - i) - 140
        out += [f'<text x="{x}" y="66" font-family="{SVG_MONO}" font-size="10.5" letter-spacing="1.2" fill="{t["sub"]}">{label}</text>',
                f'<text x="{x}" y="100" font-family="{SVG_SANS}" font-size="30" font-weight="300" fill="{t["fg"]}">{val}</text>']
    note = CONTRIB["note"]["dark" if t["win"] else "light"]
    out.append(f'<text x="{w - X0}" y="130" text-anchor="end" font-family="{SVG_MONO}" font-size="10" fill="{t["mute"]}">{note}</text>')
    return out


def panel(cal: Calendar, name):
    t = palette(name)
    w = X0 * 2 + len(cal.weeks) * CW + 7 * DX
    h = BASE + 40 + GRASS_H
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    if t.get("sky"):
        out += _sky(w, h, t)
    else:  # 밤하늘이 없는 테마는 다른 섹션과 같은 헤어라인으로 시작한다
        out.append(f'<line x1="0" y1="6" x2="{w}" y2="6" stroke="{THEMES[name]["rule"]}"/>')
    out += _header(cal, w, t)
    out += city(cal, X0, BASE, t)
    out += [f'<text x="{X0 + i * CW}" y="{BASE + 24}" font-family="{SVG_MONO}" font-size="10" fill="{t["mute"]}">{m:02d}</text>'
            for i, m in cal.month_starts()]
    out += grass(cal, X0, w, BASE + 40, t)
    out.append("</svg>")
    return "".join(out)


def render(out, cal):
    for name in THEMES:
        with open(f"{out}/contrib-{name}.svg", "w", encoding="utf-8") as f:
            f.write(panel(cal, name))
