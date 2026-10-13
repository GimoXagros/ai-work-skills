# v2026.10.13.1

- kr-patch-qa, create-kr-patch-template, emucap을 Codex용 독립 번들 스킬로 추가.
- QA 원본은 설치 폴더 밖 표준을 참조하므로 고정 커밋의 문서로 연결합니다. 원본 문서를 재배포하지 않습니다.
- 템플릿과 emucap은 독립 SKILL.md가 없는 저장소여서 역할별 엔트리포인트를 작성했습니다. MCP/어댑터/게임 이미지 설치를 스킬 설치와 구분합니다.
- humanize-korean 원본 b37e0206d31fffd9149bf57168d4d62eb2086bee의 입력 처리·검증 갱신을 반영하고 Windows 독립 실행 보완을 유지합니다.
- 2026-10-11 main의 기존 스킬 및 글리프 의존성 갱신도 로컬에 동기화합니다.
- 활성 33개(번들 30개 + 고정 upstream 3개), 은퇴 2개, unresolved 없음.

설치: python -X utf8 install.py
도구: python -X utf8 setup_tools.py
목록: python -X utf8 install.py --list

스킬·설치 검사는 실제 게임 QA와 에뮬레이터 실행을 대신하지 않습니다.

최종 검사: 신규 3개와 humanize-korean validator PASS; unittest 49개 PASS; 설치된 humanize-korean 입력·변경률·보존·서법 smoke PASS; 전체 33개 오프라인 설치 지문 확인 완료; Unresolved 없음. fonttools 4.66.1 적용. 실제 게임 실행·QA·MCP 런타임 설치는 이번 작업 대상이 아닙니다.
