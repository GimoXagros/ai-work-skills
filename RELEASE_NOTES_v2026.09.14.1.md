# v2026.09.14.1

## 개요
- `ai-work-skills` 문서 정합성 정리 완료
- README/REVIEW를 현재 설치 상태 기준으로 정렬
- 실제 점검에서 `create-plan`, `code-review`는 은퇴 처리 정책에 따라 대체된 상태 반영

## 포함 변경
- `README.md`
  - 활성 스킬 집계를 **15개 스킬(은퇴 항목 2개 제외)** 기준으로 표기
  - `create-kr-patch` 안내를 플러그인 의존 설명에서 `install.py` 기준 번들/직접 설치 방식으로 수정
- `REVIEW.md`
  - 동일 기준(활성 15개/은퇴 2개 제외)으로 정렬
  - `create-kr-patch` 활성 상태 표기를 플러그인 중심 설명에서 번들/직접 설치 기준으로 수정

## 점검 상태
- `python .\ai-work-skills\install.py` 실행: `CURRENT` 항목으로 15개 스킬 모두 정상이었음
- `python .\ai-work-skills\install.py --list` 실행: 15개 설치 + 2개 퇴역 항목, `Unresolved` 없음

## 관련 커밋
- `67a7559` - docs(skills): align README and review with active inventory

## 태그
- `v2026.09.14.1`
