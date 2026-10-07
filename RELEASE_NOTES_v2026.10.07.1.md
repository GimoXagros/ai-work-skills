# v2026.10.07.1

- humanize-korean 추가: 한국어 AI 문체 진단·윤문, 의미·수치·인용 보존 검사.
- epoko77-ai/im-not-ai v2.3.2 / 2f3d943d08056b612a92e12bfb72ea94dd2acd18, MIT 라이선스 보존.
- Codex 전용 엔트리포인트와 독립 실행 런타임을 패키징하고 Windows 참조 경로 및 Python 호출 조정.
- 활성 30개(번들 27개, 고정 upstream 3개), 은퇴 2개, unresolved 0개.
- 기존 외부 원본 7개 점검: 변경된 저장소에서도 대상 스킬 내용은 동일하여 기존 고정 커밋 유지.
- main의 글리프 도구 의존성 업데이트 포함.
- README, REVIEW, 전체 관리 목록과 설치 테스트 목록 갱신.

설치: python -X utf8 install.py
도구 갱신: python -X utf8 setup_tools.py
목록: python -X utf8 install.py --list

새 스킬은 다음 Codex 턴에서 사용할 수 있습니다. 목록이 갱신되지 않으면 새 작업을 열거나 앱을 다시 시작합니다.

검증: skill-creator validator PASS, 저장소 unittest 49개 PASS, 설치된 독립 런타임의 한국어 입력 준비·변경률·보존 게이트·서법 복원 smoke PASS, install.py 설치 지문 검사 PASS, install.py --list 30 active / 2 retired / Unresolved 없음, git diff --check PASS. 실제 LLM 윤문과 암묵적 자동 선택은 미실행.
