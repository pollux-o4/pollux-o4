"""README.md를 content에서 생성한다. GitHub README는 CSS가 없어 간격은 블록 단위로 조절한다:
섹션 사이 <p><br></p>, 섹션 안 카드 행 사이 빈 줄(문단), 카드와 링크 바 사이 <br>."""

from .content import (AI_PROJECTS, CLAIMS, CLAIMS_TITLE, CONTACT_ALT, CONTRIB, PERSON, SECTIONS, SHIPPED,
                      STACK_ALT, TIMELINE_ALT)

from .art.profile_links import H as HEIGHT, width

GAP = "\n\n<p><br></p>\n\n"
CARD_W, HALF_W = "49.2%", "24.6%"  # 두 장 + &nbsp;(≈4.5px). 남는 1.6%가 본문 폭 300px까지 &nbsp;보다 커서 모바일에서도 한 행


def themed(name, alt, ext="png", href=None, size='width="100%"'):
    """라이트/다크 한 쌍 그림. GitHub는 CSS가 없어 테마 전환은 <picture>로만 된다."""
    pic = (f'<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/{name}-dark.{ext}">'
           f'<img src="./assets/{name}-light.{ext}" alt="{alt}" {size}></picture>')
    return f'<a href="{href}">{pic}</a>' if href else pic


def img(href, name, alt, width):
    return f'<a href="{href}"><img src="./assets/{name}.png" alt="{alt}" width="{width}"></a>'


def link_bars(p):
    width = HALF_W if len(p.links) > 1 else CARD_W
    return "".join(img(l.url, f"link-{l.key}", f"{p.title} {l.action} ({l.platform})", width) for l in p.links)


def grid(projects):
    """두 장씩 한 행: 카드 행<br>링크 바 행. 행 사이는 문단으로 띄운다."""
    rows = []
    for a, b in zip(projects[::2], projects[1::2]):
        cards = "&nbsp;".join(img(p.url, f"card-{p.key}", p.alt, CARD_W) for p in (a, b))
        rows.append(f"{cards}<br>{link_bars(a)}&nbsp;{link_bars(b)}")
    return "\n\n".join(rows)


def section(key, body):
    n, title, _ = SECTIONS[key]
    return themed(f"head-{n}", f"{n} — {title}", "svg") + "\n\n" + body


def stack_block():
    """주장 세 개와 각 주장의 실물 아이콘."""
    alt = "01 — " + CLAIMS_TITLE + ": " + " → ".join(
        f"{c[0]}(" + ", ".join(i[1] for i in c[1]) + ")" for c in CLAIMS)
    return themed("journey", alt, "svg")


def build():
    links = "&emsp;&emsp;".join(  # 링크 사이 > 아이콘·글자·화살표 사이: 두 링크가 따로 읽힌다
        themed(f"profile-{k}", f"{t} 열기", "svg", u, f'height="{HEIGHT}" width="{width(t)}"')
        for k, t, u, _ in PERSON["links"])
    blocks = [
        themed("hero", f'{PERSON["name"]} — {PERSON["role"]}. {" ".join(PERSON["lines"])}')
        + f'\n\n<p align="right">{links}</p>',
        stack_block(),
        themed("timeline", TIMELINE_ALT) + "\n\n" + themed("stack", STACK_ALT, "svg"),
        section("ai", grid(AI_PROJECTS)),
        section("shipped", grid(SHIPPED)),
        themed("contrib", CONTRIB["alt"], "svg"),
        themed("contact", CONTACT_ALT.format(email=PERSON["email"]), href=f'mailto:{PERSON["email"]}'),
    ]
    return GAP.join(blocks) + "\n"
