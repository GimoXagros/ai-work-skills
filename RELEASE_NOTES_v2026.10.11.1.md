# ai-work-skills v2026.10.11.1

30개 관리 스킬의 외부 원본을 재검토하고 최신 고정 커밋과 Codex 어댑터를 반영했습니다.

## 주요 변경

- 외부 원본 8개를 최신 HEAD까지 비교하고, 결과와 Git tree 근거를 문서화했습니다.
- create-kr-patch 3.4.0: 요청한 플레이스루 검증, 공유 글리프·표시 범위·제어 토큰 사례를 반영했습니다.
- deep-interview와 frontend-testing-debugging: 스킬 내용은 동일하며 원본 pin만 최신 커밋으로 갱신했습니다.
- akm-workflow 1.1.0: 선택적 레이어, 근거와 상태의 분리, 연결된 지식 갱신과 제한된 유지보수 지침을 반영했습니다. 원본 전체 스킬 묶음은 포함하지 않는 독립 어댑터입니다.
- free-llm-apis 1.0.0-codex.1: 오래된 무료 한도·모델명 단정을 제거하고 공식 문서 확인 절차와 환경변수 예제를 적용했습니다.
- fonttools 4.66.1 업데이트를 포함하며 Python 3.10용 4.65.0 고정을 유지합니다.

## 설치와 업데이트

```powershell
git clone --branch v2026.10.11.1 https://github.com/GimoXagros/ai-work-skills.git
cd ai-work-skills
python install.py
python setup_tools.py
```

기존 main 체크아웃은 `git pull --ff-only` 후 `python install.py`, `python setup_tools.py`를 실행합니다. 변경된 직접 설치 스킬은 자동 백업됩니다. 플러그인 캐시와 시스템 스킬은 수정하지 않습니다.

## 검증과 제한

- 전체 30개 새 설치 성공, 자동 테스트 49개 통과, pip check 정상.
- 외부 API 호출·결제 설정·게임 실기기 검증은 이 배포 검증에 포함하지 않습니다.
- 실행 중 작업의 이전 판단까지 소급 변경되지는 않습니다. 새 스킬이 보이지 않으면 작업을 다시 열거나 Codex를 재시작하세요.

[외부 원본 검토 기록](https://github.com/GimoXagros/ai-work-skills/blob/v2026.10.11.1/docs/UPSTREAM_REVIEW_2026-10-11.md) · [전체 관리 목록](https://github.com/GimoXagros/ai-work-skills/blob/v2026.10.11.1/docs/MANAGED_SKILLS.md)

스킬 메타데이터 검사: 29개 통과. deep-interview 원본의 `argument-hint` 필드 1건은 현재 범용 quick_validate 허용 키 목록에 없어 경고로 남깁니다. 이 필드는 이번 변경 전후 동일하며, 원본 보존을 위해 제거하지 않았습니다. 전체 설치와 로컬 30개 파일 해시 대조는 통과했습니다.
