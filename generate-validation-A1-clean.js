const fs = require('fs');

const formula = `日线:=PERIOD=5;
周线:=PERIOD=6;
月线:=PERIOD=7;

有效周期:=日线 OR 周线 OR 月线;
足够K:=BARSCOUNT(C)>IF(周线,80,IF(月线,48,120));
显示许可:=有效周期 AND 足够K;

BBN:=IF(周线,13,IF(月线,12,20));
VN:=IF(周线,13,IF(月线,12,20));

P:=2;
BP:=0.45;
YP:=0.45;
VP:=1.2;
BVP:=1.8;

{一、PCTB基础}
MID:=MA(C,BBN);
TMP:=STD(C,BBN);
BUP:=MID+P*TMP;
BDN:=MID-P*TMP;
PCTB:=(C-BDN)/MAX(BUP-BDN,0.0001);

{二、K线质量}
K幅:=MAX(H-L,0.0001);
实体:=ABS(C-O);
实占:=实体/K幅;
上影:=(H-MAX(C,O))/K幅;
下影:=(MIN(C,O)-L)/K幅;
收盘位:=(C-L)/K幅;

阳强:=C>O AND 实占>=BP;
长上:=上影>=YP;
明显长上:=上影>=0.55;
极端长上:=上影>=0.65;

强收中阳候选:=C>O
AND 收盘位>=0.70
AND 实占>=0.30
AND NOT(长上);

{三、成交额}
AMT0:=IF(AMOUNT>0,AMOUNT,VOL*C*100);
均额:=MA(AMT0,VN);
有额:=AMT0>0 AND 均额>0;

温额:=有额 AND AMT0>=均额;
放额:=有额 AND AMT0>=均额*VP;
巨额:=有额 AND AMT0>=均额*BVP;

额比:=AMT0/MAX(均额,0.0001);
较昨额比:=AMT0/MAX(REF(AMT0,1),0.0001);
近5最高额:=REF(HHV(AMT0,5),1);
较前5高额比:=AMT0/MAX(近5最高额,0.0001);

较昨放额:=较昨额比>=1.20;
较前5放额:=较前5高额比>=1.20;

{四、A1精简显示}
图顶:1.30,COLORGRAY,DOTLINE;
图底:-0.30,COLORGRAY,DOTLINE;
PCTB线:MIN(MAX(PCTB,-0.30),1.30),COLORYELLOW,LINETHICK2;

{低区：上影风险}
STICKLINE(显示许可 AND 长上,0.16,0.22,1,0),COLORFF80FF;
STICKLINE(显示许可 AND 明显长上,0.24,0.30,2,0),COLORFF80FF;
STICKLINE(显示许可 AND 极端长上,0.32,0.40,3,0),COLORMAGENTA;

{中区：实体质量}
STICKLINE(显示许可 AND 阳强,0.48,0.54,1,0),COLORRED;
STICKLINE(显示许可 AND 强收中阳候选,0.56,0.64,2,0),COLORFF9900;

{高区：量能}
STICKLINE(显示许可 AND 放额,0.74,0.80,2,0),COLORRED;
STICKLINE(显示许可 AND 巨额,0.82,0.90,3,0),COLORMAGENTA;
STICKLINE(显示许可 AND 较前5放额,0.94,1.02,2,0),COLORCYAN;

{只标关键文字，避免满屏重复}
DRAWTEXT(显示许可 AND 极端长上,0.42,'极上'),COLORMAGENTA;
DRAWTEXT(显示许可 AND 明显长上 AND NOT(极端长上),0.32,'长上'),COLORFF80FF;
DRAWTEXT(显示许可 AND 强收中阳候选,0.66,'中阳'),COLORFF9900;
DRAWTEXT(显示许可 AND 巨额,0.92,'巨'),COLORMAGENTA;
DRAWTEXT(显示许可 AND 放额 AND NOT(巨额),0.82,'放'),COLORRED;
DRAWTEXT(显示许可 AND 较前5放额,1.04,'量'),COLORCYAN;

{A1精简说明：低区=上影风险，中区=实体质量，高区=量能。详细数值看A1-front。}
`;

fs.writeFileSync('validation-indicator-A1-clean-draft.txt', formula, 'utf8');
console.log('generated validation-indicator-A1-clean-draft.txt');
