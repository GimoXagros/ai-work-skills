# v2026.10.25.2 — 보안 경고 해소와 플러그인·실행 도구 업데이트

## 변경 내용

이 배포는 v2026.10.25.1의 독립 스킬 77개를 유지하며, 별도로 관리하는 플러그인·실행 도구를 정식 배포 기준으로 갱신합니다.

| 항목 | 적용 버전 |
|---|---|
| Claude-Mem 공식 로컬 런타임 | 15.0.2 |
| Superpowers | 7.0.1 |
| HyperFrames 플러그인·CLI | 0.8.192 |
| ECC / Ponytail | 2.2.3 / 5.3.2 (최신 정식 릴리스 확인) |
| GSD Core | 1.18.0 |
| Agent Browser / Chrome DevTools MCP | 0.39.2 / 1.12.0 |
| Firecrawl CLI | 1.26.22 |
| Graphify / yt-dlp | 0.9.95 / 2026.10.21 |
| Headroom / Whisper / FFmpeg | 0.41.0 / 20250625 / 9.0.2 (최신 정식 배포 확인) |
| Node LTS / Python 실행 계열 / uv / Bun | 24.22.1 / 3.13.17 / 0.13.5 / 1.4.4 |

Node는 최신 LTS, Python은 기존 호환 계열 3.13의 최신 패치입니다. 최신 Current/메이저 버전으로 무조건 전환하지 않습니다. 원본 소스 커밋과 실제 패키지 버전은 별도 기록합니다.

## 보안 수정

- 기존 npm 경고 6개를 해소했습니다. Zod 4.6.7, zod-to-json-schema 3.25.2, Fallow 3.35.0을 명시적으로 고정했습니다. 경고를 숨기거나 Firecrawl을 구버전으로 되돌리지 않았습니다.
- 추가 검사에서 ECC의 fast-uri 3.1.7 경고를 발견해 3.1.9로 보완했습니다. 설치기는 공식 플러그인의 다른 override를 보존하면서 이 의존성만 수정하고, 잠금 파일 생성과 설치 모두 lifecycle script 없이 수행합니다. 훅 명령·인증·신뢰 기록은 수정하지 않습니다.
- 저장소 npm 트리, 현재 PC의 관리 npm 트리, ECC 운영 의존성에서 `npm audit` 경고 **0개**를 확인했습니다. 이는 모든 Python 패키지·개발 의존성·외부 서비스에 취약점이 없다는 보증이 아닙니다.
- `node tools/npm/test-runtime.cjs`로 Firecrawl의 JSON Schema 및 Zod v3 호환 입력을 로컬 HTTP 서버에 보내고 요청 스키마·응답 보존을 검사합니다. 이 스크립트는 계정 키나 외부 API 없이 실행됩니다.

- GitHub 전체 경고 추가 검사에서 Python 3.10용 Pillow 12.3 fallback의 치명적 경고를 확인해 제거했습니다. 글리프 도구는 Pillow 13.0.0·fontTools 4.67.0과 Python 3.11 이상을 요구합니다. 기본 스킬 설치는 계속 Python 3.10을 지원합니다. 오래된 `.venv`는 삭제하지 말고 Python 3.11 이상으로 만든 별도 체크아웃/가상환경을 사용하세요.

## 다른 PC 설치·업데이트

실행 중인 Codex/도구가 파일을 잠그면 해당 앱을 닫은 별도 PowerShell에서 진행합니다.

```powershell
git pull --ff-only
python -X utf8 install.py
python -X utf8 setup_tools.py
python -X utf8 setup_integrations.py --install --plugins --user-path
python -X utf8 configure_codex.py
. "$env:USERPROFILE/.codex/toolchains/ai-work-skills-env.ps1"
```

기존 Claude-Mem local은 중복 설치 방지를 위해 자동 플러그인 설치에서 건너뜁니다. 설정·SQLite 데이터를 로컬 백업한 뒤 다음 공식 설치기로 별도 갱신합니다. 로그인 화면이 나오면 해당 PC에서 직접 완료합니다.

```powershell
npm exec --yes --package=claude-mem@15.0.2 -- claude-mem install --ide codex-cli --provider codex --runtime worker --no-auto-start
npm exec --yes --package=claude-mem@15.0.2 -- claude-mem restart
```

`codex --no-daemon`으로 새 CLI를 열고 `/hooks`에서 변경된 훅을 검토·승인합니다. 현재 PC에서는 Claude-Mem 6개·ECC 1개·Ponytail 3개를 재승인했고 GSD 1개는 승인이 유지됐습니다. 최종 신뢰 상태는 **11개 모두 trusted**입니다. 다른 PC의 신뢰 해시나 인증 파일을 복사하지 않습니다. 잠금 오류 복구와 플러그인 전용 HyperFrames 실행 방법은 [ACTIVATION.md](docs/ACTIVATION.md)를 참조합니다.

## 실제 작동 검증

- 글리프 고정 의존성(Pillow·fontTools)은 pip-audit에서 알려진 취약점 0개를 확인했습니다. 다른 Python 도구의 전체 의존성 검사는 별도입니다.
- unittest **62개** 통과. ECC 보안 override 적용·다른 override 보존 검사 포함.
- Firecrawl: 기존 인증으로 실제 example.com 페이지 수집 성공. 로컬 스키마 호환 검사 성공.
- Chrome DevTools: 새 1.12.0 MCP 프로세스에서 도구 32개 발견, 실제 페이지 열기·명시한 pageId의 스냅샷 성공.
- Agent Browser: 0.39.2에서 실제 페이지 열기·스냅샷·시험 세션 종료 성공.
- HyperFrames: 기본 예제 10초, 1920×1080, 30fps, H.264 영상 렌더 성공. FFprobe 확인 및 FFmpeg 전체 디코딩 성공. 정적인 기본 예제라 검사에 정지 화면 안내 1개가 있었으며 오류는 0개입니다.
- Headroom: 새 프로세스에서 합성 로그 압축·원문 복원 성공. 프록시 라우팅은 설정하지 않았습니다.
- Whisper: 설치된 base 모델로 영어 합성 음성 전사 성공. 한국어 실음성 정확도 검증은 아닙니다.
- Graphify: 기존 합성 코드의 로컬 그래프 재추출 성공. 외부 LLM 의미 추출은 호출하지 않았습니다.
- yt-dlp: 로컬 HTTP로 제공한 시험 영상 다운로드 후 원본과 SHA-256 일치.
- Claude-Mem: 15.0.2 재시작, health=ok, initialized/mcpReady=true, degraded=false. 새 CLI 세션의 자동 초기화가 worker 로그에 기록됐습니다.
- 새 CLI 세션에서 정상 응답과 GSD·Ponytail·Claude-Mem 컨텍스트 주입을 확인했습니다. GSD·ECC·Ponytail SessionStart 등록 명령은 별도 합성 입력에서도 종료 코드 0입니다. 시험 중 생성된 HyperFrames 전역 중복 스킬은 백업 위치로 옮겼고, 정리 후 새 세션에서는 스킬 목록 용량 오류가 재현되지 않았습니다.

## 검증 한계

모든 플러그인 workflow나 모든 훅 이벤트의 전체 수명주기를 실행한 것은 아닙니다. GSD 변환기는 일부 `.claude` 경로 참조 경고를 출력하므로 개별 workflow의 호환성은 별도 확인이 필요합니다. 다른 물리 PC, 게임·실기, 한국어 음성 정확도, 외부 LLM/유료 영상 생성, 전체 Python 의존성 보안 감사는 미검증입니다. 로그인·메모리 DB·신뢰 기록·모델·실행 도구 캐시는 배포 ZIP에 포함하지 않습니다.
