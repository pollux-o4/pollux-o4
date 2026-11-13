"""카드 아래 링크 바: 아이콘 · 무엇을 하는지(한국어) · 어디로 가는지(플랫폼) · ↗."""
from PIL import Image, ImageDraw

from ..content import AI_PROJECTS, SHIPPED
from ..style import CARD, font, raster
from .draw import arrow, save
from .icons import ICONS

H = 126
HALF, FULL = 600, 1200  # 카드 폭 1200의 절반 / 전체


def link_bar(link, width, divider):
    c = raster(CARD)
    im = Image.new("RGB", (width, H), c["bg"])
    d = ImageDraw.Draw(im)
    ICONS[link.icon](d, 80, 63, 22, c)
    d.text((128, 49), link.action, font=font("bold", 31), fill=c["icon"], anchor="lm")
    d.text((128, 88), link.platform, font=font("mono", 23), fill=c["plat"], anchor="lm")
    arrow(d, width - 60, 54, 20, c["acc"], 4)
    if divider:
        d.line((width - 1, 26, width - 1, H - 26), fill=c["rule"], width=2)
    return im


def render(out):
    for p in AI_PROJECTS + SHIPPED:
        width = FULL if len(p.links) == 1 else HALF
        for i, link in enumerate(p.links):
            save(link_bar(link, width, divider=i < len(p.links) - 1), out, f"link-{link.key}")
