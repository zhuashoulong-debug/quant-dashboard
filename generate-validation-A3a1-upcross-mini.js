const fs = require('fs');

const formula = `日线:=PERIOD=5;
周线:=PERIOD=6;
月线:=PERIOD=7;
有效周期:=日线 OR 周线 OR 月线;
足够K:=BARSCOUNT(C)>IF(周线,80,IF(月线,48,120));
显示许可:=有效周期 AND 足够K;

BBN:=IF(周线,13,IF(月线,12,20));
P:=2;

MID:=MA(C,BBN);
TMP:=STD(C,BBN);
BUP:=MID+P*TMP;
BDN:=MID-P*TMP;
PCTB:=(C-BDN)/MAX(BUP-BDN,0.0001);

图顶:1.30,COLORGRAY,DOTLINE;
图底:-0.30,COLORGRAY,DOTLINE;
PCTB线:MIN(MAX(PCTB,-0.30),1.30),COLORYELLOW,LINETHICK2;

轨上:=PCTB>1;
STICKLINE(显示许可 AND 轨上,0.06,0.18,1,0),COLORCYAN;
DRAWTEXT(显示许可 AND 轨上 AND NOT(REF(轨上,1)),0.20,'轨'),COLORCYAN;

手工上穿:=REF(PCTB,1)<1 AND PCTB>=1;
STICKLINE(显示许可 AND 手工上穿,0.32,0.48,2,0),COLORWHITE;
DRAWTEXT(显示许可 AND 手工上穿,0.50,'手'),COLORWHITE;

CROSS上穿:=CROSS(PCTB,1);
STICKLINE(显示许可 AND CROSS上穿,0.58,0.76,3,0),COLORYELLOW;
DRAWTEXT(显示许可 AND CROSS上穿,0.78,'C'),COLORYELLOW;

上穿回撤N:=IF(周线,3,IF(月线,2,5));
上穿回撤阈:=IF(周线,0.88,IF(月线,0.90,0.85));
上穿前低P:=REF(LLV(PCTB,上穿回撤N),1);
近期曾在轨上:=REF(COUNT(PCTB>1,上穿回撤N),1)>=1;
浅绕回上穿:=近期曾在轨上 AND 上穿前低P>上穿回撤阈;
STICKLINE(显示许可 AND CROSS上穿 AND 浅绕回上穿,0.84,0.98,2,0),COLORGRAY;
DRAWTEXT(显示许可 AND CROSS上穿 AND 浅绕回上穿,1.00,'浅'),COLORGRAY;

有效上穿1:=CROSS上穿 AND NOT(浅绕回上穿);
STICKLINE(显示许可 AND 有效上穿1,1.06,1.24,3,0),COLORRED;
DRAWTEXT(显示许可 AND 有效上穿1,1.26,'效'),COLORRED;

{读法：青=轨上；白=手工上穿；黄=CROSS；灰=浅绕过滤；红=有效上穿。}`;

fs.writeFileSync('validation-indicator-A3a1-upcross-mini-draft.txt', formula, 'utf8');
console.log('generated validation-indicator-A3a1-upcross-mini-draft.txt');
