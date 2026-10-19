/** Render the real PPTX objects. Does not create or alter product screenshots. */
import fs from 'node:fs/promises';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {PresentationFile,FileBlob} from '/Users/harsh/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs';
const root=path.resolve(import.meta.dirname,'../..');
for(const name of ['Anvest_Seed_Deck','Anvest_Strategic_Integration_Deck']){
 const dir=path.join(root,'.tmp/investor-materials-20261020/rendered',name);await fs.mkdir(dir,{recursive:true});
 const source=path.join(root,'Strategy/Investor_Materials',`${name}.pptx`);
 const p=await PresentationFile.importPptx(await FileBlob.load(source));
 for(const [i,slide] of p.slides.items.entries()){
  const png=await p.export({slide,format:'png',scale:2.5});await fs.writeFile(path.join(dir,`${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
 }
 const result=spawnSync('/opt/homebrew/bin/python3',[path.join(import.meta.dirname,'assemble_pdf.py'),source,dir,path.join(root,'Strategy/Investor_Materials',`${name}.pdf`)],{encoding:'utf8'});
 if(result.status)throw Error(result.stderr);console.log(result.stdout);
}
