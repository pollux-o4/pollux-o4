"""02 — 연도표. 해마다 한 줄: 월 축 위에 썸네일, 아래에 교육 띠·자격증 점."""
from PIL import Image, ImageDraw, ImageOps

from ..content import SECTIONS, TIMELINE, TIMELINE_LEGEND
from ..style import THEMES, axis, font, raster
from .draw import save, source

W, GX, ROW_H = 2000, 330, 410
X0 = axis(W)
CW = (W - X0 - GX) / 12
TS = int(CW - 22)  # 썸네일 한 변


def thumb(key):
    im = source(key)
    if key.startswith("silmari"):
        im = im.crop((0, 0, im.width, im.width))
    return ImageOps.fit(im, (TS, TS), Image.LANCZOS, centering=(.5, .35))


class Row:
    """한 해의 줄. 위치 계산(월→x)을 한곳에 둔다."""

    def __init__(self, d, t, top, year, now):
        self.d, self.t, self.axis = d, t, top + 420
        d.text((X0 - 4, self.axis - 150), str(year), font=font("serif", 120), fill=t["acc"] if now else t["ink"])
        d.line((GX + X0, self.axis, W - X0, self.axis), fill=t["ink"], width=2)
        for m in range(TIMELINE[year]["start"], 13):
            x = self.x(m)
            d.line((x, self.axis, x, self.axis + 10), fill=t["ink"], width=2)
            d.text((x + 4, self.axis + 14), f"{m:02d}", font=font("mono", 20), fill=t["sub"])

    @staticmethod
    def x(month):
        return GX + X0 + (month - 1) * CW

    def cert(self, month, label, dy):
        """점은 해당 월에 고정, 오른쪽 여백이 모자라면 라벨을 점 왼쪽에 둔다."""
        d, fo = self.d, font("bold", 20)
        cx, cy = self.x(month) + 14, self.axis + dy
        d.ellipse((cx - 9, cy - 9, cx + 9, cy + 9), fill=self.t["acc"])
        if cx + 16 + d.textlength(label, font=fo) > W - X0 + 20:
            d.text((cx - 16, cy - 15), label, font=fo, fill=self.t["acc"], anchor="ra")
        else:
            d.text((cx + 16, cy - 15), label, font=fo, fill=self.t["acc"])

    def tile(self, im, month, key, label, stack=0, framed=False, bold=False):
        x, y = int(self.x(month) + 4), self.axis - 44 - TS - stack * (TS + 44)
        im.paste(thumb(key), (x, y))
        if framed:
            self.d.rectangle((x - 4, y - 4, x + TS + 3, y + TS + 3), outline=self.t["acc"], width=4)
        weight = "bold" if framed or bold else "medium"
        self.d.text((x, y + TS + 6), label, font=font(weight, 17 if len(label) > 9 else 19), fill=self.t["ink"])
        return x


def legend(d, t):
    x0 = W - X0 - 560
    for i, (kind, label) in enumerate(TIMELINE_LEGEND):
        x, y = x0 + i * 140, 52
        if kind == "project":
            d.rectangle((x, y - 9, x + 18, y + 9), fill=t["mute"])
        elif kind == "course":
            d.rectangle((x, y - 4, x + 26, y + 4), fill=t["sub"])
        elif kind == "cert":
            d.ellipse((x, y - 8, x + 16, y + 8), fill=t["acc"])
        else:
            d.rectangle((x, y - 9, x + 18, y + 9), outline=t["acc"], width=3)
        d.text((x + 32, y - 15), label, font=font("medium", 22), fill=t["sub"])


def timeline(name):
    t = raster(THEMES[name])
    im = Image.new("RGB", (W, 1320), t["bg"])
    d = ImageDraw.Draw(im)
    n, title, _ = SECTIONS["timeline"]
    d.line((0, 2, W, 2), fill=t["rule"], width=2)
    d.text((X0, 40), f"{n} — {title}", font=font("mono", 22), fill=t["sub"])
    legend(d, t)
    years = sorted(TIMELINE)
    for i, year in enumerate(years):
        data, row = TIMELINE[year], Row(d, t, 10 + i * ROW_H, year, now=year == years[-1])
        seen = {}
        for m, key, label in data.get("projects", ()):  # 같은 달은 위로 쌓는다
            row.tile(im, m, key, label, stack=seen.setdefault(m, 0))
            seen[m] += 1
        for a, b, key, label in data.get("spans", ()):
            x = row.tile(im, a, key, label, bold=True)
            d.rectangle((x, row.axis - 5, row.x(b) + CW - 14, row.axis + 5), fill=t["sub"])
        for m, key, label in data.get("shipped", ()):
            row.tile(im, m, key, label, framed=True)
        for a, b, label in data.get("courses", ()):
            y = row.axis + 56
            d.rectangle((row.x(a) + 4, y, min(row.x(b) + CW - 14, W - X0), y + 8), fill=t["sub"])
            d.text((row.x(a) + 4, y + 14), label, font=font("medium", 19), fill=t["sub"])
        for m, label in data.get("certs", ()):
            row.cert(m, label, 128 if data.get("courses") else 90)
    return im.crop((0, 0, W, row.axis + 130))


def render(out):
    for name in THEMES:
        save(timeline(name), out, f"timeline-{name}")
