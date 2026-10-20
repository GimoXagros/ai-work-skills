# 외부 스킬·플러그인·실행 도구 관리

검토일: 2026-10-18. 요청한 23개 링크는 서로 다른 저장소 22개입니다. Anthropic skills의 두 경로는 같은 저장소의 동일 커밋으로 관리합니다.

## 설치와 업데이트

Chrome DevTools MCP 1.10.1은 ECC의 브라우저 실행 의존성으로 npm 잠금 파일에 추가 관리합니다. 등록과 스킬 목록 예산 적용은 설치 후 `configure_codex.py`로 진행합니다. [도구 승인과 CLI 복구 안내](BROWSER_SETUP.md)를 참조하세요.

훅 의존성 복구와 다른 PC의 계정·모델·MCP·신뢰 승인 절차는 [추가 설정 안내](ACTIVATION.md)를 따릅니다. 아래 표는 최초 2026-10-18 검토 범위이며, 이후 실제 활성화 검증은 해당 안내에 별도로 기록했습니다.

Windows x64, Git, Python 3.10 이상, 플러그인 명령을 지원하는 Codex CLI가 필요합니다. 저장소를 유지할 경로에 체크아웃합니다.

```powershell
git pull --ff-only
python -X utf8 install.py
python -X utf8 setup_tools.py
python -X utf8 setup_integrations.py --install --plugins --user-path
```

`setup_integrations.py`만 실행하면 설치 계획을 출력합니다. `--install`은 Node·격리된 Python 실행 환경·npm CLI·FFmpeg·GSD Codex 구성까지 설치합니다. `--plugins`는 공식 플러그인 5개를 별도로 설치합니다. `--skip-gsd`는 CLI만 설치하고 GSD의 Codex 설정·에이전트·훅 생성을 생략합니다. `--user-path`는 기존 Windows 사용자 PATH를 보존하고 도구 경로를 추가하며, 이전 값은 로컬 toolchains 폴더에 백업합니다.

새 터미널/Codex를 열거나 현재 PowerShell에서 다음 파일을 불러옵니다.

```powershell
. "$env:USERPROFILE/.codex/toolchains/ai-work-skills-env.ps1"
```

CODEX_HOME을 사용하는 경우 위 `.codex` 대신 해당 경로를 사용합니다. 다른 운영체제에서는 개별 스킬 설치와 플러그인 목록을 사용할 수 있지만, 실행 도구 자동 설치기는 Windows x64만 지원합니다. Python 도구는 uv의 사용자별 격리 환경, npm 도구는 `CODEX_HOME/toolchains/ai-work-skills-npm`에 설치합니다. Whisper의 Torch 의존성을 포함해 디스크와 네트워크 사용량이 큽니다.

## 관리 범위와 중복

- `skills-lock.json`: 독립 스킬 64개. 같은 설치기·변경 전 백업·파일 해시 검증을 적용합니다.
- `.agents/plugins/marketplace.json`: ECC, Claude-Mem, Ponytail, Superpowers, HyperFrames의 공식 Codex 플러그인 5개. 원본 커밋을 고정하고 Codex 설치기로 관리합니다.
- GSD Core 1.17.0: 공식 Codex 변환 설치기가 사용자 `.agents/skills`에 72개 스킬, `.codex`에 런타임·64개 에이전트 역할·업데이트 확인 훅을 생성합니다. 독립 스킬 64개에 포함하지 않습니다.
- `integrations-lock.json`: 요청 원본 전체의 검토 커밋과 실행 패키지 버전을 기록합니다. 소스 HEAD와 패키지 배포 버전은 별도입니다.
- `tools/npm/package-lock.json`: npm 하위 의존성의 버전·무결성 값을 보존합니다. Python은 최상위 버전 고정이며, 하위 의존성 전체를 모든 PC에서 동일하게 잠그지는 않습니다.

기존 Remotion 플러그인과 직접 설치한 Remotion 스킬은 중복 노출될 수 있습니다. 이번 직접 설치본은 4.0.536입니다. 기존 플러그인 캐시를 수동 수정하거나 삭제하지 않습니다. ECC·GSD·Superpowers·Ponytail의 계획/검증 기능도 겹치므로 한 작업에 모두 강제 호출하지 말고 요청과 프로젝트 지침에 맞춰 선택합니다.

## 요청별 반영 결과

| 요청 | 반영 방식 | 사용 조건·검증 범위 |
|---|---|---|
| Headroom | CLI 0.41.0 + 독립 안내 스킬 | proxy/code/mcp extras 설치. 버전 확인. 프록시 전환·대화 수집·서비스 자동 시작은 하지 않음 |
| Claude-Mem | 공식 Codex 플러그인 14.0.1 | 패키지 등록 확인. 메모리 provider 설정과 훅 신뢰·실제 수집은 별도 |
| claude-code-setup | claude-automation-recommender | Claude Code 자동화 추천 안내. Codex 설정 자동 전환 기능으로 표시하지 않음 |
| task-observer | Codex용 수정 번들 | 명시적인 회고·관찰 요청으로 범위 제한. 자동 영구 메모리/주간 작업 생성 제거, CC BY 4.0 출처 유지 |
| ECC | 공식 Codex 플러그인 2.2.3 | 원본 플러그인 스킬 제공. 모든 workflow/MCP 서버의 실제 실행 검증은 아님 |
| Ponytail | 공식 Codex 플러그인 5.3.2 | 고정 커밋 설치. 훅 신뢰는 Codex에서 관리 |
| Karpathy skills | karpathy-guidelines 고정 다운로드 | SKILL.md는 MIT로 표기하지만 루트 라이선스 파일은 없어 원본 파일을 이 저장소에 번들하지 않고 고정 다운로드 |
| UI UX Pro Max | 데이터·스크립트 포함 수정 번들 | Claude 전용 설치 경로 수정. 로컬 UX 검색 성공 |
| Firecrawl | build 스킬 5개 + CLI 1.26.9 | CLI 버전 확인. 호스팅 API 로그인/키는 별도, self-host 서버 배포는 포함하지 않음 |
| kr-patch-qa | 기존 독립 Codex 래퍼 유지 | 원본 HEAD가 기존 pin과 동일. 외부 QA 표준 링크 유지 |
| agent-browser | 수정 스킬 + CLI 0.39.1 | 실행 파일·버전 확인. 호스트 브라우저 도구 정책 우선, 실제 브라우저 세션 검증은 아님 |
| GSD Core | CLI 1.17.0 + 공식 Codex 변환 설치 | 72 스킬·64 역할 확인. 다른 런타임 탐색 경로와 일부 Claude 복구 문구가 남아 있어 실패 시 Codex 설치 명령 사용 |
| taste-skill | design-taste-frontend 고정 다운로드 | Node 데이터 목록 조회 성공. 브라우저 시각 검사는 별도 |
| find-skills | 고정 다운로드 | 원본 안내 스킬 |
| mcp-builder | 고정 다운로드 | 포함된 라이선스 보존 |
| Superpowers | 공식 Codex 플러그인 7.0.0 | 설치·등록 확인, 모든 다단계 workflow 검증은 아님 |
| frontend-design | 고정 다운로드 | 포함된 라이선스 보존 |
| Remotion | 12개 스킬 4.0.536 고정 다운로드 | 프로젝트별 Remotion 패키지 설치나 영상 렌더는 별도 |
| HyperFrames | 공식 플러그인 + CLI 0.8.171 | Windows 긴 경로 설치 보완, 버전 확인. 영상 렌더는 별도 |
| yt-dlp | CLI 2026.8.19 + 독립 안내 스킬 | 버전 확인. 사용자 콘텐츠 다운로드는 하지 않음 |
| Whisper | 패키지 20250625 + 독립 안내 스킬 | CLI import/help 성공. 모델 가중치 다운로드·전사 정확도 검증은 별도 |
| FFmpeg | 9.0.2 Windows essentials + 독립 안내 스킬 | 공식 다운로드 페이지가 안내하는 Gyan 빌드 SHA-256 검증. 합성 영상 1초 encode/probe/full decode 성공 |
| Graphify | graphifyy 0.9.92 + 독립 안내 스킬 | 합성 코드에서 2 nodes/1 edge 생성. 전역 always-on AGENTS.md·훅 대신 요청별 실행 |

## 설치와 활성화의 구분

공식 플러그인 등록이 API 로그인이나 훅 신뢰를 대신하지 않습니다. 계정 키·결제·모델 다운로드는 배포 파일에 포함하지 않습니다. 새 스킬이 현재 진행 중인 모든 작업에 소급 적용되거나, 실제 게임 QA·영상 품질·메모리 정확도를 보장하는 것으로 해석하면 안 됩니다.

GSD 설치 전 기존 설정·에이전트·훅을 `integration-backups/<UTC>/`에 백업합니다. 2026-10-18 이 PC 검사에서는 기존 config.toml 값의 제거·변경이 없었습니다. GSD 파일의 `.claude` 참조를 무조건 치환하지 않습니다. 여러 런타임을 탐색하는 호환 경로도 포함돼 있기 때문입니다. 누락 런타임 복구는 `gsd-core --codex --global`을 사용합니다.

## 출처와 재배포

원본 커밋은 [integrations-lock.json](../integrations-lock.json), 개별 스킬 pin은 [skills-lock.json](../skills-lock.json)에 있습니다. 독립 CLI 래퍼는 이 저장소에서 작성한 안내이며 원본 프로젝트의 공식 스킬이라고 표시하지 않습니다. 외부 실행 파일·모델·node_modules·가상환경은 릴리스 ZIP에 넣지 않습니다.

FFmpeg Windows 빌드 출처: [Gyan 빌드 페이지](https://www.gyan.dev/ffmpeg/builds/), [9.0.2 checksum](https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-9.0.2-essentials_build.zip.sha256). 이 빌드는 GPLv3이며 원본 저장소의 라이선스 표기와 구분합니다. Firecrawl build 스킬의 ISC 표기와 서버 저장소의 AGPL 라이선스도 구분합니다.
