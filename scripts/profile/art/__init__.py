"""정적 그림 렌더러 레지스트리. 새 그림은 render(out)를 가진 모듈을 만들고 여기 한 줄 추가한다."""
from . import cards, hero, journey, links, profile_links, sections, stack, timeline

RENDERERS = (hero, profile_links, journey, timeline, stack, sections, cards, links)
