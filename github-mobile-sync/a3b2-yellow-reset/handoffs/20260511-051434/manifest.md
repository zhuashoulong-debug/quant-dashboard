# A3b2 Mobile Handoff Manifest

## Package Identity

```text
package: github-mobile-sync/a3b2-yellow-reset/handoffs/20260511-051434/
source: desktop
task: A3b2 买点公式黄许可 / 黄后重置 / 再缩+时重风险保护验证
branch: codex/formula-project
created_at: 2026-05-11 05:14:34 Asia/Shanghai
remote_branch: codex/mobile-sync-a3b2-20260511-051434
```

## Non-Overwrite Rule

本包是 A 对话买点公式专用交接包。不要和 B 对话卖点/减仓公式混用，不要覆盖旧包。手机端如果继续推进，也要新建自己的时间戳包。

## Included Files

```text
manifest.md
handoff.md
required-paths.md
changed-files.md
next-session-prompt.md
```

## Background Process Rule

用户已入规：`退出` 和 `新建会话` 都不能停止后台下载进程。本次只巡检下载进度，不杀进程，不重启下载。

## Next Concrete Action

新会话先读本包，再读本地 `current-checkpoint.md`、`next-session-resume.md` 和 `yellow-reset-risk-protection-candidate-note.md`。继续时先把风险保护读法固化成说明，不新增字段、不改主公式。