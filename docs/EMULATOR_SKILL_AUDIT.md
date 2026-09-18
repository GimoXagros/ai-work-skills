# Emulator skill audit

매니페스트/릴리스 검토일 표기는 사용자 지정 2026-09-17이며 실제 감사·작성·검증 수행일은 2026-09-18입니다.
기준: clean main `06badc7e4b6f6f7f1f2bfde4ec0c23b2ae8a8efc`, origin/main과 동일. 변경 전 31개 테스트 PASS.

## 기존 15개 역할과 의존성

source 미기재 항목은 현재 설치기의 upstream 다운로드 방식입니다. adaptation의 upstream 정보는 출처이며 필수 실행 의존성을 의미하지 않습니다. version 미기재 항목에 가상 버전을 부여하지 않았습니다.

| canonical name | requested_name | source | status | version | requires | upstream / runtime | 역할·신규 스킬 경계 |
|---|---|---|---|---|---|---|---|
| exec-plan | exec-plan | bundled | custom | 1.0.0 | 없음 | 없음 | 장기 작업 계획·체크포인트; 에뮬레이터 판정 규칙 없음 |
| deep-interview | deep-interview | upstream 다운로드 | current | manifest 미기재 | 없음 | Yeachan-Heo/oh-my-codex@cb955b0d5becbef76d2c1f0096b6e1f238e1e7f7; OMX 확장 기능은 OMX runtime 필요 | 요구사항 모호성 해소; CPU·하드웨어 분석을 대신하지 않음 |
| frontend-testing-debugging | frontend-testing-debugging | upstream 다운로드 | current | manifest 미기재 | 없음 | openai/plugins@1dc195897af4161d039b80d8471ec0a10c9bbc89; Browser 또는 프로젝트 Playwright 환경 | 브라우저 UI QA; guest BG/OBJ·DS VRAM 디버깅과 다름 |
| log-analyzer | log-analyzer | bundled | custom | 2.0.0 | 없음 | 없음 | 로그 타임라인·최초 오류 정리; ISA/장치 기대값을 정의하지 않음 |
| create-kr-patch | create-retro-game-kr-patch | upstream 다운로드 | current | manifest 미기재 (plugin 3.2.0) | 없음 | mcpads/create-retro-game-kr-patch@56b31cc138926d769de97820df76e11beec6abb0 | 한글화 제품·텍스트 엔진 통합; 에뮬레이터 코어 회귀 전문성 별도 |
| akm-workflow | akm-workflow | bundled | adapted | 1.0.0 | 없음 | DECK6/akm@f26ace2a16caba724b24db12cbee238ebb52498f | 기존 AKM 지식 라우팅·Learn Back; 장치 분석을 대신하지 않음 |
| gba-pointer-fixer | gba-pointer-fixer | bundled | custom | 1.0.0 | 없음 | 없음 | ROM 내부 포인터; JIT 캐시·save persistence와 다름 |
| binary-re | binary-parser | bundled | adapted | 1.1.0 | 없음 | 2389-research/binary-re@42aee9063f3f3d52616700df3aa16df82b848604 | 실행 바이너리 triage·역공학; 알려진 CPU의 상태 비교와 다름 |
| image-glyph-generator | image-glyph-generator | bundled | custom | 1.0.0 | 없음 | 없음; Pillow/fontTools | 고정 셀 글리프 rasterization; 렌더러 pipeline과 다름 |
| encoding-mapper | encoding-mapper | bundled | custom | 1.0.0 | 없음 | 없음 | ROM 텍스트 인코딩; guest 버스 주소 decode와 다름 |
| nftr-font-editor | nftr-font-editor | bundled | custom | 1.0.0 | 없음 | 없음 | NFTR 구조·글자폭; DS VRAM pipeline과 다름 |
| ws-tile-compressor | ws-tile-compressor | bundled | custom | 1.0.0 | 없음 | 없음 | raw tile packing·dedup; WS 하드웨어 구현과 다름 |
| retro-font-allocator | retro-font-allocator | bundled | custom | 1.0.0 | 없음 | 없음 | 글리프 메모리 예산; BG/OBJ priority 분석과 다름 |
| script-translator-limiter | script-translator-limiter | bundled | custom | 1.0.0 | encoding-mapper | 없음 | 텍스트 길이·제어코드; emulator compatibility와 다름 |
| re | hex-analyzer | bundled | adapted | 1.1.0 | 없음 | vgrichina/re-skill@64c3bffb54ae4b9d99804a03fa4f179f4dd080c5 | ROM/bank/machine-code 조사; 코어 테스트·장치 판정 절차 별도 |

## 신규 13개 독립성 판정

모두 자체 작성 bundled/custom 1.0.0입니다. 기존 15개의 metadata·upstream pin·파일 의미·retired 정책은 보존합니다. 기존 기능만으로 완전히 대체되는 후보는 없었습니다. 겹치는 자료를 보조로 사용하는 경우에도 주 분석 단위를 분리했습니다. 스킬 이름이나 프로젝트 이름만으로 전체 작업에 무조건 적용하지 않고 description의 증상·작업 유형으로 선택합니다.
installer와 setup_tools는 수정하지 않습니다. 새 스킬에는 실행 파일, 바이너리, 필수 runtime, requires 항목이 없습니다. 보조 스킬 언급은 조건부이며 설치 의존성을 만들지 않습니다. 기존 script-translator-limiter → encoding-mapper 의존성만 유지됩니다.

| 신규 스킬 | 주 분석 단위 | 기존/다른 신규 스킬과 경계 |
|---|---|---|
| emulator-regression-tester | 기능별 before/after matrix | log triage나 특정 opcode 원인 분석과 다름 |
| cpu-isa-differential-analyzer | architectural state/ISA divergence | binary decoding·JIT 주소/캐시 수명과 다름 |
| timing-interrupt-dma-analyzer | event timestamp/order | ISA 값·로그 그룹 대신 scheduler 인과관계 |
| git-bisect-regression-debugger | 확인된 good/bad commit boundary | 일반 review·기능 matrix와 다름 |
| nds-homebrew-build-validator | toolchain/link/header/package | runtime compatibility나 global version upgrade와 다름 |
| graphics-vram-pipeline-debugger | guest→host render/transfer/composition | browser frontend·raw tile codec·font budgets와 다름 |
| save-nvram-state-validator | device/file/state persistence round trip | ROM pointer·mapper bus decoding과 다름 |
| cartridge-mapper-peripheral-analyzer | address decode/device state machine | host save serialization과 다름 |
| sgb-host-debugger | SGB packet→host CPU/audio/composition | 일반 GB CPU·NiFi serial과 다름 |
| gb-link-nifi-debugger | paired guest serial→transport correlation | SGB JOYP command protocol과 다름 |
| arm7-arm946-jit-analyzer | GBARunner translation/mapping/cache/abort | generic ISA comparison·ROM pointer repair와 다름 |
| v30mz-cpu-analyzer | model-specific V30MZ CPU vectors | generic x86·Sphinx device behavior와 다름 |
| wonderswan-hardware-analyzer | model-specific peripheral integration | V30 opcode semantics·raw tile compression과 다름 |

## 읽기 전용 프로젝트 근거

다음은 검사 시점의 체크아웃을 읽은 결과입니다. 세 프로젝트를 빌드하거나 수정하지 않았고 ROM을 읽거나 복사하지 않았습니다. 동시 진행 작업이 있을 수 있으므로 이후 HEAD가 바뀌더라도 이 표는 감사 시점 snapshot입니다.

| 프로젝트 | 검사 시점 HEAD | 확인한 경계 |
|---|---|---|
| GameYob-Publish | `1e36db0de67f0b6e4eda732535a422e83804a347` | BUILDING.md, DS CI, docs/features/sgb-host-coverage.md, sgb_protocol/host 및 nifi_protocol 테스트. 65C816 dispatch coverage는 completeness 증거가 아니며 SPC700/DSP·OBJ final composition의 미구현 범위를 구분. |
| GBARunner3-custom | `504a2d67177d6e4432c51addfeabaa07b9996654` | README, CI, bootstrap 및 ARM9 core/JIT 경로. direct/replaced execution, hicode mapping, cache/MPU 및 RTC/save adapter 경계를 분리. 낡은 release docs 대신 유지되는 build docs 우선. |
| NitroSwan-0.7.7 | `a3fa3363a040c5e2baad6aa9a08e5dec026cd0e5` | gitmodules, ARMV30MZ/README, Sphinx/README와 cartridge/EEPROM 모듈. V30MZ CPU·Sphinx SoC·저장장치 경계 및 core에서 선언한 semantic/timing 제약을 분리. |


## Source provenance와 안전성

신규 스킬은 원본 지침 작성이며 외부 스킬/코드/매뉴얼을 복사하지 않았습니다. 외부 프로젝트의 공식 스킬로 표시하지 않습니다. 아래는 모델·프로토콜·도구 기대값을 조사할 때 찾아볼 primary reference이며, 링크만으로 모든 명세가 검증되었다고 주장하지 않습니다.

- [Git bisect 공식 문서](https://git-scm.com/docs/git-bisect): classifier, skip, ambiguous boundary, reset.
- [BlocksDS 문서](https://blocksds.skylyrac.net/docs/): 프로젝트 CI/Makefile에 맞춘 toolchain·ARM7/ARM9 build 조사.
- [Pan Docs SGB packets](https://gbdev.io/pandocs/SGB_Command_Packet.html), [GB serial](https://gbdev.io/pandocs/Serial_Data_Transfer_(Link_Cable).html): JOYP packet boundary와 guest serial state. 웹 본문은 접근 제한으로 동일 upstream Markdown 원문을 읽었습니다. NiFi transport 명세는 GameYob 코드에서 별도로 확인해야 합니다.
- [GBARunner3](https://github.com/Gericom/GBARunner3), [ARM documentation index](https://developer.arm.com/documentation/): guest/host 모델별 문서를 구분. Arm 상세 매뉴얼 본문을 이번 감사에서 검증하지 못했으므로 특정 instruction edge behavior를 새 명세로 만들지 않았습니다.
- [NitroSwan](https://github.com/FluBBaOfWard/NitroSwan), [ARMV30MZ](https://github.com/FluBBaOfWard/ARMV30MZ), [Sphinx](https://github.com/FluBBaOfWard/Sphinx): 구현 경계와 선언된 제약. README implementation caveat를 하드웨어 명세로 취급하지 않습니다.

저작권 ROM·게임 데이터·테스트 ROM·실행 바이너리는 추가하지 않습니다. 사용자 ROM 원본은 read-only 보존하며 해시만 기록하도록 모든 entrypoint에 명시합니다. source/baseline/candidate/first divergence, 최소 수정, 무관한 정리 금지, test 없는 fixed 주장 금지, PC/reference/real hardware 구분, unsupported behavior 명시 원칙을 공통 보존합니다.

## 프로젝트별 합성 라우팅 검토

아래는 description과 workflow를 대조한 문서 수준 예시입니다. [JSON fixture](../tests/fixtures/emulator-routing.json)의 참조·중복·범위 검사는 자동화하지만 실제 Codex UI의 암묵적 선택을 실행한 결과가 아닙니다. 보조 스킬은 해당 원인이 드러날 때만 읽습니다.

| 프로젝트 | 요청/증상 | 주 스킬 | 조건부 보조 | 경계 |
|---|---|---|---|---|
| GameYob | SGB DATA transfer accepted but host DSP output fails | sgb-host-debugger | cpu-isa-differential-analyzer | Protocol → host/SPC/DSP boundary; not ordinary GB CPU or browser QA. |
| GameYob | SM83 opcode changes carry flag for a minimal vector | cpu-isa-differential-analyzer | 없음 | Guest architectural state; not SGB packet handling. |
| GameYob | MBC bank register selects wrong ROM window | cartridge-mapper-peripheral-analyzer | re | Bus decoding; not ROM pointer repair. |
| GameYob | Two link peers diverge after a reordered NiFi packet | gb-link-nifi-debugger | timing-interrupt-dma-analyzer | Correlate guest serial and transport separately. |
| GameYob | OBJ/window priority corrupts a stable scanline | graphics-vram-pipeline-debugger | 없음 | Pixel → renderer/register trace; not web frontend layout. |
| GameYob | Audio underrun coincides with changed timer IRQ ordering | timing-interrupt-dma-analyzer | 없음 | First scheduled event divergence, not guessed DSP semantics. |
| GameYob | Compatibility audio/graphics matrix changed after a core patch | emulator-regression-tester | log-analyzer | Before/after functional coverage; no fabricated game outcomes. |
| GameYob | Confirmed passing/failing revisions need first bad commit | git-bisect-regression-debugger | emulator-regression-tester | Verify endpoints and deterministic predicate before searching. |
| GBARunner3 | ARM7 guest vs ARM946 host LDM state differs | cpu-isa-differential-analyzer | arm7-arm946-jit-analyzer | Architectural semantics first; translation is conditional. |
| GBARunner3 | Thumb hicode fails after relocation and cache reuse | arm7-arm946-jit-analyzer | binary-re | Translation/mapping/cache ownership, not ROM-internal pointers. |
| GBARunner3 | BG palette is stale in final DS framebuffer | graphics-vram-pipeline-debugger | 없음 | Separate guest palette from host display transfers. |
| GBARunner3 | DMA transfer completion and IRQ service order changed | timing-interrupt-dma-analyzer | 없음 | Request/completion/service timestamps, not build log grouping. |
| GBARunner3 | Timer IRQ serviced at the wrong guest cycle | timing-interrupt-dma-analyzer | 없음 | Guest clock units and interrupt masks must be traced. |
| GBARunner3 | EEPROM/SRAM/Flash data lost after process restart | save-nvram-state-validator | cartridge-mapper-peripheral-analyzer | Persistence round trip; device selection only when implicated. |
| GBARunner3 | ARM9 linker fails under project CI toolchain | nds-homebrew-build-validator | log-analyzer | Use project CI version, not an arbitrary global upgrade. |
| GBARunner3 | Verified game boot regression starts between two revisions | git-bisect-regression-debugger | emulator-regression-tester | Commit boundary isolation; no source history rewrite. |
| NitroSwan | V30MZ divide/prefix/segment vector differs in flags | v30mz-cpu-analyzer | 없음 | Model-specific CPU semantics; x86 is not a hardware oracle. |
| NitroSwan | V30MZ instruction cycle validation vector fails | v30mz-cpu-analyzer | timing-interrupt-dma-analyzer | CPU cycles first; peripheral scheduling conditional. |
| NitroSwan | Sphinx DMA request precedes a scanline IRQ unexpectedly | timing-interrupt-dma-analyzer | wonderswan-hardware-analyzer | Ordered event evidence with WonderSwan model authority. |
| NitroSwan | Color sprite/window hardware-test signature differs | wonderswan-hardware-analyzer | graphics-vram-pipeline-debugger | Guest model/register behavior; not raw tile compression. |
| NitroSwan | Cartridge RTC register latch sequence fails | cartridge-mapper-peripheral-analyzer | wonderswan-hardware-analyzer | Cartridge protocol rather than clock-file persistence. |
| NitroSwan | Internal EEPROM content not restored after restart | save-nvram-state-validator | wonderswan-hardware-analyzer | Persistence; distinguish internal and cartridge EEPROM. |
| NitroSwan | ROM cartridge bank window decoded incorrectly | cartridge-mapper-peripheral-analyzer | wonderswan-hardware-analyzer | Cartridge address decoding, not V30MZ instruction semantics. |
| NitroSwan | WonderSwan serial register completion differs by model | wonderswan-hardware-analyzer | timing-interrupt-dma-analyzer | WS peripheral, not GB NiFi or generic wireless setup. |
| NitroSwan | NDS build regression leaves missing ARM7 output | nds-homebrew-build-validator | git-bisect-regression-debugger | Build artifact first; bisect only after endpoints confirmed. |


## 검증 범위와 제한

테스트는 manifest preservation, dependency/name uniqueness, required structure/guard concepts, cache 없는 bundled offline install, 각 신규 스킬 선택 설치, --list, README count 및 합성 라우팅 참조를 검사합니다. 기존 전체 설치·backup·retired·alias·dependency와 포인터/인코딩/타일/폰트/번역 helper 테스트도 유지됩니다. 실제 결과는 REVIEW.md에 기록합니다.
실제 게임 호환성, CPU 정확도, DS/DSi boot, 실기 NiFi, SGB DSP와 WonderSwan 주변장치 실행은 이번 작업에서 검증하지 않습니다. Codex 자동선택/이미 실행 중 작업 적용 여부는 파일 설치만으로 증명할 수 없습니다. 새 턴/재시작 후 확인이 필요합니다.
