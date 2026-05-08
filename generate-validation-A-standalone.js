const fs = require('fs');

const source = fs.readFileSync('formula-v1-draft.txt', 'utf8');
const lines = source.split(/\r?\n/);

const endMarker = '黄信号源:=黄温源 OR 黄暴源;';
const endIndex = lines.findIndex((line) => line.trim() === endMarker);

if (endIndex < 0) {
  throw new Error(`Missing marker: ${endMarker}`);
}

let base = lines.slice(0, endIndex + 1).join('\n');

// v2 confirmed correction: use 1.10 for the middle breakout split.
base = base
  .replace('中位温上:=中位收缩突破 AND PCTB<1.105;', '中位温上:=中位收缩突破 AND PCTB<1.10;')
  .replace('中位暴上:=中位收缩突破 AND PCTB>=1.105;', '中位暴上:=中位收缩突破 AND PCTB>=1.10;');

// Standalone validation chart: turn early plotted lines into internal variables.
// EastMoney often gives display priority to earlier output series, so validation
// charts should avoid inheriting the original plotted PCTB/reference outputs.
base = base
  .replace('PCTB:(C-BDN)/MAX(BUP-BDN,0.0001),COLORYELLOW,LINETHICK2;', 'PCTB:=(C-BDN)/MAX(BUP-BDN,0.0001);')
  .replace('超买:1,COLORRED,DOTLINE;', '超买线:=1;')
  .replace('中轴:0.5,COLORGRAY,DOTLINE;', '中轴线:=0.5;')
  .replace('超卖:0,COLORGREEN,DOTLINE;', '超卖线:=0;')
  .replace('极上线:1+深限,COLORMAGENTA,DOTLINE;', '极上线值:=1+深限;')
  .replace('极下线:0-深限,COLORCYAN,DOTLINE;', '极下线值:=0-深限;')
  .replace('STICKLINE(挤压,-0.05,-0.02,5,0),COLORMAGENTA;', '{原挤压显示移到A图显示层}');

const appendix = `

{================ 验证副图A-独立显示版 ================}
{定位：不继承原PCTB输出，只显示基础 / 背景 / 源头诊断。}

{A0、显示范围与核心线}
A顶:2.20,COLORGRAY,DOTLINE;
A底:-0.90,COLORGRAY,DOTLINE;
PCTB线:MIN(MAX(PCTB,-0.30),1.30),COLORYELLOW,LINETHICK2;

{A1、基础K线 / 价格位置 / 成交额补充}
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

{A1、基础状态柱}
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

{A2、背景状态柱}
STICKLINE(挤压,-0.08,-0.14,2,0),COLORMAGENTA;
STICKLINE(效挤,-0.17,-0.23,2,0),COLORCYAN;
STICKLINE(分散挤原,-0.26,-0.32,2,0),COLORCYAN;
STICKLINE(有效挤压,-0.35,-0.41,2,0),COLORCYAN;
STICKLINE(迟发挤压背景,-0.44,-0.50,2,0),COLORFF9900;
STICKLINE(真正收缩,-0.53,-0.59,2,0),COLORGREEN;
STICKLINE(启动前持宽,-0.62,-0.68,2,0),COLORGRAY;
STICKLINE(宽近高,-0.71,-0.77,2,0),COLORGRAY;
STICKLINE(首扩宽度许可,-0.80,-0.86,2,0),COLORGREEN;

DRAWTEXT(挤压,-0.08,'挤'),COLORMAGENTA;
DRAWTEXT(效挤,-0.17,'效'),COLORCYAN;
DRAWTEXT(分散挤原,-0.26,'散'),COLORCYAN;
DRAWTEXT(有效挤压,-0.35,'有'),COLORCYAN;
DRAWTEXT(迟发挤压背景,-0.44,'迟'),COLORFF9900;
DRAWTEXT(真正收缩,-0.53,'缩'),COLORGREEN;
DRAWTEXT(启动前持宽,-0.62,'持'),COLORGRAY;
DRAWTEXT(宽近高,-0.71,'近'),COLORGRAY;
DRAWTEXT(首扩宽度许可,-0.80,'宽'),COLORGREEN;

{A3、源头状态柱}
STICKLINE(有效上穿1,1.02,1.08,2,0),COLORYELLOW;
STICKLINE(突破背景,1.11,1.17,2,0),COLORGREEN;
STICKLINE(温上,1.20,1.26,2,0),COLORYELLOW;
STICKLINE(暴上,1.29,1.35,2,0),COLORRED;
STICKLINE(极上,1.38,1.44,2,0),COLORMAGENTA;
STICKLINE(中位收缩突破,1.47,1.53,2,0),COLORYELLOW;
STICKLINE(首扩候选,1.56,1.62,2,0),COLORRED;
STICKLINE(首扩启,1.65,1.71,2,0),COLORRED;
STICKLINE(扩后再缩原,1.74,1.80,2,0),COLORMAGENTA;
STICKLINE(速有效,1.83,1.89,2,0),COLORMAGENTA;
STICKLINE(冲候选预,1.92,1.98,2,0),COLORFF00FF;
STICKLINE(冲有效,2.01,2.07,2,0),COLORFF00FF;
STICKLINE(蓝优质背景,2.10,2.16,2,0),COLORCYAN;
STICKLINE(蓝信号源,2.10,2.20,4,0),COLORCYAN;
STICKLINE(黄信号源,2.10,2.20,1,0),COLORYELLOW;

DRAWTEXT(有效上穿1,1.08,'穿'),COLORYELLOW;
DRAWTEXT(突破背景,1.17,'背'),COLORGREEN;
DRAWTEXT(温上,1.26,'温'),COLORYELLOW;
DRAWTEXT(暴上,1.35,'暴'),COLORRED;
DRAWTEXT(极上,1.44,'极'),COLORMAGENTA;
DRAWTEXT(中位收缩突破,1.53,'中'),COLORYELLOW;
DRAWTEXT(首扩候选,1.62,'候'),COLORRED;
DRAWTEXT(首扩启,1.71,'启'),COLORRED;
DRAWTEXT(扩后再缩原,1.80,'速源'),COLORMAGENTA;
DRAWTEXT(速有效,1.89,'速'),COLORMAGENTA;
DRAWTEXT(冲候选预,1.98,'冲源'),COLORFF00FF;
DRAWTEXT(冲有效,2.07,'冲'),COLORFF00FF;
DRAWTEXT(蓝优质背景,2.16,'蓝背'),COLORCYAN;
DRAWTEXT(蓝信号源,2.20,'蓝'),COLORCYAN;
DRAWTEXT(黄信号源,2.20,'黄'),COLORYELLOW;
`;

fs.writeFileSync('validation-indicator-A-standalone-draft.txt', `${base}${appendix}\n`, 'utf8');
console.log('generated validation-indicator-A-standalone-draft.txt');
