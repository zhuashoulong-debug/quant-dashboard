const fs = require('fs');

const source = fs.readFileSync('validation-indicator-A-early-output-draft.txt', 'utf8');

const debugAppendix = `

{A图后置显示测试：如果这里显示红柱和'A测'，说明后置STICKLINE/DRAWTEXT可用}
A后置测试:=C>0;
STICKLINE(A后置测试,2.00,2.12,2,0),COLORRED;
DRAWTEXT(A后置测试,2.12,'A测'),COLORYELLOW;
`;

fs.writeFileSync('validation-indicator-A-early-output-debug-draft.txt', `${source.trimEnd()}${debugAppendix}\n`, 'utf8');
console.log('generated validation-indicator-A-early-output-debug-draft.txt');
