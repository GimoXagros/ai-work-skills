# 다른 PC에서 추가 설정과 훅 활성화

스킬 목록 용량과 Chrome DevTools MCP 설치·승인·CLI 시작 오류 해결은 [브라우저 설정 안내](BROWSER_SETUP.md)에 있습니다.

2026-10-19 기준. 먼저 저장소 루트에서 다음 명령을 실행합니다(Windows x64).

```powershell
python -X utf8 install.py
python -X utf8 setup_tools.py
python -X utf8 setup_integrations.py --install --plugins --user-path
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
. "$codexHome/toolchains/ai-work-skills-env.ps1"
```

기존 터미널·Codex는 재시작해야 새 사용자 PATH를 읽습니다. 생성된 환경 파일에는 Node, npm 도구, Python 도구, FFmpeg, **uv/uvx와 Bun**이 포함됩니다. Bun 1.4.3 공식 ZIP은 고정 SHA-256 검증 후 설치합니다. ECC는 플러그인 원본 package-lock.json으로 `npm ci --omit=dev --ignore-scripts --no-audit --no-fund`를 실행합니다. 이 단계가 없으면 SessionStart에서 `Cannot find module 'js-yaml'` 오류가 발생할 수 있습니다. 기존 설치는 `python -X utf8 setup_integrations.py --plugins`로 ECC 의존성을 복구할 수 있습니다.

## Claude-Mem

이 기능은 대화·도구 실행 관찰 내용을 메모리로 기록합니다. 사용할 PC에서 아래 공식 설치기를 실행하고 브라우저에서 직접 로그인합니다. 계정·체험판 조건은 화면에서 확인합니다.

```powershell
npm exec --yes --package=claude-mem@14.0.1 -- claude-mem install --ide codex-cli --provider codex --no-auto-start
```

Codex provider에는 해당 PC의 `codex login` 구독 인증이 필요합니다. API 키 방식과 구분하며, 인증 파일을 저장소나 다른 PC로 복사하지 않습니다. 설치 전 `$codexHome/config.toml`과 기존 `$env:USERPROFILE/.claude-mem/settings.json`을 별도 로컬 경로에 백업합니다.

설치 후 `.claude-mem/settings.json`의 다른 항목을 유지하면서 다음 값을 설정합니다. 아래 경로 표기는 실제 절대 경로로 바꿉니다.

| 항목 | 값 |
|---|---|
| `CLAUDE_MEM_RUNTIME` | `worker` |
| `CLAUDE_MEM_PROVIDER` | `codex` |
| `CLAUDE_MEM_CHROMA_UVX_PATH` | `$codexHome/toolchains/ai-work-skills-bootstrap/Scripts/uvx.exe`의 실제 경로 |
| `CLAUDE_MEM_CODEX_PATH` | PowerShell `(Get-Command codex).Source` 결과 |

Codex 설정에서 `[plugins."claude-mem@claude-mem-local"]`은 `enabled = true`, `[plugins."claude-mem@ai-work-skills"]`은 `enabled = false`로 두어 공식 런타임 하나만 사용합니다. `[hooks.state]`는 수정하지 않습니다. 이 저장소 설치기는 활성화된 `claude-mem-local`을 감지하면 중복 플러그인을 다시 켜지 않습니다.

```powershell
npm exec --yes --package=claude-mem@14.0.1 -- claude-mem start
Invoke-RestMethod http://127.0.0.1:37777/api/health
```

정상 기준은 `status=ok`, `initialized=true`, `mcpReady=true`, `dependencies.degraded=false`입니다. uvx 오류가 남으면 위 절대 경로를 확인하고 `start` 대신 `restart`를 실행합니다. 로컬 뷰어는 <http://127.0.0.1:37777>입니다.

## Headroom · Firecrawl · Whisper

Headroom은 프록시 라우팅 변경 없이 요청 시 실행되는 로컬 MCP로 등록합니다. 먼저 Codex 설정을 백업합니다.

```powershell
codex mcp add headroom --env DO_NOT_TRACK=1 --env HEADROOM_TELEMETRY=off --env HEADROOM_BEACON=off -- (Get-Command headroom).Source mcp serve
firecrawl login --browser
firecrawl status
firecrawl scrape https://example.com --format markdown
```

Firecrawl 브라우저에서 해당 PC의 CLI 연결 승인을 직접 완료합니다. API 키를 채팅이나 저장소에 넣지 않습니다. Headroom MCP 모드에서는 프록시가 실행되지 않으므로 `headroom doctor`의 프록시 경고만으로 실패를 판단하지 않습니다.

Whisper는 첫 실행 시 선택한 모델을 다운로드합니다(다국어 base 약 139MiB). 본인 테스트 음성 경로로 다음을 실행합니다. 영어 음성이라면 `--language English`를 사용합니다.

```powershell
whisper "C:/path/to/test.wav" --model base --language Korean --fp16 False --output_dir "C:/path/to/transcript"
```

## 훅 신뢰 승인 — PC마다 사용자가 직접 진행

프로젝트 폴더에서 터미널의 대화형 **`codex`**를 실행하고 **`/hooks`**를 입력합니다. 표시된 출처와 실행 명령을 검토한 뒤 새롭거나 변경된 훅을 신뢰 승인합니다. 화면 버튼 문구는 CLI 버전에 따라 다릅니다. 승인 후 새 세션에서 SessionStart 실행을 확인합니다. 플러그인 설치와 훅 신뢰는 별개이며, 다른 PC의 신뢰 해시를 복사하거나 신뢰 검사 우회 옵션을 사용하지 않습니다.

공식 안내: <https://learn.chatgpt.com/docs/hooks>

## 검증 범위

2026-10-19 유지보수 PC에서 GSD·ECC·Ponytail의 등록된 SessionStart 콜백을 격리된 입력으로 직접 실행해 종료 코드 0을 확인했습니다. ECC는 의존성 설치 전 실패, 설치 후 정상 응답을 확인했습니다. Claude-Mem은 실제 Codex 대화의 세션 초기화·관찰 저장·종료 요약 저장 로그를 확인했습니다. Headroom 합성 로그 압축/복원, Firecrawl example.com 수집, Whisper base 영어 합성 음성 전사를 확인했습니다.

이 결과는 새 PC의 로그인·훅 승인 완료를 의미하지 않습니다. 모든 이벤트(PostCompact·SubagentStart 등), 모든 플러그인 workflow, 한국어 실음성 정확도는 검증하지 않았습니다. Superpowers의 Codex 매니페스트에는 자동 훅이 없습니다. 계정 인증·신뢰 기록·모델·node_modules는 배포 ZIP에 포함하지 않습니다.
