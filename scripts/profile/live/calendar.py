"""GitHub 기여 달력: 가져오기와 파생 수치. 그리는 쪽은 Calendar만 안다."""
import json
import os
import urllib.request
from dataclasses import dataclass

QUERY = """query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{
totalContributions weeks{contributionDays{date contributionCount}}}}}}"""


@dataclass(frozen=True)
class Calendar:
    total: int
    weeks: tuple  # 주마다 일~토 기여 수(마지막 주는 짧을 수 있다)
    months: tuple  # 주마다 첫날의 월(1~12)

    @property
    def days(self):
        return [c for wk in self.weeks for c in wk]

    def quantile(self, r):
        """기여가 있었던 날 기준 분위값."""
        flat = sorted(c for c in self.days if c)
        return flat[min(len(flat) - 1, int(len(flat) * r))] if flat else 1

    @property
    def active_days(self):
        return sum(1 for c in self.days if c)

    @property
    def longest_streak(self):
        best = run = 0
        for c in self.days:
            run = run + 1 if c else 0
            best = max(best, run)
        return best

    def month_starts(self):
        """(주 인덱스, 월) — 월이 바뀌는 첫 주. 끝의 두 주는 라벨이 잘려 뺀다."""
        last = None
        for i, m in enumerate(self.months[:-2]):
            if m != last:
                yield i, m
                last = m


def fetch(user=None, token=None):
    user = user or os.environ.get("USERNAME", "pollux-o4")
    token = token or os.environ["GITHUB_TOKEN"]
    req = urllib.request.Request("https://api.github.com/graphql",
                                 json.dumps({"query": QUERY, "variables": {"u": user}}).encode(),
                                 {"Authorization": f"bearer {token}", "Content-Type": "application/json"})
    cal = json.load(urllib.request.urlopen(req))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = cal["weeks"]
    return Calendar(cal["totalContributions"],
                    tuple(tuple(d["contributionCount"] for d in w["contributionDays"]) for w in weeks),
                    tuple(int(w["contributionDays"][0]["date"][5:7]) for w in weeks))
