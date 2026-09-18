# v2026.09.19.2 — all 28 skills under repository management

All 28 active skills, including the 13 emulator-specialist skills, are managed by `skills-lock.json` and the same install/update/selection/backup workflow. The preceding main release already included these entries. This release makes that scope explicit and corrects historical wording that could be mistaken for a current 15-skill limit.

- `install.py --list` reports the full repository-managed count (25 bundled + 3 pinned upstream) separately from the selected entries.
- README and docs/MANAGED_SKILLS.md provide the complete management scope and inventory. Historical audit numbers are clearly dated.
- No skill implementation, upstream pin, plugin cache or retirement/backup policy changes.

Validation: 49 unittest tests PASS. A fresh clone of GitHub main at `072ab53`, without an existing source cache, installed all 28 skills into an isolated destination. Every installed inventory matched its pinned source; repeat offline installation reported all 28 CURRENT. Local verification reports 27 direct installations and one reused pinned create-kr-patch plugin CURRENT. Repository-wide and selected-list totals, dependency expansion, retired replacement and read-only listing are covered by the new regression check. Listing describes repository scope rather than proving local installation.
