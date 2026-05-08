const fs = require('fs');

let formula = fs.readFileSync('validation-indicator-A2-front-draft.txt', 'utf8');

formula = formula
  .replace("DRAWTEXT(显示许可 AND 启动前持宽,1.12,'持'),COLORGRAY;\n", '')
  .replace("DRAWTEXT(显示许可 AND 宽近高,1.20,'近高'),COLORGRAY;\n", '')
  .replace(
    '{A2-front说明：低区=挤压，中区=收缩，高区=迟发/宽度。按算完马上画结构编写。}',
    '{A2-readable说明：低区=挤压，中区=收缩，高区=迟发/宽度。持宽/近高只保留灰柱，避免文字过密。}'
  );

fs.writeFileSync('validation-indicator-A2-readable-draft.txt', formula, 'utf8');
console.log('generated validation-indicator-A2-readable-draft.txt');
