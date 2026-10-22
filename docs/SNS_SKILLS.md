# SNS 관리 스킬 묶음

2026-10-22 기준. Instagram 전용 13개를 같은 설치기에 등록했습니다. 원본은 [Jakeschincariol/instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill/tree/d03c56bb598be770c60b201f94237e5d1a4268a6), MIT이며 각 폴더에 라이선스를 보존합니다.

| 작업 | 스킬 | 산출물 |
|---|---|---|
| 계정 방향·진단 | `ig-profile`, `ig-audit` | 프로필 수정안, 제공된 성과 자료 분석 |
| 조사·일정 | `ig-viral`, `ig-plan` | 근거가 있는 사례와 주간 콘텐츠 계획 |
| 콘텐츠 제작 | `ig-reel`, `ig-caption`, `ig-carousel`, `ig-story` | 대본·캡션·슬라이드 문안·스토리 구성 |
| 커뮤니티 응대 | `ig-comment`, `ig-reply`, `ig-dm` | 댓글·답글·DM 초안 |
| 재활용·윤문 | `ig-repurpose`, `ig-human` | 기존 콘텐츠 재구성과 영어 문체 검사 |

권장 흐름은 프로필/실적 확인 → 조사 → 주간 계획 → 형식별 초안 → 검토입니다. 전 과정을 강제하지 않으며, 캡션 한 건 요청에는 해당 스킬만 사용합니다. Codex에서는 `$ig-plan`, `$ig-caption` 등으로 호출합니다.

## 기존 스킬과의 조합

| 필요 | 보조 스킬 | 경계 |
|---|---|---|
| 한국어 윤문 | `humanize-korean` | `ig-human`의 영어 점수를 한국어 품질이나 AI 작성 여부의 증거로 쓰지 않음 |
| 자료 조사 | `firecrawl-build-*`, 승인된 브라우저 도구 | 로그인·접근 권한과 최신성 확인은 별도. 없는 성과 수치를 만들지 않음 |
| 이미지·브랜드 시각물 | 설치된 ImageGen/PixVerse 등 | Instagram 문안 스킬이 실제 이미지를 자동 생성한 것으로 표시하지 않음 |
| 영상 제작 | `remotion-*`, HyperFrames, `ffmpeg-local`, `whisper` | 대본 작성과 영상 렌더·전사·실제 업로드를 구분 |
| 운영 데이터 | 연결된 Airtable/Notion/Sheets | 별도 계정·도구가 필요하며 스킬 설치만으로 연결되지 않음 |

ECC의 콘텐츠·브랜드·SNS 관련 스킬은 플러그인 제공 기능입니다. 같은 기능을 복제하거나 모든 SNS 작업에 함께 강제하지 않습니다. 이번 묶음은 Instagram 전용 초안·검토를 중심으로 합니다.

## 설치와 개인 자료

기본 `python -X utf8 install.py`는 활성 77개를 관리합니다. SNS 전체만 선택하려면:

```powershell
python -X utf8 install.py --skill ig-profile --skill ig-audit --skill ig-viral --skill ig-plan --skill ig-reel --skill ig-caption --skill ig-carousel --skill ig-story --skill ig-comment --skill ig-reply --skill ig-dm --skill ig-repurpose --skill ig-human
```

필요한 스킬만 골라도 매니페스트에 기록된 `ig-human` 의존성은 설치기가 함께 설치합니다. 각 스킬의 `assets/voice.md`는 빈 참고 양식이며 실제 계정 정보는 넣지 않습니다. 사용자 선택에 따라 `~/.codex/instagram/`에 말투·계획·사례를 보관할 수 있지만 공개 저장소에는 포함하지 않습니다. 기존 사용자 자료를 덮어쓰지 않습니다.

원본 Python 스크립트 6개는 표준 라이브러리 기반 로컬 도구입니다. 영어 어휘 점수·말하기 시간은 휴리스틱이며 한국어 정확도·성과·AI 탐지를 보장하지 않습니다. 설치된 스킬의 실제 절대 경로에서 실행합니다. 플랫폼 크기·제한·알고리즘 관련 주장은 필요할 때 최신 공식 자료로 확인합니다.

## 실행 범위

계정 로그인·Instagram API·게시 자동화는 포함하지 않습니다. 댓글·답글·DM 역시 초안이며, 실제 게시·전송·계정 변경에는 해당 행동에 대한 사용자의 지시와 지원되는 인증 도구가 필요합니다. 이번 작업에서 실제 계정 접근, 게시, 댓글 또는 메시지 전송을 수행하지 않았습니다.
