"""섹션 라벨(03·04), 06 연락처. 라벨은 모두 같은 서체·좌측 5% 축·헤어라인."""
from PIL import Image, ImageDraw

from ..content import CONTACT_LINES, PERSON, SECTIONS
from ..style import SVG_MONO, THEMES, axis, font, raster
from .draw import arrow, halftone_sphere, save
from .svg import svg, text, write


def head(key, t):
    n, title, note = SECTIONS[key]
    w, x0 = 1200, axis(1200)
    return svg(w, 68, f'<line x1="0" y1="8" x2="{w}" y2="8" stroke="{t["rule"]}"/>'
                + text(x0, 45, f"{n} — {title}", t["sub"], 13.2, SVG_MONO, 500, spacing=1.44)
                + text(w - x0, 45, note, t["sub"], 14, anchor="end"))


def contact(name):
    t, dark = raster(THEMES[name]), name == "dark"
    W, H = 2400, 640
    x0 = axis(W)
    im = Image.new("RGB", (W, H), t["bg"])
    d = ImageDraw.Draw(im)
    n, title, _ = SECTIONS["contact"]
    d.line((0, 16, W, 16), fill=t["rule"], width=2)
    d.text((x0, 62), f"{n} — {title}", font=font("mono", 26), fill=t["sub"])
    for i, line in enumerate(CONTACT_LINES):
        d.text((x0, 170 + i * 120), line, font=font("bold", 92), fill=t["ink"] if i == 0 else t["sub"])
    fo = font("mono", 46)
    d.text((x0, 560), PERSON["email"], font=fo, fill=t["ink"], anchor="ls")
    w = d.textlength(PERSON["email"], font=fo)
    d.line((x0, 580, x0 + w, 580), fill=t["acc"], width=4)
    arrow(d, x0 + w + 66, 532, 26, t["acc"], 5)
    halftone_sphere(d, W - x0 - 230, 360, 200, 18, 4.2, t["ink"], dark)  # 히어로 구체를 되받아 처음과 끝을 묶는다
    return im


def render(out):
    for name, t in THEMES.items():
        for key in ("ai", "shipped"):
            write(out, f"head-{SECTIONS[key][0]}-{name}", head(key, t))
        save(contact(name), out, f"contact-{name}")
