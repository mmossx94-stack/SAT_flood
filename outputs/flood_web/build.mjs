import fs from 'node:fs/promises';
await fs.copyFile('outputs/flood_web/template.html','outputs/flood_web/index.html');
console.log('UI built. Data comes directly from Google Sheets via /api/data.');
