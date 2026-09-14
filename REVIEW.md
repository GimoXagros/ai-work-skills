# 현재 스킬 검토표

확인일: **2026-09-14**

이 문서는 [skills-lock.json](skills-lock.json)에 따라 현재 설치되는 **15개 스킬**만 설명합니다.
구성은 고정된 외부 원본 3개와 저장소 번들 12개입니다. 이 PC에서는 `create-kr-patch`가 동일 버전 플러그인으로 제공되므로 독립 폴더 14개와 플러그인 스킬 1개가 활성 상태입니다.

## 교체 판정

| 이전 항목 | 현재 처리 | 근거 |
|---|---|---|
| `create-plan` | 설치 중단. 짧은 계획은 내장 `/plan`, 장기 다단계 작업은 `exec-plan` | 오래된 실험 패키지 대신 현재 Codex 계획 기능과 장기 실행 계획 스킬을 분리 사용 |
| `code-review` | 설치 중단. Codex 내장 `/review`로 대체 | 현재 Codex가 전용 리뷰어와 범위 선택을 제공하므로 OMX 독립 에이전트 의존 스킬이 불필요 |
| Fractary `log-analyzer` | 번들 `log-analyzer` 2.0으로 교체 | 원본이 보관 경로에 있고 Fractary 로그 형식과 Bash 스크립트에 결합되어 있어 범용·읽기 전용 절차로 대체 |

Codex 공식 문서는 `/review`가 전용 리뷰어를 실행해 변경 없이 우선순위화된 결과를 제공한다고 설명합니다. 스킬 자체는 여전히 지원되며, 공식 예시에도 장기 작업용 Exec Plan이 포함됩니다.

## 현재 설치 목록

| 스킬 | 제공 방식 | 용도 | 범위와 제한 |
|---|---|---|---|
| `exec-plan` | 번들 1.0.0 | 장기 다단계 계획, 체크포인트, 인계 | 일반적인 짧은 계획은 `/plan` 사용 |
| `deep-interview` | [oh-my-codex 고정 커밋](https://github.com/Yeachan-Heo/oh-my-codex/tree/cb955b0d5becbef76d2c1f0096b6e1f238e1e7f7/skills/deep-interview) | 모호한 요구사항의 단계별 인터뷰 | 기본 질문은 네이티브 대체 경로 사용 가능. OMX 상태·자동 인계는 OMX 런타임 필요 |
| `frontend-testing-debugging` | [OpenAI plugins 고정 커밋](https://github.com/openai/plugins/tree/1dc195897af4161d039b80d8471ec0a10c9bbc89/plugins/build-web-apps/skills/frontend-testing-debugging) | 렌더링 UI 확인과 디버깅 | 브라우저 도구 우선. 허용된 경우 프로젝트 Playwright로 대체 |
| `log-analyzer` | 번들 2.0.0 | 앱·빌드·테스트·운영 로그의 타임라인과 오류 패턴 분석 | 로그는 읽기 전용. 형식·시간대·상관관계 불확실성을 명시 |
| `create-kr-patch` | [mcpads 3.2.0 고정 커밋](https://github.com/mcpads/create-retro-game-kr-patch/tree/56b31cc138926d769de97820df76e11beec6abb0/skills/create-kr-patch) | 레트로 게임 한글 패치 전체 흐름 | 이 PC에서는 동일 버전 플러그인 제공. 게임별 분석과 도구는 별도 필요 |
| `akm-workflow` | 번들 1.0.0, [DECK6/akm 기반](https://github.com/DECK6/akm/tree/f26ace2a16caba724b24db12cbee238ebb52498f) | AKM 계층, 증거, 위험 기반 검증, Learn Back | 지식 저장소나 메모리 서비스 자체는 포함하지 않음 |
| `gba-pointer-fixer` | 번들 1.0.0 | GBA 데이터·ARM·THUMB 포인터 분석과 안전한 수정 절차 | 게임별 포인터 소비자와 압축 형식은 별도 분석 필요 |
| `binary-re` | 번들 1.1.0, [MIT 원본 기반](https://github.com/2389-research/binary-re/tree/42aee9063f3f3d52616700df3aa16df82b848604) | 실행 파일·펌웨어·바이트코드 역공학 | 분석 도구 자체가 아니라 도구 사용 절차와 참조 자료 |
| `image-glyph-generator` | 번들 1.0.0 | 고정 셀 글리프 아틀라스 생성 | 사용자 제공 폰트와 Pillow/fontTools 필요 |
| `encoding-mapper` | 번들 1.0.0 | 바이트-문자 테이블과 왕복 검증 | 자동 인코딩 추측이나 게임별 테이블 발견은 하지 않음 |
| `nftr-font-editor` | 번들 1.0.0 | 표준 리틀엔디언 NFTR 검사와 폭 수정 | 확인된 기존 CWDH 폭 엔트리만 수정 |
| `ws-tile-compressor` | 번들 1.0.0 | WonderSwan 2bpp·4bpp 타일 변환과 중복 제거 | 게임 고유 압축 스트림은 별도 역공학 필요 |
| `retro-font-allocator` | 번들 1.0.0 | 글리프 저장 용량과 활성 슬롯 배분 | ROM 재배치나 실제 렌더러 수정은 포함하지 않음 |
| `script-translator-limiter` | 번들 1.0.0 | 번역문의 바이트·행·픽셀·제어 토큰 제한 검사 | `encoding-mapper`의 명시적 테이블 필요. 자동 축약하지 않음 |
| `re` | 번들 1.1.0, [MIT 원본 기반](https://github.com/vgrichina/re-skill/tree/64c3bffb54ae4b9d99804a03fa4f179f4dd080c5) | 레트로 ROM 주소 맵, 디스어셈블리, 자산 조사 | 완성된 디스어셈블러나 에뮬레이터를 포함하지 않음 |

## 최신성 확인

2026-09-14 기준 외부 원본 7개를 확인했으며, 유지 중인 3개와 번들 스킬의 기반 원본 3개 모두 매니페스트의 고정 커밋이 해당 저장소 `HEAD`와 일치했습니다. 제외한 Fractary 원본도 비교를 위해 확인했습니다.

| 원본 | 확인 커밋 |
|---|---|
| `Yeachan-Heo/oh-my-codex` | `cb955b0d5becbef76d2c1f0096b6e1f238e1e7f7` |
| `openai/plugins` | `1dc195897af4161d039b80d8471ec0a10c9bbc89` |
| `mcpads/create-retro-game-kr-patch` | `56b31cc138926d769de97820df76e11beec6abb0` |
| `DECK6/akm` | `f26ace2a16caba724b24db12cbee238ebb52498f` |
| `2389-research/binary-re` | `42aee9063f3f3d52616700df3aa16df82b848604` |
| `vgrichina/re-skill` | `64c3bffb54ae4b9d99804a03fa4f179f4dd080c5` |
| `fractary/core` | `accb3215b3514a36d3149b307e9ff9ceb0e67259` - 확인 후 설치 대상에서 제외 |

## 설치 안전성

- 외부 소스는 전체 40자리 커밋 SHA로 고정합니다.
- 기존 폴더가 다르면 먼저 `skill-backups/`에 보존합니다.
- 은퇴 대상은 알려진 파일 지문과 정확히 일치할 때만 제거합니다.
- 동명 사용자 정의 스킬, 플러그인 캐시, 인증 정보, Codex 설정은 변경하지 않습니다.
- ROM, 상용 폰트, 개인 로그와 같은 사용자 데이터는 저장소에 포함하지 않습니다.

## 공식 기준

- [Codex 스킬 문서](https://developers.openai.com/codex/skills)
- [Codex 코드 리뷰 문서](https://developers.openai.com/codex/code-review)
