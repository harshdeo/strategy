import fs from 'node:fs/promises';
import {FileBlob,SpreadsheetFile} from '/Users/harsh/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const [payloadPath,out]=process.argv.slice(2);
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(out));
const data=JSON.parse(await fs.readFile(payloadPath,'utf8'));
for(const [name,rows] of Object.entries(data)){
 const sheet=wb.worksheets.getItem(name);const last=String.fromCharCode(64+rows[0].length);
 sheet.getRange(`A1:${last}${rows.length}`).values=rows;
 if(name==='Read me'){
  const r=sheet.getRange('A1:A6');r.format.columnWidthPx=1000;r.format.wrapText=true;r.format.rowHeightPx=48;
 } else if(name==='Assumptions'){
  sheet.getRange(`B2:E${rows.length}`).format.wrapText=true;
  sheet.getRange(`B1:E${rows.length}`).format.columnWidthPx=320;
  sheet.getRange(`A1:E${rows.length}`).format.autofitRows();
 } else {
  sheet.getRange(`B2:T${rows.length}`).setNumberFormat('#,##0;(#,##0);–');
  sheet.getRange('B1:T1').format.columnWidthPx=125;
  sheet.getRange('A1:T1').format.wrapText=true;
  sheet.getRange('A1:T1').format.rowHeightPx=38;
  sheet.getRange(`D2:D${rows.length}`).setNumberFormat('#,##0.0');
 }
}
wb.recalculate();
console.log((await wb.inspect({kind:'region',sheetId:'Scenario',range:'M58:T61',maxChars:1800})).ndjson);
const errors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#NULL!',options:{useRegex:true,maxResults:50},maxChars:1000});console.log(errors.ndjson);
for(const [sheetName,range] of [['Read me','A1:A6'],['Scenario','M56:T61'],['Assumptions','A1:C8']]){
 const blob=await wb.render({sheetName,range,scale:1.3});await fs.writeFile(new URL(`../../.tmp/investor-materials-20261020/workbook-${sheetName.replaceAll(' ','_')}.png`,import.meta.url),new Uint8Array(await blob.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(wb)).save(out);
console.log(out);
