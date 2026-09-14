# ai-work-skills

<p align="center">
  <img src="logo.png" alt="AI Work Skills logo" width="560">
</p>

현재 Codex 환경에서 사용하는 **15개 스킬**(은퇴 항목 2개 제외)을 동일한 버전으로 설치하는 공개 저장소입니다.
최종 점검일은 **2026-09-14**이며, 전체 판정과 제한 사항은 [REVIEW.md](REVIEW.md)에 정리되어 있습니다.

## 현재 설치되는 스킬

| 분류 | 스킬 |
|---|---|
| 계획·요구사항 | `exec-plan`, `deep-interview` |
| 품질·분석 | `frontend-testing-debugging`, `log-analyzer` |
| 지식 관리 | `akm-workflow` |
| 역공학·한글화 | `create-kr-patch`, `binary-re`, `re`, `gba-pointer-fixer`, `encoding-mapper`, `image-glyph-generator`, `nftr-font-editor`, `ws-tile-compressor`, `retro-font-allocator`, `script-translator-limiter` |

`create-plan`은 설치하지 않습니다. 짧은 계획은 Codex 내장 `/plan`, 장기 다단계 작업은 `exec-plan`을 사용합니다.
외부 OMX용 `code-review`도 설치하지 않습니다. 현재 Codex의 전용 `/review` 기능으로 대체합니다.
보관된 Fractary 원본의 `log-analyzer`는 특정 로그 구조와 Bash 의존성이 없는 번들 버전으로 교체했습니다.

## 설치

Git과 Python 3.10 이상을 준비합니다. 공개 저장소이므로 GitHub 로그인은 필요하지 않습니다.

```powershell
git clone https://github.com/GimoXagros/ai-work-skills.git
cd ai-work-skills
python install.py
python setup_tools.py
```

기본 설치 위치는 `$CODEX_HOME/skills`이며, 환경 변수가 없으면 `~/.codex/skills`입니다.
`setup_tools.py`는 글리프 생성에 필요한 Pillow와 fontTools를 저장소의 `.venv`에 설치합니다.
설치 후 목록이 바로 갱신되지 않으면 Codex를 다시 시작합니다.

다른 위치에 설치하려면 다음처럼 지정합니다.

```powershell
python install.py --dest "$env:USERPROFILE/.agents/skills"
```

## 업데이트

```powershell
git pull --ff-only
python install.py
python setup_tools.py
```

- 설치기는 [skills-lock.json](skills-lock.json)에 기록된 고정 커밋과 번들 스킬만 사용합니다.
- 같은 내용은 건너뛰고, 변경된 기존 스킬은 `skill-backups/<UTC 시각>/`에 보존합니다.
- 확인된 구형 `create-plan`과 OMX `code-review`만 안전하게 은퇴시키며, 사용자가 수정한 동명 스킬은 보존합니다.
- `.system`, 플러그인 캐시, 인증 정보, Codex 전체 설정은 변경하지 않습니다.
- 오프라인 재설치: `python install.py --offline`
- 목록 확인: `python install.py --list`
- 선택 설치: `python install.py --skill log-analyzer`

## 이름과 제공 방식

- `binary-parser`의 실제 설치 이름은 `binary-re`입니다.
- `create-retro-game-kr-patch`의 실제 설치 이름은 `create-kr-patch`입니다.
- `hex-analyzer` 요청은 실제 설치 이름 `re`로 연결됩니다.
- `create-kr-patch`는 현재 `install.py` 기준으로 번들/직접 설치 방식으로 관리됩니다.
- `deep-interview`의 기본 질문 흐름은 사용할 수 있지만 OMX 상태 저장과 자동 인계는 별도 OMX 런타임이 필요합니다.
- `frontend-testing-debugging`은 현재 브라우저 도구를 우선 사용하고, 허용된 경우 프로젝트 Playwright 환경으로 대체합니다.

## 검증 명령

검사가 필요할 때 다음 명령을 사용할 수 있습니다.

```powershell
python install.py
python setup_tools.py
.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -v
```

검사는 합성 데이터와 설치 동작을 대상으로 하며 실제 게임별 호환성을 보장하지 않습니다.

## 라이선스

외부 스킬은 각 원본의 라이선스와 이용 조건을 따릅니다. 다운로드 전용 원본은 이 저장소에서 재배포하지 않습니다.
`skills/binary-re`와 `skills/re`는 각 MIT 원본의 저작권 및 라이선스를 보존한 Codex용 수정본입니다.
`vendor/skill-installer`는 Apache-2.0 라이선스를 보존합니다.
직접 제작한 스킬은 OpenAI 또는 외부 프로젝트의 공식 배포물로 표시하지 않습니다.
