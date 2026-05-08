const fs = require('fs');

const source = fs.readFileSync('formula-v1-draft.txt', 'utf8');
const lines = source.split(/\r?\n/);

function indexOfLine(marker) {
  const index = lines.findIndex((line) => line.trim() === marker);
  if (index < 0) {
    throw new Error(`Missing marker: ${marker}`);
  }
  return index;
}

function prepareBase(untilMarker) {
  const endIndex = indexOfLine(untilMarker);
  let base = lines.slice(0, endIndex + 1).join('\n');

  base = base
    .replace(
      'PCTB:(C-BDN)/MAX(BUP-BDN,0.0001),COLORYELLOW,LINETHICK2;',
      [
        'PCTB:=(C-BDN)/MAX(BUP-BDN,0.0001);',
        '',
        '{验证副图提前输出：保证东方财富通识别输出项}',
        '图顶:1.30,COLORGRAY,DOTLINE;',
        '图底:-0.30,COLORGRAY,DOTLINE;',
        'PCTB线:MIN(MAX(PCTB,-0.30),1.30),COLORYELLOW,LINETHICK2;'
      ].join('\n')
    )
    .replace('超买:1,COLORRED,DOTLINE;', '超买线:=1;')
    .replace('中轴:0.5,COLORGRAY,DOTLINE;', '中轴线:=0.5;')
    .replace('超卖:0,COLORGREEN,DOTLINE;', '超卖线:=0;')
    .replace('极上线:1+深限,COLORMAGENTA,DOTLINE;', '极上线值:=1+深限;')
    .replace('极下线:0-深限,COLORCYAN,DOTLINE;', '极下线值:=0-深限;')
    .replace('STICKLINE(挤压,-0.05,-0.02,5,0),COLORMAGENTA;', '{原挤压显示移到验证副图显示层}');

  return base;
}

const a1Base = prepareBase('巨额:=有额 AND AMT0>=均额*BVP;');

const a1Appendix = `

{================ 验证A1：基础K线 / 价格位置 / 成交额 ================}
收盘位:=(C-L)/K幅;
阳线:=C>O;
阴线:=C<O;

涨跌幅:=C/MAX(REF(C,1),0.0001)-1;
振幅:=K幅/MAX(REF(C,1),0.0001);
跳空幅度:=O/MAX(REF(C,1),0.0001)-1;
盘中冲高回落比:=(H-C)/K幅;

额比:=AMT0/MAX(均额,0.0001);
较昨额比:=AMT0/MAX(REF(AMT0,1),0.0001);
近5最高额:=REF(HHV(AMT0,5),1);
较前5高额比:=AMT0/MAX(近5最高额,0.0001);
较昨放额:=较昨额比>=1.20;
较前5放额:=较前5高额比>=1.20;

强收中阳候选:=C>O
AND 收盘位>=0.70
AND 实占>=0.30
AND NOT(长上);

实占线:实占,COLORWHITE,DOTLINE;
上影线:上影,COLORRED,DOTLINE;
收盘位线:收盘位,COLORGREEN,DOTLINE;
额比线:MIN(额比,3)/3,COLORCYAN,DOTLINE;

STICKLINE(阳强,0.05,0.11,2,0),COLORRED;
STICKLINE(强收中阳候选,0.14,0.20,2,0),COLORFF9900;
STICKLINE(长上,0.23,0.29,2,0),COLORFF80FF;
STICKLINE(明显长上,0.32,0.38,2,0),COLORFF80FF;
STICKLINE(极端长上,0.41,0.47,2,0),COLORFF80FF;
STICKLINE(温额,0.50,0.56,2,0),COLORYELLOW;
STICKLINE(放额,0.59,0.65,2,0),COLORRED;
STICKLINE(巨额,0.68,0.74,2,0),COLORMAGENTA;
STICKLINE(较昨放额,0.77,0.83,2,0),COLORCYAN;
STICKLINE(较前5放额,0.86,0.92,2,0),COLORCYAN;

DRAWTEXT(阳强,0.11,'阳'),COLORRED;
DRAWTEXT(强收中阳候选,0.20,'中'),COLORFF9900;
DRAWTEXT(长上,0.29,'上'),COLORFF80FF;
DRAWTEXT(温额,0.56,'温'),COLORYELLOW;
DRAWTEXT(放额,0.65,'放'),COLORRED;
DRAWTEXT(巨额,0.74,'巨'),COLORMAGENTA;
DRAWTEXT(较昨放额,0.83,'昨'),COLORCYAN;
DRAWTEXT(较前5放额,0.92,'量'),COLORCYAN;
`;

const a2Base = prepareBase('真正收缩:=有效挤压 OR (压缩低位 AND 收缩过程);');

const a2Appendix = `

{================ 验证A2：挤压 / 收缩 / 宽度背景 ================}
宽比线:MIN(当前宽比,2)/2,COLORMAGENTA,DOTLINE;
二年位线:二年位,COLORGRAY,DOTLINE;

STICKLINE(挤压,0.05,0.11,2,0),COLORMAGENTA;
STICKLINE(效挤,0.14,0.20,2,0),COLORCYAN;
STICKLINE(分散挤原,0.23,0.29,2,0),COLORCYAN;
STICKLINE(有效挤压,0.32,0.38,2,0),COLORCYAN;
STICKLINE(迟发挤压背景,0.41,0.47,2,0),COLORFF9900;
STICKLINE(收缩幅度,0.50,0.56,2,0),COLORGREEN;
STICKLINE(压缩低位,0.59,0.65,2,0),COLORGREEN;
STICKLINE(有效缩窄,0.68,0.74,2,0),COLORGREEN;
STICKLINE(真正收缩,0.77,0.83,2,0),COLORGREEN;
STICKLINE(启动前持宽,0.86,0.92,2,0),COLORGRAY;
STICKLINE(宽近高,0.95,1.01,2,0),COLORGRAY;
STICKLINE(首扩宽度许可,1.04,1.10,2,0),COLORRED;

DRAWTEXT(挤压,0.11,'挤'),COLORMAGENTA;
DRAWTEXT(效挤,0.20,'效'),COLORCYAN;
DRAWTEXT(分散挤原,0.29,'散'),COLORCYAN;
DRAWTEXT(有效挤压,0.38,'有'),COLORCYAN;
DRAWTEXT(迟发挤压背景,0.47,'迟'),COLORFF9900;
DRAWTEXT(收缩幅度,0.56,'幅'),COLORGREEN;
DRAWTEXT(压缩低位,0.65,'低'),COLORGREEN;
DRAWTEXT(有效缩窄,0.74,'窄'),COLORGREEN;
DRAWTEXT(真正收缩,0.83,'缩'),COLORGREEN;
DRAWTEXT(启动前持宽,0.92,'持'),COLORGRAY;
DRAWTEXT(宽近高,1.01,'近'),COLORGRAY;
DRAWTEXT(首扩宽度许可,1.10,'宽'),COLORRED;
`;

fs.writeFileSync('validation-indicator-A1-basic-draft.txt', `${a1Base}${a1Appendix}\n`, 'utf8');
fs.writeFileSync('validation-indicator-A2-background-draft.txt', `${a2Base}${a2Appendix}\n`, 'utf8');

let a3Base = prepareBase('黄信号源:=黄温源 OR 黄暴源;');
a3Base = a3Base
  .replace('中位温上:=中位收缩突破 AND PCTB<1.105;', '中位温上:=中位收缩突破 AND PCTB<1.10;')
  .replace('中位暴上:=中位收缩突破 AND PCTB>=1.105;', '中位暴上:=中位收缩突破 AND PCTB>=1.10;');

const a3Appendix = `

{================ 验证A3：启动源头 / 蓝黄来源 ================}
源头码:=IF(首扩启,1,
IF(速有效,2,
IF(冲有效,3,
IF(蓝信号源,4,
IF(黄信号源,5,
IF(有效上穿1,6,0))))));

背景码:=IF(蓝优质背景,4,
IF(突破背景,3,
IF(迟发挤压背景,2,
IF(有效挤压,1,0))));

源头码线:源头码/6,COLORWHITE,LINETHICK2;
背景码线:背景码/4,COLORCYAN,DOTLINE;

STICKLINE(有效上穿1,0.05,0.11,2,0),COLORYELLOW;
STICKLINE(突破背景,0.14,0.20,2,0),COLORGREEN;
STICKLINE(温上,0.23,0.29,2,0),COLORYELLOW;
STICKLINE(暴上,0.32,0.38,2,0),COLORRED;
STICKLINE(极上,0.41,0.47,2,0),COLORMAGENTA;
STICKLINE(中位收缩突破,0.50,0.56,2,0),COLORYELLOW;
STICKLINE(首扩候选,0.59,0.65,2,0),COLORRED;
STICKLINE(首扩启,0.68,0.74,2,0),COLORRED;
STICKLINE(扩后再缩原,0.77,0.83,2,0),COLORMAGENTA;
STICKLINE(速有效,0.86,0.92,2,0),COLORMAGENTA;
STICKLINE(冲候选预,0.95,1.01,2,0),COLORFF00FF;
STICKLINE(冲有效,1.04,1.10,2,0),COLORFF00FF;
STICKLINE(蓝优质背景,1.13,1.19,2,0),COLORCYAN;
STICKLINE(蓝信号源,1.22,1.28,2,0),COLORCYAN;
STICKLINE(黄信号源,1.22,1.28,1,0),COLORYELLOW;

DRAWTEXT(有效上穿1,0.11,'穿'),COLORYELLOW;
DRAWTEXT(突破背景,0.20,'背'),COLORGREEN;
DRAWTEXT(温上,0.29,'温'),COLORYELLOW;
DRAWTEXT(暴上,0.38,'暴'),COLORRED;
DRAWTEXT(极上,0.47,'极'),COLORMAGENTA;
DRAWTEXT(中位收缩突破,0.56,'中'),COLORYELLOW;
DRAWTEXT(首扩候选,0.65,'候'),COLORRED;
DRAWTEXT(首扩启,0.74,'启'),COLORRED;
DRAWTEXT(扩后再缩原,0.83,'速源'),COLORMAGENTA;
DRAWTEXT(速有效,0.92,'速'),COLORMAGENTA;
DRAWTEXT(冲候选预,1.01,'冲源'),COLORFF00FF;
DRAWTEXT(冲有效,1.10,'冲'),COLORFF00FF;
DRAWTEXT(蓝优质背景,1.19,'蓝背'),COLORCYAN;
DRAWTEXT(蓝信号源,1.28,'蓝'),COLORCYAN;
DRAWTEXT(黄信号源,1.28,'黄'),COLORYELLOW;
`;

fs.writeFileSync('validation-indicator-A3-source-draft.txt', `${a3Base}${a3Appendix}\n`, 'utf8');

console.log('generated validation-indicator-A1-basic-draft.txt');
console.log('generated validation-indicator-A2-background-draft.txt');
console.log('generated validation-indicator-A3-source-draft.txt');
