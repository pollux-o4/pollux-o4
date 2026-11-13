"""색·서체 토큰(SSoT). 무채색 + 강조색 하나, 라이트/다크 두 벌."""
import os
from functools import lru_cache

# tag: 강조색 면 위에 얹는 글자색
THEMES = {
    "light": dict(tag="#ffffff", bg="#ffffff", ink="#111111", sub="#6e6e6e", mute="#bebebe", rule="#dcdcd8", tile="#f2f2f0", acc="#ff5a1f"),
    "dark": dict(tag="#ffffff", bg="#0d1117", ink="#ecece8", sub="#96969a", mute="#4a4e55", rule="#30363d", tile="#1c2026", acc="#ff6b35"),
}
# 카드·링크 바는 테마와 무관하게 어두운 면(사진·스크린샷이 가장 잘 보이는 바탕)
CARD = dict(bg="#16171b", ink="#f0f0ec", sub="#969698", rule="#34363c", icon="#ecece8", plat="#82868c", acc="#ff5e28")

AXIS = .05  # 모든 섹션이 공유하는 좌측 축(폭의 5%)


def axis(width):
    return round(width * AXIS)


SVG_SANS = "-apple-system,'Pretendard','Apple SD Gothic Neo','Noto Sans KR',Arial,sans-serif"
SVG_MONO = "ui-monospace,'SF Mono',Menlo,Consolas,monospace"

_NOTO = "/usr/share/fonts/opentype/noto/NotoSansCJK-{}.ttc"
_FONTS = {
    "bold": _NOTO.format("Bold"), "medium": _NOTO.format("Medium"), "light": _NOTO.format("Light"),
    "mono": "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf",
    "serif": next((p for p in ("/usr/share/fonts/opentype/urw-base35/NimbusRoman-Italic.otf",
                               "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
                               "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf") if os.path.exists(p)), None),
}


def rgb(hex_):
    h = hex_.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def raster(theme):
    """Pillow용 RGB 튜플 팔레트."""
    return {k: rgb(v) for k, v in theme.items()}


@lru_cache(maxsize=None)
def font(kind, size):
    from PIL import ImageFont
    path = _FONTS[kind]
    # CJK ttc의 index 1이 KR 글리프
    return ImageFont.truetype(path, size, index=1) if path.endswith(".ttc") else ImageFont.truetype(path, size)
