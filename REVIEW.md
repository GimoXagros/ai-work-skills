# 최종 검토 기록

확인일: **2026-09-14**. 기존 요청 **15개**와 AKM 워크플로 **1개**를 설치 대상으로 반영했습니다.
구성은 외부 원본 5개, 외부 원본을 Codex용으로 구성한 3개, 직접 제작한 8개입니다.
`hex-analyzer` 요청에는 새 링크가 인용한 `vgrichina/re-skill`을 실제 배포 이름 `re`로 반영했습니다. 앞서 제공된 Hex 데이터 분석 CLI는 여전히 제외합니다.

이 PC에는 설치 후 독립 스킬 15개가 있고, `create-kr-patch`는 같은 버전의 기존 플러그인을 사용합니다.
새 PC에서는 설치기가 16개를 독립 스킬로 설치합니다. 플러그인 전체와 외부 실행 환경이 모두 복제되는 것은 아닙니다.

## 요청별 반영 결과

| 요청 이름 | 반영한 이름 / 출처 | 확인된 범위와 제한 |
|---|---|---|
| create-plan | 은퇴: 내장 `/plan` 및 [`exec-plan`](skills/exec-plan/SKILL.md), [공유 답변](https://share.google/aimode/WHjCpsy0o0MAg6rMB), [공식 OpenAI 스킬 문서](https://developers.openai.com/codex/skills) | 삭제된 실험 패키지는 설치 대상에서 제거. 짧은 계획은 Codex 내장 `/plan`, 여러 단계·세션의 장기 계획은 자체 번들 `exec-plan` 사용 |
| akm-workflow | [`akm-workflow`](skills/akm-workflow/SKILL.md), [DECK6/akm](https://github.com/DECK6/akm/tree/f26ace2a16caba724b24db12cbee238ebb52498f) | AKM의 분류·증거·위험 기반 검증·Learn Back·보안·제한적 마이그레이션을 Codex 절차로 구성. 지식 저장소나 메모리 런타임 자체는 포함하지 않음 |
| deep-interview | `deep-interview`, [oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex/tree/cb955b0d5becbef76d2c1f0096b6e1f238e1e7f7/skills/deep-interview) | 인터뷰 지침. 전체 상태 저장·복구·후속 흐름은 OMX 런타임과 관련 스킬 필요 |
| code-review | `code-review`, [oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex/tree/cb955b0d5becbef76d2c1f0096b6e1f238e1e7f7/skills/code-review) | 독립 리뷰 에이전트 필요. OMX 통합 기능은 별도 런타임 필요 |
| frontend-testing-debugging | `frontend-testing-debugging`, [OpenAI plugins](https://github.com/openai/plugins/tree/1dc195897af4161d039b80d8471ec0a10c9bbc89/plugins/build-web-apps/skills/frontend-testing-debugging) | 현재 호스트의 브라우저 도구 또는 프로젝트 Playwright 환경 필요 |
| log-analyzer | `log-analyzer`, [Fractary 보관본](https://github.com/fractary/core/tree/accb3215b3514a36d3149b307e9ff9ceb0e67259/plugins/logs/archived/skills/log-analyzer) | Fractary 로그 관례와 Bash 도구에 의존. Windows는 Git Bash/WSL 등 필요 |
| create-retro-game-kr-patch | `create-kr-patch`, [mcpads 안정판 3.2.0](https://github.com/mcpads/create-retro-game-kr-patch/tree/56b31cc138926d769de97820df76e11beec6abb0/skills/create-kr-patch) | 한글패치 방법론·참조 문서. 게임별 도구·에뮬레이터는 별도 |
| hex-analyzer | [`re`](skills/re/SKILL.md), [vgrichina/re-skill](https://github.com/vgrichina/re-skill/tree/64c3bffb54ae4b9d99804a03fa4f179f4dd080c5) | MIT 원본을 Codex용으로 구성. 역공학 절차·기록 양식이며 별도 분석 실행 파일은 포함하지 않음. Hex 데이터 분석 CLI와 무관 |
| binary-parser | [`binary-re`](skills/binary-re/SKILL.md), [2389-research 원본](https://github.com/2389-research/binary-re/tree/42aee9063f3f3d52616700df3aa16df82b848604) | MIT 원본의 단계 문서와 참조를 독립 스킬로 구성. radare2/Ghidra 등은 별도 |
| image-glyph-generator | [직접 제작 1.0.0](skills/image-glyph-generator/SKILL.md) | 선택한 폰트의 글리프를 고정 셀로 래스터화. 누락·잘림·빈 글리프 검사. AI 이미지 생성 모델 자체를 설치하지 않음 |
| encoding-mapper | [직접 제작 1.0.0](skills/encoding-mapper/SKILL.md) | 명시적 바이트↔텍스트 테이블과 왕복 검사. 상태 없는 prefix-free 코드 지원; 게임별 상태 기계는 별도 |
| gba-pointer-fixer | [직접 제작 1.0.0](skills/gba-pointer-fixer/SKILL.md) | GBA 주소 변환·정렬·포인터 검사. 제공 도구는 읽기 전용 |
| nftr-font-editor | [직접 제작 1.0.0](skills/nftr-font-editor/SKILL.md) | 표준 리틀엔디언 NFTR 1.0/1.1 검사와 기존 3바이트 글자폭 수정. 글리프 추가·CMAP 확장·변형 포맷은 지원하지 않음 |
| ws-tile-compressor | [직접 제작 1.0.0](skills/ws-tile-compressor/SKILL.md) | 원더스완 8×8 planar/packed 2bpp·4bpp 변환과 완전히 같은 타일 중복 제거. 게임별 LZ/RLE 코덱은 별도 |
| retro-font-allocator | [직접 제작 1.0.0](skills/retro-font-allocator/SKILL.md) | 전체 글리프 저장량과 상태별 슬롯 용량 계산. 실제 로더·수명·전환 스케줄을 자동 증명하지 않음 |
| script-translator-limiter | [직접 제작 1.0.0](skills/script-translator-limiter/SKILL.md) | 번역 지침과 인코딩 바이트·행·픽셀 제한 및 명시된 제어 토큰 검사. 자동 잘라내기 없음. encoding-mapper 함께 설치 |

`deep-interview`, `code-review`, `log-analyzer`는 사용자가 처음 제시한 두 저장소에서 찾지 못해 위 배포본을 선택했습니다.
동일한 이름의 모든 배포본이 같은 스킬이라는 뜻은 아닙니다. 외부 원본의 정확한 버전은 [skills-lock.json](skills-lock.json)에 기록했습니다.

## AKM 반영 범위

[DECK6/akm](https://github.com/DECK6/akm)의 최신 검토 커밋 `f26ace2a16caba724b24db12cbee238ebb52498f`를 기준으로 Codex 어댑터, ROUTER, LOOP, VERIFICATION, SECURITY, SCHEMA와 로컬 메모리 런타임 계약을 확인했습니다.

- `akm-workflow`를 추가해 자료 분류, 원본·Markdown의 정본성, 검색 후보와 직접 읽은 증거의 구분, Tier 0–3 검증, 실패의 Learn Back, 비밀·개인 데이터 및 Git 경계를 한 절차로 연결했습니다.
- 장기 조사 성격의 `re`와 `binary-re`에는 AKM 저장소가 이미 있거나 사용자가 지속 기록을 요청한 경우에만 적용되는 계층별 기록 규칙을 추가했습니다.
- 단순 계산·변환 도구에는 AKM 규칙을 반복 삽입하지 않았습니다. 일회성 실행에 지식 저장소를 만들거나 불필요한 실행 로그를 보존하지 않도록 범위를 제한했습니다.
- AKM의 Hermes 로컬 메모리 런타임은 별도 어댑터 구현이므로 복사하거나 자동 실행하지 않습니다. 런타임 후보·인덱스가 원본 Markdown보다 우선하지 않는다는 권한 경계만 스킬에 반영했습니다.

## Google 공유 답변 검토

공유 페이지 7개를 브라우저로 열어 내용을 확인했습니다. 어느 페이지에도 해당 이름의 설치 가능한 `SKILL.md` 원본이 제시되어 있지 않았습니다.
답변의 주장을 공식 배포 사실로 취급하지 않고, 앞선 레트로 게임 한글화 요청에 맞춘 **직접 제작 스킬**로 반영했습니다.

| 공유 링크 | 답변의 내용 | 반영 판단 |
|---|---|---|
| [create-plan 대체](https://share.google/aimode/WHjCpsy0o0MAg6rMB) | 구형 Codex 모델 종료와 최신 도구 호출형 에이전트를 근거로 `create-plan`이 불필요하다고 설명 | 삭제된 실험 패키지가 현행 배포 대상이 아니라는 결론은 반영. 다만 현재 스킬 체계까지 종료됐다는 혼동은 수정하고, 공식 문서에 따라 짧은 계획은 `/plan`, 장기 계획은 자체 `exec-plan`으로 분리 |
| [image-glyph-generator](https://share.google/aimode/VuGAF4XPpp5O6RJGA) | AI 아이콘 생성용 일반 설명과 스킬 구성 예시 | 확인되지 않은 생성 옵션을 사용하지 않음. 실제 폰트 파일을 입력받는 래스터화 도구 제작 |
| [encoding-mapper](https://share.google/aimode/S6fjPZoAW0lDWrQJ8) | 저장소 파일 연결과 파일 인코딩 개념이 섞인 설명 | ROM의 명시적 코드 테이블을 별도 설계 |
| [nftr-font-editor](https://share.google/aimode/B3VqSsH04az599c4O) | NFTR 편집 프로그램 소개와 포맷 설명 | 실제 편집기 소스와 디스크 태그를 대조. 기존 글자폭 수정만 좁게 지원 |
| [ws-tile-compressor](https://share.google/aimode/754jMci6L6FinvuR2) | WebSocket 세션·컨텍스트 압축 설명 | 원더스완과 무관한 내용을 채택하지 않음. 원더스완 PPU 구현으로 타일 형식 확인 |
| [retro-font-allocator](https://share.google/aimode/EyG4NAMRMZPwwBB8W) | 웹 폰트·CSS 타이포그래피 설명 | 게임의 글리프 저장 공간과 활성 슬롯 배분 도구로 제작 |
| [script-translator-limiter](https://share.google/aimode/nIHEmpXNyOrJjOFHn) | 일반 번역·코드 변환·토큰 제한 프롬프트 설명 | 실제 인코딩 결과의 바이트 수와 폰트 폭을 검사하도록 제작 |

앞서 제공된 [GBA 공유 답변](https://share.google/aimode/Ae9wpvuK7SkxrN8nv)도 개념 설명이어서 `gba-pointer-fixer`를 직접 제작했습니다.
추가 스킬을 OpenAI, mcpads 또는 Google의 공식 배포본으로 표시하지 않습니다.

형식·API의 대조 근거:

- NFTR: [Epicpkmn11/nftr-editor의 읽기·쓰기 구현](https://github.com/Epicpkmn11/nftr-editor/blob/2e8ee2affd9316371812815758a51b2fd719e952/js/nftr.js). 표준 3바이트 폭 구조를 전제로 하며 짧은 패딩 블록의 변형까지 자동 식별하지는 못합니다.
- 원더스완 타일: [ares의 planar/packed 2bpp·4bpp fetch 구현](https://github.com/ares-emulator/ares/blob/af4cbb04f067682a8a3cf42695ff78bed634b38d/ares/ws/ppu/memory.cpp).
- 글리프 생성: [Pillow ImageFont](https://pillow.readthedocs.io/en/stable/reference/ImageFont.html), [fontTools TTFont](https://fonttools.readthedocs.io/en/latest/ttLib/ttFont.html).

참조한 외부 편집기·에뮬레이터 코드를 실행하거나 이 저장소에 복사하지 않았습니다.

## hex-analyzer 추가 링크 검토

[새 Google 공유 답변](https://share.google/aimode/rxr4oChTUr5Bdkqrn)은 **일부만 정확합니다**.
인용한 [vgrichina/re-skill](https://github.com/vgrichina/re-skill)의 실제 저장소, `SKILL.md`, 참조 문서, 설치 및 반복 실행 스크립트, MIT 라이선스를 고정 커밋에서 확인했습니다.

- 실제 스킬 이름은 `re`이며 원본 대상은 Claude Code입니다. `retro-game-hex-analyzer`는 공유 답변의 예시 이름으로, 그 이름의 공식 배포본을 확인한 것은 아닙니다.
- 헤더·주소 맵·역어셈블·에셋·실행 검증을 체계적으로 진행하는 절차는 실제 원본에 있습니다.
- 원본에 등장하는 `dis.py`, `xref.py`, CPU 데이터베이스, 에뮬레이터 등은 프로젝트에서 만들 도구의 예시입니다. 저장소에 완성된 실행 파일로 들어 있지 않습니다. 정적 패턴만으로 체력·좌표 같은 의미를 확정할 수도 없습니다.
- 공유 답변의 Game Boy를 일반 Z80로 보는 표현을 바로잡았습니다. 해당 원본 README도 SM83/LR35902로 구분합니다.

반영 내용:

- `skills/re`에 Codex용 진입 문서·단계 문서와 원본에서 가져온 조사/실패 기록 양식 및 MIT LICENSE를 포함했습니다.
- Claude 전용 프런트매터, 셸 문맥 삽입, `$ARGUMENTS` 및 Claude 전용 도구명을 현재 Codex 작업 방식으로 대체했습니다.
- 원본의 `install.sh`, `re_loop_template.sh`는 검토만 했고 실행하거나 설치하지 않았습니다. 따라서 별도의 Claude CLI, jq 또는 자동 커밋 루프는 설치되지 않습니다.
- 질문 범위에 맞게 필요한 조사 단계를 선택하게 했습니다. 자체 CPU 에뮬레이터 작성과 웹 이식은 필수가 아니며, 검증된 기존 분석 도구를 사용할 수 있습니다.
- 압축된 일부 구간과 원본 전체를 구분하고 주소 대응을 보존하도록 명확히 했습니다. 원본 단계 문서의 에뮬레이터 플랫폼 혼용 예시도 특정 제품을 잘못 지정하지 않도록 수정했습니다.
- 기록 양식에 입력 SHA-256을 추가하고, 해결된 실패 기록의 자동 삭제를 보관 방식으로 바꿨습니다.

원본 커밋: `64c3bffb54ae4b9d99804a03fa4f179f4dd080c5`.
설치기에서는 `python install.py --skill hex-analyzer`로 선택할 수 있고, 실제 호출 이름은 `$re`입니다.
스킬 설치는 분석 절차를 제공하는 것이며, 특정 게임에서의 분석 정확도나 모든 CPU·압축 형식 지원을 보증하지 않습니다.

## 검증 결과와 남은 한계

자동 검사 **31개 통과**:

- 빈 임시 설치 경로에 16개 설치, 같은 내용 재설치 시 건너뛰기, 기존 파일 백업, `create-plan`의 안전한 은퇴·대체, 이름 별칭 3쌍 및 번역 스킬의 의존성 설치.
- GBA 주소 경계·정렬·원본 보존.
- 인코딩 충돌·예약 코드·알 수 없는 문자·되돌릴 수 없는 조합 거부.
- 번역의 실제 바이트·픽셀 경계, 종결자와 제어 토큰, 줄 수 검사.
- 글리프 저장 용량과 상태별 슬롯 용량의 구분, 전환 시 초과와 예약 슬롯 충돌.
- 원더스완 네 가지 타일 형식의 알려진 바이트 벡터와 중복 제거 후 원래 순서 복원.
- 합성 NFTR의 크기·포인터·연결 순환·문자 맵 오류, 원본 해시·예상 바이트 검사, 지정한 폭 필드만 변경, 기존 출력 보호.
- 합성 테스트 폰트의 반복 생성 일치, 이진 픽셀 출력, 없는 문자·잘림·허용하지 않은 빈 글리프 거부, 기존 출력 보호.

추가로 저장소에 포함한 스킬 11개의 `SKILL.md` 형식 검사를 통과했습니다.
이 PC의 맑은 고딕으로 한글 14자와 문장부호 2자를 생성하여 누락·잘림 검사를 통과하고 아틀라스도 시각 확인했습니다.
해당 폰트와 시험 출력은 GitHub에 올리지 않았습니다. 2026-09-12 검토에서는 기존 8개를 유지하고 새 7개를 추가해 15개 구성을 확인했습니다.
이전 14개 구성은 캐시 없는 임시 Git 복제본에서 외부 원본 6개를 새로 내려받아 설치하는 검사도 통과했습니다.
이번 16개 구성은 빈 임시 설치 경로의 설치·재설치 검사와 전체 자동 검사 31개를 통과했습니다.

실제 게임 ROM에서의 실행 검증, 모든 NFTR 변형, 번역 의미 품질, OMX/Fractary 외부 런타임의 완전한 동작은 이번 확인 범위에 포함되지 않습니다.
게임·상용 폰트·인증 정보는 저장소에 포함하지 않았습니다.

## 다른 PC에서 재현

[README의 설치 순서](README.md#다른-pc에서-설치)를 따르면 같은 원본 커밋과 직접 제작 스킬을 가져옵니다.
`setup_tools.py`는 글리프 도구의 Pillow/fontTools를 저장소 안의 `.venv`에 준비합니다.
나머지 직접 제작 도구는 Python 표준 라이브러리로 실행할 수 있습니다.
외부 원본 스킬의 추가 실행 환경은 위 표에 명시한 대로 대상 PC에서 별도로 준비해야 합니다.
