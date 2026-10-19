/** Focused Artifact Tool edits with an OOXML preservation pass for original media/charts.
 * Run update_decks.py first, then this file with Codex's bundled Node runtime.
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const runtime=process.env.ANVEST_ARTIFACT_MODULES ?? '/Users/harsh/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
process.env.RUNTIME_NODE_MODULES ??= runtime;
const {FileBlob,PresentationFile}=await import(pathToFileURL(path.join(runtime,'@oai/artifact-tool/dist/artifact_tool.mjs')));
const root=path.resolve(import.meta.dirname,'../..');
const build=path.join(root,'.tmp/investor-materials-20261020');
const skill='/Users/harsh/.codex/plugins/cache/openai-primary-runtime/presentations/26.1015.12040/skills/presentations';
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')));
for(const name of ['Anvest_Seed_Deck','Anvest_Strategic_Integration_Deck']){
  const candidate=path.join(build,`${name}.preserved.pptx`);
  const p=await PresentationFile.importPptx(await FileBlob.load(candidate));
  const edits=JSON.parse(await fs.readFile(path.join(build,`${name}.edits.json`),'utf8'));
  // Apply the same focused edits to the imported objects. The preservation package
  // retains native PowerPoint data-label formatting and untouched screenshot bytes.
  for(const e of edits){
    const shape=p.slides.items[e.slide-1].shapes.items.find(s=>s.id===e.id);
    if(!shape) throw Error(`Missing shape ${e.slide}/${e.id}`);
    const current=String(shape.text);
    if(current!==e.new) throw Error(`Unexpected imported text ${e.slide}/${e.id}`);
    shape.text=e.new;
  }
  await (await PresentationFile.exportPptx(p)).save(path.join(build,`${name}.artifact-draft.pptx`));
  await fs.mkdir(path.join(build,'validated'),{recursive:true});
  const out=path.join(build,'validated',`${name}.validated.pptx`);
  // The finalizer refuses overwrites. Use a new validation filename on each run.
  const finalPath=out.replace('.pptx',`-${Date.now()}.pptx`);
  const result=await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath,
    pythonExecutable:'/Users/harsh/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3',
    integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
    layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
    layoutArgs:['--expected-slide-size-emu','12192000,6858000'],
    explicitTotalSlideCount:name==='Anvest_Seed_Deck'?21:10,
    requiredNativeChartOwnerSlides:name==='Anvest_Seed_Deck'?[13]:[],
    verifyArtifactToolImport:true,
    receiptPath:path.join(build,`${name}.validation-${Date.now()}.json`)});
  console.log(name,JSON.stringify(result));
  await fs.copyFile(finalPath,path.join(root,'Strategy/Investor_Materials',`${name}.pptx`));
}
