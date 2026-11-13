"""래스터 그림 공용 도구: 원본 이미지, 하프톤 구체, 화살표, 저장."""
import math
from pathlib import Path

from PIL import Image, ImageDraw

SOURCES = Path(__file__).resolve().parents[2] / "sources"


def source(key):
    return Image.open(SOURCES / f"{key}.jpg").convert("RGB")


def rounded(im, radius, bg):
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, *im.size), radius, fill=255)
    out = Image.new("RGB", im.size, bg)
    out.paste(im, (0, 0), mask)
    return out


def sphere_level(dx, dy, dark):
    """빛을 받는 구의 밝기(0~1). 다크는 밝은 점, 라이트는 어두운 점이 많아지도록 뒤집는다."""
    z = math.sqrt(max(0.0, 1 - dx * dx - dy * dy))
    lam = max(0.0, -dx * .5 - dy * .55 + z * .67)
    return .12 + .88 * lam ** 1.4 if dark else .15 + .85 * max(0.0, 1 - lam) ** 1.2


def halftone_sphere(d, cx, cy, r, step, dot, ink, dark):
    for y in range(cy - r, cy + r, step):
        for x in range(cx - r, cx + r, step):
            dx, dy = (x - cx) / r, (y - cy) / r
            if dx * dx + dy * dy > 1:
                continue
            s = 1 + dot * sphere_level(dx, dy, dark)
            d.ellipse((x - s, y - s, x + s, y + s), fill=ink)


def arrow(d, x, y, size, color, width):
    """↗ — 글꼴에 없는 기호라 선으로 그린다. (x, y)는 화살촉 끝."""
    d.line((x - size, y + size, x, y), fill=color, width=width)
    d.line((x - size * .7, y, x, y), fill=color, width=width)
    d.line((x, y, x, y + size * .7), fill=color, width=width)


def save(im, out, name):
    im.save(Path(out) / f"{name}.png", optimize=True)
