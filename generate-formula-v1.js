const fs = require('fs');
const path = require('path');
const root = process.cwd();
let text = fs.readFileSync(path.join(root, 'initial-formula-original.txt'), 'utf8');

function replaceOrThrow(s, oldText, newText, label) {
  if (!s.includes(oldText)) throw new Error('missing block: ' + label);
  return s.replace(oldText, newText);
}

function replaceNTimes(s, oldText, newText, n, label) {
  for (let i = 0; i < n; i++) {
    if (!s.includes(oldText)) throw new Error('missing repeated block: ' + label + ' #' + (i + 1));
    s = s.replace(oldText, newText);
  }
  return s;
}

function replaceSlice(s, startMarker, endMarker, newText, label) {
  const start = s.indexOf(startMarker);
  const end = s.indexOf(endMarker);
  if (start < 0 || end < 0 || end <= start) throw new Error('bad slice: ' + label);
  return s.slice(0, start) + newText + s.slice(end);
}

text = replaceOrThrow(
  text,
  `日线:=PERIOD=5;\n周线:=PERIOD=6;\n月线:=PERIOD=7;`,
  `日线:=PERIOD=5;\n周线:=PERIOD=6;\n月线:=PERIOD=7;\n\n有效周期:=日线 OR 周线 OR 月线;\n足够K:=BARSCOUNT(C)>IF(周线,80,IF(月线,48,120));\n显示许可:=有效周期 AND 足够K;`,
  '显示许可',
);

text = replaceOrThrow(text, `SQN:=IF(周线,3,IF(月线,2,5));`, `SQN:=IF(周线,3,IF(月线,3,5));`, 'SQN');

text = replaceOrThrow(
  text,
  `近挤:=COUNT(挤压,SQN)>=1;\n效挤:=COUNT(挤压,SQN)>=2;`,
  `近挤:=COUNT(挤压,2)>=1;\n效挤:=IF(日线,\nCOUNT(挤压,5)>=2 AND BARSLAST(挤压)<=2,\nCOUNT(挤压,SQN)>=2);`,
  '近挤效挤',
);

text = replaceOrThrow(text, `前宽比2:=REF(带宽,1)/MAX(前有效宽均,0.0001);`, `前宽比:=REF(带宽,1)/MAX(前有效宽均,0.0001);`, '前宽比');
text = replaceOrThrow(text, `带宽相高:=当前宽比>带宽相高线 OR 前宽比2>带宽相高线;`, `带宽相高:=当前宽比>带宽相高线 OR 前宽比>带宽相高线;`, '带宽相高');

const startupLateBlock = `

{四、启动前带宽过滤}
启动前带宽:=REF(带宽,1);
启动前均宽:=前有效宽均;
启动前高宽:=前有效高宽;
启动前低宽:=前有效低宽;

启动前宽比:=启动前带宽/MAX(启动前均宽,0.0001);
启动前相高:=启动前带宽/MAX(启动前高宽,0.0001);

启动前绝宽高:=启动前带宽>带宽绝高线;
启动前相宽高:=启动前宽比>带宽相高线;
启动前持宽:=REF(持宽,1);

首扩宽度许可:=NOT(启动前绝宽高 OR 启动前相宽高 OR 启动前持宽);

{五、迟发挤压背景}
迟发挤N:=IF(周线,6,IF(月线,6,10));
迟发曾挤:=REF(COUNT(挤压,迟发挤N),1)>=1;

位N:=IF(周线,104,IF(月线,24,500));
位高:=HHV(H,位N);
位低:=LLV(L,位N);
二年位:=(C-位低)/MAX(位高-位低,0.0001);
高位2年:=二年位>=0.80;
低位2年:=二年位<=0.40;

迟发绝宽线:=IF(高位2年,
IF(周线,0.35,IF(月线,0.45,0.22)),
IF(低位2年,
IF(周线,0.45,IF(月线,0.55,0.28)),
IF(周线,0.40,IF(月线,0.50,0.25))));

迟发绝宽许可:=带宽<迟发绝宽线;

迟发近宽N:=IF(周线,3,IF(月线,3,5));
迟发近宽未破:=带宽<=REF(HHV(带宽,迟发近宽N),1)*1.03;

迟发均宽许可:=带宽/MAX(前有效宽均,0.0001)<1.08;
迟发宽速许可:=宽速率<=微扩阈;

迟发宽未扩:=迟发绝宽许可
AND 迟发近宽未破
AND 迟发均宽许可
AND NOT(启动前持宽)
AND NOT(REF(宽近高,1))
AND 迟发宽速许可;

迟发挤压背景:=迟发曾挤 AND 迟发宽未扩;
`;

text = replaceOrThrow(text, `持宽:=硬高宽 OR 软持宽;\n\n{四、收缩识别}`, `持宽:=硬高宽 OR 软持宽;${startupLateBlock}\n{六、收缩识别}`, '插入迟发');

const oldBandFilter = `{五、带宽过滤}
启动前带宽:=REF(带宽,1);
启动前均宽:=前有效宽均;
启动前高宽:=前有效高宽;
启动前低宽:=前有效低宽;

启动前宽比:=启动前带宽/MAX(启动前均宽,0.0001);
启动前相高:=启动前带宽/MAX(启动前高宽,0.0001);
启动前相低:=启动前带宽/MAX(启动前低宽,0.0001);

启动前绝宽高:=启动前带宽>带宽绝高线;
启动前相宽高:=启动前宽比>带宽相高线;
启动前持宽:=REF(持宽,1);

首扩宽度许可:=NOT(启动前绝宽高 OR 启动前相宽高 OR 启动前持宽);

`;

text = replaceOrThrow(text, oldBandFilter, '', '删除旧带宽过滤');

text = replaceOrThrow(
  text,
  `有效挤压:=REF(效挤,1) OR REF(COUNT(挤压,SQN*2),1)>=1;`,
  `日分散挤原:=COUNT(挤压,10)>=2 AND COUNT(挤压,3)>=1;\n周分散挤原:=COUNT(挤压,7)>=2 AND COUNT(挤压,2)>=1;\n月分散挤原:=COUNT(挤压,5)>=2 AND COUNT(挤压,2)>=1;\n\n分散挤原:=IF(日线,日分散挤原,IF(周线,周分散挤原,月分散挤原));\n\n挤压宽许可:=带宽/MAX(前有效宽均,0.0001)<1.15\nAND NOT(启动前持宽)\nAND NOT(REF(宽近高,1));\n\n有效挤压:=(REF(效挤,1) OR 分散挤原) AND 挤压宽许可;`,
  '有效挤压',
);

text = text.replace(`阴强:=C<O AND 实占>=BP;\n`, '');
text = text.replace(`长下:=下影>=YP;\n`, '');

text = replaceOrThrow(
  text,
  `{七、成交额}\nAMT:=AMOUNT;\n均额:=MA(AMT,VN);\n温额:=AMT>=均额;\n放额:=AMT>=均额*VP;\n缩额:=AMT<=均额*0.8;\n巨额:=AMT>=均额*BVP;`,
  `{七、成交额}\nAMT0:=IF(AMOUNT>0,AMOUNT,VOL*C*100);\nAMT:=AMT0;\n均额:=MA(AMT0,VN);\n有额:=AMT0>0 AND 均额>0;\n\n温额:=有额 AND AMT0>=均额;\n放额:=有额 AND AMT0>=均额*VP;\n缩额:=有额 AND AMT0<=均额*0.8;\n巨额:=有额 AND AMT0>=均额*BVP;`,
  '成交额',
);

text = text.replace(`\n强空:=长向<0 AND C<长线 AND 短线<长线;\n初空:=NOT(强空) AND 短向<0 AND C<短线 AND C<长线;\n`, `\n`);

text = replaceOrThrow(text, `突破背景:=REF(近挤,1) OR REF(真正收缩,1) OR 真正收缩;`, `突破背景:=REF(近挤,1)\nOR 迟发挤压背景\nOR REF(真正收缩,1)\nOR 真正收缩;`, '突破背景');
text = replaceOrThrow(text, `中位突破保护:=中位收缩突破 AND NOT(长上);`, `中位突破保护:=中位收缩突破;`, '中位突破保护');

text = replaceOrThrow(text, `AND (温额 OR 构上);\n\n高位平台再突`, `;\n\n高位平台再突`, '平台突破特征重复');
text = replaceNTimes(text, `AND (放额 OR 构上)\nAND 阳强`, `AND 阳强`, 2, '平台强启重复量能');
text = replaceNTimes(text, `AND NOT(长上)\nAND NOT(巨额 AND 明显长上);`, `AND NOT(长上);`, 3, '平台长上重复');
text = replaceOrThrow(text, `AND NOT(长上)\nAND NOT(巨额 AND 长上);`, `AND NOT(长上);`, '首扩强突贴轨重复');
text = replaceOrThrow(text, `\n前宽比:=REF(带宽,1)/MAX(前有效宽均,0.0001);\n前持宽:=REF(持宽,1);`, `\n前持宽:=REF(持宽,1);`, '删除后段前宽比重复');
text = replaceOrThrow(text, `AND PCTB>1\nAND NOT(长上)\nAND NOT(巨额 AND 明显长上);`, `AND PCTB>1\nAND NOT(长上);`, 'PCTB高位惯性重复');

const blueYellow = `{二十二、蓝柱/黄柱源头拆分}
温上源:=温上 OR 中位温上;
暴上源:=暴上 OR 中位暴上;

蓝压缩质量:=启动前宽比<1.05
AND 启动前相高<0.70
AND NOT(启动前持宽)
AND NOT(REF(宽近高,1))
AND NOT(平台高热状态);

蓝挤压背景:=有效挤压;

蓝收缩背景:=REF(真正收缩,1) OR 真正收缩 OR 中位收缩突破;
昨收缩突破背景:=REF(真正收缩,1);

蓝优质背景:=(蓝挤压背景 OR (蓝收缩背景 AND 收缩过程) OR 昨收缩突破背景)
AND 蓝压缩质量;

蓝温源:=温上源 AND 蓝优质背景;
蓝暴源:=暴上源 AND 蓝优质背景;

黄温源:=温上源 AND NOT(蓝优质背景);
黄暴源:=暴上源 AND NOT(蓝优质背景);

蓝信号源:=蓝温源 OR 蓝暴源;
黄信号源:=黄温源 OR 黄暴源;

蓝候选原:=蓝信号源;
普通黄候选原:=黄信号源;

蓝温有效:=蓝温源
AND NOT(首扩启)
AND NOT(速有效)
AND NOT(速后运行);

蓝暴有效:=蓝暴源
AND NOT(首扩启);

蓝有效:=蓝温有效 OR 蓝暴有效;

黄可显示占用原:=黄信号源
AND 阳强
AND (放额 OR 构上)
AND NOT(首扩启)
AND NOT(速有效)
AND NOT(速后运行);

冷却占用信号原:=首扩启
OR 速有效
OR 冲有效
OR 蓝有效
OR 黄可显示占用原;

近上轨信号:=REF(COUNT(冷却占用信号原,黄色冷却N),1)>0;

黄段结束:=PCTB<0.50
OR C<MID
OR (C<短线 AND PCTB<0.70);

近段已结束:=REF(COUNT(黄段结束,黄色趋势段N),1)>=1;

黄有效再收缩:=REF(有效挤压,1)
OR REF(真正收缩,1)
OR (REF(收缩过程,1)
AND REF(带宽,1)<前有效宽均*IF(周线,0.95,IF(月线,1.00,0.90)))
OR (REF(收缩过程,1)
AND REF(带宽,1)<前有效高宽*0.55);

近期强势N:=IF(周线,2,IF(月线,2,4));
近期仍强:=REF(COUNT(PCTB>0.75 AND C>短线,近期强势N),1)>=IF(周线,1,IF(月线,1,2));

强趋势运行:=REF(COUNT(PCTB>0.75 AND C>短线,黄色趋势段N),1)>=IF(周线,4,IF(月线,3,7))
AND 近期仍强
AND NOT(近段已结束);

距上轨信号:=BARSLAST(REF(冷却占用信号原,1));

时间解禁:=距上轨信号>黄色趋势段N;

时间回落重置:=时间解禁
AND REF(COUNT(PCTB<0.70 OR C<MID OR (C<短线 AND PCTB<0.80),黄新鲜N),1)>=1;

黄色显示许可:=(NOT(近上轨信号)
OR 近段已结束
OR 黄有效再收缩
OR 时间回落重置)
AND NOT(强趋势运行 AND 近上轨信号 AND NOT(近段已结束) AND NOT(黄有效再收缩));

近期强推:=REF(COUNT(PCTB>=1.15 OR PCTB>=1+深限 OR 速有效 OR 首扩启 OR 冲有效 OR 蓝有效,黄新鲜N),1)>=1;

黄色充分重置:=近段已结束
OR 黄有效再收缩
OR 时间回落重置
OR REF(COUNT(PCTB<0.60 OR C<MID OR (C<短线 AND PCTB<0.75),黄新鲜N),1)>=1;

黄色新鲜许可:=NOT(近期强推) OR 黄色充分重置;

黄温有效:=黄温源
AND 黄色显示许可
AND 黄色新鲜许可
AND NOT(首扩启)
AND NOT(速有效)
AND NOT(速后运行);

黄暴有效:=黄暴源
AND 黄色显示许可
AND 黄色新鲜许可
AND NOT(首扩启)
AND NOT(速有效)
AND NOT(速后运行);

黄有效:=黄温有效 OR 黄暴有效;

有效启动信号预:=首扩启
OR 速有效
OR 蓝有效
OR 冲有效
OR 黄有效;

`;

text = replaceSlice(text, `{二十二、蓝柱/黄柱源头拆分}`, `{二十三、布林滞后 / PCTB伪弱保护}`, blueYellow, '蓝黄整段');

const confirm = `{二十四、确认信号}
确认强区:=PCTB>0.90 OR 布林滞后保护;

高质启动:=首扩启 OR 速有效 OR 蓝有效 OR 冲有效;

确认基础条件:=C>REF(C,1)
AND C>O
AND 实占>=BP
AND 确认强区
AND C>短线
AND 短向>0
AND (温额 OR 构上);

确2前两实体高:=MAX(REF(实体高,2),REF(实体高,1));

确2候选:=REF(高质启动,2)
AND REF(C,1)>REF(C,2)
AND C>REF(C,1)
AND C>确2前两实体高
AND 确认基础条件;

确2:=确2候选;
确2长上警:=确2 AND 长上;

确3前三实体高:=REF(HHV(实体高,3),1);

确3候选:=REF(高质启动,3)
AND C>确3前三实体高
AND 确认基础条件;

确3:=确3候选 AND NOT(REF(确2,1));
确3长上警:=确3 AND 长上;

确4前四实体高:=REF(HHV(实体高,4),1);

确4中间未坏:=REF(COUNT(C<MID OR PCTB<0.65,3),1)=0;

确4候选:=REF(高质启动,4)
AND C>确4前四实体高
AND 确认基础条件
AND 确4中间未坏
AND NOT(长上);

确4:=确4候选 AND NOT(REF(确2,2)) AND NOT(REF(确3,1));
确4长上候选:=REF(高质启动,4)
AND C>确4前四实体高
AND 确认基础条件
AND 确4中间未坏
AND 长上;

风险上破:=暴上险 OR 极上险;

险反:=REF(风险上破,1)
AND C>REF(H,1)
AND 阳强
AND NOT(长上)
AND (温额 OR 构上);

确:=确2 OR 确3 OR 确4 OR 险反;

`;

text = replaceSlice(text, `{二十四、确认信号}`, `{二十五、风险提示}`, confirm, '确认整段');

text = replaceOrThrow(
  text,
  `初扩早期起点:=首扩启\nOR 扩张保护起点\nOR (真正收缩\nAND 带宽初扩\nAND PCTB>0.70\nAND PCTB<1+深限\nAND 上轨趋势);`,
  `初扩早期起点:=首扩启\nOR 扩张保护起点;`,
  '初扩早期起点',
);

text = replaceOrThrow(
  text,
  `风险前上启:=首扩启\nOR 速有效\nOR 蓝有效\nOR 冲有效\nOR 黄有效\nOR 确;`,
  `风险前启动源:=首扩启\nOR 速有效\nOR 蓝有效\nOR 冲有效\nOR 黄有效;\n\n风险前确认源:=确;\n\n风险前上启:=风险前启动源\nOR 风险前确认源;`,
  '风险前上启拆分',
);

text = replaceOrThrow(text, `较前放额:=AMT>=REF(AMT,1)*1.2;`, `较昨放额:=AMT>=REF(AMT,1)*1.2;\n较前5高额:=AMT>=REF(HHV(AMT,5),1)*1.2;`, '较昨放额');
text = replaceOrThrow(text, `高险放量:=巨额 OR 放额 OR 较前放额;`, `高险放量:=巨额 OR 放额 OR 较昨放额;`, '高险放量');

text = replaceOrThrow(
  text,
  `前5高点距:=HHVBARS(REF(H,1),5)+1;\n前5高点PCTB:=REF(PCTB,前5高点距);`,
  `前5高点PCTB:=IF(REF(H,1)>=REF(H,2)\nAND REF(H,1)>=REF(H,3)\nAND REF(H,1)>=REF(H,4)\nAND REF(H,1)>=REF(H,5),\nREF(PCTB,1),\nIF(REF(H,2)>=REF(H,1)\nAND REF(H,2)>=REF(H,3)\nAND REF(H,2)>=REF(H,4)\nAND REF(H,2)>=REF(H,5),\nREF(PCTB,2),\nIF(REF(H,3)>=REF(H,1)\nAND REF(H,3)>=REF(H,2)\nAND REF(H,3)>=REF(H,4)\nAND REF(H,3)>=REF(H,5),\nREF(PCTB,3),\nIF(REF(H,4)>=REF(H,1)\nAND REF(H,4)>=REF(H,2)\nAND REF(H,4)>=REF(H,3)\nAND REF(H,4)>=REF(H,5),\nREF(PCTB,4),\nREF(PCTB,5)))));`,
  '前5高点PCTB固定展开',
);

text = replaceOrThrow(
  text,
  `高险共用背景:=高险前高已成\nAND 高险当前续高\nAND 高险已有涨幅\nAND 高险趋势仍强\nAND 高险放量\nAND 高险PCTB背离\nAND NOT(扩张保护期)\nAND NOT(初扩早期险过滤);`,
  `高险共用背景原:=高险前高已成\nAND 高险当前续高\nAND 高险已有涨幅\nAND 高险趋势仍强\nAND 高险放量\nAND 高险PCTB背离;\n\n高险保护许可:=NOT(扩张保护期)\nAND NOT(初扩早期险过滤);`,
  '高险源头保护拆分',
);

text = replaceOrThrow(text, `高位放量创新高长上险:=高险共用背景\nAND 长上;`, `高位放量创新高长上险:=高险共用背景原\nAND 高险保护许可\nAND 长上;`, '高险长上');
text = replaceOrThrow(text, `高位放量创新高冲回险:=高险共用背景\nAND 高险冲回形态;`, `高位放量创新高冲回险:=高险共用背景原\nAND 高险冲回形态;`, '高险冲回');

text = replaceOrThrow(
  text,
  `高位放量创新高险:=高位放量创新高长上险\nOR 高位放量创新高冲回险;`,
  `高位放量创新高可保护险:=高位放量创新高长上险;\n高位放量创新高硬险:=高位放量创新高冲回险;\n\n高位放量创新高险:=高位放量创新高可保护险\nOR 高位放量创新高硬险;`,
  '高险拆分',
);

const oldRiskMerge = `绝对硬险:=极上绝对险
OR 极端长上险
OR 巨额明显长上险;

可保护硬险:=极上险
OR (PCTB>=1+深限 AND 长上)
OR ((PCTB>1 AND 巨额 AND 长上)
AND NOT(启后冲高回落保护)
AND NOT(准启试冲保护));

可滞后保护软险:=高宽热轨 OR 高宽连冲;

不可滞后保护软险:=暴上险风险
OR 续热险风险
OR 高宽冲顶
OR 高位极上险
OR 穿轨长上险
OR 高位放量创新高险;

软险:=(可滞后保护软险 AND NOT(布林滞后保护))
OR 不可滞后保护软险;

险原:=绝对硬险 OR ((可保护硬险 OR 软险) AND NOT(扩张保护期) AND NOT(中位突破保护));

险:=险原 AND NOT(初扩早期险过滤);
`;

const newRiskMerge = `不可早期过滤硬险:=高位放量创新高硬险;

硬险源:=极上绝对险
OR 极端长上险
OR 巨额明显长上险;

可保护硬险:=极上险
OR 高位放量创新高可保护险
OR (PCTB>=1+深限 AND 长上)
OR ((PCTB>1 AND 巨额 AND 长上)
AND NOT(启后冲高回落保护)
AND NOT(准启试冲保护));

可滞后保护软险:=高宽热轨 OR 高宽连冲;

不可滞后保护软险:=暴上险风险
OR 续热险风险
OR 高宽冲顶
OR 高位极上险
OR 穿轨长上险;

软险:=(可滞后保护软险 AND NOT(布林滞后保护))
OR 不可滞后保护软险;

普通险原:=硬险源
OR ((可保护硬险 OR 软险)
AND NOT(扩张保护期)
AND NOT(中位突破保护));

险:=不可早期过滤硬险
OR (普通险原 AND NOT(初扩早期险过滤));
`;

text = replaceOrThrow(text, oldRiskMerge, newRiskMerge, '风险出口');

text = replaceOrThrow(
  text,
  `慎源:=慎滞高位背景\nAND 阶段高位不创新高\nAND 慎滞严格放量\nAND NOT(扩张保护期)\nAND NOT(初扩早期险过滤);`,
  `慎源原:=慎滞高位背景\nAND 阶段高位不创新高\nAND 慎滞严格放量;\n\n慎保护许可:=NOT(扩张保护期)\nAND NOT(初扩早期险过滤);\n\n慎源:=慎源原\nAND 慎保护许可;`,
  '慎源拆分',
);

text = replaceOrThrow(
  text,
  `滞弱化:=滞收阴\nOR 滞小实体\nOR 滞长上\nOR 滞低前收\nOR 滞破短线\nOR 滞冲回;`,
  `滞强弱化:=滞长上\nOR 滞破短线\nOR 滞冲回;\n\n滞轻弱化:=滞收阴\nOR 滞小实体\nOR 滞低前收;\n\n滞弱化:=滞强弱化 OR 滞轻弱化;`,
  '滞强轻拆分',
);

const show = `{二十七、显示控制：0/1归一化正式版，蓝暴优先于速显、蓝温}

首启标:=IF(首扩启,1,0);
险标:=IF(险,1,0);
败标:=IF(上败,1,0);

蓝暴有效标:=IF(蓝暴有效,1,0);
蓝温有效标:=IF(蓝温有效,1,0);
速有效标:=IF(速有效,1,0);
冲有效标:=IF(冲有效,1,0);
黄暴有效标:=IF(黄暴有效,1,0);
黄温有效标:=IF(黄温有效,1,0);
确标:=IF(确,1,0);
警源标:=IF(启后长上警 OR 准启长上警,1,0);

慎源标:=IF(慎源,1,0);
滞源标:=IF(滞源,1,0);

首扩显:=IF(显示许可 AND 首启标=1 AND 险标=0 AND 败标=0,1,0);

蓝暴最终:=IF(显示许可
AND 蓝暴有效标=1
AND 首扩显=0
AND 险标=0
AND 败标=0,1,0);

速显:=IF(显示许可
AND 速有效标=1
AND 首扩显=0
AND 蓝暴最终=0
AND 险标=0
AND 败标=0,1,0);

蓝温显:=IF(显示许可
AND 蓝温有效标=1
AND 首扩显=0
AND 蓝暴最终=0
AND 速显=0
AND 险标=0
AND 败标=0,1,0);

冲显:=IF(显示许可
AND 冲有效标=1
AND 首扩显=0
AND 蓝暴最终=0
AND 速显=0
AND 蓝温显=0
AND 险标=0
AND 败标=0,1,0);

黄暴显:=IF(显示许可
AND 黄暴有效标=1
AND 首扩显=0
AND 蓝暴最终=0
AND 速显=0
AND 蓝温显=0
AND 冲显=0
AND 险标=0
AND 败标=0,1,0);

黄温显:=IF(显示许可
AND 黄温有效标=1
AND 首扩显=0
AND 蓝暴最终=0
AND 速显=0
AND 蓝温显=0
AND 冲显=0
AND 黄暴显=0
AND 险标=0
AND 败标=0,1,0);

确显:=IF(显示许可
AND 确标=1
AND 首扩显=0
AND 蓝暴最终=0
AND 速显=0
AND 蓝温显=0
AND 冲显=0
AND 黄暴显=0
AND 黄温显=0
AND 险标=0
AND 败标=0,1,0);

警显:=IF(显示许可 AND 警源标=1 AND 险标=0 AND 败标=0,1,0);

滞显:=IF(显示许可 AND 滞源标=1 AND 险标=0 AND 败标=0,1,0);

慎显:=IF(显示许可
AND 慎源标=1
AND 滞显=0
AND 险标=0
AND 败标=0,1,0);

险显:=IF(显示许可 AND 险标=1,1,0);
败显:=IF(显示许可 AND 败标=1,1,0);

{二十八、图形显示}
STICKLINE(首扩显=1,-0.05,1.1,4,0),COLORRED;
DRAWTEXT(首扩显=1,1.05,'启'),COLORRED;

STICKLINE(蓝暴最终=1,-0.05,1.1,5,0),COLORCYAN;
DRAWTEXT(蓝暴最终=1,0.88,'蓝暴'),COLORCYAN;

STICKLINE(速显=1,-0.05,1.1,4,0),COLORMAGENTA;
DRAWTEXT(速显=1,1.05,'速'),COLORMAGENTA;

STICKLINE(蓝温显=1,-0.05,1.1,2,0),COLORCYAN;

DRAWTEXT(冲显=1,1.05,'冲'),COLORFF00FF;

STICKLINE(黄暴显=1,-0.05,1.1,5,0),COLORYELLOW;
STICKLINE(黄温显=1,-0.05,1.1,2,0),COLORYELLOW;

DRAWTEXT(确显=1,1.08,'确'),COLORYELLOW;

DRAWTEXT(警显=1,1.00,'警'),COLORFF9900;

DRAWTEXT(滞显=1,0.78,'滞'),COLORFF6600;
DRAWTEXT(慎显=1,0.62,'慎'),COLORFF9900;

STICKLINE(险显=1,-0.05,1.1,2,0),COLORFF80FF;
DRAWTEXT(险显=1,1.05,'险'),COLORFF80FF;

STICKLINE(败显=1,-0.05,1.1,5,0),COLORGRAY;
DRAWTEXT(败显=1,0.50,'败'),COLORGRAY;
`;

const showStart = text.indexOf('{二十七、显示控制');
if (showStart < 0) throw new Error('missing display section');
text = text.slice(0, showStart) + show;

fs.writeFileSync(path.join(root, 'formula-v1-draft.txt'), text, 'utf8');

const now = new Date();
const notes = `# formula-v1-change-notes

生成时间：${now.toLocaleString('zh-CN', { hour12: false })}

## 定位

这是整理版公式草案 v1，不是最终版。

v1 只纳入已经讨论确认的结构性优化，暂不主动调整尚需验证的参数。

## 已写入 v1 的主要内容

- 增加 \`有效周期 / 足够K / 显示许可\`，只作用于最终显示层。
- \`SQN\` 月线从 2 改为 3。
- 更新 \`近挤 / 效挤\`。
- 新增 \`分散挤原 / 挤压宽许可 / 新版有效挤压\`。
- 新增 \`迟发挤压背景\` 及宽度未扩判断链。
- \`突破背景\` 增加 \`迟发挤压背景\`。
- 成交额改为 \`AMT0 / 有额\` 防空值版本。
- 删除无用变量：\`启动前相低 / 阴强 / 长下 / 强空 / 初空 / 蓝显示许可\`。
- 删除多处重复条件。
- \`蓝挤压背景\` 改用新版 \`有效挤压\`。
- \`优质黄背景\` 改为 \`蓝优质背景\`。
- 新增 \`昨收缩突破背景\`。
- 冷却占用信号改用 \`蓝有效 / 黄可显示占用原\`。
- \`近期强推\` 改用 \`蓝有效\`。
- 确认信号改为 \`确2 / 确3 / 确4 / 险反\`，取消 \`确1\`。
- 高位放量创新高风险拆成 \`可保护险 / 硬险\`。
- 最终风险出口增加 \`不可早期过滤硬险\`。
- \`慎源\` 拆成 \`慎源原 / 慎保护许可 / 慎源\`。
- 增加 \`滞强弱化 / 滞轻弱化\` 诊断变量。
- 最终显示层统一加入 \`显示许可\`，图形显示使用 0/1 标记。
- \`前5高点PCTB\` 动态引用改为固定展开。

## 暂未写入主公式、后续进验证副图的内容

- 强收中阳替代 \`阳强\`。
- 温上承接不足过滤。
- 连续小阳慢推信号。
- 上败弱化版。
- 早期趋势健康扩展。
- 保护期走出失效。
- 保护用收缩 / 保护用初扩 / 保护用低点新鲜。
- 高险跌坏冲回。
- 黄后确认候选。
- 平台高波动自适应。
- 成交额分位过滤。
- 带宽自适应参考。

## 需要人工/编译检查

- 东方财富通是否接受 \`BARSCOUNT\`、多行 \`IF\`、多层固定展开。
- \`VOL*C*100\` 作为 \`AMOUNT\` 兜底是否符合你的数据口径。
- \`确2/确3/确4\` 的最终条件是否完全符合你希望的确认逻辑。
- \`黄可显示占用原\` 没有使用 \`黄色显示许可 / 黄色新鲜许可\`，是为了避免冷却链条循环引用；后续可在验证副图观察影响。
- \`重置有效挤压\` 暂未改为新版 \`有效挤压\`，避免未经确认影响首扩重置。

## 下一步建议

1. 先做文本级检查：旧变量残留、动态 REF、显示许可覆盖、关键变量存在。
2. 再由你粘贴到东方财富通编译，记录是否报错。
3. 如果编译通过，再开始设计验证副图 v1。
`;

fs.writeFileSync(path.join(root, 'formula-v1-change-notes.md'), notes, 'utf8');
console.log('written formula-v1-draft.txt', text.length);
console.log('written formula-v1-change-notes.md');
