# v2026.10.22.1

- Instagram 전용 ig-* 13개를 Codex용 수정 번들로 추가했습니다.
- 원본: Jakeschincariol/instagram-agent-skill, d03c56bb598be770c60b201f94237e5d1a4268a6, MIT. 각 폴더에 라이선스를 보존합니다.
- 경로를 ~/.codex/instagram으로 조정하고 명시 호출·Windows Python 절대경로 예시를 반영했습니다. 빈 voice 양식을 포함하며 개인 계정 자료는 저장소에 포함하지 않습니다.
- 게시·댓글·DM 초안과 실제 전송을 구분하고 한국어 윤문·영어 점수 도구의 한계를 명시했습니다.
- SNS 관리 문서에서 계획·조사·제작·응대·분석 및 기존 미디어/윤문/플러그인의 역할을 정리했습니다.
- 독립 관리 스킬 77개 = 번들 56개 + 고정 upstream 21개. 플러그인 5개·GSD 72개·은퇴 2개는 별도입니다.

설치: python -X utf8 install.py
SNS 묶음과 선택 설치: docs/SNS_SKILLS.md

Instagram 계정 연결·게시·메시지 전송 및 실제 SNS 성과 검증은 수행하지 않았습니다.

검증: 신규 13개 skill validator PASS, unittest 61개 PASS(6개 Python 엔트리포인트와 의존성/템플릿/라이선스 검사 포함), 전체 오프라인 설치·지문 확인 PASS, 목록 77 active / 2 retired / Unresolved 없음, git diff --check PASS. 기존 로컬 ig-* 13개는 설치기가 변경 전 백업했습니다. 계정 접근·게시·댓글·DM 전송·실제 SNS 성과는 미실행입니다.
