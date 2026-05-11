# A3b2 Yellow Reset Handoff Manifest

- Package: `github-mobile-sync/a3b2-yellow-reset/handoffs/20260511-144821/`
- Created at: `2026-05-11 14:48 +08:00`
- Source: desktop local session, `D:\我的文档\Documents\New project 3`
- Repository: `zhuashoulong-debug/quant-dashboard`
- Local branch: `codex/formula-project`
- Remote sync target: `codex/mobile-sync-a3b2-20260511-051434`
- Project line: A conversation buy-point formula project
- Current mainline: `A3b2 黄许可 / 黄后重置 / 再缩+时重风险保护验证`

## Included Files

- `manifest.md`
- `handoff.md`
- `required-paths.md`
- `changed-files.md`
- `next-session-prompt.md`
- `download-status.md`

## Current Decision State

- This is not the B conversation sell/reduce-position formula project.
- The main formula is not changed.
- A3b2 validation subchart structure is temporarily closed.
- `热追` is the first strong risk-protection prompt, only for validation-subchart reading, not for the main formula.
- `极弱续高` is the second risk image, but no new boolean field is added now.
- After removing those two, the remaining risk does not form a clean third branch, so no more fields are added to avoid overfitting.

## Must Not Do

- Do not stop the active market-data download because of exit, new chat, or handoff.
- Do not merge this A3b2 package into the B sell v13 namespace.
- Do not rewrite the main formula from the current risk-protection reading.
- Do not add a new subchart or new boolean field unless expanded samples repeatedly prove a clean missing branch.

## Next Action

1. On resume, first read `next-session-prompt.md`.
2. Confirm whether GitHub has a newer mobile update package.
3. Inspect download progress only; do not stop the downloader.
4. Continue from expanded sample review and display-wording compression for A3b2 validation subcharts.
