const fs = require('fs');

const formula = String.raw`日线:=PERIOD=5;
周线:=PERIOD=6;
月线:=PERIOD=7;
有效周期:=日线 OR 周线 OR 月线;
足够K:=BARSCOUNT(C)>IF(周线,80,IF(月线,48,120));
显示许可:=有效周期 AND 足够K;

BBN:=IF(周线,13,IF(月线,12,20));
KCN:=IF(周线,13,IF(月线,12,20));
MAN:=IF(周线,8,IF(月线,6,13));
TN:=IF(周线,26,IF(月线,24,60));
TM:=IF(周线,5,IF(月线,3,10));
WM:=IF(周线,26,IF(月线,24,60));
WRP:=0.85;
SQN:=IF(周线,3,IF(月线,3,5));
VN:=IF(周线,13,IF(月线,12,20));
VP:=1.2;
BP:=0.45;
YP:=0.45;
BRN:=IF(周线,13,IF(月线,12,20));
P:=2;
KCP:=1.5;
深限:=IF(周线,0.25,IF(月线,0.20,0.30));

MID:=MA(C,BBN);
TMP:=STD(C,BBN);
BUP:=MID+P*TMP;
BDN:=MID-P*TMP;
PCTB:=(C-BDN)/MAX(BUP-BDN,0.0001);

图顶:1.65,COLORGRAY,DOTLINE;
图底:-0.20,COLORGRAY,DOTLINE;
PCTB线:MIN(MAX(PCTB,-0.20),1.65),COLORYELLOW,LINETHICK2;

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

STICKLINE(显示许可 AND 首扩宽度许可,0.04,0.12,1,0),COLORGREEN;
STICKLINE(显示许可 AND 启动前持宽,0.14,0.22,1,0),COLORGRAY;
STICKLINE(显示许可 AND (启动前绝宽高 OR 启动前相宽高),0.24,0.32,1,0),COLORMAGENTA;
DRAWTEXT(显示许可 AND 首扩宽度许可 AND NOT(REF(首扩宽度许可,1)),0.14,'宽许'),COLORGREEN;
DRAWTEXT(显示许可 AND 启动前持宽 AND NOT(REF(启动前持宽,1)),0.24,'持'),COLORGRAY;

TRV:=MAX(MAX(H-L,ABS(H-REF(C,1))),ABS(L-REF(C,1)));
ATRV:=MA(TRV,KCN);
KCU:=MID+KCP*ATRV;
KCD:=MID-KCP*ATRV;
挤压:=BUP<KCU AND BDN>KCD;
效挤:=IF(日线,COUNT(挤压,5)>=2 AND BARSLAST(挤压)<=2,COUNT(挤压,SQN)>=2);

缩窄N:=IF(周线,5,IF(月线,3,10));
缩窄对比N:=缩窄N*2;
缩幅比例:=IF(周线,0.88,IF(月线,0.92,0.85));
低位均比:=IF(周线,1.00,IF(月线,1.05,0.98));
低位低比:=IF(周线,1.25,IF(月线,1.30,1.25));
带宽高点前:=REF(HHV(带宽,缩窄对比N),1);
带宽低点近:=REF(LLV(带宽,缩窄N),1);
收缩幅度:=带宽低点近/MAX(带宽高点前,0.0001)<缩幅比例;
压缩低位:=带宽低点近<前有效宽均*低位均比;
压缩低位:=压缩低位 OR 带宽低点近<=前有效低宽*低位低比;
缩窄次数:=REF(COUNT(带宽<REF(带宽,1),缩窄N),1);
有效缩窄:=缩窄次数>=IF(周线,2,IF(月线,1,4));
日分散挤原:=COUNT(挤压,10)>=2 AND COUNT(挤压,3)>=1;
周分散挤原:=COUNT(挤压,7)>=2 AND COUNT(挤压,2)>=1;
月分散挤原:=COUNT(挤压,5)>=2 AND COUNT(挤压,2)>=1;
分散挤原:=IF(日线,日分散挤原,IF(周线,周分散挤原,月分散挤原));
挤压宽许可:=带宽/MAX(前有效宽均,0.0001)<1.15;
挤压宽许可:=挤压宽许可 AND NOT(启动前持宽) AND NOT(REF(宽近高,1));
有效挤压:=(REF(效挤,1) OR 分散挤原) AND 挤压宽许可;
收缩过程:=收缩幅度 OR 有效缩窄;
真正收缩:=有效挤压 OR (压缩低位 AND 收缩过程);

STICKLINE(显示许可 AND 有效挤压,0.38,0.46,1,0),COLORMAGENTA;
STICKLINE(显示许可 AND 收缩过程,0.48,0.56,1,0),COLORCYAN;
STICKLINE(显示许可 AND 真正收缩,0.58,0.68,2,0),COLORGREEN;
DRAWTEXT(显示许可 AND 真正收缩 AND NOT(REF(真正收缩,1)),0.70,'真缩'),COLORGREEN;

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
实体高:=MAX(C,O);
构上:=C>REF(HHV(实体高,BRN),1);
长线:=MA(C,TN);
短线:=MA(C,MAN);
长向:=长线-REF(长线,TM);
短向:=短线-REF(短线,3);
强多:=长向>0 AND C>长线 AND 短线>长线;
初多:=NOT(强多) AND 短向>0 AND C>短线 AND C>长线;
上轨趋势:=C>短线 AND 短向>0 AND (C>长线 OR 初多 OR 强多);

STICKLINE(显示许可 AND 阳强,0.74,0.82,1,0),COLORRED;
STICKLINE(显示许可 AND 长上,0.84,0.92,1,0),COLORMAGENTA;
STICKLINE(显示许可 AND (温额 OR 构上),0.94,1.02,1,0),COLORYELLOW;
STICKLINE(显示许可 AND 上轨趋势,1.04,1.12,1,0),COLORWHITE;
DRAWTEXT(显示许可 AND 上轨趋势 AND NOT(REF(上轨趋势,1)),1.14,'趋'),COLORWHITE;

初扩根数:=IF(周线,2,IF(月线,1,3));
初扩连续数:=COUNT(带宽>REF(带宽,1),初扩根数);
带宽初扩:=带宽>REF(带宽,1);
带宽初扩:=带宽初扩 AND (带宽>REF(带宽,宽速N) OR 初扩连续数>=IF(周线,1,IF(月线,1,2)));

STICKLINE(显示许可 AND 带宽初扩,1.16,1.26,2,0),COLORRED;
DRAWTEXT(显示许可 AND 带宽初扩 AND NOT(REF(带宽初扩,1)),1.28,'初扩'),COLORRED;

平台N:=IF(周线,8,IF(月线,5,20));
平台涨幅限:=IF(周线,0.30,IF(月线,0.45,0.25));
平台振幅限:=IF(周线,0.30,IF(月线,0.40,0.18));
平台高点:=REF(HHV(H,平台N),1);
平台低点:=REF(LLV(L,平台N),1);
平台前涨幅:=REF(C,1)/MAX(REF(C,平台N),0.0001)-1;
平台未大涨:=平台前涨幅<平台涨幅限;
平台振幅:=平台高点/MAX(平台低点,0.0001)-1;
平台窄幅整理:=平台振幅<平台振幅限;
平台压缩整理:=REF(真正收缩,1);
平台压缩整理:=平台压缩整理 OR (REF(收缩过程,1) AND 启动前宽比<1.15 AND 启动前相高<0.75 AND NOT(REF(宽近高,1)));
平台有整理:=平台窄幅整理 OR (平台压缩整理 AND 平台振幅<平台振幅限*1.25);
平台前热数:=REF(COUNT(PCTB>=1+深限 OR PCTB>1.20,平台N),1);
平台前未热:=平台前热数<=IF(周线,1,IF(月线,1,2));
平台宽不高:=启动前宽比<1.30 AND NOT(启动前持宽) AND NOT(REF(宽近高,1)) AND NOT(前带宽绝高);
平台贴轨数:=REF(COUNT(PCTB>1,平台N),1);
平台强势数:=REF(COUNT(PCTB>0.85 AND C>短线,平台N),1);
平台极热数:=REF(COUNT(PCTB>=1+深限 OR PCTB>1.15,平台N),1);
平台高热状态:=平台极热数>IF(周线,1,IF(月线,1,2));
平台高热状态:=平台高热状态 OR 平台贴轨数>=IF(周线,3,IF(月线,2,6));
平台高热状态:=平台高热状态 OR 平台强势数>=IF(周线,6,IF(月线,4,12));
平台高热状态:=平台高热状态 OR 启动前宽比>=1.30 OR 启动前持宽 OR REF(宽近高,1) OR 前带宽绝高 OR 平台前涨幅>=平台涨幅限;
平台突破:=C>平台高点 AND 构上;
平台前强趋势:=REF(COUNT(PCTB>0.75 AND C>短线,平台N),1)>=IF(周线,4,IF(月线,3,8));
平台前强趋势:=平台前强趋势 OR REF(COUNT(C>长线 AND C>短线,平台N),1)>=IF(周线,4,IF(月线,3,8));
平台突破特征:=平台突破 AND 平台有整理 AND 平台宽不高 AND 阳强 AND NOT(长上);
高位平台再突:=平台突破特征 AND 平台前强趋势;

STICKLINE(显示许可 AND 高位平台再突,1.30,1.38,2,0),COLORMAGENTA;
DRAWTEXT(显示许可 AND 高位平台再突,1.40,'平热'),COLORMAGENTA;

首扩N:=IF(周线,5,IF(月线,3,10));
首扩涨N:=IF(周线,6,IF(月线,4,11));
前持宽:=REF(持宽,1);
前宽未大开:=前宽比<1.30 AND NOT(前持宽);
前极上数:=REF(COUNT(PCTB>=1+深限,首扩N),1);
前大热数:=REF(COUNT(PCTB>1.20,首扩N),1);
前未极热:=前极上数=0 AND 前大热数<=IF(周线,1,IF(月线,1,1));
首扩前涨幅:=REF(C,1)/MAX(REF(C,首扩涨N),0.0001)-1;
前未大涨:=首扩前涨幅<IF(周线,0.30,IF(月线,0.45,0.25));
中期涨N:=IF(周线,26,IF(月线,12,60));
中期涨幅:=REF(C,1)/MAX(REF(C,中期涨N),0.0001)-1;
中期未大涨:=中期涨幅<IF(周线,0.90,IF(月线,1.20,0.80));
首扩未走出:=前宽未大开 AND 前未极热 AND 前未大涨 AND 中期未大涨;
首扩普通贴轨:=PCTB>0.80 AND PCTB<1+深限;
首扩强突贴轨:=PCTB>=1+深限 AND PCTB<1+深限*2.00 AND 阳强 AND NOT(长上);
贴轨首扩:=首扩普通贴轨 OR 首扩强突贴轨;
首扩候选:=真正收缩 AND 首扩宽度许可 AND 首扩未走出 AND 带宽初扩;
首扩候选:=首扩候选 AND 贴轨首扩 AND 上轨趋势 AND NOT(长上) AND (温额 OR 构上) AND NOT(高位平台再突);

STICKLINE(显示许可 AND 首扩未走出,1.42,1.48,1,0),COLORCYAN;
STICKLINE(显示许可 AND 贴轨首扩,1.50,1.56,1,0),COLORYELLOW;
STICKLINE(显示许可 AND 首扩候选,1.58,1.65,3,0),COLORRED;
DRAWTEXT(显示许可 AND 首扩候选,1.62,'候'),COLORRED;

冷却N:=IF(周线,5,IF(月线,3,15));
历史N:=冷却N*4;
候选首扩:=首扩候选 AND NOT(REF(首扩候选,1));
近史候选数:=REF(COUNT(候选首扩,历史N),1);
首轮通过:=近史候选数=0;
距前候选:=BARSLAST(REF(候选首扩,1));
间隔通过:=距前候选>冷却N;
回落重置:=REF(COUNT(PCTB<0.70,冷却N),1)>=1;
回落重置:=回落重置 OR REF(COUNT(C<短线,冷却N),1)>=1 OR REF(COUNT(C<MID,冷却N),1)>=1;
重置高点:=REF(HHV(带宽,冷却N*2),1);
重置低点:=REF(LLV(带宽,冷却N),1);
重置缩幅:=重置低点/MAX(重置高点,0.0001)<缩幅比例;
重置压缩低位:=重置低点<前有效宽均*低位均比;
重置压缩低位:=重置压缩低位 OR 重置低点<=前有效低宽*低位低比;
重置缩窄次数:=REF(COUNT(带宽<REF(带宽,1),冷却N),1)>=IF(周线,2,IF(月线,1,4));
重置有效挤压:=REF(效挤,1) OR REF(COUNT(挤压,SQN*2),1)>=1;
重置收缩过程:=重置缩幅 OR 重置缩窄次数;
重置真正收缩:=重置有效挤压 OR (重置压缩低位 AND 重置收缩过程);
热度冷却:=REF(COUNT(PCTB>=1+深限,冷却N),1)=0 AND REF(COUNT(PCTB>1.20,冷却N),1)<=1;
宽度冷却:=前宽比<1.30 AND NOT(前持宽);
新周期重置:=重置真正收缩 AND 宽度冷却 AND 热度冷却 AND 回落重置 AND 中期未大涨 AND 首扩宽度许可;
首扩周期许可:=首轮通过 OR (间隔通过 AND 新周期重置);
首扩启预:=首扩候选 AND 首扩周期许可;
首扩启:=首扩启预 AND NOT(REF(首扩启预,1));

STICKLINE(显示许可 AND 首扩周期许可,0.04,1.65,1,0),COLORWHITE;
STICKLINE(显示许可 AND 首扩启,0.04,1.65,4,0),COLORRED;
DRAWTEXT(显示许可 AND 首扩周期许可 AND 首扩候选,1.48,'许'),COLORWHITE;
DRAWTEXT(显示许可 AND 首扩启,1.56,'首扩'),COLORRED;

{读法：绿宽许=启动前宽度许可；真缩=真正收缩；趋=上轨趋势；初扩=带宽初扩；平热=高位平台再突阻断；候=首扩候选；白柱=周期许可；红粗柱=首扩启。}
`;

fs.writeFileSync('validation-indicator-A3b1-first-expand-mini-draft.txt', formula, 'utf8');
