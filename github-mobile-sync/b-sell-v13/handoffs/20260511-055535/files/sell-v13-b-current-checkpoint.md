# B 对话卖点 v13 当前断点

更新时间：2026-05-11

## 主线定位

- [已确认] B 对话研究的是“预警 / 减仓 / 卖点”正式公式，不是 A 对话买点黄许可主线。
- [已确认] 主公式当前文件：`D:\我的文档\Documents\New project 3\sell-formula-v13-main.md`。
- [已确认] 后续可以借用 A 对话实验环境的底盘和显示方法，但 B 第一版只新增独立模块、独立输出和独立验证副图，不改 A 页面与 A 主线文件。

## 当前完成

- [已确认] 已整理第一版最小验证字段：`D:\我的文档\Documents\New project 3\sell-v13-validation-view-minimum-fields.md`。
- [已确认] 已新增本地输出复核：`D:\我的文档\Documents\New project 3\sell-v13-minimum-field-output-review.md`。
- [已确认] 已完成动态 `REF` 兼容性复核：`D:\我的文档\Documents\New project 3\sell-formula-v13-compatible-notes.md`。
- [已确认] 已整理本地验证标签口径：`D:\我的文档\Documents\New project 3\sell-v13-validation-label-rules.md`。
- [已确认] 已完成 4 张东方财富通验证副图草稿。
- [已确认] B 侧相关测试通过：`23 tests OK`。
- [已确认] 全量本地测试通过：`69 tests OK`。
- [已确认] 新增非确认段源头诊断后，全量本地测试通过：`89 tests OK`。
- [已确认] 已完成一轮最新小样本批量冒烟：`D:\我的文档\Documents\New project 3\data\processed\reports\sell-v13-b-latest-smoke\`。
- [已确认] 已完成最新 200 只缓存样本分片重跑、合并和复核：`D:\我的文档\Documents\New project 3\sell-v13-b-cache200-latest-conclusion.md`。
- [已确认] 已建立 B 卖点专用文件索引：`D:\我的文档\Documents\New project 3\sell-v13-b-file-index.md`。
- [已确认] 已整理下一轮主公式调整候选：`D:\我的文档\Documents\New project 3\sell-v13-next-adjustment-candidates.md`。
- [已确认] 已新增东方财富通动态 `REF` 最小兼容测试：`D:\我的文档\Documents\New project 3\sell-v13-dynamic-ref-compatibility-test.txt`。
- [已确认] 已建立东方财富通人工看图观察记录：`D:\我的文档\Documents\New project 3\sell-v13-manual-observation-log.md`。
- [已确认] 已修复 B3 验证副图尾部变量错配：`强滞原始 / 放量下跌原始 / 天量天价原始 / 放量滞涨原始` 改为主公式实际变量。
- [已确认] B3 复制安全版第 4 行加入 `版本线:0.2,COLORCYAN;`，用于确认东方财富已加载新版。
- [已确认] 后续需要用户打开、查看或复制本地公式文件时，直接提供文件本体链接和完整路径，不再默认依赖右侧预览区复制；右侧预览可能缓存旧内容。
- [已确认] 后续需要用户把公式复制到东方财富通时，优先提供“直接复制公式正文”的方式；如果右键复制入口只能复制路径，则用剪贴板或复制块兜底，避免用户必须打开文件后全选复制。
- [已确认] 用户说 `新建会话` 时，B 对话必须停止继续推进，先做全面交接总结，更新必要断点/交接文件，并把新会话需要读取的文件链接和完整路径发给用户，让新会话接着当前 B 卖点公式任务继续。
- [已确认] `300749` 已用 B3 明显版本线版复测，副图显示 `版本线:0.200`，并出现 `天败 / 强滞 / 强败 / 压` 等资金失衡与确认层信号，说明 B3 新版加载和变量修复均生效。
- [已确认] B 对话 GitHub 手机同步必须使用专属目录 `github-mobile-sync/b-sell-v13/`，并按时间戳创建不可覆盖快照；不得混入 A 对话或其他主线目录，也不得覆盖旧交接包。
- [已确认] 后续遇到工具、命令、依赖、脚本、数据、缓存或环境缺口时，按“缺什么补什么”执行，以高质量、高效率为优先；能用等价高质量方案修复就直接修复，不能用低质量手工绕路替代必要能力。

## 最新小样本批量冒烟

输出：

```text
D:\我的文档\Documents\New project 3\data\processed\reports\sell-v13-b-latest-smoke\
D:\我的文档\Documents\New project 3\sell-v13-b-latest-smoke-review.md
D:\我的文档\Documents\New project 3\sell-v13-b-latest-smoke-non-confirmed-review.md
```

结果：

- [已确认] 默认 6 只股票中，4 只本地缓存可用：`600590 / 300084 / 300749 / 600537`。
- [记录观察] `601958 / 688120` 本地缓存缺失，本次冒烟不影响公式输出链路结论。
- [已确认] 输出最终显示事件 `98` 个，风险段 `47` 个。
- [已确认] 风险段标签：`risk_confirmed` 46 个，`possible_sensitive` 1 个。
- [记录观察] 唯一非确认段为 `300084 2025-09-18 形警`，分类为“形态轻警后快速修复”。
- [暂不改待验证] 当前不因单个 `形警` 修复样本收紧主公式，后续扩大样本后再判断。

## 四张验证副图

1. `B卖点验证1：最终显示与压制`
   `D:\我的文档\Documents\New project 3\sell-v13-validation-subchart-1-display-copy-safe.txt`

2. `B卖点验证2：动能衰减与动态 REF`
   `D:\我的文档\Documents\New project 3\sell-v13-validation-subchart-2-momentum-copy-safe.txt`

3. `B卖点验证3：资金失衡与确认层`
   `D:\我的文档\Documents\New project 3\sell-v13-validation-subchart-3-funds-confirmation-copy-safe.txt`

4. `B卖点验证4：结构转弱与形态预警`
   `D:\我的文档\Documents\New project 3\sell-v13-validation-subchart-4-structure-pattern-copy-safe.txt`

复制测试说明：

`D:\我的文档\Documents\New project 3\sell-v13-validation-subchart-test-instructions.md`

## 当前风险点

- [已确认] 东方财富通动态 `REF` 最小兼容公式已通过人工测试。
- [已确认] `B卖点验证1` 复制安全版已通过东方财富通人工测试。
- [已确认] `B卖点验证3` 复制安全版已通过东方财富通人工测试；截图显示副图正常加载 `零轴:0.000`，未再出现输出项报错。
- [已确认] `B卖点验证2` 复制安全版已通过东方财富通人工测试；截图显示副图正常加载 `零轴:0.000`，未出现兼容性报错。
- [已确认] `B卖点验证4` 复制安全版已通过东方财富通人工测试；截图显示副图正常加载 `零轴:0.000`，未出现兼容性报错。
- [记录观察] `B卖点验证3` 原版触发“公式至少要有一个输出项”，当前改用复制安全版继续测试。
- [已确认] 四张 B 卖点验证副图复制安全版均已通过东方财富通编译/加载测试。
- [记录观察] B3 第一版虽能加载，但资金源头诊断线引用了不存在变量；已重新生成，需重新粘贴复测。
- [暂不改待验证] 主公式和验证副图仍保留严格动态 `REF`。
- [记录观察] 若东方财富通不支持动态 `REF`，先记录报错位置，再讨论兼容版，不直接改主公式逻辑。
- [记录观察] `current-checkpoint.md` 当前尾部有 A 主线内容，B 主线先以本文件作为当前断点，避免和 A 对话互相覆盖。
- [记录观察] `文件说明-中文索引.md` 存在旧编码片段，暂不强行追加；B 侧先用 `sell-v13-b-file-index.md` 独立维护。
- [记录观察] 本地标签口径只服务批量验证，不能把标签结果机械等同于主公式买卖建议。
- [暂不改待验证] 200 样本复核后，主公式 v13 暂不改；下一步先核图非确认段。
- [暂不改待验证] 直接过滤探针未找到清晰单阈值：成交额比例、MA20 破位质量、MA5 下压都不能稳定区分敏感与有效样本。

## 下一步

- [下一步] 第一组人工观察样本继续看 `300502 / 600590 / 600537`，优先从 B3 资金失衡与确认层开始。
- [下一步] 对 `300749` 暂定结论为“风险段能识别”，后续要判断的是该类顶部段信号密度是否需要显示层优化，而不是立即改主公式逻辑。
- [下一步] B 对话本地侧优先核图 `弱 / 形警 / 天` 三类非确认段。
- [下一步] 若副图报错，先记录错误行和错误提示；优先判断公式兼容性，再判断信号逻辑。
- [下一步] B 对话继续维护正式卖点公式、验证口径和后续主公式统一调整。

## 新建会话交接

- [已确认] 2026-05-11 收到用户暗号 `新建会话`，当前停止继续推进公式讨论，进入 B 卖点 v13 交接流程。
- [已确认] 本次交接必须生成 GitHub 手机同步快照，写入 `github-mobile-sync/b-sell-v13/handoffs/` 下的新时间戳目录，不覆盖旧包，不混入 A 对话。
- [下一步] 新会话恢复后先读取本文件和本次 GitHub 快照 `manifest.md`，再从 `300502 / 600590 / 600537` 的 B3 观察继续。
