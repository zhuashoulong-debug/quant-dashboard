# GitHub Sync Status

更新日期：2026-05-11

## Remote

```text
origin = https://github.com/zhuashoulong-debug/quant-dashboard.git
```

状态：已配置并完成 `git fetch origin --prune`。

## Local Branch

```text
codex/formula-project
```

状态：本地工作树存在大量项目变更，当前只建立跨设备同步目录和规则，不把全量工作树直接推送。

## Sync Folder

```text
github-mobile-sync/
```

用途：退出、新建会话、手机继续推进、手机切回电脑时使用的专用交接文件夹。

## Package Naming Rule

每次同步都必须先进入当前主线专属目录，再创建独立包目录，避免和其他会话或任务混淆。当前 B 卖点 v13 使用：

```text
github-mobile-sync/b-sell-v13/handoffs/YYYYMMDD-HHMMSS/
github-mobile-sync/b-sell-v13/mobile-updates/YYYYMMDD-HHMMSS/
```

每个包必须包含：

```text
manifest.md
```

`manifest.md` 必须说明任务、来源、分支、包含文件、下一步、禁止覆盖事项。

禁止覆盖旧同步包。手机端进展拉回电脑前，必须先读对应 `manifest.md`，确认它属于当前任务，再合并。

## Safety Notes

- `.gitignore` 已排除 `data/raw/`、`data/processed/`、`.venv-*`、`node_modules/`、环境文件等。
- 跨设备同步优先推送 `github-mobile-sync/` 内的交接包和必要小型文档。
- 不直接上传行情原始缓存、处理后大报告、虚拟环境、账号密钥、日志大文件。
- 从手机切回电脑前，必须先检查 GitHub 是否有更新，再继续本地推进。

## Current Rule

用户说 `退出` 或 `新建会话` 时，助手需要先总结、整理记录、列路径，再把相关交接文件同步到 GitHub 专用文件夹；若发现 GitHub 远端缺失，应主动补配置。
## B Sell v13 Namespace

```text
github-mobile-sync/b-sell-v13/
github-mobile-sync/b-sell-v13/handoffs/
github-mobile-sync/b-sell-v13/mobile-updates/
```

状态：已建立 B 对话卖点 v13 专属同步目录。后续 B 线 `退出` / `新建会话` / 手机端推进都只写入此目录下的时间戳快照，不与 A 对话或其他会话混用，不覆盖旧包。
