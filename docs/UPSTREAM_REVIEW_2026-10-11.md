# 외부 원본 검토 — 2026-10-11

검토 시점의 GitHub 기본 브랜치 HEAD와 고정 원본을 비교했습니다. 활성 30개 중 외부 원본 추적 8개, 저장소 자체 관리 22개입니다. 외부 저장소 전체 커밋과 실제 스킬 폴더의 변경을 구분했습니다.

| 스킬 | 확인한 최신 원본 | 반영 결과 |
|---|---|---|
| `deep-interview` | [2db7d5136b22](https://github.com/Yeachan-Heo/oh-my-codex/commit/2db7d5136b22252e83091a12ea27567b2fdd5971) | 스킬 트리 동일, 최신 저장소 커밋으로 pin 갱신 |
| `frontend-testing-debugging` | [0722921d5542](https://github.com/openai/plugins/commit/0722921d5542fc593105c27bd52630babd8b8c2a) | 스킬 트리 동일, 최신 저장소 커밋으로 pin 갱신 |
| `create-kr-patch` | [4b360ab36399](https://github.com/mcpads/create-retro-game-kr-patch/commit/4b360ab36399aea0c7dbd4ea1b5a0acec075726f) | 3.4.0 반영: 플레이스루 검증 및 소비 경계 사례 |
| `akm-workflow` | [70e99b51b4e6](https://github.com/DECK6/akm/commit/70e99b51b4e6b075dc98aab8754c9ef16f602dfe) | 1.1.0 어댑터: 선택적 레이어, 근거/상태 분리, 연결 지식과 제한된 유지보수 |
| `binary-re` | [31d0a3fdf705](https://github.com/2389-research/binary-re/commit/31d0a3fdf705ed78c9d8f7d7c1aef673ad15a3a0) | 원본 HEAD 동일, 기존 Codex 번들 유지 |
| `re` | [64c3bffb54ae](https://github.com/vgrichina/re-skill/commit/64c3bffb54ae4b9d99804a03fa4f179f4dd080c5) | 원본 HEAD 동일, 기존 Codex 번들 유지 |
| `free-llm-apis` | [cf97c32fec1b](https://github.com/mnfst/awesome-free-llm-apis/commit/cf97c32fec1b2e96e9936746e2731a81bd5ea33f) | 1.0.0-codex.1: 원본 스킬 트리는 동일하나 제공업체 데이터 변경. 오래된 한도/모델 추천 제거 및 공식 문서 확인 절차 적용 |
| `humanize-korean` | [2f3d943d0805](https://github.com/epoko77-ai/im-not-ai/commit/2f3d943d08056b612a92e12bfb72ea94dd2acd18) | 원본 HEAD 동일, 기존 Codex 번들 유지 |

## 재현 근거와 적용 범위

- `deep-interview` (`skills/deep-interview`): 이전 Git tree `5831d1e6da3cd85afd312e5d9c8ea7ddaffa01eb`, 현재 `5831d1e6da3cd85afd312e5d9c8ea7ddaffa01eb`. 재귀 트리 API의 truncation 없음 확인.
- `frontend-testing-debugging` (`plugins/build-web-apps/skills/frontend-testing-debugging`): 이전 Git tree `e31dfad87123a11167c1a610d7bd5560cb787ef7`, 현재 `e31dfad87123a11167c1a610d7bd5560cb787ef7`. 재귀 트리 API의 truncation 없음 확인.
- `create-kr-patch` (`skills/create-kr-patch`): 이전 Git tree `531a665abe4251631769b97cb4d7df18fe7d5fa2`, 현재 `39e3535d8dd14d3bc16168af7ac642ac9617c26f`. 재귀 트리 API의 truncation 없음 확인.
- `free-llm-apis` (`free-llm-apis`): 이전 Git tree `0cf8c22a5a93316262a6069f30144e02ca9de210`, 현재 `0cf8c22a5a93316262a6069f30144e02ca9de210`. 재귀 트리 API의 truncation 없음 확인.

AKM은 독립 실행 지침 어댑터입니다. 원본의 전체 다중 스킬 묶음·공유 스크립트를 설치했다는 뜻이 아닙니다. 기존 분류/보안/검증 지침을 보존하면서 최신 계약·작업공간·지속 운영 지침을 반영했습니다.

free-llm-apis의 최신 README/data.json에서 모델 폐기, 카탈로그와 한도 변경이 확인됐지만 스킬 하위 트리는 갱신되지 않았습니다. 갱신된 카탈로그 숫자를 현재 보장값으로 복제하지 않고, 공식 가격·지역·모델·계정별 한도를 사용 시 확인하도록 보완했습니다. 예제는 환경변수에서 키와 모델을 읽으며, 실제 API 호출·신규 계정·결제 설정은 수행하지 않았습니다.

## 검증

- 격리된 새 경로에 전체 30개 설치 성공, 새 upstream 3개를 고정 SHA로 다운로드.
- Python 3.14: unittest 49개 통과, pip check 정상.
- fonttools: Python 3.10용 4.65.0과 Python 3.11 이상용 4.66.1 조건부 고정 유지.
- 이 결과는 스킬 설치·구조·설치기 검증이며 게임 런타임·실기기 검증이나 모든 외부 API의 실동작 보장이 아닙니다.

스킬 메타데이터 검사: 29개 통과. deep-interview 원본의 `argument-hint` 필드 1건은 현재 범용 quick_validate 허용 키 목록에 없어 경고로 남깁니다. 이 필드는 이번 변경 전후 동일하며, 원본 보존을 위해 제거하지 않았습니다. 전체 설치와 로컬 30개 파일 해시 대조는 통과했습니다.
