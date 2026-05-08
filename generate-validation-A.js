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

const appendix = `

{================ 验证副图A：基础 / 背景 / 源头 ================}
{定位：本副图用于诊断某根K线是否具备潜在信号基础，不作为正式交易信号。}

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

{A图核心数值线：都压在0-1.5附近，便于观察}
实占线:实占,COLORWHITE,DOTLINE;
上影线:上影,COLORRED,DOTLINE;
收盘位线:收盘位,COLORGREEN,DOTLINE;
额比线:MIN(额比,3)/3,COLORCYAN,DOTLINE;
宽比线:MIN(当前宽比,2)/2,COLORMAGENTA,DOTLINE;
二年位线:二年位,COLORGRAY,DOTLINE;

{A1状态提示}
DRAWTEXT(阳强,0.12,'阳强'),COLORRED;
DRAWTEXT(强收中阳候选,0.20,'中阳'),COLORFF9900;
DRAWTEXT(长上,0.28,'长上'),COLORFF80FF;
DRAWTEXT(明显长上,0.36,'明上'),COLORFF80FF;
DRAWTEXT(极端长上,0.44,'极上影'),COLORFF80FF;
DRAWTEXT(温额,0.52,'温额'),COLORYELLOW;
DRAWTEXT(放额,0.60,'放额'),COLORRED;
DRAWTEXT(巨额,0.68,'巨额'),COLORMAGENTA;
DRAWTEXT(较昨放额,0.76,'较昨'),COLORCYAN;
DRAWTEXT(较前5放额,0.84,'破量'),COLORCYAN;

{A2背景提示}
DRAWTEXT(挤压,-0.10,'挤'),COLORMAGENTA;
DRAWTEXT(效挤,-0.18,'效'),COLORCYAN;
DRAWTEXT(分散挤原,-0.26,'散'),COLORCYAN;
DRAWTEXT(有效挤压,-0.34,'有挤'),COLORCYAN;
DRAWTEXT(迟发挤压背景,-0.42,'迟'),COLORFF9900;
DRAWTEXT(真正收缩,-0.50,'缩'),COLORGREEN;
DRAWTEXT(启动前持宽,-0.58,'持宽'),COLORGRAY;
DRAWTEXT(宽近高,-0.66,'近高'),COLORGRAY;
DRAWTEXT(首扩宽度许可,-0.74,'宽许'),COLORGREEN;

{A3源头提示}
DRAWTEXT(有效上穿1,0.92,'上穿'),COLORYELLOW;
DRAWTEXT(突破背景,1.00,'背景'),COLORGREEN;
DRAWTEXT(温上,1.08,'温'),COLORYELLOW;
DRAWTEXT(暴上,1.16,'暴'),COLORRED;
DRAWTEXT(极上,1.24,'极'),COLORMAGENTA;
DRAWTEXT(中位收缩突破,1.32,'中'),COLORYELLOW;
DRAWTEXT(首扩候选,1.40,'首候'),COLORRED;
DRAWTEXT(首扩启,1.48,'启'),COLORRED;
DRAWTEXT(扩后再缩原,1.56,'速源'),COLORMAGENTA;
DRAWTEXT(速有效,1.64,'速'),COLORMAGENTA;
DRAWTEXT(冲候选预,1.72,'冲源'),COLORFF00FF;
DRAWTEXT(冲有效,1.80,'冲'),COLORFF00FF;
DRAWTEXT(蓝优质背景,1.88,'蓝背'),COLORCYAN;
DRAWTEXT(蓝信号源,1.96,'蓝源'),COLORCYAN;
DRAWTEXT(黄信号源,2.04,'黄源'),COLORYELLOW;
`;

fs.writeFileSync('validation-indicator-A-draft.txt', `${base}${appendix}\n`, 'utf8');
console.log('generated validation-indicator-A-draft.txt');
