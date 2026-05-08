const fs = require('fs');

let formula = fs.readFileSync('validation-indicator-A2-clean-draft.txt', 'utf8');

formula = formula.replace(
  `迟发基准绝宽线:=IF(周线,0.35,IF(月线,0.45,0.22));
迟发绝宽线:=IF(高位2年,迟发基准绝宽线*0.90,IF(低位2年,迟发基准绝宽线*1.10,迟发基准绝宽线));

迟发绝宽许可:=带宽<迟发绝宽线;`,
  `迟发基准绝宽线:=IF(周线,0.35,IF(月线,0.45,0.22));
迟发高位绝宽线:=迟发基准绝宽线*0.90;
迟发低位绝宽线:=迟发基准绝宽线*1.10;
迟发非低位绝宽线:=IF(高位2年,迟发高位绝宽线,迟发基准绝宽线);
迟发绝宽线:=IF(低位2年,迟发低位绝宽线,迟发非低位绝宽线);

迟发绝宽许可:=带宽<迟发绝宽线;`
);

fs.writeFileSync('validation-indicator-A2-clean-v2-draft.txt', formula, 'utf8');
console.log('generated validation-indicator-A2-clean-v2-draft.txt');
