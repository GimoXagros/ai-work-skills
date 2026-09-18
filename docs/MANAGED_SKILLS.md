# 저장소 전체 관리 목록

기준: 2026-09-19, `main`의 `skills-lock.json`. 활성 **28개 전체**가 이 저장소의 기본 설치·업데이트 대상입니다. 기존 15개와 에뮬레이터 전문 13개를 별도 관리 집합으로 나누지 않습니다.

번들 25개는 이 저장소의 파일로 관리하고, upstream 3개는 매니페스트의 고정 커밋으로 관리합니다. 원본 최신 커밋을 자동 추종하지 않으며 검토 후 pin을 변경합니다. `create-kr-patch`도 관리 목록에 포함되며 동일 pin의 플러그인이 있으면 캐시를 수정하지 않고 재사용합니다. 직접 설치본과 플러그인 노출 수를 더해서 별개 스킬로 세지 않습니다.

| 실제 스킬 이름 | 관리 원본 | 버전 또는 고정 커밋 |
|---|---|---|
| `exec-plan` | `skills/exec-plan` | `1.0.0` |
| `deep-interview` | `Yeachan-Heo/oh-my-codex/skills/deep-interview` | `cb955b0d5becbef76d2c1f0096b6e1f238e1e7f7` |
| `frontend-testing-debugging` | `openai/plugins/plugins/build-web-apps/skills/frontend-testing-debugging` | `1dc195897af4161d039b80d8471ec0a10c9bbc89` |
| `log-analyzer` | `skills/log-analyzer` | `3.0.0` |
| `create-kr-patch` | `mcpads/create-retro-game-kr-patch/skills/create-kr-patch` | `56b31cc138926d769de97820df76e11beec6abb0` |
| `akm-workflow` | `skills/akm-workflow` | `1.0.0` |
| `gba-pointer-fixer` | `skills/gba-pointer-fixer` | `1.0.0` |
| `binary-re` | `skills/binary-re` | `1.1.0` |
| `image-glyph-generator` | `skills/image-glyph-generator` | `1.0.0` |
| `encoding-mapper` | `skills/encoding-mapper` | `1.0.0` |
| `nftr-font-editor` | `skills/nftr-font-editor` | `1.0.0` |
| `ws-tile-compressor` | `skills/ws-tile-compressor` | `1.0.0` |
| `retro-font-allocator` | `skills/retro-font-allocator` | `1.0.0` |
| `script-translator-limiter` | `skills/script-translator-limiter` | `1.0.0` |
| `re` | `skills/re` | `1.1.0` |
| `emulator-regression-tester` | `skills/emulator-regression-tester` | `1.0.0` |
| `cpu-isa-differential-analyzer` | `skills/cpu-isa-differential-analyzer` | `1.0.0` |
| `timing-interrupt-dma-analyzer` | `skills/timing-interrupt-dma-analyzer` | `1.0.0` |
| `git-bisect-regression-debugger` | `skills/git-bisect-regression-debugger` | `1.0.0` |
| `nds-homebrew-build-validator` | `skills/nds-homebrew-build-validator` | `1.0.0` |
| `graphics-vram-pipeline-debugger` | `skills/graphics-vram-pipeline-debugger` | `1.0.0` |
| `save-nvram-state-validator` | `skills/save-nvram-state-validator` | `1.0.0` |
| `cartridge-mapper-peripheral-analyzer` | `skills/cartridge-mapper-peripheral-analyzer` | `1.0.0` |
| `sgb-host-debugger` | `skills/sgb-host-debugger` | `1.0.0` |
| `gb-link-nifi-debugger` | `skills/gb-link-nifi-debugger` | `1.0.0` |
| `arm7-arm946-jit-analyzer` | `skills/arm7-arm946-jit-analyzer` | `1.0.0` |
| `v30mz-cpu-analyzer` | `skills/v30mz-cpu-analyzer` | `1.0.0` |
| `wonderswan-hardware-analyzer` | `skills/wonderswan-hardware-analyzer` | `1.0.0` |

## 관리 절차

```powershell
git switch main
git pull --ff-only
python install.py --list
python install.py
python setup_tools.py
```

`--list`는 현재 체크아웃의 저장소 관리 총수와 선택된 항목 수를 표시하며, PC에 실제 설치되었다는 판정을 대신하지 않습니다. `install.py`는 전체 관리 목록을 설치·동기화하고 변경된 기존 폴더를 `skill-backups/<UTC 시각>/`에 보존합니다. 동일 파일은 CURRENT로 건너뜁니다. 이 정책은 전문 13개에도 동일하게 적용됩니다.

은퇴 항목 `create-plan`, `code-review` 2개는 활성 28개에 포함하지 않습니다. 알려진 원본만 백업 후 은퇴시키고 사용자 수정본은 보존합니다. 시스템 스킬, 플러그인 캐시와 매니페스트에 없는 사용자 스킬은 변경하지 않습니다.

15개라고 표시된 보고서는 체크아웃 커밋과 과거 검토일을 함께 확인해야 합니다. 최신 수치는 이 문서보다도 현재 `skills-lock.json`과 `python install.py --list`를 우선합니다.
