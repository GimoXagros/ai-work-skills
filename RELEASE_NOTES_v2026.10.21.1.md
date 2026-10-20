# v2026.10.21.1 — 스킬 목록 용량과 Chrome 브라우저 설정 재현

- 스킬 목록 예산을 10,000토큰으로 설정하는 `configure_codex.py`를 추가했습니다. 설정 전 백업하며 스킬을 삭제하거나 비활성화하지 않습니다.
- Chrome DevTools MCP 1.10.1을 npm 잠금 파일로 설치하고, Node·서버 JS 절대 경로로 등록해 Windows의 `npx` 실행 파일 탐색 실패를 방지합니다.
- 사용자 브라우저와 분리된 headless·isolated 모드를 적용하고 사용 통계·CrUX 조회를 끕니다.
- 대화형 `verify_browser.ps1`을 추가했습니다. 사용자가 페이지 열기와 스냅샷 요청을 승인하고 동일 페이지 ID의 제목·본문을 확인합니다.
- `no complete local package` 시작 오류에는 `-NoDaemon` 옵션을 사용하도록 안내합니다. 도구 승인과 훅 신뢰를 구분하며 승인 우회는 하지 않습니다.

설치 후 설정:

```powershell
python -X utf8 setup_integrations.py --install --plugins --user-path
python -X utf8 configure_codex.py
pwsh -NoProfile -File ./verify_browser.ps1 -NoDaemon
```

독립 관리 스킬 64개는 유지합니다. 계정 인증·훅 신뢰 기록·node_modules·브라우저 프로필은 ZIP에 포함하지 않습니다.

유지보수 PC의 새 승인 가능 CLI 세션에서 실제 페이지 열기와 스냅샷 성공을 확인했습니다. 다른 실물 PC 및 로그인·업로드·성능 측정은 검증하지 않았습니다. 상세 절차는 `docs/BROWSER_SETUP.md`를 참조하세요.
