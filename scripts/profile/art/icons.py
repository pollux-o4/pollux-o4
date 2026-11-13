"""링크 바 아이콘 레지스트리. 브랜드 로고 대신 같은 선 두께의 단색 기호로 통일한다.
새 플랫폼은 함수를 하나 만들고 @icon으로 등록하면 content.Link.icon에서 이름으로 쓴다."""
# shortcut: 링크 바는 Pillow 래스터라 marks(SVG)와 별도 아이콘 세트를 둔다, 링크 바를 SVG로 옮길 때 marks로 합친다
ICONS = {}
W = 4  # 선 두께


def icon(fn):
    ICONS[fn.__name__] = fn
    return fn


@icon
def globe(d, x, y, r, c):
    d.ellipse((x - r, y - r, x + r, y + r), outline=c["icon"], width=W)
    d.ellipse((x - r * .45, y - r, x + r * .45, y + r), outline=c["icon"], width=W)
    d.line((x - r, y, x + r, y), fill=c["icon"], width=W)


@icon
def play(d, x, y, r, c):
    d.polygon([(x - r * .7, y - r), (x - r * .7, y + r), (x + r, y)], outline=c["icon"], width=W)


@icon
def box(d, x, y, r, c):
    d.polygon([(x, y - r), (x + r, y - r * .5), (x, y), (x - r, y - r * .5)], outline=c["icon"], width=W)
    d.line((x - r, y - r * .5, x - r, y + r * .5, x, y + r, x + r, y + r * .5, x + r, y - r * .5),
           fill=c["icon"], width=W, joint="curve")
    d.line((x, y, x, y + r), fill=c["icon"], width=W)


@icon
def code(d, x, y, r, c):
    for s in (-1, 1):
        d.line((x + s * r * .35, y - r * .8, x + s * r, y, x + s * r * .35, y + r * .8), fill=c["icon"], width=W, joint="curve")
    d.line((x + r * .15, y - r, x - r * .15, y + r), fill=c["acc"], width=W)


@icon
def window(d, x, y, r, c):
    d.rectangle((x - r, y - r * .8, x + r, y + r * .8), outline=c["icon"], width=W)
    d.line((x - r, y - r * .3, x + r, y - r * .3), fill=c["icon"], width=W)
    for i in range(3):
        cx, cy = x - r + 10 + i * 12, y - r * .55
        d.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=c["acc"] if i == 0 else c["icon"])


@icon
def branch(d, x, y, r, c):
    a, b, m, k = (x - r * .5, y - r * .8), (x - r * .5, y + r * .8), (x + r * .6, y - r * .3), 7
    d.line((a, b), fill=c["icon"], width=W)
    d.line((m[0], m[1] + k, m[0], y + r * .1, a[0], y + r * .6), fill=c["icon"], width=W, joint="curve")
    for p in (a, b, m):
        d.ellipse((p[0] - k, p[1] - k, p[0] + k, p[1] + k), fill=c["bg"], outline=c["acc"] if p == m else c["icon"], width=W)


@icon
def video(d, x, y, r, c):
    d.rectangle((x - r, y - r * .7, x + r, y + r * .7), outline=c["icon"], width=W)
    d.polygon([(x - r * .3, y - r * .35), (x - r * .3, y + r * .35), (x + r * .4, y)], fill=c["acc"])
