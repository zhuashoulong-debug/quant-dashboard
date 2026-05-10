# GitHub Mobile Sync

This folder is the dedicated GitHub handoff area for phone and cross-device work.

## Purpose

When the user says `退出` or `新建会话`, the assistant should prepare a compact handoff package here before pushing to GitHub. The package lets a phone-based session continue from the latest state and lets the desktop session later recover phone-side progress.

## What To Sync

- Latest handoff summary.
- Required file path list.
- Current checkpoint and next action.
- Collaboration rules that affect the next session.
- Current formula text or validation subchart text needed for the active task.
- Small Markdown/CSV reports needed for reasoning.
- A changed-files manifest for the handoff.

## Session Namespace Rule

Do not mix handoffs from different chats or tasks. Do not overwrite previous handoff packages.

Each active mainline must use its own namespace folder first. Current B sell v13 work uses:

```text
github-mobile-sync/b-sell-v13/
```

Within that namespace, each sync creates a new timestamped package:

```text
github-mobile-sync/b-sell-v13/handoffs/YYYYMMDD-HHMMSS/
github-mobile-sync/b-sell-v13/mobile-updates/YYYYMMDD-HHMMSS/
```

Each package should include a `manifest.md` that states:

- Which chat or task this package belongs to.
- Whether it came from desktop or phone work.
- The local/GitHub branch it is based on.
- The files included in the package.
- The next concrete action.
- Which files are reference-only and must not overwrite the current mainline.

If a same-day task needs another sync, create another timestamped package or an explicit version suffix. Never silently replace an older package. If a "latest" entry is needed, maintain an index that points to the newest snapshot; do not overwrite historical package contents.

## What Not To Sync

- `data/raw` market caches.
- Virtual environments such as `.venv-*`.
- Large generated charts, logs, browser artifacts, or temporary files.
- Account credentials, API keys, cookies, or secrets.
- Anything that would be unsafe or confusing to use from GitHub.

## Return-To-Desktop Rule

Before continuing locally after phone-side work, check GitHub for newer files first. Use a safe fetch/compare flow and do not overwrite local work destructively.

Read the package `manifest.md` before applying any phone-side update. If local and remote both changed the same file, compare and merge deliberately; do not overwrite by default.
