# Changed Files

## A3b2 Validation Subchart / Reading Layer

- `formula_lab\a3b2b1.py`
- `formula_lab\validation_views.py`
- `tests\test_a3b2b1_backgrounds.py`
- `tests\test_validation_views.py`
- `generate-validation-A3b2c-yellow-reset-mini.js`
- `validation-indicator-A3b2c-yellow-reset-mini-draft.txt`
- `generate-validation-A3b2d-strong-reset-mini.js`
- `validation-indicator-A3b2d-strong-reset-mini-draft.txt`
- `validation-indicator-A3b2-remaining-status.md`

## Download Resilience

- `scripts\download_market_data.py`
- `tests\test_download_market_data.py`

Key behavior added:

- `--per-stock-timeout`
- `--resume-from-manifest`
- Timeout keeps one stuck stock from blocking the whole download run.

## Project Handoff / Restore Files

- `current-checkpoint.md`
- `next-session-resume.md`
- `new-chat-handoff.md`
- `github-mobile-sync\handoff-template.md`
- `github-mobile-sync\sync-status.md`
- `github-mobile-sync\a3b2-yellow-reset\handoffs\20260511-144821\manifest.md`
- `github-mobile-sync\a3b2-yellow-reset\handoffs\20260511-144821\handoff.md`
- `github-mobile-sync\a3b2-yellow-reset\handoffs\20260511-144821\required-paths.md`
- `github-mobile-sync\a3b2-yellow-reset\handoffs\20260511-144821\changed-files.md`
- `github-mobile-sync\a3b2-yellow-reset\handoffs\20260511-144821\next-session-prompt.md`
- `github-mobile-sync\a3b2-yellow-reset\handoffs\20260511-144821\download-status.md`

## Dirty Worktree Caution

The local worktree contains other project changes. Do not assume every dirty file belongs to this A3b2 handoff. Keep this package scoped to the A conversation buy-point formula project.
