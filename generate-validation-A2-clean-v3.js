const fs = require('fs');

let formula = fs.readFileSync('validation-indicator-A2-clean-v2-draft.txt', 'utf8');

// EastMoney may report "at least one output item required" when the first
// plotted output appears too late. Move the base outputs right after PCTB.
formula = formula.replace(
  `PCTB:=(C-BDN)/MAX(BUP-BDN,0.0001);

TRV:=MAX(MAX(H-L,ABS(H-REF(C,1))),ABS(L-REF(C,1)));`,
  `PCTB:=(C-BDN)/MAX(BUP-BDN,0.0001);

{A2提前输出：防止东方财富通在前段判定无输出项}
图顶:1.30,COLORGRAY,DOTLINE;
图底:-0.30,COLORGRAY,DOTLINE;
PCTB线:MIN(MAX(PCTB,-0.30),1.30),COLORYELLOW,LINETHICK2;

TRV:=MAX(MAX(H-L,ABS(H-REF(C,1))),ABS(L-REF(C,1)));`
);

// Remove the later duplicate base outputs. Keep 宽比线 because 当前宽比 is only
// available after the bandwidth section.
formula = formula.replace(
  `{五、A2精简显示}
图顶:1.30,COLORGRAY,DOTLINE;
图底:-0.30,COLORGRAY,DOTLINE;
PCTB线:MIN(MAX(PCTB,-0.30),1.30),COLORYELLOW,LINETHICK2;
宽比线:MIN(当前宽比,2)/2,COLORMAGENTA,DOTLINE;`,
  `{五、A2精简显示}
宽比线:MIN(当前宽比,2)/2,COLORMAGENTA,DOTLINE;`
);

fs.writeFileSync('validation-indicator-A2-clean-v3-draft.txt', formula, 'utf8');
console.log('generated validation-indicator-A2-clean-v3-draft.txt');
