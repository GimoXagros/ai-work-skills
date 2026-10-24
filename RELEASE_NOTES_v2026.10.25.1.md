# v2026.10.25.1 — 스킬 원본 점검과 의존성 업데이트

## 변경 내용

- 독립 관리 스킬 77개(번들 56개, 고정 upstream 21개)를 유지합니다. 10월 22일 추가된 Instagram 스킬 13개도 포함합니다.
- 외부 원본 33개를 확인하고 관측한 커밋과 처리 결과를 `docs/UPSTREAM_AUDIT_2026-10-25.json`에 기록했습니다.
- Remotion 스킬 12개를 4.0.538 원본으로 갱신했습니다. 타임라인 구조, 연결된 컴포지션, 자막과 오디오 경계 지침을 포함합니다.
- design-taste-frontend를 최신 고정 원본으로 갱신했습니다. 앱 화면 방향, 차트 및 장면 자료가 추가되었습니다.
- deep-interview, claude-automation-recommender, find-skills는 최신 커밋에서 진입 문서가 동일함을 확인하고 고정 커밋을 갱신했습니다.
- AKM의 선호·제약 정보 저장 위치와 메모리 포인터 규칙을 반영했습니다. free-llm-apis에는 Gonka Broker를 검증 전 후보로 기록했습니다. 무료 요금제나 API 작동을 보증하지 않습니다.
- UI/UX, Agent Browser 안내 진입점과 Firecrawl build 5개는 원본 진입 문서의 변경이 없음을 확인했습니다. Codex용 경로와 호스트 정책 안내를 유지합니다.
- Dependabot PR #3–#6의 fontTools 4.67.0, Pillow 13.0.0, fast-uri 3.1.9, body-parser 2.4.0을 반영했습니다. Pillow 13의 Python 3.10 지원 종료를 확인하여 Python 3.10에서는 Pillow 12.3.0·fontTools 4.65.0을 유지하도록 보완했습니다.

## 설치 및 업데이트

```powershell
git pull --ff-only
python -X utf8 install.py
python -X utf8 setup_tools.py
python -X utf8 setup_integrations.py --install --skip-gsd
```

스킬 설치기는 변경 전 파일을 자동 백업합니다. 기존 계정 인증, 플러그인 훅 신뢰와 GSD 설정을 갱신하는 배포가 아닙니다. 스킬 목록이 바뀌지 않으면 Codex를 다시 시작하세요.

## 검증 범위

- unittest 61개 통과: 설치·백업·경계 검증과 합성 글리프/인코딩/포인터/폰트/압축 사례 포함.
- 저장소 밖 새 설치 위치와 현재 PC에서 스킬 77개 모두 파일별 SHA-256 지문 일치.
- Python 3.10용 Pillow 12.3.0·fontTools 4.65.0 Windows wheel 다운로드 확인(3.10 실행 검증과 구분).
- npm 잠금 파일 설치 성공, fast-uri URI 처리와 body-parser JSON 미들웨어 생성 확인.
- 디자인 스킬 JavaScript 모듈 구문 검사 통과. 실제 웹사이트 제작이나 모든 디자인 지침의 실행 검증은 별도입니다.
- 현재 PC 실행 도구 재설치 성공 및 FFmpeg, Headroom, yt-dlp 버전 명령 확인.

## 유지한 항목과 한계

외부 원본의 최신 HEAD와 실제 배포 버전은 다릅니다. 이번 배포는 관리 스킬과 위 의존성 갱신입니다. `integrations-lock.json`의 실행 도구·플러그인·GSD 버전은 기존 검증본을 유지하며, 이들을 모두 최신 버전으로 올렸다는 의미가 아닙니다. 독립 작성된 emucap·Headroom·Graphify·미디어 도구 안내도 기존 런타임 기준을 유지합니다. 인증 API 호출, 브라우저 승인 흐름, 실제 게임·실기 동작, 다른 물리 PC와 Python 3.10 실행은 이번에 재검증하지 않았습니다.

## 남아 있는 보안 경고

2026-10-25 `npm audit` 기준 관리 npm 구성은 critical 0, high 4, low 2입니다. high 4는 Firecrawl의 Zod 3 계열 의존 경로에서 파생되며 [GHSA-mrhx-c7xc-m3w5](https://github.com/advisories/GHSA-mrhx-c7xc-m3w5)의 대용량 검증 입력에 의한 메모리 소진 문제입니다. low 2는 GSD/Fallow의 프로젝트 외부 경로 접근 관련 [GHSA-h4fr-cmh5-qr62](https://github.com/advisories/GHSA-h4fr-cmh5-qr62), [GHSA-jfwm-3p3c-6hx5](https://github.com/advisories/GHSA-jfwm-3p3c-6hx5) 경로입니다. 상위 패키지를 포함한 경고 수이며 독립 취약점 6개라는 뜻은 아닙니다. 자동 수정 제안이 Firecrawl CLI의 이전 버전으로 되돌리기를 포함하므로 무검증 강제 변경하지 않았습니다. 신뢰하지 않는 대용량 입력과 저장소 분석에는 이 잔여 위험이 있습니다. GitHub 저장소 전체 경고 집계와 이 npm 설치 트리의 검사 범위는 다릅니다.
