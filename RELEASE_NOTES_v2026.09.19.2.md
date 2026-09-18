# ai-work-skills v2026.09.19.2

## 개요

- 에뮬레이터 전문 스킬 13개와 `log-analyzer v3.0.0`을 포함해 **활성 스킬 28개 전체**를 관리합니다. 은퇴 항목 2개는 제외합니다.
- 모든 활성 스킬은 `skills-lock.json`과 동일한 설치기를 통해 설치·업데이트·선택 설치·변경 전 백업을 수행합니다.
- 기존 v2026.09.19.1의 내용을 이 릴리스에 통합했습니다.

## 포함 변경

- 기본 브랜치 `main`에 에뮬레이터 스킬 추가와 로그 분석 개선을 병합하고 다른 PC용 설치 안내를 갱신했습니다. 기존 커밋 이력을 보존했습니다.
- 관리 구성은 **저장소 번들 25개 + 고정 upstream 3개**입니다. 전문 스킬 13개도 별도 수동 설치 항목이 아닌 저장소 관리 대상입니다.
- `install.py --list`에 저장소 관리 총수와 선택된 항목 수를 구분해서 표시하도록 개선했습니다. 선택 수에는 필요한 의존성과 은퇴 스킬의 대체 항목이 반영됩니다.
- README와 [전체 관리 목록](https://github.com/GimoXagros/ai-work-skills/blob/main/docs/MANAGED_SKILLS.md)을 정리하고, 과거 문서의 “현재 15개” 표현을 2026-09-14 당시 기록으로 정정했습니다.
- `create-plan` → `exec-plan`, `code-review` → Codex 내장 `/review` 대체 정책을 유지합니다. 알려진 구형 원본만 백업 후 은퇴시키며 사용자 수정본은 보존합니다.

### 에뮬레이터 전문 스킬 13개

- 공통 8개: `emulator-regression-tester`, `cpu-isa-differential-analyzer`, `timing-interrupt-dma-analyzer`, `git-bisect-regression-debugger`, `nds-homebrew-build-validator`, `graphics-vram-pipeline-debugger`, `save-nvram-state-validator`, `cartridge-mapper-peripheral-analyzer`
- GameYob 2개: `sgb-host-debugger`, `gb-link-nifi-debugger`
- GBARunner3 1개: `arm7-arm946-jit-analyzer`
- NitroSwan 2개: `v30mz-cpu-analyzer`, `wonderswan-hardware-analyzer`

모두 자체 작성한 번들 스킬 1.0.0입니다. 실행 파일이나 새 런타임 의존성 없이 분석·검증 지침을 제공합니다. 스킬별 역할과 적용 범위는 [라우팅 감사 문서](https://github.com/GimoXagros/ai-work-skills/blob/main/docs/EMULATOR_SKILL_AUDIT.md)에 기록했습니다.

### log-analyzer v3.0.0

- 정상 실행과 실패 실행의 로그를 비교하고 구조를 맞춰 **최초 차이**를 추적하도록 개선했습니다.
- 기존의 근거 중심 분류, 오류 묶음, 시간순 분석, 정상 구간 비교, 민감 정보 가림 및 원본 읽기 전용 원칙을 유지합니다.
- 주소·값·시간·상관관계 등 의미 있는 정보는 보존하고, 정규화한 내용은 기록하도록 했습니다.
- 반복 오류 패턴과 제한된 허용 목록은 보조 단서로 사용합니다. 패턴 일치만으로 원인이나 정상 실행을 확정하지 않습니다.
- 여러 로그의 시계 불확실성, 여러 실행의 간헐적 실패, 빌드·테스트의 재시도·건너뜀·시간 초과·환경 차이를 구분하도록 했습니다.
- GameYob·GBARunner3·NitroSwan 전문 스킬로 필요에 따라 연결하며 일반 애플리케이션·서버 로그 분석도 지원합니다.
- 비교와 패턴 분류 참고 문서를 추가했습니다. 별도 자동 파서, MCP 서버, 외부 LLM, 상주 프로세스나 새 패키지 의존성은 추가하지 않았습니다.

djm81/log_analyzer_mcp(MIT + Commons Clause), microsoft/log_analyzer(MIT), lnav(BSD-2-Clause), faultline-cli/faultline(MIT)의 개념과 라이선스를 검토했습니다. 외부 구현이나 패턴 목록은 복사·재배포하지 않았습니다. 원본 커밋과 채택 판단은 [검토 기록](https://github.com/GimoXagros/ai-work-skills/blob/main/REVIEW.md)에 있습니다.

## 검증 결과

- 최종 자동 검사 **49개 통과**. 기존 통합 단계의 48개 검사에 관리 총수·선택 수·읽기 전용 목록 조회 회귀 검사 1개를 추가했습니다.
- 번들 스킬 25개 형식 검사, 전체·선택 설치, 글리프 도구 준비, 파일 목록·해시 및 백업 검사 통과.
- 기존 캐시 없이 GitHub `main`의 `072ab53`을 새로 받아 고정 upstream 다운로드를 포함한 **28개 전체 설치**를 확인했습니다. 모든 설치 파일의 해시가 고정 원본과 일치했고 오프라인 재설치에서도 28개 모두 CURRENT였습니다.
- 배포된 `71a26c0`으로 해당 새 체크아웃을 갱신한 뒤 관리 총수 표시와 28개 재설치 CURRENT를 다시 확인했습니다.
- 로컬은 직접 설치 27개와 동일 고정 커밋의 `create-kr-patch` 플러그인 재사용 1개가 CURRENT입니다. 플러그인 원본 내용은 줄바꿈 차이를 정규화해 비교했습니다. 변경된 기존 스킬은 백업하고 시스템 스킬·플러그인 캐시·관련 없는 사용자 파일은 보존했습니다.
- 별도로 합성 로그 사례 5개를 검토했습니다. 이는 자동 파서 검사나 실기 검증 횟수에 포함하지 않습니다.
- 스킬 원본의 고정 커밋과 은퇴·백업 정책을 유지합니다. 저작권 있는 ROM, 게임 자산, 임시 로그와 생성 바이너리는 포함하지 않습니다.

검증은 스킬 패키지와 설치 동작을 대상으로 합니다. 실제 게임·에뮬레이터·하드웨어 정확도 및 실행 중 작업의 자동 스킬 선택을 검증한 결과는 아닙니다. 목록 명령은 저장소 관리 범위를 표시하며 PC 설치 상태 판정을 대신하지 않습니다.

## 관련 커밋

- `21fb703` — 에뮬레이터 개발 스킬 13개 추가
- `d2ed83b` — log-analyzer v3.0.0 개선
- `072ab53` — main 배포 안내 및 최종 검증 기록
- `71a26c0` — 28개 전체 관리 범위 명시 및 목록 표시 개선
