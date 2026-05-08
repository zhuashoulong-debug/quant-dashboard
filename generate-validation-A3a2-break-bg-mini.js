const fs = require('fs');

const formula = `日线:=PERIOD=5;
周线:=PERIOD=6;
月线:=PERIOD=7;
有效周期:=日线 OR 周线 OR 月线;
足够K:=BARSCOUNT(C)>IF(周线,80,IF(月线,48,120));
显示许可:=有效周期 AND 足够K;

BBN:=IF(周线,13,IF(月线,12,20));
KCN:=IF(周线,13,IF(月线,12,20));
WM:=IF(周线,26,IF(月线,24,60));
WRP:=0.85;

P:=2;
KCP:=1.5;
SQN:=IF(周线,3,IF(月线,3,5));

MID:=MA(C,BBN);
TMP:=STD(C,BBN);
BUP:=MID+P*TMP;
BDN:=MID-P*TMP;
PCTB:=(C-BDN)/MAX(BUP-BDN,0.0001);

图顶:1.30,COLORGRAY,DOTLINE;
图底:-0.30,COLORGRAY,DOTLINE;
PCTB线:MIN(MAX(PCTB,-0.30),1.30),COLORYELLOW,LINETHICK2;

TRV:=MAX(MAX(H-L,ABS(H-REF(C,1))),ABS(L-REF(C,1)));
ATRV:=MA(TRV,KCN);
KCU:=MID+KCP*ATRV;
KCD:=MID-KCP*ATRV;
挤压:=BUP<KCU AND BDN>KCD;
近挤:=COUNT(挤压,2)>=1;
效挤:=IF(日线,COUNT(挤压,5)>=2 AND BARSLAST(挤压)<=2,COUNT(挤压,SQN)>=2);

STICKLINE(显示许可 AND 挤压,0.04,0.12,1,0),COLORMAGENTA;
DRAWTEXT(显示许可 AND 挤压 AND NOT(REF(挤压,1)),0.14,'挤'),COLORMAGENTA;

背景近挤:=REF(近挤,1);
STICKLINE(显示许可 AND 背景近挤,0.20,0.32,2,0),COLORWHITE;
DRAWTEXT(显示许可 AND 背景近挤 AND NOT(REF(背景近挤,1)),0.34,'近'),COLORWHITE;

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
启动前持宽:=REF(持宽,1);

迟发挤N:=IF(周线,6,IF(月线,6,10));
迟发曾挤:=REF(COUNT(挤压,迟发挤N),1)>=1;
位N:=IF(周线,104,IF(月线,24,500));
位高:=HHV(H,位N);
位低:=LLV(L,位N);
二年位:=(C-位低)/MAX(位高-位低,0.0001);
高位2年:=二年位>=0.80;
低位2年:=二年位<=0.40;
迟发高位绝宽线:=IF(周线,0.35,IF(月线,0.45,0.22));
迟发低位绝宽线:=IF(周线,0.45,IF(月线,0.55,0.28));
迟发中位绝宽线:=IF(周线,0.40,IF(月线,0.50,0.25));
迟发非高位绝宽线:=IF(低位2年,迟发低位绝宽线,迟发中位绝宽线);
迟发绝宽线:=IF(高位2年,迟发高位绝宽线,迟发非高位绝宽线);
迟发绝宽许可:=带宽<迟发绝宽线;
迟发近宽N:=IF(周线,3,IF(月线,3,5));
迟发近宽未破:=带宽<=REF(HHV(带宽,迟发近宽N),1)*1.03;
迟发均宽许可:=带宽/MAX(前有效宽均,0.0001)<1.08;
迟发宽速许可:=宽速率<=微扩阈;
迟发宽未扩:=迟发绝宽许可 AND 迟发近宽未破 AND 迟发均宽许可;
迟发宽未扩:=迟发宽未扩 AND NOT(启动前持宽) AND NOT(REF(宽近高,1));
迟发宽未扩:=迟发宽未扩 AND 迟发宽速许可;
迟发挤压背景:=迟发曾挤 AND 迟发宽未扩;

STICKLINE(显示许可 AND 迟发挤压背景,0.42,0.56,2,0),COLORMAGENTA;
DRAWTEXT(显示许可 AND 迟发挤压背景 AND NOT(REF(迟发挤压背景,1)),0.58,'迟'),COLORMAGENTA;

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
背景昨缩:=REF(真正收缩,1);
背景今缩:=真正收缩;

STICKLINE(显示许可 AND 背景昨缩,0.68,0.80,2,0),COLORCYAN;
STICKLINE(显示许可 AND 背景今缩,0.84,0.96,2,0),COLORGREEN;
DRAWTEXT(显示许可 AND 背景昨缩 AND NOT(REF(背景昨缩,1)),0.82,'昨缩'),COLORCYAN;
DRAWTEXT(显示许可 AND 背景今缩 AND NOT(REF(背景今缩,1)),0.98,'今缩'),COLORGREEN;

突破背景:=背景近挤 OR 迟发挤压背景 OR 背景昨缩 OR 背景今缩;
STICKLINE(显示许可 AND 突破背景,1.08,1.24,3,0),COLORRED;
DRAWTEXT(显示许可 AND 突破背景 AND NOT(REF(突破背景,1)),1.26,'背'),COLORRED;

{读法：紫=当根挤压；白=近挤背景；粉=迟发；青=昨缩；绿=今缩；红=突破背景总开关。}`;

fs.writeFileSync('validation-indicator-A3a2-break-bg-mini-draft.txt', formula, 'utf8');
console.log('generated validation-indicator-A3a2-break-bg-mini-draft.txt');
