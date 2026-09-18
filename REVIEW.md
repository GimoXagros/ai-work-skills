# 전체 28개 관리 재확인 — 2026-09-19

원격 `main`의 `072ab53`을 확인했으며 활성 28개는 이미 `skills-lock.json`에 등록되어 있었습니다. 전문 13개도 별도 수동 설치 대상이 아니라 같은 설치기의 전체/선택 설치·업데이트·백업 대상입니다. 과거 2026-09-14 검토표의 “현재 15개” 문구를 당시 기록으로 정정하고, README와 [전체 관리 목록](docs/MANAGED_SKILLS.md)에 25개 번들 + 3개 고정 upstream 구성을 명시했습니다.

`install.py --list`에 매니페스트 기반 저장소 관리 총수와 선택된 항목 수를 구분하는 요약을 추가했습니다. 선택 설치의 의존성·은퇴 대체 항목을 포함한 수치와 설치하지 않는 목록 조회를 검증하는 회귀 검사도 추가했습니다. 목록은 저장소의 관리 범위를 표시하며 PC 설치 상태를 판정하는 명령은 아닙니다.

검증: 전체 49개 unittest PASS. 기존 캐시가 없는 임시 위치에 GitHub `main`의 `072ab53`을 새로 clone하고, 별도 설치 위치를 지정해 upstream 3개 다운로드를 포함한 28개 전체 설치 PASS. 설치된 이름 집합과 모든 파일 SHA-256 inventory가 각각 고정 원본과 일치했고, 오프라인 재설치 28개 모두 CURRENT였습니다. 로컬도 동일 원본과 일치하며 재설치 결과 직접 설치 27개 CURRENT + 동일 pin 플러그인 1개 CURRENT입니다. 플러그인 내용 비교는 파일 집합과 LF/CRLF 정규화 후 전체 바이트를 비교했습니다. 원본 pin·스킬 구현·은퇴/백업 정책은 이번 정정에서 변경하지 않았습니다.

# Main release verification — 2026-09-19

Fetched `origin` before integration: remote `main` remained at `06badc7e4b6f6f7f1f2bfde4ec0c23b2ae8a8efc`, with no divergent commits. Fast-forwarded local `main` through `21fb703` (13 emulator skills) and `d2ed83b` (log-analyzer v3), retaining the existing history. Updated the installation guide and release notes for main delivery. The feature-development records below describe their original delivery state.

Final checks on the integrated checkout: 48 unittest tests PASS; all 25 bundled skill format validators PASS; full offline installation, repeated installation and isolated glyph dependency setup PASS. All 28 active entries match their pinned sources: 27 direct installations match SHA-256 file inventories; the existing create-kr-patch plugin matches the pinned revision and complete file content after newline normalization. Its original byte inventory is unchanged.

Local synchronization replaced log-analyzer v2 content with v3; 22 other replacements only synchronize LF/CRLF byte differences. All 23 replaced directories have exact prior-inventory backups under `~/.codex/skill-backups/20260918T153829*Z/` (UTC timestamps; September 19 in Korea). System skills, unrelated local skill files and the existing kr-patch plugin byte inventories remain unchanged. A second full installation reports every entry CURRENT, including plugin reuse. No installer, setup script, source pin or retirement policy was changed for this release. Package/install validation does not establish live implicit skill selection or real emulator/hardware correctness.

# Log analyzer v3 review — 2026-09-19

## Initial audit and plan

Started on clean `feat/emulator-development-skills` at `21fb703f510d664008a3f973b0da9cac07b2bc22`; remote tracking matched after fetch. Baseline: 28 active skills, log-analyzer bundled/custom 2.0.0, 43 tests PASS. Work branch `feat/log-analyzer-v3` is based on that checkout and includes the previous emulator suite; main is not changed or merged.
Read the log skill, manifest, installer/setup, tests, README/REVIEW, release convention and .gitignore before changing implementation. Existing installer supports bundled directories with references, backed-up replacement and inventory checks without modification.

v2 described general application/build/test/operational log triage without Fractary/Bash assumptions. Its workflow was narrow inventory → format parsing → first failure timeline → normalized groups → correlation → evidence/interpretation separation → healthy-window comparison. Modes covered incident, errors, patterns, builds/tests and sessions. Output required location, count/time range, component, confidence, next check and limits. Read-only input, untrusted embedded instructions, redaction, malformed-record accounting and minimal quotations are retained in v3.

Plan: review external source/licenses and decide adoption → write v3 workflow and focused references → extend package/install regression tests → independent synthetic analysis → actual install/backup/inventory verification → final diff/commit/push. The adoption table was completed before implementation. The scope needs context-dependent format/clock/anchor choices; no repeated fixed-schema workload justified a generic parser. Therefore no helper script or new runtime dependency is added. The skill provides a reproducible procedure, not a newly implemented automatic parsing engine.

## Reviewed external projects

Read-only source snapshots were downloaded outside the repository for inspection; they were not executed, installed, vendored or copied into the skill. Commit times below are upstream history timestamps, not promises of maintenance. Repository metadata reported all four repositories unarchived at review; this does not establish support or correctness. Full source/license links identify reviewed revisions.

| Project | Useful concepts | Not useful for this task | License | Adopt? | Reason |
|---|---|---|---|---|---|
| djm81/log_analyzer_mcp | Scoped search, context extraction, content/time filters | Mandatory MCP/daemon, project test/coverage runner and client configuration | MIT + Commons Clause v1.0 | Concepts only; optional future integration | Extra runtime/configuration and license restriction unnecessary for a standalone skill |
| microsoft/log_analyzer | Good-log comparison, signatures, scoped whitelist, source-tagged multi-log views | Broad address/value stripping, guessed clock repair, local LLM/ADO/GPU/BMC/CPER/HTML workflows | MIT | Concepts adapted; project not vendored | Preserve semantic evidence and avoid domain/runtime coupling |
| tstack/lnav | Human navigation, filtering, merge views, SQLite exploration | Required viewer installation or trusting inferred chronology | BSD-2-Clause project license | Optional helper only | Useful for volume; core analysis must work without it |
| faultline-cli/faultline | Evidence-bearing known-pattern classification and explicit unmatched results | Bundled CI catalog as an emulator oracle; extra executable/runtime | MIT | Design reference only | No need to import a classifier; matches remain hints |

### djm81/log_analyzer_mcp

Reviewed default-branch HEAD [`3ca9c8f6f653c23ac050889af27778015a6a77f6`](https://github.com/djm81/log_analyzer_mcp/tree/3ca9c8f6f653c23ac050889af27778015a6a77f6), committed 2025-06-08. Last repository push reported 2025-06-08. The inspected default branch shows no newer commit at review, not proof the project is abandoned.

Actual source: [analysis_engine.py](https://github.com/djm81/log_analyzer_mcp/blob/3ca9c8f6f653c23ac050889af27778015a6a77f6/src/log_analyzer_mcp/core/analysis_engine.py), CLI `src/log_analyzer_client/cli.py`, server `src/log_analyzer_mcp/log_analyzer_mcp_server.py`, pytest parser and config loader. CLI exposes all/time/first/last searches; engine applies regex/content/level filters and file-local before/after context. Time filtering uses relative minutes/hours/days against local now; parser handles a particular datetime format and drops comma milliseconds. These are not a general multi-clock alignment solution. File/line metadata and bounded context are useful concepts.

MCP exposes search and pytest analysis plus subprocess-backed test/unit-test and coverage operations. Coverage generates reports via Hatch/coverage; this is executable project automation, not pure read-only log inspection. Configuration reads environment/.env values for directories, patterns, scopes and context. `pyproject.toml` declares Python >=3.10 (README says 3.9+), Click/Pydantic/dotenv/dateutil/Rich/MCP and other packages; development adds pytest/Hatch/coverage. Source uses portable path/subprocess APIs in places, but inspected CI runs Ubuntu Python 3.12 only; Windows support was not execution-tested here. README/configuration placeholders and differing entrypoint/version descriptions make source-level checks necessary.

[LICENSE.md](https://github.com/djm81/log_analyzer_mcp/blob/3ca9c8f6f653c23ac050889af27778015a6a77f6/LICENSE.md) is MIT plus Commons Clause v1.0, not unmodified MIT: the additional condition restricts selling the software as defined there and requires retaining its notice when applicable. No code is copied, so this change does not relicense or distribute that project. Any future optional MCP integration needs separate runtime/configuration/license review; none is installed now.

### microsoft/log_analyzer

Reviewed default-branch HEAD [`bd61d728cc5b54a0b276ec9dd7afd1988c25c406`](https://github.com/microsoft/log_analyzer/tree/bd61d728cc5b54a0b276ec9dd7afd1988c25c406), committed 2026-01-15 UTC. Repository push metadata is later (2026-02-06); it is not the default-branch commit date. [LICENSE](https://github.com/microsoft/log_analyzer/blob/bd61d728cc5b54a0b276ec9dd7afd1988c25c406/LICENSE) is MIT.

Inspected [common/lib_log.py](https://github.com/microsoft/log_analyzer/blob/bd61d728cc5b54a0b276ec9dd7afd1988c25c406/common/lib_log.py), CLI, `sut/settings.sample.json` and requirements. Good-log processing normalizes and fuzzily compares candidate lines against baseline lines; some reporting paths call a configured LLM and write normalized sidecars. An unordered similarity threshold can miss order/count differences. v3 instead preserves ordered structural anchors and missing/inserted events.

Signature configuration has match type, file scope, error/pass text and whitelist fields. Text matching uses configured inclusion/exclusion strings; these concepts inform optional hints, not root-cause rules. `normalize_log_line` removes several hardware values and hex addresses; v3 does not inherit those transformations. `recalculate_timestamps` assigns corrected values to some 1970/2000 records from later timestamps; v3 never adopts guessed timestamps. Source-tagged merge and JSON/XML-to-CSV handling inform format/clock intake, without assuming conversions preserve all structure. Reports include line differences and summaries, but successful fuzzy matching is not adopted as an anomaly-free verdict.

**concepts adapted; project not vendored**. All new text is independently written. No Microsoft regex, code, signature catalog or report template is copied. Local LLM, Azure DevOps, GPU/server hardware, BMC SEL, CPER and HTML features are excluded; no external license notice obligations are introduced by copied implementation because none is included.

### GitHub log-analyzer ecosystem

Reviewed the [topic index](https://github.com/topics/log-analyzer) as discovery, not an authority on correctness/license. The fetched topic page did not expose lnav/faultline entries, so their primary repositories were reviewed separately. “faultline” is ambiguous; this review explicitly selects the CI log tool `faultline-cli/faultline`, not similarly named Rails/security projects.

[lnav README](https://github.com/tstack/lnav), [official docs](https://docs.lnav.org/en/latest/intro.html) and [LICENSE](https://github.com/tstack/lnav/blob/master/LICENSE) document navigation/filtering/time views/SQLite and the BSD-2-Clause project license. Releases are documented for Linux/macOS/Windows, but no binary was installed or tested. Package/dependency licenses must still be checked for any future redistribution. It remains optional; format recognition cannot resolve absent clock evidence.

[Faultline revision `01038450447fd8f66f40fca65e43b168c4cec612`](https://github.com/faultline-cli/faultline/tree/01038450447fd8f66f40fca65e43b168c4cec612), committed 2026-06-05 UTC, has an [MIT LICENSE](https://github.com/faultline-cli/faultline/blob/01038450447fd8f66f40fca65e43b168c4cec612/LICENSE). Inspected `internal/matcher/matcher.go` and `internal/engine/analyzer.go`: explicit patterns/ranking, evidence collection and unmatched/input error states support a bounded classifier. Its confidence/ranking and CI catalog are not adopted. No executable, Go dependency or playbook is added.

## v3 design and quality audit

| Question | Decision/evidence |
|---|---|
| v2 behavior preserved? | First failure/timeline, grouping/counts, correlation, healthy windows, evidence separation, redaction/read-only/malformed reporting and minimal quotes retained explicitly |
| Baseline more than text diff? | Ordered phase/operation anchors, insertion/deletion/reordering, ambiguity and raw evidence recheck in comparison reference |
| Signatures confused with causes? | Hints only; scope/provenance, overlap counts and retained whitelist evidence |
| Normalization hides evidence? | Conservative default, documented opt-in transformations; addresses/opcodes/cycles preserved; correlation aliases keep joins |
| First ERROR confused with first divergence? | Separate output fields and synthetic before-ERROR mismatch |
| PC/log vs hardware evidence? | Explicit evidence categories, no hardware/fixed claim without appropriate confirming test |
| Standalone? | No scripts, mandatory MCP/LLM/service or package requirements |
| Emulator relevance? | GameYob SGB/link/CPU; GBARunner ARM/JIT/DMA/save; NitroSwan CPU/peripheral clock distinctions; names are routing hints, no invented log formats |
| Generic logs retained? | Application/web/server/operational plus build/test modes and generic record intake |
| Role overlap controlled? | Log evidence and bounded questions handed to installed specialists if available; no hard dependencies |

## Validation results

All requested checks completed on 2026-09-19 Asia/Seoul (backup timestamps use UTC).

| Command/check | Result | Evidence scope |
|---|---|---|
| skill-creator quick_validate | PASS | v3 YAML/name/frontmatter; Windows UTF-8 mode |
| python install.py --list | PASS | 28 active entries, log-analyzer present |
| python install.py --skill log-analyzer | PASS | v3 installed with prior v2 directory backed up |
| python install.py | PASS | all 28 current, including matching create-kr-patch plugin |
| python setup_tools.py | PASS | existing pinned glyph dependencies; no new v3 dependency |
| .venv Python -X utf8 -m unittest discover -s tests | PASS | 48 tests; original 43 plus 5 log-v3 packaging/install tests |
| --offline --skill log-analyzer, no cache/vendor | PASS | independent temporary checkout; repeat installation unchanged |
| original v2 backup | PASS | complete inventory equals pre-install snapshot |
| installed v3 | PASS | SKILL.md and both references match source inventory |
| other skills and protected directories | PASS | pre/post inventories equal; .system and kr-patch cache unchanged |
| manifest/policy preservation | PASS | other 27 entries, upstream pins, retired/unresolved unchanged |
| source preservation | PASS | installer/setup/vendor/retired/other bundled skills/old fixtures unchanged |
| git diff --check | PASS | final staged change set checked before commit |

Installed destination: `$CODEX_HOME/skills/log-analyzer`, resolved on this PC to `C:/Users/rlgh0/.codex/skills/log-analyzer`. Original v2 backup: `skill-backups/20260918T152200887948Z/log-analyzer` relative to Codex home. A final wording correction (count versus rate) also used the normal backup installer; the original v2 backup was verified independently. CLI listing does not print versions, so v3 is established by manifest 3.0.0 plus installed/source hash equality.

Baseline 43 tests passed before editing. New tests validate manifest v3, frontmatter/modes/references, offline selected installation without vendor/cache and backup/preservation. Existing 43 tests remain, with only the approved log version/note exception and non-frozen date in the historical emulator test. The old baseline fixture is unchanged.

Independent explicit-call synthetic evaluation read the skill and references and handled four cases: pre-ERROR copy timeout, address-bearing intermittent JIT logs with whitelist, incompatible clocks plus malformed/truncated input, and a failed CI attempt followed by pass plus instruction injection. It preserved semantic addresses, refused uncertain chronology/root-cause claims, retained retries/skips/counts and did not follow log instructions. This is qualitative behavior evidence, not automated parsing or hardware verification. Two cases overlap worked examples. An additional unseen NitroSwan repeated-poll/missing-record case correctly reported ambiguous alignment and capture uncertainty instead of declaring a V30MZ timing defect or proposing a skip-cycle patch. These five bounded examples do not establish general automatic-selection or parser correctness.

## Limitations

No real logs/ROMs were supplied for this upgrade. No emulator source, game assets or hardware was modified or executed. Actual GameYob/GBARunner3/NitroSwan compatibility, parser throughput, external tool Windows execution and real hardware correctness are NOT RUN. No helper parser exists, so automated normalization/divergence/encoding tests are not claimed. Installed bytes and skill-validator results can be checked; live implicit selection on arbitrary requests is separate from explicit synthetic evaluation.

## Prior review history

The following 2026-09-18 and 2026-09-14 records retain their original counts, versions and scope. Their statements about unchanged log-analyzer describe those earlier operations, not the v3 upgrade above.

# Emulator suite review — 2026-09-18

사용자 지정 manifest 검토일/릴리스 버전일: 2026-09-17. 실행일: 2026-09-18.
신규 13개 bundled/custom 1.0.0 추가로 활성 스킬은 28개, retired 2개입니다.
기존 15개 원본 항목·upstream pin·retired 정책을 변경하지 않았으며 기존 스킬 폴더, install.py, setup_tools.py, vendor, retired 구현도 수정하지 않습니다.

[전체 역할·의존성·중복·출처·프로젝트 감사](docs/EMULATOR_SKILL_AUDIT.md)와 [라우팅 예시](tests/fixtures/emulator-routing.json)를 함께 검토했습니다. 모든 13개 역할은 별도의 분석 단위를 갖고 기존 log/binary/ROM/font/frontend 도구는 조건부 보조로만 연결합니다. 신규 지침은 직접 작성했으며 외부 스킬이나 바이너리, ROM/게임 자산을 복사하지 않았습니다.

## 이번 실행 검증

| 검사 | 결과 | 실제 범위 |
|---|---|---|
| 변경 전 baseline | PASS | 31 tests |
| skill-creator quick_validate | PASS | 신규 13개 frontmatter/YAML/name/placeholder; Windows UTF-8 모드 |
| install.py | PASS | 기존 14 direct CURRENT + 동일 커밋 플러그인 CURRENT, 신규 13 INSTALLED |
| setup_tools.py | PASS | repository .venv의 pinned Pillow/fontTools, 전역 패키지 변경 없음 |
| .venv Python unittest discover | PASS | 43 tests (기존 31 + 신규 12; 선택 설치 13개 subcase 포함) |
| install.py --list | PASS | 활성 28개, 신규 13개 모두 표시; retired 2개 |
| cache 없는 bundled offline install | PASS | 25개 bundled skill, vendor/upstream cache 없는 임시 checkout |
| --skill 선택 설치 | PASS | 신규 13개 각각 temporary destination, 다른 사용자 파일 보존 |
| 기본 destination offline 재실행 | PASS | direct 27 CURRENT + plugin 1 CURRENT, replacement 없음 |
| 실제 local inventory | PASS | 신규 13개 source SHA-256 inventory와 일치; 기존 모든 local snapshot 그대로 |
| 기존 implementation preservation | PASS | git baseline 대비 기존 bundled source, installer/setup, vendor/retired 변경 없음 |
| .system / kr-patch plugin cache | PASS | 설치 전후 inventory hash 일치 |
| backup / retired / aliases / dependencies | PASS | 기존 통합 테스트 및 unknown user-owned code-review 보존 검사 |
| git diff --check | PASS | 신규 스킬·manifest·문서·tests 전체 변경 검사 |
| description routing 예시 | PASS (문서 검사) | 25개 합성 예시의 name 참조·범위·중복 검토; live 자동선택 아님 |
| 명시 호출 기반 독립 행동 검토 | PASS (합성 자료) | SGB OBJ, paired NiFi, ARM hicode 3사례; 추가 증거와 NOT RUN을 올바르게 유지 |
| 실제 Codex skill discovery / 암묵적 자동선택 | NOT RUN | 설치 파일 확인 완료; 현재 작업 context의 실시간 갱신을 확인할 수 없음 |
| DS/DSi/SGB/WonderSwan 실기·게임 호환성 | NOT RUN | 본 작업은 지침·설치·합성 검증에 한정 |

실행 명령은 Windows 인코딩 문제를 피하려고 Python `-X utf8`을 사용했습니다. 초기 validator의 cp949 읽기와 description의 YAML 콜론 문제를 수정한 뒤 최종 13개 모두 PASS했습니다. 최종 reread에서 ARM 해시 설명의 반복을 제거했고 설치기로 새 지침을 동기화했습니다. 이 refinement 이전 신규 ARM 지침은 installer의 정상 backup에 보존되었으며 기존 15개를 교체한 작업은 없습니다.
로컬 inventory snapshot은 ignored .cache에만 두고 자산·인증 정보는 기록하지 않았습니다. Codex UI 자동선택이나 실기 결과를 테스트 수에 포함하지 않았습니다.

## 해석 한계

파일·설치·합성 fixture 검사는 emulator core correctness 또는 hardware accuracy 검사가 아닙니다. PC tests / reference emulator observations / real hardware tests를 별도 기록하도록 지시합니다. 실제 DS/DSi, SGB 및 WonderSwan 실행과 copyrighted ROM 기반 테스트는 수행하지 않습니다. Codex discovery/자동선택/이미 실행 중 작업 적용은 재시작 또는 다음 턴에서 별도 확인해야 합니다.

## 이전 검토 기록 — 2026-09-14 기준

아래 내용의 15개/31개 숫자, 검토일과 upstream 최신성 판정은 그 당시 기록이며 이번 실행 결과를 의미하지 않습니다. create-kr-patch의 현재 제공 방식은 고정 upstream 또는 동일 커밋 플러그인 재사용으로 README에 명확히 기록했습니다.

# 과거 스킬 검토표 — 2026-09-14 당시 15개

확인일: **2026-09-14**

아래 표는 **2026-09-14 당시 15개 스킬**(은퇴 항목 2개 제외)의 기록입니다. 당시 구성은 고정된 외부 원본 3개와 저장소 번들 12개였습니다. 최신 매니페스트는 **28개 전체**를 관리하며, 현재 목록은 [전체 관리 목록](docs/MANAGED_SKILLS.md)을 기준으로 확인합니다.

## 교체 판정

| 이전 항목 | 현재 처리 | 근거 |
|---|---|---|
| `create-plan` | 설치 중단. 짧은 계획은 내장 `/plan`, 장기 다단계 작업은 `exec-plan` | 오래된 실험 패키지 대신 현재 Codex 계획 기능과 장기 실행 계획 스킬을 분리 사용 |
| `code-review` | 설치 중단. Codex 내장 `/review`로 대체 | 현재 Codex가 전용 리뷰어와 범위 선택을 제공하므로 OMX 독립 에이전트 의존 스킬이 불필요 |
| Fractary `log-analyzer` | 번들 `log-analyzer` 2.0으로 교체 | 원본이 보관 경로에 있고 Fractary 로그 형식과 Bash 스크립트에 결합되어 있어 범용·읽기 전용 절차로 대체 |

Codex 공식 문서는 `/review`가 전용 리뷰어를 실행해 변경 없이 우선순위화된 결과를 제공한다고 설명합니다. 스킬 자체는 여전히 지원되며, 공식 예시에도 장기 작업용 Exec Plan이 포함됩니다.

## 2026-09-14 당시 설치 목록

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
