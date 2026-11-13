"""python3 -m unittest discover scripts/tests — 네트워크·Pillow 없이 도는 계약 검사."""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from profile.content import AI_PROJECTS, SHIPPED, TIMELINE  # noqa: E402
from profile.live.calendar import Calendar  # noqa: E402
from profile.readme import build  # noqa: E402


class CalendarTest(unittest.TestCase):
    cal = Calendar(total=9, weeks=((0, 1, 2, 0, 0, 0, 0), (3, 3, 0, 0, 0, 0, 0), (0,)), months=(11, 12, 12))

    def test_streak_and_active(self):
        self.assertEqual(self.cal.active_days, 4)
        self.assertEqual(self.cal.longest_streak, 2)

    def test_quantile_ignores_empty_days(self):
        self.assertEqual(self.cal.quantile(0), 1)
        self.assertEqual(self.cal.quantile(.99), 3)

    def test_month_starts_skip_tail(self):
        self.assertEqual(list(self.cal.month_starts()), [(0, 11)])


class ContentContract(unittest.TestCase):
    def test_links_are_unique_and_iconed(self):
        from profile.art.icons import ICONS
        keys = [l.key for p in AI_PROJECTS + SHIPPED for l in p.links]
        self.assertEqual(len(keys), len(set(keys)))
        for p in AI_PROJECTS + SHIPPED:
            for l in p.links:
                self.assertIn(l.icon, ICONS)
                self.assertNotRegex(l.platform, "[가-힣]")  # 고정폭 서체에 한글 글리프가 없다

    def test_every_mark_key_is_registered(self):
        """01 아이콘·기술 칸·프로필 링크가 쓰는 표식 이름은 모두 marks 레지스트리에 있어야 한다."""
        from profile.content import CLAIMS, PERSON, STACK
        from profile.art.marks import MARKS
        keys = [k for _, items in CLAIMS for k, *_ in items] + [s for _, items in STACK for _, s in items] \
            + [l[3] for l in PERSON["links"]]
        self.assertEqual([k for k in keys if k not in MARKS], [])
        self.assertTrue(all(len(items) <= 4 for _, items in CLAIMS))

    def test_grids_are_pairs(self):
        self.assertEqual(len(AI_PROJECTS) % 2, 0)
        self.assertEqual(len(SHIPPED) % 2, 0)

    def test_timeline_sources_exist(self):
        src = ROOT / "scripts" / "sources"
        for year in TIMELINE.values():
            for group in ("projects", "spans", "shipped"):
                for item in year.get(group, ()):
                    self.assertTrue((src / f"{item[-2]}.jpg").exists(), item)

    def test_readme_references_existing_assets(self):
        for path in set(re.findall(r'(?:src|srcset)="\./(assets/[^"]+)"', build())):
            self.assertTrue((ROOT / path).exists(), path)


if __name__ == "__main__":
    unittest.main()
