const fs = require('fs');

const formula = `日线:=PERIOD=5;
周线:=PERIOD=6;
月线:=PERIOD=7;
有效周期:=日线 OR 周线 OR 月线;
足够K:=BARSCOUNT(C)>IF(周线,80,IF(月线,48,120));
显示许可:=有效周期 AND 足够K;

BBN:=IF(周线,13,IF(月线,12,20));
KCN:=IF(周线,13,IF(月线,12,20));
MAN:=IF(周线,8,IF(月线,6,13));
VN:=IF(周线,13,IF(月线,12,20));
BRN:=IF(周线,13,IF(月线,12,20));
TN:=IF(周线,26,IF(月线,24,60));
TM:=IF(周线,5,IF(月线,3,10));
WM:=IF(周线,26,IF(月线,24,60));
WRP:=0.85;

P:=2;
KCP:=1.5;
深限:=IF(周线,0.25,IF(月线,0.20,0.30));
SQN:=IF(周线,3,IF(月线,3,5));
VP:=1.2;
BVP:=1.8;
BP:=0.45;
YP:=0.45;

{一、PCTB基础，马上画}
MID:=MA(C,BBN);
TMP:=STD(C,BBN);
BUP:=MID+P*TMP;
BDN:=MID-P*TMP;
PCTB:=(C-BDN)/MAX(BUP-BDN,0.0001);
图顶:1.30,COLORGRAY,DOTLINE;
图底:-0.30,COLORGRAY,DOTLINE;
PCTB线:MIN(MAX(PCTB,-0.30),1.30),COLORYELLOW,LINETHICK2;

{二、基础质量}
K幅:=MAX(H-L,0.0001);
实体:=ABS(C-O);
实占:=实体/K幅;
上影:=(H-MAX(C,O))/K幅;
阳强:=C>O AND 实占>=BP;
长上:=上影>=YP;

AMT0:=IF(AMOUNT>0,AMOUNT,VOL*C*100);
均额:=MA(AMT0,VN);
有额:=AMT0>0 AND 均额>0;
温额:=有额 AND AMT0>=均额;
放额:=有额 AND AMT0>=均额*VP;
巨额:=有额 AND AMT0>=均额*BVP;

实体高:=MAX(C,O);
实体低:=MIN(C,O);
构上:=C>REF(HHV(实体高,BRN),1);

{三、趋势}
长线:=MA(C,TN);
短线:=MA(C,MAN);
长向:=长线-REF(长线,TM);
短向:=短线-REF(短线,3);
强多:=长向>0 AND C>长线 AND 短线>长线;
初多:=NOT(强多) AND 短向>0 AND C>短线 AND C>长线;
上轨趋势:=C>短线 AND 短向>0 AND (C>长线 OR 初多 OR 强多);

{四、挤压/收缩背景，算完马上画背景柱}
TRV:=MAX(MAX(H-L,ABS(H-REF(C,1))),ABS(L-REF(C,1)));
ATRV:=MA(TRV,KCN);
KCU:=MID+KCP*ATRV;
KCD:=MID-KCP*ATRV;
挤压:=BUP<KCU AND BDN>KCD;
近挤:=COUNT(挤压,2)>=1;
效挤:=IF(日线,COUNT(挤压,5)>=2 AND BARSLAST(挤压)<=2,COUNT(挤压,SQN)>=2);

带宽:=(BUP-BDN)/MAX(MID,0.0001);
长均宽:=MA(带宽,WM);
短均宽:=MA(带宽,BBN);
长高宽:=HHV(带宽,WM);
短高宽:=HHV(带宽,BBN);
长低宽:=LLV(带宽,WM);
短低宽:=LLV(带宽,BBN);
有效宽均:=IF(长均宽>0.001,长均宽,IF(短均宽>0.001,短均宽,带宽));
有效高宽:=IF(长高宽>0.001,长高宽,IF(短高宽>0.001,短高宽,带宽));
有效低宽:=IF(长低宽>0.001,长低宽,IF(短低宽>0.001,短低宽,带宽));
前有效宽均:=IF(REF(有效宽均,1)>0.001,REF(有效宽均,1),MAX(REF(带宽,1),0.0001));
前有效高宽:=IF(REF(有效高宽,1)>0.001,REF(有效高宽,1),MAX(REF(带宽,1),0.0001));
前有效低宽:=IF(REF(有效低宽,1)>0.001,REF(有效低宽,1),MAX(REF(带宽,1),0.0001));
当前宽比:=带宽/MAX(有效宽均,0.0001);
前宽比:=REF(带宽,1)/MAX(前有效宽均,0.0001);
宽比线:MIN(当前宽比,2)/2,COLORMAGENTA,DOTLINE;

带宽绝高线:=IF(周线,0.55,IF(月线,0.80,0.35));
带宽相高线:=IF(周线,1.25,IF(月线,1.30,1.35));
带宽绝高:=带宽>带宽绝高线;
前带宽绝高:=REF(带宽,1)>带宽绝高线;
带宽相高:=当前宽比>带宽相高线 OR 前宽比>带宽相高线;
宽近高:=带宽>=有效高宽*WRP;
宽速N:=IF(周线,3,IF(月线,2,5));
宽速:=带宽-REF(带宽,宽速N);
宽速率:=宽速/MAX(REF(带宽,宽速N),0.0001);
微扩阈:=IF(周线,0.05,IF(月线,0.06,0.04));
硬高宽:=带宽绝高 OR 前带宽绝高 OR 带宽相高;
软持宽:=宽近高 AND 宽速率<=微扩阈;
持宽:=硬高宽 OR 软持宽;
启动前带宽:=REF(带宽,1);
启动前均宽:=前有效宽均;
启动前高宽:=前有效高宽;
启动前宽比:=启动前带宽/MAX(启动前均宽,0.0001);
启动前相高:=启动前带宽/MAX(启动前高宽,0.0001);
启动前绝宽高:=启动前带宽>带宽绝高线;
启动前相宽高:=启动前宽比>带宽相高线;
启动前持宽:=REF(持宽,1);
首扩宽度许可:=NOT(启动前绝宽高 OR 启动前相宽高 OR 启动前持宽);

日分散挤原:=COUNT(挤压,10)>=2 AND COUNT(挤压,3)>=1;
周分散挤原:=COUNT(挤压,7)>=2 AND COUNT(挤压,2)>=1;
月分散挤原:=COUNT(挤压,5)>=2 AND COUNT(挤压,2)>=1;
分散挤原:=IF(日线,日分散挤原,IF(周线,周分散挤原,月分散挤原));
挤压宽许可:=带宽/MAX(前有效宽均,0.0001)<1.15 AND NOT(启动前持宽) AND NOT(REF(宽近高,1));
有效挤压:=(REF(效挤,1) OR 分散挤原) AND 挤压宽许可;

缩窄N:=IF(周线,5,IF(月线,3,10));
缩窄对比N:=缩窄N*2;
缩幅比例:=IF(周线,0.88,IF(月线,0.92,0.85));
低位均比:=IF(周线,1.00,IF(月线,1.05,0.98));
低位低比:=IF(周线,1.25,IF(月线,1.30,1.25));
带宽高点前:=REF(HHV(带宽,缩窄对比N),1);
带宽低点近:=REF(LLV(带宽,缩窄N),1);
收缩幅度:=带宽低点近/MAX(带宽高点前,0.0001)<缩幅比例;
压缩低位:=带宽低点近<前有效宽均*低位均比 OR 带宽低点近<=前有效低宽*低位低比;
缩窄次数:=REF(COUNT(带宽<REF(带宽,1),缩窄N),1);
有效缩窄:=缩窄次数>=IF(周线,2,IF(月线,1,4));
收缩过程:=收缩幅度 OR 有效缩窄;
真正收缩:=有效挤压 OR (压缩低位 AND 收缩过程);

突破背景:=REF(近挤,1) OR REF(真正收缩,1) OR 真正收缩;
蓝优质背景:=有效挤压 OR (REF(真正收缩,1) OR 真正收缩);

STICKLINE(显示许可 AND 突破背景,0.10,0.18,2,0),COLORGREEN;
STICKLINE(显示许可 AND 蓝优质背景,0.20,0.28,2,0),COLORCYAN;

{五、普通上穿源头，算完马上画}
上穿回撤N:=IF(周线,3,IF(月线,2,5));
上穿回撤阈:=IF(周线,0.88,IF(月线,0.90,0.85));
上穿前低P:=REF(LLV(PCTB,上穿回撤N),1);
近期曾在轨上:=REF(COUNT(PCTB>1,上穿回撤N),1)>=1;
浅绕回上穿:=近期曾在轨上 AND 上穿前低P>上穿回撤阈;
有效上穿1:=CROSS(PCTB,1) AND NOT(浅绕回上穿);

温上基:=有效上穿1 AND 突破背景 AND PCTB<1.1 AND REF(PCTB,1)<1;
温上:=温上基 AND (温额 OR 构上) AND NOT(长上);
暴上原:=有效上穿1 AND 突破背景 AND REF(PCTB,1)<1 AND PCTB>=1.1 AND PCTB<1+深限;
暴上:=暴上原 AND (放额 OR 构上) AND 阳强 AND NOT(长上);
极上原:=突破背景 AND REF(PCTB,1)<1 AND PCTB>=1+深限;
极上:=极上原 AND (放额 OR 构上) AND 阳强 AND NOT(长上);

STICKLINE(显示许可 AND 有效上穿1,0.34,0.40,1,0),COLORYELLOW;
STICKLINE(显示许可 AND 温上,0.42,0.50,2,0),COLORYELLOW;
STICKLINE(显示许可 AND 暴上,0.52,0.60,2,0),COLORRED;
STICKLINE(显示许可 AND 极上,0.62,0.70,2,0),COLORMAGENTA;
DRAWTEXT(显示许可 AND 温上,0.52,'温'),COLORYELLOW;
DRAWTEXT(显示许可 AND 暴上,0.62,'暴'),COLORRED;
DRAWTEXT(显示许可 AND 极上,0.72,'极'),COLORMAGENTA;

{六、中位突破与首扩源头，算完马上画}
中位收缩背景:=收缩过程 AND 启动前宽比<1.20 AND 启动前相高<0.80 AND NOT(启动前持宽) AND NOT(REF(宽近高,1));
中位收缩突破:=中位收缩背景 AND 有效上穿1 AND REF(PCTB,1)<1 AND PCTB>=1 AND PCTB<1+深限 AND (温额 OR 构上) AND 阳强 AND NOT(长上);
中位温上:=中位收缩突破 AND PCTB<1.10;
中位暴上:=中位收缩突破 AND PCTB>=1.10;

初扩根数:=IF(周线,2,IF(月线,1,3));
带宽初扩:=带宽>REF(带宽,1) AND (带宽>REF(带宽,宽速N) OR COUNT(带宽>REF(带宽,1),初扩根数)>=IF(周线,1,IF(月线,1,2)));
首扩普通贴轨:=PCTB>0.80 AND PCTB<1+深限;
首扩强突贴轨:=PCTB>=1+深限 AND PCTB<1+深限*2.00 AND 阳强 AND NOT(长上) AND NOT(巨额 AND 长上);
贴轨首扩:=首扩普通贴轨 OR 首扩强突贴轨;
首扩候选:=真正收缩 AND 首扩宽度许可 AND 带宽初扩 AND 贴轨首扩 AND 上轨趋势 AND NOT(长上) AND (温额 OR 构上);

STICKLINE(显示许可 AND 中位收缩突破,0.76,0.84,2,0),COLORYELLOW;
STICKLINE(显示许可 AND 首扩候选,0.86,0.94,2,0),COLORRED;
DRAWTEXT(显示许可 AND 中位收缩突破,0.86,'中'),COLORYELLOW;
DRAWTEXT(显示许可 AND 首扩候选,0.96,'首候'),COLORRED;

{七、蓝黄源头，算完马上画}
温上源:=温上 OR 中位温上;
暴上源:=暴上 OR 中位暴上;
蓝压缩质量:=启动前宽比<1.05 AND 启动前相高<0.70 AND NOT(启动前持宽) AND NOT(REF(宽近高,1));
蓝信号源:=(温上源 OR 暴上源) AND 蓝优质背景 AND 蓝压缩质量;
黄信号源:=(温上源 OR 暴上源) AND NOT(蓝信号源);

STICKLINE(显示许可 AND 蓝信号源,1.00,1.10,3,0),COLORCYAN;
STICKLINE(显示许可 AND 黄信号源,1.12,1.22,2,0),COLORYELLOW;
DRAWTEXT(显示许可 AND 蓝信号源,1.12,'蓝源'),COLORCYAN;
DRAWTEXT(显示许可 AND 黄信号源,1.24,'黄源'),COLORYELLOW;

{A3-clean说明：低区=背景，中区=上穿/温暴极，高区=中位/首扩/蓝黄源头。源头层不含最终冷却显示。}
`;

fs.writeFileSync('validation-indicator-A3-clean-draft.txt', formula, 'utf8');
console.log('generated validation-indicator-A3-clean-draft.txt');
