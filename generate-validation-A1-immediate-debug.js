const fs = require('fs');

const source = fs.readFileSync('formula-v1-draft.txt', 'utf8');
const lines = source.split(/\r?\n/);

const endMarker = 'PCTB:(C-BDN)/MAX(BUP-BDN,0.0001),COLORYELLOW,LINETHICK2;';
const endIndex = lines.findIndex((line) => line.trim() === endMarker);

if (endIndex < 0) {
  throw new Error(`Missing marker: ${endMarker}`);
}

let base = lines.slice(0, endIndex + 1).join('\n');

base = base.replace(
  'PCTB:(C-BDN)/MAX(BUP-BDN,0.0001),COLORYELLOW,LINETHICK2;',
  [
    'PCTB:=(C-BDN)/MAX(BUP-BDN,0.0001);',
    '图顶:1.30,COLORGRAY,DOTLINE;',
    '图底:-0.30,COLORGRAY,DOTLINE;',
    'PCTB线:MIN(MAX(PCTB,-0.30),1.30),COLORYELLOW,LINETHICK2;',
    '',
    '{紧跟输出的固定绘图测试}',
    '早测:=C>0;',
    'STICKLINE(早测,1.05,1.20,3,0),COLORRED;',
    "DRAWTEXT(早测,1.20,'早测'),COLORYELLOW;"
  ].join('\n')
);

fs.writeFileSync('validation-indicator-A1-immediate-debug.txt', `${base}\n`, 'utf8');
console.log('generated validation-indicator-A1-immediate-debug.txt');
