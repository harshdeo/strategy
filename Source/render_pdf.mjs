import {createRequire} from 'node:module';
import {access} from 'node:fs/promises';
import {pathToFileURL} from 'node:url';
const require=createRequire('/Users/harsh/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/__runtime__.cjs');
const {chromium}=require('playwright');
const [input,output]=process.argv.slice(2);
const systemChrome='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
let executablePath;
try{await access(systemChrome);executablePath=systemChrome;}catch{}
const b=await chromium.launch(executablePath?{executablePath}:{});const page=await b.newPage();
await page.goto(pathToFileURL(input).href,{waitUntil:'networkidle'});
await page.pdf({path:output,format:'A4',printBackground:true,preferCSSPageSize:true});
console.log(output);await b.close();
