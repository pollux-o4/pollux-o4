"""프로젝트 카드: 위는 그림(MEDIA 레지스트리), 아래는 제목·메타·결과 한 줄."""
from PIL import Image, ImageDraw

from ..content import AGRI_CHART, AI_PROJECTS, SHIPPED
from ..style import CARD, font, raster
from .draw import rounded, save, source

W, H, MEDIA_H = 1200, 860, 650  # 그림 영역은 구분선(660) 위까지
C = raster(CARD)
MEDIA = {}  # project.key → (draw) 함수. 그림이 없는 프로젝트는 카드를 만들 수 없다.


def media(key):
    def reg(fn):
        MEDIA[key] = fn
        return fn
    return reg


def shot(key, radius):
    return lambda: rounded(source(key), radius, C["bg"])


@media("silmari")
def _silmari():
    phones = [rounded(source(f"silmari-{k}"), 36, C["bg"]) for k in ("circle", "timeline", "list")]
    out = Image.new("RGB", (sum(p.width for p in phones) + 80, phones[0].height), C["bg"])
    x = 0
    for p in phones:
        out.paste(p, (x, 0))
        x += p.width + 40
    return out


MEDIA["memoivy"] = shot("memoivy", 20)
MEDIA["md2ebook"] = shot("md2ebook", 16)
MEDIA["design-home"] = shot("design-home", 16)
MEDIA["nutrition"] = shot("nutrition", 10)


@media("agri")
def _agri():
    """누수로 부풀었던 0.98을 지우고 날짜순 검증 점수를 쌓아 올린 R² 막대."""
    axis, bars = AGRI_CHART
    im = Image.new("RGB", (W, MEDIA_H), C["bg"])
    d = ImageDraw.Draw(im)
    base, scale = 560, 330
    d.text((60, 50), axis, font=font("mono", 28), fill=C["sub"])
    d.line((60, base, W - 60, base), fill=(90, 92, 98), width=2)
    for i, (label, v, note) in enumerate(bars):
        x, h = 60 + i * 275, v * scale
        if i == 0:
            for yy in range(int(base - h), base, 14):
                d.line((x, yy, x + 190, yy), fill=(70, 72, 78), width=2)
            d.text((x, base - h - 90), f"{v:.2f}", font=font("light", 72), fill=(110, 110, 112))
            d.line((x, base - h - 48, x + 150, base - h - 48), fill=(140, 140, 142), width=4)
        else:
            best = i == len(bars) - 1
            d.rectangle((x, base - h, x + 190, base), fill=C["acc"] if best else ((96, 97, 102) if i == 1 else (150, 151, 156)))
            d.text((x, base - h - 90), f"{v:.2f}", font=font("medium" if best else "light", 72),
                   fill=C["acc"] if best else (150, 151, 156))
        d.text((x, base + 20), label, font=font("medium", 30), fill=C["ink"])
        if note:
            d.text((x, base + 60), note, font=font("medium", 26), fill=C["sub"])
    return im


def card(p):
    im = Image.new("RGB", (W, H), C["bg"])
    d = ImageDraw.Draw(im)
    m = MEDIA[p.key]()
    if m.width == W:  # 카드 폭으로 직접 그린 그림
        im.paste(m, (0, 0))
    else:  # 스크린샷은 여백 안에 맞춰 가운데
        mw, mh = W - 120, 560
        m.thumbnail((mw, mh), Image.LANCZOS)
        im.paste(m, ((W - m.width) // 2, 30 + (mh - m.height) // 2))
    d.line((60, 660, W - 60, 660), fill=C["rule"], width=2)
    d.text((60, 690), p.title, font=font("bold", 52), fill=C["ink"])
    d.text((60, 775), p.meta, font=font("mono", 28) if p.meta.isascii() else font("medium", 30), fill=C["sub"])
    if p.stat:
        d.text((W - 60, 700), p.stat, font=font("mono", 34), fill=C["acc"], anchor="ra")
    return im


def render(out):
    for p in AI_PROJECTS + SHIPPED:
        save(card(p), out, f"card-{p.key}")
