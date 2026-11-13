"""아이콘 표식 레지스트리(Strategy). 이름 하나로 그리되, 그리는 방식은 두 가지다.
- LineGlyph: 24칸 격자 위 단색 선 기호(직접 그림). 무엇을 만들었는지를 형태로 알린다.
- BrandLogo: Simple Icons 공식 로고(CC0, logos.json). 바탕과 대비가 모자라면 본문색.
새 표식은 GLYPHS 또는 logos.json에 항목만 추가하면 모든 그림에서 쓸 수 있다."""
import json
from pathlib import Path

from ..style import rgb

# 24×24 격자 위 선 기호. 무엇을 만들었는지(탐지 박스, 시계열, 링…)를 형태로 바로 알린다.
GLYPHS = {
    "briefcase": '<rect x="2.5" y="7" width="19" height="13" rx="1"/><path d="M8.5 7V4.5h7V7M2.5 12.5h19M11 12.5v2h2v-2"/>',
    "detect": '<rect x="3" y="5" width="12" height="11"/><rect x="11" y="10" width="10" height="9"/><path d="M3 2h5M11 7h4"/>',
    "classify": '<rect x="3" y="3" width="8" height="8"/><rect x="13" y="3" width="8" height="8"/><rect x="3" y="13" width="8" height="8"/><path d="M14 17l2 2 4-4"/>',
    "series": '<path d="M2 20h20M2 16l5-5 4 3 5-8 6 4"/>',
    "bars": '<path d="M2 21h20M5 21v-6M10 21V9M15 21v-9M20 21V4"/>',
    "meal": '<circle cx="12" cy="13" r="8"/><circle cx="12" cy="13" r="4"/><path d="M12 2v3"/>',
    "server": '<rect x="3" y="3" width="18" height="7"/><rect x="3" y="14" width="18" height="7"/><path d="M7 6.5h2M7 17.5h2"/>',
    "ring": '<circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 1 8.5 12"/><circle cx="12" cy="12" r="4"/>',
    "nodes": '<rect x="2" y="3" width="8" height="6"/><rect x="14" y="15" width="8" height="6"/><rect x="14" y="3" width="8" height="6"/><path d="M10 6h4M18 9v6"/>',
    "book": '<path d="M12 6c-3-2-6-2-9-1v15c3-1 6-1 9 1 3-2 6-2 9-1V5c-3-1-6-1-9 1zM12 6v15"/>',
    "grid": '<rect x="2" y="3" width="20" height="18"/><path d="M2 8h20M9 8v13"/>',
}


def _lum(hex_):
    r, g, b = (c / 255 for c in rgb(hex_))
    return .2126 * r + .7152 * g + .0722 * b


class LineGlyph:
    def __init__(self, body):
        self.body = body

    def render(self, x, y, t, size, ink=None, stroke=2):
        return (f'<g transform="translate({x},{y}) scale({size / 24})" fill="none" stroke="{ink or t["ink"]}" '
                f'stroke-width="{stroke}" stroke-linejoin="round" stroke-linecap="round">{self.body}</g>')


class BrandLogo:
    def __init__(self, path, hex_):
        self.path, self.color = path, "#" + hex_

    def render(self, x, y, t, size, ink=None, stroke=None):
        fill = self.color if abs(_lum(self.color) - _lum(t["bg"])) > .25 else t["ink"]
        return f'<path transform="translate({x},{y}) scale({size / 24})" d="{self.path}" fill="{fill}"/>'


_LOGOS = json.loads(Path(__file__).with_name("logos.json").read_text())
MARKS = {**{k: LineGlyph(v) for k, v in GLYPHS.items()},
         **{k: BrandLogo(v["path"], v["hex"]) for k, v in _LOGOS.items()}}


def mark(key, x, y, t, size=18, ink=None, stroke=2):
    return MARKS[key].render(x, y, t, size, ink, stroke)
