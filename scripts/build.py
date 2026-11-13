"""프로필 산출물 빌드.

  python3 scripts/build.py live     # 기여 패널(GITHUB_TOKEN 필요) — 워크플로가 매일 실행
  python3 scripts/build.py art      # 정적 그림(히어로·카드·링크 바·섹션·연도표) — Pillow 필요
  python3 scripts/build.py readme   # README.md
  python3 scripts/build.py all
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
sys.path.insert(0, str(Path(__file__).parent))


def live():
    from profile.live import calendar, panel
    panel.render(ASSETS, calendar.fetch())


def art():
    from profile.art import RENDERERS
    for mod in RENDERERS:
        mod.render(ASSETS)


def readme():
    from profile.readme import build
    (ROOT / "README.md").write_text(build(), encoding="utf-8")


TARGETS = {"live": live, "art": art, "readme": readme}

if __name__ == "__main__":
    names = sys.argv[1:] or ["all"]
    for name in (list(TARGETS) if names == ["all"] else names):
        TARGETS[name]()
