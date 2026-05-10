# B 卖点 v13 文件索引

更新时间：2026-05-10

用途：单独索引 B 对话卖点 v13 相关文件。总索引 `文件说明-中文索引.md` 存在旧编码片段，本文件先独立维护，避免破坏总索引。

## 断点与说明

- `sell-v13-b-current-checkpoint.md`：B 对话卖点 v13 独立断点。
- `sell-v13-validation-subchart-test-instructions.md`：四张东方财富通验证副图复制测试说明。
- `sell-v13-validation-label-rules.md`：本地验证标签口径。
- `sell-v13-manual-observation-log.md`：东方财富通验证副图人工看图观察记录。
- `sell-v13-dynamic-ref-compatibility-test.txt`：东方财富通动态 `REF` 最小兼容测试公式。
- `sell-v13-dynamic-ref-compatibility-test-notes.md`：动态 `REF` 兼容测试中文说明。

## 正式公式与兼容性

- `sell-formula-v13-main.md`：B 卖点 v13 当前主公式。
- `sell-formula-v13-compatible-notes.md`：动态 `REF` 兼容性复核。

## 东方财富验证副图

- `sell-v13-validation-subchart-1-display.txt`：B卖点验证1，最终显示与压制。
- `sell-v13-validation-subchart-2-momentum.txt`：B卖点验证2，动能衰减与动态 REF。
- `sell-v13-validation-subchart-3-funds-confirmation.txt`：B卖点验证3，资金失衡与确认层。
- `sell-v13-validation-subchart-4-structure-pattern.txt`：B卖点验证4，结构转弱与形态预警。
- `sell-v13-validation-subchart-1-display-copy-safe.txt`：B卖点验证1复制安全版，人工粘贴首选。
- `sell-v13-validation-subchart-2-momentum-copy-safe.txt`：B卖点验证2复制安全版，人工粘贴首选。
- `sell-v13-validation-subchart-3-funds-confirmation-copy-safe.txt`：B卖点验证3复制安全版，人工粘贴首选。
- `sell-v13-validation-subchart-3-funds-confirmation-copy-safe-v2-marker.txt`：B卖点验证3明显版本线版，当前人工复测首选；第 4 行应为 `版本线:0.2,COLORCYAN;`。
- `sell-v13-validation-subchart-4-structure-pattern-copy-safe.txt`：B卖点验证4复制安全版，人工粘贴首选。
- `sell-v13-validation-subchart-partition-plan.md`：四张验证副图分区方案。

## 批量复核输出

- `sell-v13-b-cache200-latest-conclusion.md`：最新 200 样本复核结论。
- `sell-v13-b-cache200-latest-review.md`：最新 200 样本批量摘要。
- `sell-v13-b-cache200-latest-non-confirmed-review.md`：最新 200 样本非确认段复核。
- `sell-v13-b-cache200-latest-source-diagnostics.md`：非确认段源头诊断。
- `data/processed/reports/sell-v13-b-cache200-latest/`：最新 200 样本合并输出目录。
- `data/processed/reports/sell-v13-b-cache200-latest-non-confirmed.html`：非确认段 HTML/SVG 核图报告。
- `data/processed/reports/sell-v13-b-cache200-latest-source-diagnostics.csv`：非确认段源头诊断 CSV。

## 脚本与测试

- `formula_lab/sell_v13.py`：B 卖点 v13 本地计算、事件表、风险段和验证标签逻辑。
- `scripts/run_sell_v13_validation.py`：运行 B 卖点本地批量验证。
- `scripts/merge_sell_v13_validation_outputs.py`：合并多个 B 卖点批量输出目录。
- `scripts/generate_sell_v13_validation_subchart.py`：生成东方财富验证副图草稿。
- `scripts/generate_sell_v13_batch_review.py`：生成批量复核摘要。
- `scripts/generate_sell_v13_non_confirmed_review.py`：生成非确认段结构复核。
- `scripts/generate_sell_v13_non_confirmed_charts.py`：生成非确认段 HTML/SVG 核图。
- `scripts/generate_sell_v13_non_confirmed_source_diagnostics.py`：生成非确认段源头诊断。
- `tests/test_sell_v13.py`：B 卖点核心逻辑测试。
- `tests/test_sell_v13_validation_subchart_generator.py`：验证副图生成测试。
- `tests/test_sell_v13_non_confirmed_source_diagnostics.py`：非确认段源头诊断测试。

## 当前状态

- [已确认] 四张东方财富验证副图草稿已生成。
- [已确认] 四张东方财富验证副图复制安全版已生成，后续人工粘贴优先使用 `copy-safe` 文件。
- [已确认] 动态 `REF` 最小公式已通过东方财富通人工测试。
- [已确认] `B卖点验证1` 复制安全版已通过东方财富通人工测试。
- [已确认] `B卖点验证2` 复制安全版已通过东方财富通人工测试。
- [已确认] `B卖点验证3` 复制安全版已通过东方财富通人工测试。
- [已确认] `B卖点验证4` 复制安全版已通过东方财富通人工测试。
- [已确认] 四张 B 卖点验证副图复制安全版均已通过东方财富通编译/加载测试。
- [已确认] 已建立人工看图观察记录：`sell-v13-manual-observation-log.md`。
- [已确认] 已修复并重新生成 B3 验证副图：尾部资金源头变量改为主公式实际变量。
- [已确认] B3 复测当前优先打开文件本体 `sell-v13-validation-subchart-3-funds-confirmation-copy-safe-v2-marker.txt`，避免右侧预览缓存旧内容。
- [记录观察] `B卖点验证3` 原版触发“公式至少要有一个输出项”，已改用复制安全版继续验证。
- [已确认] 最新 200 样本复核已完成。
- [暂不改待验证] 主公式 v13 暂不改。
- [下一步] 重新粘贴修复后的 `B卖点验证3`，先复测 `300749`。
