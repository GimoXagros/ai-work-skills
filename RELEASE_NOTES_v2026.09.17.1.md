# v2026.09.17.1 — emulator development skills

사용자 지정 릴리스/검토일: 2026-09-17. 실제 작성·검증: 2026-09-18.

## Added
13개 original bundled/custom 1.0.0 스킬을 추가했습니다. 활성 manifest 수는 28개입니다.
- 공통 8개: emulator-regression-tester, cpu-isa-differential-analyzer, timing-interrupt-dma-analyzer, git-bisect-regression-debugger, nds-homebrew-build-validator, graphics-vram-pipeline-debugger, save-nvram-state-validator, cartridge-mapper-peripheral-analyzer.
- GameYob: sgb-host-debugger, gb-link-nifi-debugger.
- GBARunner3: arm7-arm946-jit-analyzer.
- NitroSwan: v30mz-cpu-analyzer, wonderswan-hardware-analyzer.

## Installer compatibility
Schema 2, installer와 setup_tools 구현을 유지합니다. 신규 스킬에는 필수 runtime이나 hard dependency가 없습니다. 기존 15개 항목, immutable upstream pins, retired 정책, inventory/staging/backup 및 link/destination/plugin protection을 보존합니다.

## Tests and documentation
Manifest baseline preservation fixture, 신규 entrypoint 구조·guardrails, unique name/alias 및 acyclic dependencies, 캐시 없는 bundled offline 설치, 신규 13개 각각 선택 설치, --list, README count, retired user-content 보존 검사를 추가했습니다. README의 8개 분류, REVIEW, 프로젝트별 역할·출처 감사 및 25개 문서 수준 라우팅 예시를 갱신했습니다. 43 tests와 신규 13개 quick_validate, 실제 local install/--list/재설치 및 inventory preservation이 PASS했습니다. 실제 검사 결과는 REVIEW.md를 참조합니다.

## Known limitations
설치/합성 검사는 실제 게임 호환성, CPU/hardware accuracy나 Codex UI 자동 선택을 보장하지 않습니다. 다음 턴 또는 Codex 재시작에서 discovery를 확인해야 합니다. 실제 DS/DSi, SGB, WonderSwan hardware test는 별도입니다. ROM/game assets/test ROM/binaries는 포함하지 않았으며 프로젝트 소스·ROM·.system·plugin cache·인증/전역 설정을 변경하지 않았습니다.

## Delivery
작업 브랜치: feat/emulator-development-skills. 검증 완료 후 해당 브랜치만 commit/push하며 main 병합은 수행하지 않습니다.
