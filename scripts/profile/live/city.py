"""05 — 도시: 하루가 건물 한 채, 기여 수가 높이. 라이트는 흰 건축 모형, 다크는 상위 날만 불이 켜진 야경."""
from ..style import THEMES

CW, DX, DY = 15, 10, 8  # 주 칸 폭 · 깊이(요일) 방향 오프셋

# 재질은 도시 전용, 글자색·강조색은 style.THEMES가 원본
MATERIALS = {
    "light": dict(top="#ffffff", front="#ecebe7", side="#d9d8d3", edge="#c9c8c3", ground="#f1f0ec", glass="#c3c7cc",
                  glass_side="#b3b6ba", glass_acc="#ffd9c7", shade=".07", acc_front="#ff7a45", acc_side="#e0521f", win=None),
    "dark": dict(top="#4a515c", front="#2c3139", side="#1c2026", edge="#11141a", ground="#151920", glass="#1a1d22",
                 glass_side="#14171b", glass_acc="#ffd9c7", shade=".35", acc_side="#b8461f", win="#ffc46b",
                 sky=("#0b0f17", "#18202d")),
}


def palette(name):
    s = THEMES[name]
    return dict(fg=s["ink"], sub=s["sub"], mute="#a3a3a3" if name == "light" else "#5c5c5c", acc=s["acc"]) | MATERIALS[name]


def box(x, y, w, d, dx, dy, h, faces, edge):
    """오블리크 투영 직육면체: 앞면·옆면·윗면."""
    top = f"{x},{y - h} {x + w},{y - h} {x + w + dx},{y - h - dy} {x + dx},{y - h - dy}"
    side = f"{x + w},{y} {x + w + dx},{y - dy} {x + w + dx},{y - h - dy} {x + w},{y - h}"
    return (f'<polygon points="{side}" fill="{faces[2]}"/>'
            f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="{faces[1]}"/>'
            f'<polygon points="{top}" fill="{faces[0]}" stroke="{edge}" stroke-width=".5"/>')


def building(x, y, w, dx, dy, h, rank, t):
    """창문·옥상·그림자가 있는 건물 한 채. rank: lit(상위 5%) · warm(상위 30%) · ''."""
    lit = rank == "lit"
    day = t["win"] is None
    faces = (t["acc"], t["acc_front"], t["acc_side"]) if lit and day else (t["top"], t["front"], t["side"])
    out = [f'<polygon points="{x + w},{y} {x + w + h * .55},{y} {x + w + h * .55 + dx},{y - dy} {x + w + dx},{y - dy}" '
           f'fill="#000" fill-opacity="{t["shade"]}"/>']  # 오른쪽으로 떨어지는 그림자
    body = h
    tower = h > 55
    if tower:  # 높은 건물은 위층이 좁아진다
        body = round(h * .72, 1)
    out.append(box(x, y, w, 0, dx, dy, body, faces, t["edge"]))
    out += windows(x, y, w, dx, dy, body, rank, t, day)
    if tower:
        tx, tw, th = x + 2, w - 4, h - body
        out.append(box(tx, y - body, tw, 0, dx * .8, dy * .8, th, faces, t["edge"]))
        out += windows(tx, y - body, tw, dx * .8, dy * .8, th, rank, t, day)
        ax = tx + tw / 2 + dx * .4
        out.append(f'<line x1="{ax}" y1="{y - h - dy * .4}" x2="{ax}" y2="{y - h - dy * .4 - 9}" stroke="{t["edge"] if day else t["top"]}" stroke-width="1"/>')
        if not day:
            out.append(f'<circle cx="{ax}" cy="{y - h - dy * .4 - 9}" r="1.2" fill="{t["acc"]}"/>')
    # 옥상 난간
    out.append(f'<line x1="{x}" y1="{y - body + 1}" x2="{x + w}" y2="{y - body + 1}" stroke="{t["edge"]}" stroke-width=".8"/>')
    return "".join(out)


def windows(x, y, w, dx, dy, h, rank, t, day):
    """앞면 2열·옆면 1열 창문. 밤에는 기여가 많은 날만 불이 켜진다."""
    out = []
    rows = int((h - 5) // 6)
    for k in range(rows):
        wy = y - h + 4 + k * 6
        for col in (0, 1):
            wx = x + 2 + col * (w / 2 - .5)
            if day:
                fill, op = (t["glass_acc"], .9) if rank == "lit" else (t["glass"], .9)
            elif rank == "lit":
                fill, op = t["win"], (1 if (k + col) % 3 else .45)
            elif rank == "warm":
                fill, op = t["win"], (.55 if (k * 7 + col * 3) % 5 == 0 else 0)
            else:
                fill, op = t["glass"], 1
            if op:
                out.append(f'<rect x="{wx:.1f}" y="{wy:.1f}" width="{w / 2 - 3:.1f}" height="2.6" fill="{fill}" fill-opacity="{op}"/>')
        sy = wy - dy * .5
        sx = x + w + dx * .25
        side_fill = t["glass_side"] if day else (t["win"] if rank == "lit" and k % 2 else t["glass_side"])
        side_op = .35 if (not day and rank == "lit" and k % 2) else (.9 if day else 1)
        out.append(f'<polygon points="{sx:.1f},{wy + 1:.1f} {sx + dx * .5:.1f},{wy + 1 - dy * .5:.1f} {sx + dx * .5:.1f},{wy + 3.6 - dy * .5:.1f} {sx:.1f},{wy + 3.6:.1f}" fill="{side_fill}" fill-opacity="{side_op}"/>')
    return out


def city(cal, x0, base, t):
    """뒤 줄(토요일)부터 앞 줄(일요일)로 그려 가림 순서를 맞춘다."""
    n = len(cal.weeks)
    hi, warm, peak = cal.quantile(.95), cal.quantile(.7), max(cal.days) or 1
    out = [f'<polygon points="{x0},{base + 3} {x0 + n * CW},{base + 3} {x0 + n * CW + 7 * DX},{base + 3 - 7 * DY} '
           f'{x0 + 7 * DX},{base + 3 - 7 * DY}" fill="{t["ground"]}"/>']
    for j in range(6, -1, -1):
        for i, wk in enumerate(cal.weeks):
            if j >= len(wk):
                continue
            c, x, y = wk[j], x0 + i * CW + j * DX, base - j * DY
            if not c:
                out.append(f'<polygon points="{x + 2},{y} {x + CW - 2},{y} {x + CW - 2 + DX},{y - DY} {x + 2 + DX},{y - DY}" '
                           f'fill="{t["front"]}" opacity=".7"/>')
                continue
            rank = "lit" if c >= hi else ("warm" if c >= warm else "")
            out.append(building(x + 1.5, y, CW - 3, DX, DY, round(4 + 100 * (c / peak) ** .55, 1), rank, t))
    return out
