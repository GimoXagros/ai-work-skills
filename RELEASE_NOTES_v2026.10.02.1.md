# v2026.10.02.1

## 개요

- `free-llm-apis`를 CC0 원본과 참조 문서 그대로 저장소 관리 스킬에 추가
- 활성 관리 스킬을 29개(번들 26개, 고정 upstream 3개)로 갱신
- 변경된 외부 원본을 검토하고 필요한 스킬만 업데이트

## 포함 변경

- `free-llm-apis`
  - 원본: `mnfst/awesome-free-llm-apis`
  - 기준 커밋: `167013ff729e30f3a92bb8d416062d6c34a84507`
  - 공급자 선택, 무료 API 키 발급 및 OpenAI 호환 엔드포인트 설정 안내
- `create-kr-patch`
  - 고정 커밋을 `10de53e790535ad656ddccf916759661c4269f68`로 갱신
  - 프로젝트 기록, 이름 입력, 글리프·폰트·타일·UI 관련 최신 참조 자료 반영
- `binary-re`
  - 상위 원본을 `31d0a3fdf705ed78c9d8f7d7c1aef673ad15a3a0`까지 검토
  - Codex 독립 실행용 안전 조정은 유지하고 적응판 버전을 `1.2.0`으로 갱신

## 저장소 정리

- 이미 `main`에 병합된 `feat/emulator-development-skills`와 `feat/log-analyzer-v3` 원격 브랜치 정리
- 기존 릴리스와 태그는 변경 이력으로 보존

## 설치

```powershell
git pull --ff-only
python install.py
```

설치 후 목록이 갱신되지 않으면 Codex에서 새 작업을 열거나 앱을 다시 시작합니다.
