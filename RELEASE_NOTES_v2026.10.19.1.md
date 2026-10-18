# v2026.10.19.1 — 훅 의존성 복구와 다른 PC 설정 안내

- ECC 설치 후 원본 잠금 파일의 실행 의존성을 자동 설치하여 SessionStart의 `js-yaml` 누락 오류를 해결합니다. npm 설치 스크립트는 실행하지 않습니다.
- Bun 1.4.3 공식 ZIP과 SHA-256을 고정하고, Bun·uv·uvx 경로를 생성 환경 파일과 선택적 사용자 PATH에 포함합니다.
- 공식 Claude-Mem 로컬 런타임이 활성화된 PC에서는 중복 플러그인을 다시 활성화하지 않습니다.
- 다른 PC의 Claude-Mem provider·uvx 경로, Headroom MCP, Firecrawl 로그인, Whisper 모델 및 Codex `/hooks` 신뢰 승인 절차를 한글로 정리했습니다.
- 독립 관리 스킬은 64개로 유지합니다. 계정 인증·훅 신뢰 기록·모델·실행 의존성 파일은 ZIP에 포함하지 않습니다.

설치: `python -X utf8 setup_integrations.py --install --plugins --user-path`

기존 ECC 의존성 복구: `python -X utf8 setup_integrations.py --plugins`

자세한 절차와 실제 검증 범위는 `docs/ACTIVATION.md`를 참조하세요. 새 PC에서는 로그인과 훅 신뢰 승인을 직접 완료해야 합니다. 모든 훅 이벤트와 모든 플러그인 workflow를 검증한 것은 아닙니다.
