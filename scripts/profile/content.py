"""프로필의 사실·링크·문구 원본(SSoT). 그림과 README는 모두 여기서 읽는다."""
from dataclasses import dataclass, field

GH = "https://github.com/pollux-o4/"

PERSON = dict(
    name="주연석",
    latin="YEONSEOK JU",
    role="AI · 풀스택 개발자",
    lines=("데이터 분석부터 모델링, 서비스까지.", "데이터로 풀 수 있는 문제를 찾아,", "실제로 쓰이는 서비스로 만듭니다."),
    motto="쓰는 사람의 하루가 조금 나아지도록.",  # 업의 본질. p-oneul(오늘)과 같은 결
    tag="reliable  0.81",  # 히어로 탐지 박스 라벨 — 농산물 예측의 날짜순 검증 R²(팀)
    email="yeonseok.ju@gmail.com",
    # (키, 이름, 주소, 아이콘: logos.json slug 또는 journey.GLYPHS 키)
    links=(("portfolio", "Portfolio", "https://pollux-o4.github.io/itIsMe/", "briefcase"),
           ("linkedin", "LinkedIn", "https://www.linkedin.com/in/yeonseok-ju-37b2b7370/", "linkedin")),
)

# 02 아래 — 대표 기술. 분류별 공식 로고(Simple Icons, CC0 — art/logos.json). (이름, 로고 slug)
STACK = (  # 팀 프로젝트 + 혼자 만든 앱에서 실제로 쓴 것. 칸마다 최대 5개, 웹·커뮤니티 인기순(내림차순).
    # slug가 logos.json에 없으면 선 기호(AWS는 공식 로고를 배포하지 않음)
    ("AI · 데이터", (("Python", "python"), ("pandas", "pandas"), ("PyTorch", "pytorch"), ("OpenCV", "opencv"), ("YOLO", "ultralytics"))),
    ("웹", (("TypeScript", "typescript"), ("React", "react"), ("Next.js", "nextdotjs"), ("Vite", "vite"), ("PWA", "pwa"))),
    ("앱", (("Rust", "rust"), ("Google Play", "googleplay"), ("GTK", "gtk"), ("Capacitor", "capacitor"))),
    ("서버 · 배포", (("AWS EC2", "server"), ("Google Cloud", "googlecloud"), ("Firebase", "firebase"),
                 ("GitHub Actions", "githubactions"), ("FastAPI", "fastapi"))),
)
STACK_ALT = "주로 쓰는 기술 — " + " / ".join(f"{c}: " + ", ".join(n for n, _ in items) for c, items in STACK)

# 01 — 독자(채용 담당자)에게 남길 한 문장: "AI 모델부터 서비스 운영까지 직접 해 본 사람".
# 주장 셋, 각각 큰 숫자 하나 + 근거 한 줄(Manage-Career contribution.mine·metrics 기준).
CLAIMS_TITLE = "AI 모델부터 서비스 운영까지 해봤습니다"
CLAIMS = (  # 주장 · 대표 항목(아이콘 이름, 이름, 한 줄)
    ("모델을 학습시키고",
     (("detect", "음식 탐지", "YOLO11"), ("classify", "이미지 분류", "ViT"),
      ("series", "엔진 수명", "LSTM"), ("bars", "농산물 가격", "XGBoost"))),
    ("서비스로 만들어 배포하고",
     (("meal", "식사 기록", "Next.js · EC2"), ("server", "다방록", "Actions · EC2"))),
    ("개인 프로젝트로 운영까지",
     (("ring", "실마리", "웹 · Android"), ("nodes", "MemoIvy", "Linux"),
      ("book", "md2ebook", "VS Code"), ("grid", "Design Home", "웹"))),
)


@dataclass(frozen=True)
class Link:
    """카드 아래 링크 바 한 칸. icon은 art.icons의 이름."""
    key: str
    url: str
    action: str  # 무엇을 하게 되는지(한국어)
    platform: str  # 어디로 가는지(한글 금지 — 고정폭 서체에 한글 글리프가 없다)
    icon: str


def repo(name, key, note="GITHUB REPO"):
    return Link(f"{key}-repo", GH + name, "코드 보기", note, "branch")


@dataclass(frozen=True)
class Project:
    key: str
    title: str
    meta: str
    stat: str  # 결과 수치가 있을 때만. 없으면 빈 문자열(카드에 그리지 않는다)
    alt: str
    links: tuple = field(default=())

    @property
    def url(self):  # 카드 이미지는 첫 링크로 간다
        return self.links[0].url


AI_PROJECTS = (
    Project("nutrition", "음식 사진 → 식사 기록", "4인 · 36일 · PM · 풀스택 · 모델링 · EC2 배포", "mAP50 0.90 · TEAM",
            "음식 사진 → 식사 기록. 음식 탐지 결과 예시, 4인 36일, PM·풀스택·모델링, EC2 배포, mAP50 0.90(팀)",
            (Link("nutrition-video", "https://youtube.com/shorts/7hj92GtiodM", "시연 영상 보기", "YOUTUBE", "video"),
             repo("food-calorie-vision-main", "nutrition"))),
    Project("agri", "농산물 가격 예측", "6인 · 데이터 수집·전처리 · 누수 열 22개 제거", "R² 0.81 · TEAM",
            "농산물 가격 예측. 누수로 나온 0.98 대신 날짜순 검증 0.57 → 0.62 → 0.81",
            (repo("Agri-Price-Forecast", "agri", "GITHUB REPO · NOTEBOOKS"),)),
)

SHIPPED = (
    Project("silmari", "실마리", "하나의 계획, 세 가지 보기 · 웹 · Android", "",
            "실마리 — 하나의 계획을 원형·타임라인·목록으로 보는 앱",
            (Link("silmari-web", "https://silmari-todo.web.app/app/", "웹에서 바로 쓰기", "BROWSER · PWA", "globe"),
             Link("silmari-play", "https://play.google.com/store/apps/details?id=com.poneul.silmari",
                  "Android 앱 받기", "GOOGLE PLAY", "play"))),
    Project("memoivy", "MemoIvy", "연결되는 메모 캔버스 · Rust · Snap", "", "MemoIvy — 연결되는 메모 캔버스, Rust",
            (Link("memoivy", "https://snapcraft.io/memoivy", "Linux 앱 받기", "SNAP STORE · UBUNTU", "box"),
             repo("MemoIvy", "memoivy"))),
    Project("md2ebook", "md2ebook", "Markdown → 오프라인 책 리더 · VS Code", "", "md2ebook — Markdown을 오프라인 책 리더로",
            (Link("md2ebook", "https://marketplace.visualstudio.com/items?itemName=pollux-o4.markdown-ebook-reader",
                  "VS Code 확장 설치", "VS CODE MARKETPLACE", "code"),
             repo("md2ebook", "md2ebook"))),
    Project("design-home", "Design Home", "UI 트렌드 15종 라이브 데모 · 검토 도구", "",
            "Design Home — UI 트렌드 15종 라이브 데모와 디자인 검토 도구",
            (Link("design-home", "https://pollux-o4.github.io/design-home/", "사이트 열기", "WEB · NO INSTALL", "window"),
             repo("design-home", "design-home"))),
)

SECTIONS = {  # 번호 — 제목 — 오른쪽 한 줄
    "stack": ("01", "WHAT I DO", ""),
    "timeline": ("02", "TIMELINE", ""),
    "ai": ("03", "AI PROJECTS", "팀 프로젝트"),
    "shipped": ("04", "PERSONAL PROJECTS", "직접 기획·개발·배포"),
    "contrib": ("05", "CONSISTENCY", ""),
    "contact": ("06", "CONTACT", ""),
}
CONTACT_LINES = ("같이 풀 문제가 있다면,", "편하게 연락 주세요.")
CONTACT_ALT = "같이 풀 문제가 있다면 편하게 연락 주세요 — {email}"

# 03 — 농산물 카드의 R² 막대: (단계, 테스트 R², 조건). 첫 막대는 누수로 부푼 값이라 지운 표시로 그린다.
AGRI_CHART = ("TEST R²", (("초기", .98, "누수 포함"), ("누수 제거", .57, "날짜순 검증"), ("특성 선택", .62, ""),
                          ("튜닝", .81, "2023년으로 테스트")))

# 05 — CONSISTENCY. 수치는 live.calendar가 채우고 문구만 여기 둔다.
CONTRIB = dict(
    unit="contributions", stats=("ACTIVE DAYS", "LONGEST STREAK"), less="LESS", more="MORE",
    note={"light": "강조색 건물 = 상위 5% 날", "dark": "불 켜진 건물 = 상위 5% 날"},
    alt="최근 1년 GitHub 기여 기록 — 하루가 건물 한 채, 아래는 요일별 잔디",
)

# 02 — TIMELINE. 이미지는 scripts/sources/<key>.jpg
TIMELINE = {
    2025: dict(
        start=2,
        projects=((2, "arxiv-preview", "arXiv 수집"), (3, "student-preview", "성적 분석"), (3, "case-agri-onions", "농산물 예측"),
                  (4, "case-engine-a380", "엔진 수명"), (5, "thumbnail-preview", "썸네일 감정"), (5, "city-preview", "입지 분석"),
                  (7, "dropout-preview", "중퇴 예측"), (8, "vit-preview", "ViT 구현"), (9, "health", "헬스케어"),
                  (10, "hanwoo", "한우 체형"), (11, "case-nutrition-result", "음식 분석")),
        courses=((2, 6, "이스트캠프 · AI 모델"), (7, 12, "인공지능사관학교 · CV")),
        certs=((4, "SQLD"), (6, "ADsP"), (10, "AI활용"), (12, "빅데이터분석기사")),
    ),
    2026: dict(
        start=1,
        spans=((1, 3, "dabang-detect", "다방록"),),
        shipped=((6, "md2ebook", "md2ebook"), (8, "design-home", "Design Home"), (9, "silmari-circle", "실마리"),
                 (11, "memoivy", "MemoIvy")),
        certs=((12, "정보처리기사"),),
    ),
}
TIMELINE_LEGEND = (("project", "프로젝트"), ("course", "교육"), ("cert", "자격증"), ("ship", "배포"))
TIMELINE_ALT = "연도표 — 2025년 AI 교육 2과정과 프로젝트 11개·자격증 4종, 2026년 다방록과 개인 프로젝트 4종·정보처리기사"
