# 验证副图索引

更新时间：2026-05-08

本文件用于整理当前验证副图数量过多的问题。当前只做索引和状态标注，不删除、不移动、不改公式逻辑。

## 当前主线

当前主线仍按 `new-chat-handoff.md` 执行：

```text
A 图源头层：
A3a 普通上穿路径已拆成 A3a1 / A3a2 / A3a3 三张短图。
A3b1 首扩来源 mini 副图已测试可显示。
下一步进入 A3b2：蓝黄来源。
```

## 状态分类

- `当前主线`：后续诊断优先使用。
- `辅助排查`：特定问题时可临时打开。
- `历史过渡`：保留记录，不作为当前判断依据。
- `不建议依赖`：已确认存在长图或后段绘图不稳定问题。

## 当前主线副图

| 文件 | 行数 | 状态 | 用途 |
|---|---:|---|---|
| `validation-indicator-A1-clean-draft.txt` | 87 | 当前主线 | 基础K线 / 价格位置 / 成交额简洁版。 |
| `validation-indicator-A2-readable-draft.txt` | 137 | 当前主线 | 挤压 / 带宽 / 迟发 / 收缩背景可读版。 |
| `validation-indicator-A3a1-upcross-mini-draft.txt` | 45 | 当前主线 | 普通上穿路径：核对轨上、手工上穿、`CROSS(PCTB,1)`、浅绕过滤、有效上穿。 |
| `validation-indicator-A3a2-break-bg-mini-draft.txt` | 133 | 当前主线 | 普通上穿路径：核对近挤、迟发、昨缩、今缩、突破背景。 |
| `validation-indicator-A3a3-upbreak-quality-mini-draft.txt` | 167 | 当前主线 | 普通上穿路径：核对阳强、长上、量能、构上、温上 / 暴上 / 极上 / 风险源。 |
| `validation-indicator-A3b1-first-expand-mini-draft.txt` | 236 | 当前主线基本可用 | 首扩来源：核对宽度许可、真正收缩、上轨趋势、带宽初扩、平台热阻断、首扩候选、周期许可、首扩启。 |

## 辅助排查副图

| 文件 | 行数 | 状态 | 用途 |
|---|---:|---|---|
| `validation-indicator-A3a-crosscheck-draft.txt` | 126 | 辅助排查 | 核对 `PCTB>1`、手工上穿、`CROSS(PCTB,1)` 是否一致。 |
| `validation-display-smoke-test.txt` | - | 辅助排查 | 东方财富通固定线、柱、文字显示冒烟测试。 |
| `validation-indicator-A1-front-draft.txt` | 90 | 辅助排查 | A1 细节版，保留更多基础诊断信息，但日常偏花。 |
| `validation-indicator-A2-front-draft.txt` | 139 | 辅助排查 | A2 分段前置绘图版，可在 readable 需要复核时参考。 |

## 历史过渡副图

| 文件 | 行数 | 状态 | 说明 |
|---|---:|---|---|
| `validation-indicator-A1-basic-draft.txt` | 273 | 历史过渡 | A1 早期拆分版。 |
| `validation-indicator-A1-basic-debug-draft.txt` | 278 | 历史过渡 | A1 后置绘图定位版。 |
| `validation-indicator-A1-immediate-debug.txt` | 56 | 历史过渡 | 证明绘图紧跟早期输出时可显示。 |
| `validation-indicator-A2-background-draft.txt` | 232 | 历史过渡 | A2 早期拆分版。 |
| `validation-indicator-A2-clean-draft.txt` | 179 | 历史过渡 | A2 clean 初版。 |
| `validation-indicator-A2-clean-v2-draft.txt` | 182 | 历史过渡 | A2 clean 避免旧标签缓存和嵌套 IF 的过渡版。 |
| `validation-indicator-A2-clean-v3-draft.txt` | 184 | 历史过渡 | A2 clean 提前输出修正版。 |

## 不建议继续依赖的副图

| 文件 | 行数 | 状态 | 原因 |
|---|---:|---|---|
| `validation-indicator-A-draft.txt` | 688 | 不建议依赖 | 完整 A 图过长，后段绘图不稳定。 |
| `validation-indicator-A-readable-draft.txt` | 727 | 不建议依赖 | A 长图显示层修正版，仍受长图问题影响。 |
| `validation-indicator-A-standalone-draft.txt` | 720 | 不建议依赖 | A 独立版仍过长。 |
| `validation-indicator-A-early-output-draft.txt` | 720 | 不建议依赖 | 只证明提前输出核心线有效，后置状态柱仍不稳。 |
| `validation-indicator-A-early-output-debug-draft.txt` | 725 | 不建议依赖 | 后置固定绘图测试版。 |
| `validation-indicator-A3-source-draft.txt` | 668 | 不建议依赖 | A3 源头长图，后段状态显示不可靠。 |
| `validation-indicator-A3-clean-draft.txt` | 194 | 不建议依赖 | A3-clean 源头图仍显示不完整。 |
| `validation-indicator-A3a-upbreak-draft.txt` | 187 | 不建议依赖 | A3a 长图后段绘图不稳定。 |
| `validation-indicator-A3a-debug-draft.txt` | 181 | 不建议依赖 | 只显示灰柱，不能判断后段条件是否触发。 |
| `validation-indicator-A3a-debug-selfcheck-draft.txt` | 164 | 不建议依赖 | 已证明 A3a 后段绘图失效。 |
| `validation-indicator-A3a-readable-draft.txt` | 172 | 不建议依赖 | 仍偏花，且不如 A3a1/A3a2/A3a3 三张短图可靠。 |

## 生成脚本状态

生成脚本暂时不删除。后续规则：

- 当前主线副图对应脚本保留：
  - `generate-validation-A1-clean.js`
  - `generate-validation-A2-readable.js`
  - `generate-validation-A3a1-upcross-mini.js`
  - `generate-validation-A3a2-break-bg-mini.js`
  - `generate-validation-A3a3-upbreak-quality-mini.js`
  - `generate-validation-A3b1-first-expand-mini.js`
- 历史调试脚本仅在需要复查生成过程时使用。
- 后续进入 A3b 时，新脚本命名建议：
  - `generate-validation-A3b2-blue-yellow-source-mini.js`

## 下一步建议

1. 先提交当前现场和本索引，作为整理前基线。
2. 暂不移动旧文件，避免打断已有文档引用。
3. 继续设计 `A3b2：蓝黄来源 mini 副图`。
4. 若后续发现 A3b1 在其他样本后段显示不稳，再拆成 A3b1a / A3b1b。
5. 等 A3b 稳定后，再决定是否建立 `archive/validation-indicators/` 归档目录。
