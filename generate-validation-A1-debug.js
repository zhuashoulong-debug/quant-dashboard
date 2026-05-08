const fs = require('fs');

const source = fs.readFileSync('validation-indicator-A1-basic-draft.txt', 'utf8');

const appendix = `

{A1固定显示测试：如果显示红柱和'A1测'，说明A1后置绘图可用}
A1固定测试:=C>0;
STICKLINE(A1固定测试,1.12,1.24,3,0),COLORRED;
DRAWTEXT(A1固定测试,1.24,'A1测'),COLORYELLOW;
`;

fs.writeFileSync('validation-indicator-A1-basic-debug-draft.txt', `${source.trimEnd()}${appendix}\n`, 'utf8');
console.log('generated validation-indicator-A1-basic-debug-draft.txt');
