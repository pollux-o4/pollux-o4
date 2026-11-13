"""히어로: 이름·역할 + 탐지 박스가 걸린 하프톤 구체(‘믿을 수 있는 결과’의 시각화)."""
import math

from PIL import Image, ImageDraw

from ..content import PERSON
from ..style import THEMES, axis, font, raster
from .draw import save, sphere_level

W, H = 2400, 1000
X0 = axis(W)


def hero(name):
    t, dark = raster(THEMES[name]), name == "dark"
    im = Image.new("RGB", (W, H), t["bg"])
    d = ImageDraw.Draw(im)
    cx, cy, rad, step = 1720, 520, 330, 22
    for y in range(0, H + step, step):
        for x in range(0, W + step, step):
            dx, dy = (x - cx) / rad, (y - cy) / rad
            r = math.sqrt(dx * dx + dy * dy)
            v = sphere_level(dx, dy, dark) if r < 1 else max(0, .22 - .09 * (r - 1))
            v *= min(1.0, max(0.0, (x - 1000) / 800)) ** 1.5  # 글자 쪽으로 사라진다
            s = v * step * .48
            if s > .6:
                d.ellipse((x - s, y - s, x + s, y + s), fill=t["ink"])
    bx, by = cx - rad - 40, cy - rad - 40
    d.rectangle((bx, by, cx + rad + 40, cy + rad + 40), outline=t["acc"], width=4)
    tag = PERSON["tag"]
    d.rectangle((bx - 2, by - 52, bx + d.textlength(tag, font=font("mono", 30)) + 28, by), fill=t["acc"])
    d.text((bx + 14, by - 46), tag, font=font("mono", 30), fill=t["tag"])
    d.text((X0, 110), PERSON["latin"], font=font("mono", 26), fill=t["sub"])
    d.text((X0 - 10, 200), PERSON["name"], font=font("bold", 190), fill=t["ink"])
    # 묶음 간격 > 줄 간격: 이름 → 역할(한 묶음이되 숨 쉴 간격) / 소개(첫 줄 뒤 연 바꿈, 시처럼) / 가치(한 줄 더 띄움)
    d.text((X0, 490), PERSON["role"], font=font("medium", 58), fill=t["ink"])
    for i, line in enumerate(PERSON["lines"]):
        d.text((X0, 615 + i * 80 + (40 if i else 0)), line, font=font("light", 48), fill=t["sub"])
    d.text((X0, 935), PERSON["motto"], font=font("medium", 34), fill=t["acc"])
    return im


def render(out):
    for name in THEMES:
        save(hero(name), out, f"hero-{name}")
