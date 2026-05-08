# 新对话交接说明

本文件用于在上下文过长、响应卡顿、需要新开对话时快速恢复项目状态。

## 新对话建议开场白

新开对话后，可以直接发送：

```text
请先读取以下文件，恢复我们这个公式项目的上下文。先不要改公式，先告诉我你理解到的当前状态、下一步应该从哪里继续。

必须读取：
1. 文件说明-中文索引.md
2. current-checkpoint.md
3. long-term-anchors.md
4. collaboration-guidelines.md
5. validation-indicator-plan.md
6. formula-v1-draft.txt
7. formula-v1-change-notes.md
8. pending-verification-list.md

必要时再读取：
- formula-discussion-summary.md
- formula-changelog.md
- initial-formula-original.txt
- 初始公式原版.md

按场景再读取：
- project-index.md：如果需要先看项目文件结构和文件用途。
- backtest-plan.md：如果要进入 Python 回测、统计口径或导出数据分析。
- 外部文档提问复盘.md：如果要回顾外部 GPT 沟通记录中值得吸收的方法、风险显示问题或用户提问模式。
- validation-indicator-A1-clean-draft.txt：如果继续验证副图 A 的基础K线/价格位置/成交额层。
- validation-indicator-A2-readable-draft.txt：如果继续验证副图 A 的挤压/带宽/迟发/收缩背景层。
- validation-indicator-A3a1-upcross-mini-draft.txt：如果核对普通上穿路径是否发生有效上穿。
- validation-indicator-A3a2-break-bg-mini-draft.txt：如果核对普通上穿路径是否具备突破背景。
- validation-indicator-A3a3-upbreak-quality-mini-draft.txt：如果核对普通上穿路径是否进入温上/暴上/极上/风险源。
- validation-indicator-A3b1-first-expand-mini-draft.txt：如果核对首扩来源、首扩候选、首扩周期许可和首扩启。
- validation-indicator-index.md：如果需要查看当前哪些验证副图是主线、辅助排查、历史过渡或不建议依赖。

一般不需要一上来读取：
- 各类 `generate-*.js`：只有需要重新生成或修改验证副图时再读。
- 已明确不建议继续依赖的旧版/长版验证副图：只有排查历史问题时再读。

当前主线应该是：验证副图 A 的源头层。A3a 普通上穿路径已经拆成 A3a1/A3a2/A3a3 三张短图；A3b1 首扩来源 mini 副图已经生成，下一步应先测试 A3b1，若显示稳定再进入 A3b2：蓝黄来源。
```

## 当前最重要状态

### 1. 不建议继续依赖本长对话

当前对话上下文已经很长，已经出现卡顿和规则执行不完整的风险。建议新开对话，并用项目文件恢复上下文。

### 2. 当前公式工作主线

当前不是继续改主公式，而是在设计和测试验证副图。

验证副图目的：

- 解释某根K线为什么出信号；
- 解释某根K线为什么没出信号；
- 判断出信号或不出信号是否合理；
- 反向校准主公式逻辑和参数；
- 为后续回测字段和原因归因做准备。

### 3. 东方财富通副图兼容结论

已确认东方财富通对长公式后段绘图不稳定：

- 前面输出项能显示；
- 后面 `STICKLINE / DRAWTEXT` 可能不显示；
- 不能把“后面没显示”直接理解为“条件没触发”。

后续验证副图默认原则：

```text
算完一小组变量 -> 马上画这一组
如果仍然不稳定 -> 拆成更短的 mini 图
```

### 4. 当前可用验证副图状态

已测试/基本可用：

- `validation-indicator-A1-clean-draft.txt`：基础K线/价格位置/成交额简洁版。
- `validation-indicator-A2-readable-draft.txt`：挤压/带宽/迟发/收缩背景可读版。
- `validation-indicator-A3a1-upcross-mini-draft.txt`：普通上穿路径的上穿核对短图。
- `validation-indicator-A3a2-break-bg-mini-draft.txt`：普通上穿路径的突破背景短图。
- `validation-indicator-A3a3-upbreak-quality-mini-draft.txt`：普通上穿路径的温暴极质量短图。
- `validation-indicator-A3b1-first-expand-mini-draft.txt`：首扩来源、首扩候选、周期许可、首扩启核对短图，待用户测试。

不应作为当前定稿继续依赖的版本：

- `validation-indicator-A3-clean-draft.txt`：太长，显示不完整。
- `validation-indicator-A3a-upbreak-draft.txt`：长图后段不稳定。
- `validation-indicator-A3a-debug-draft.txt`：只显示灰柱，不能判断条件是否触发。
- `validation-indicator-A3a-debug-selfcheck-draft.txt`：证明后段绘图失效。
- `validation-indicator-A3a-readable-draft.txt`：仍偏花，且长图逻辑不如三张短图可靠。

可作为排查辅助但非当前主线：

- `validation-indicator-A3a-crosscheck-draft.txt`：核对 `PCTB>1`、手工上穿、`CROSS(PCTB,1)`。

### 5. 下一步

下一步应先测试：

```text
A3b1：首扩来源 mini 副图
```

如果 A3b1 显示稳定，再进入：

```text
A3b2：蓝黄来源
```

暂时不要继续纠缠 A3a 长图。A3a 已经收敛为三张短图：

```text
A3a1 = 有没有有效上穿
A3a2 = 有没有突破背景
A3a3 = 有没有进入温上/暴上/极上/风险源
```

## 长期锚点

### 主公式与验证副图必须同步

后续主公式做任何调整时，都必须同步检查所有当前仍被采用、有效、最新定稿或准定稿的验证副图版本是否需要更新。

不能只改主公式，不改副图。

每次主公式调整后必须问：

```text
这次主公式调整会影响哪些验证副图？
对应副图是否需要同步改变量、阈值、文字、颜色或读法？
```

### 新对话恢复原则

新对话不要依赖旧聊天全文。应先读项目文件，再恢复上下文。

优先读取顺序：

1. `文件说明-中文索引.md`
2. `current-checkpoint.md`
3. `long-term-anchors.md`
4. `collaboration-guidelines.md`
5. `validation-indicator-plan.md`
6. `formula-v1-draft.txt`
7. `formula-v1-change-notes.md`
8. `pending-verification-list.md`

读取后先输出：

- 当前主线；
- 已确认结论；
- 当前可用副图；
- 已作废或不建议继续依赖的副图；
- 下一步建议。

## 协作规则提醒

- 公式后必须中文解释。
- 一点一点讨论，不跳步。
- 每一块先说：当前讨论、用来判断什么、最终影响什么、属于哪一层。
- 逻辑/结构问题优先直接复查，不要什么都丢给后续验证。
- 参数和边界问题进入验证/回测。
- 不为个股过拟合。
- 验证副图字段设计宁可多审计，不能漏关键变量。
- 如果用户用“入规”，写入协作规则。
- 如果用户用“记锚”，写入长期锚点或当前断点。
