# 다른 PC의 스킬 목록·Chrome MCP·CLI 승인 설정

Windows x64, Python 3.10 이상, Git, Codex CLI 및 Google Chrome이 필요합니다.
저장소를 유지할 폴더에 체크아웃하거나 릴리스 ZIP을 압축 해제하고 그 폴더에서 실행합니다.

```powershell
python -X utf8 install.py
python -X utf8 setup_integrations.py --install --plugins --user-path
python -X utf8 configure_codex.py
```

이미 이전 버전의 도구를 설치했다면 `setup_integrations.py --install --skip-gsd`로 실행 도구를 갱신한 뒤 `configure_codex.py`를 실행할 수 있습니다. GSD 설정이나 계정 로그인을 반복할 필요는 없습니다.

## 적용되는 설정

- `skills.max_context_tokens = 10000`: 설치된 스킬을 삭제·비활성화하지 않고 초기 목록 예산을 늘립니다. 공식 최대값이며 전체 모델 문맥 크기를 늘리는 설정은 아닙니다. 앞으로 스킬이 더 늘거나 모델이 달라지면 경고가 다시 나타날 수 있습니다.
- Chrome DevTools MCP **1.12.0**: 검증한 버전을 npm package-lock.json으로 설치합니다. 최신 버전을 자동 선택하지 않습니다.
- `chrome-devtools` 사용자 MCP 설정: Node 실행 파일과 서버 JS 파일의 절대 경로를 사용해 Windows의 `npx` 탐색 실패를 방지합니다. 기존 같은 이름의 사용자 MCP 설정은 이 구성으로 교체합니다.
- 브라우저는 `--headless --isolated`로 실행합니다. 사용자 Chrome 프로필과 분리되며 사용 통계 및 CrUX 조회는 비활성화합니다.

`configure_codex.py`는 변경 전 사용자 config.toml을 `CODEX_HOME/integration-backups/<UTC>-codex/`에 백업하고, Codex 공식 설정 쓰기 기능으로 목록 예산을 저장합니다. `CODEX_HOME` 미지정 시 `~/.codex`를 사용합니다. 훅 신뢰 기록, 계정 인증, 전역 승인 정책은 변경하지 않습니다. 중간 실패 시 이미 적용된 설정은 남을 수 있으므로 오류를 해결하고 다시 실행합니다. 기존 설정이 필요하면 해당 백업과 현재 파일을 비교해 복원하세요.

## 실제 페이지 열기·스냅샷 검사

새 PowerShell 창에서 저장소 폴더로 이동하고 다음을 실행합니다.

```powershell
pwsh -NoProfile -File ./verify_browser.ps1
```

표시되는 `chrome-devtools` 도구 요청의 대상 URL을 확인하고 이번 실행을 승인합니다. `new_page`와 `take_snapshot`은 각각 승인을 요청할 수 있습니다. 버튼 문구는 Codex 버전에 따라 다릅니다.

검사 성공 기준:

1. `new_page`가 https://example.com/을 열고 페이지 ID를 반환합니다.
2. `take_snapshot`이 **반환된 동일 ID**로 성공합니다. `about:blank`의 ID를 추측해 넣지 않습니다.
3. 스냅샷에 `Example Domain` 제목과 본문이 있습니다. CLI 종료 코드 0만으로 성공을 판단하지 않습니다.

이 도메인은 문서 예시용이므로 반복 부하 검사나 상시 모니터링에 사용하지 않습니다.

## CLI 시작 오류 해결

다음 오류가 발생하면 백그라운드 서버를 사용하지 않는 실행으로 다시 시도합니다.

```text
this CLI has no complete local package; install a packaged Codex CLI or use the standalone installer
```

```powershell
pwsh -NoProfile -File ./verify_browser.ps1 -NoDaemon
```

실제 Codex 옵션은 `--no-daemon --ask-for-approval on-request --sandbox read-only`입니다. 이 실행에만 승인 요청 모드를 지정하며, 파일 쓰기는 제한합니다. 이것은 승인 우회가 아닙니다.

`MCP tool call requires approval, but approval policy is never`는 설치 실패가 아니라 도구 승인을 받을 수 없는 세션이라는 뜻입니다. 위 대화형 창에서 사용자 승인을 받아 검사합니다. 훅 신뢰(`/hooks`)와 MCP 도구 승인은 별개입니다. 조직 정책이 승인을 제한한다면 우회하지 말고 관리자에게 확인합니다.

## 확인한 범위

2026-10-21 유지보수 PC의 새 대화형 CLI 세션에서 `--no-daemon`으로 시작하고 사용자 승인 후 두 도구가 모두 completed 상태로 끝났습니다. 같은 페이지 ID의 제목·본문 및 작업 완료 기록을 확인했습니다. 이전 검사에서는 목록 예산 변경 후 용량 초과 경고가 사라졌고 567개 스킬의 활성 상태를 유지했습니다. 이 수치는 당시 PC 전체 인벤토리이며 저장소의 독립 관리 스킬 64개와 다릅니다.

모든 PC·모든 모델에서 동일한 결과를 보장하지 않습니다. 별도의 실물 PC, 로그인·업로드·성능 측정은 검증하지 않았습니다.

공식 출처: [Codex 설정](https://learn.chatgpt.com/docs/config-file/config-reference), [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp).

2026-10-25: 1.12.0의 새 MCP 프로세스에서 도구 32개 발견, 페이지 열기와 `pageId`를 명시한 스냅샷 성공을 확인했습니다. 이는 새 PC의 사용자 승인 상태를 대신하지 않습니다.
