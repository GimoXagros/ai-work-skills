# ai-work-skills

Codex 스킬을 다른 PC에서도 같은 버전으로 설치하는 개인용 저장소입니다.
확인 날짜: **2026-09-12**. 원본 스킬은 수정하지 않고 원본 GitHub 저장소에서 고정된 커밋으로 다운로드합니다.

## 다른 PC에서 설치

Git, Python 3.10 이상, GitHub CLI가 설치되어 있다면 다음 명령을 실행합니다.
비공개 저장소이므로 처음 한 번은 본인 GitHub 계정으로 로그인해야 합니다.

```powershell
gh auth login
gh repo clone GimoXagros/ai-work-skills
cd ai-work-skills
python install.py
```

macOS/Linux에서 `python`이 없으면 `python3 install.py`를 사용합니다.
GitHub에서 ZIP으로 받아 압축을 풀고 `python install.py`를 실행해도 됩니다.
스킬 기본 설치에는 Python 표준 라이브러리와 인터넷 연결만 필요합니다.

기본 설치 경로는 `$CODEX_HOME/skills`, 환경 변수가 없으면 `~/.codex/skills`입니다.
다음 Codex 턴에서 사용할 수 있습니다. 목록이 갱신되지 않으면 새 작업을 열어 주세요.
최신 공통 에이전트 스킬 경로를 원하는 환경에서는 명시적으로 지정할 수도 있습니다.

```powershell
python install.py --dest "$env:USERPROFILE/.agents/skills"
```

같은 스킬을 여러 검색 경로에 중복 설치하지 않는 편이 좋습니다.
이 PC에서 이미 같은 커밋으로 설치된 `create-kr-patch` 플러그인은 그대로 사용합니다.
새 PC에는 플러그인 전체가 아닌 독립 스킬과 참조 문서를 설치합니다.

## 설치 대상과 출처

| 요청 이름 | 실제 스킬 | 출처 / 상태 |
|---|---|---|
| create-plan | create-plan | [openai/skills](https://github.com/openai/skills/tree/a5119697b819090e00e5d11ee1d86834d7c1043a/skills/.experimental/create-plan), 삭제 직전 원본 복원 |
| deep-interview | deep-interview | [Yeachan-Heo/oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex/tree/cb955b0d5becbef76d2c1f0096b6e1f238e1e7f7/skills/deep-interview), 확인일 main |
| code-review | code-review | [Yeachan-Heo/oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex/tree/cb955b0d5becbef76d2c1f0096b6e1f238e1e7f7/skills/code-review), 확인일 main |
| frontend-testing-debugging | frontend-testing-debugging | [openai/plugins](https://github.com/openai/plugins/tree/1dc195897af4161d039b80d8471ec0a10c9bbc89/plugins/build-web-apps/skills/frontend-testing-debugging), 확인일 main |
| log-analyzer | log-analyzer | [fractary/core](https://github.com/fractary/core/tree/accb3215b3514a36d3149b307e9ff9ceb0e67259/plugins/logs/archived/skills/log-analyzer), 보관된 Fractary 버전 |
| create-retro-game-kr-patch | create-kr-patch | [mcpads/create-retro-game-kr-patch](https://github.com/mcpads/create-retro-game-kr-patch/tree/56b31cc138926d769de97820df76e11beec6abb0/skills/create-kr-patch), 안정판 3.2.0 |

`deep-interview`, `code-review`, `log-analyzer`는 동명 배포본이 여러 개일 수 있습니다.
사용자가 제시한 두 저장소에는 이 이름의 스킬이 없어, 위 출처의 원본을 선택했습니다.

### 실행 의존성과 확인 범위

- `create-plan`: 읽기 전용 계획 작성 스킬. upstream에서 삭제된 과거 버전이며 최신 지원 버전으로 표현하지 않습니다.
- `deep-interview`: OMX 원본입니다. 전체 상태 저장·복구·후속 워크플로에는 `oh-my-codex` 런타임 및 관련 스킬이 필요합니다. 스킬 파일 설치가 OMX 설치까지 의미하지는 않습니다.
- `code-review`: 독립 리뷰 에이전트가 필요합니다. 원본의 OMX 상태/HUD 통합은 OMX 런타임이 있어야 하며, 독립 검토가 없으면 승인 판정을 할 수 없습니다.
- `frontend-testing-debugging`: 현재 호스트의 브라우저 도구 또는 프로젝트의 Playwright 환경이 필요합니다. 원본에 나온 예시 API는 현재 제공되는 도구 지침과 대조해 사용합니다.
- `log-analyzer`: Fractary 로그 구조에 맞춘 보관 버전입니다. 포함된 셸 스크립트는 Bash 및 필요한 Unix 도구를 요구하므로 Windows에서는 Git Bash/WSL 등 환경이 필요합니다. 임의 형식의 모든 로그를 자동 지원하는 전용 프로그램은 아닙니다.
- `create-kr-patch`: 방법론과 참조 문서입니다. 에뮬레이터·폰트·게임별 도구 등은 대상 작업에서 준비합니다.

검증은 스킬 이름/파일, 고정된 출처, 복사 무결성, 재실행과 백업 동작에 대한 것입니다.
각 스킬의 실제 프로젝트 수행이나 외부 런타임까지 검증했다는 뜻은 아닙니다.

## 출처를 확인하지 못한 요청 이름

아래 9개는 `openai/skills`, `mcpads/create-retro-game-kr-patch`의 현재 스킬 목록과
이전 SKILL.md 경로 기록에서 독립 스킬로 발견하지 못했습니다. 공개 검색에서도 일치하는 원본을 확인하지 못했습니다.
설치 파일을 임의로 만들어 원본인 것처럼 포함하지 않았습니다.

- hex-analyzer
- binary-parser
- image-glyph-generator
- encoding-mapper
- gba-pointer-fixer
- nftr-font-editor
- ws-tile-compressor
- retro-font-allocator
- script-translator-limiter

한글패치 스킬에는 폰트, 인코딩, 포인터, 압축, NFTR 관련 참조 문서가 있지만,
위 이름의 독립 스킬이나 실행 도구가 설치된 것으로 보지는 않습니다.
정확한 원본 URL을 찾으면 `skills-lock.json`에 추가하여 같은 방식으로 설치할 수 있습니다.

## 재설치와 업데이트

```powershell
git pull --ff-only
python install.py
```

- 설치기는 저장소에 검토해 기록한 커밋을 설치합니다. 실행할 때 임의로 최신 코드를 가져오지 않습니다.
- 원본 업데이트는 원본 변경 내용을 검토하고 `skills-lock.json`의 커밋을 갱신한 뒤 반영합니다.
- 같은 파일이면 건너뜁니다. 다른 기존 스킬 폴더는 설치 경로의 상위 `skill-backups/<UTC 시각>/`에 보존합니다.
- `.system`, 기존 플러그인, 인증 파일, Codex 전체 설정은 복사하거나 변경하지 않습니다.
- 원본 다운로드 캐시는 `.cache/`에 있으며 GitHub에 올리지 않습니다. 이 저장소는 원본 복제본 대신 출처·커밋·재설치 도구를 보관합니다.
- 캐시가 준비된 PC에서는 `python install.py --offline`으로 다시 설치할 수 있습니다.
- 목록만 확인: `python install.py --list`
- 하나만 설치: `python install.py --skill create-plan`
- `create-retro-game-kr-patch`는 설치기에서 `create-kr-patch`의 별칭으로 인식합니다.

## 라이선스

다운로드하는 각 스킬은 각 원본의 라이선스/이용 조건을 따릅니다.
원본 내용을 이 저장소에서 재배포하지 않습니다.
`vendor/skill-installer`의 설치 도우미는 이 PC의 OpenAI 시스템 skill-installer에서 가져왔으며
동봉한 Apache-2.0 `LICENSE.txt`를 보존했습니다. 스크립트 내용은 수정하지 않았습니다.

참고: [OpenAI 스킬 문서](https://learn.chatgpt.com/docs/build-skills).
