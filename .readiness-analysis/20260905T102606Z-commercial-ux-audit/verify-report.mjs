import {readFile,writeFile,access,readdir} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import assert from 'node:assert/strict';
const here=new URL('./',import.meta.url), root=new URL('../../',import.meta.url);
const backlog=JSON.parse(await readFile(new URL('implementation-backlog.json',here),'utf8'));
const inventory=JSON.parse(await readFile(new URL('public-http-inventory.json',here),'utf8'));
const probes=JSON.parse(await readFile(new URL('domain-probe-results.json',here),'utf8'));
assert.equal(backlog.issues.length,64);
assert.equal(new Set(backlog.issues.map(i=>i.id)).size,64);
for(const i of backlog.issues){for(const key of ['title','evidenceKind','evidence','problem','change','acceptance','plan'])assert.ok(i[key]?.length,`${i.id}:${key}`);assert.equal(i.status,'PROPOSED_NOT_IMPLEMENTED');assert.equal(i.browserVerified,false);for(const e of i.evidence.split('; ')){const f=e.split(':')[0];await access(new URL(f,f.endsWith('.json')&&!f.startsWith('site/')?here:root));}}
assert.equal(inventory.routes.length,37);
assert.equal(inventory.routes.filter(r=>r.status===200).length,36);
assert.equal(inventory.routes.reduce((n,r)=>n+r.buttons.length,0),20);
assert.equal(inventory.sameOriginFragments.filter(x=>x.targetExistsInServerHTML===false).length,28);
assert.equal(probes.probes.length,7);assert.ok(probes.probes.every(x=>!x.error));
const checkedDocuments=['commercial-maturity-audit.md','implementation-specifications.md','public-controls-inventory.md'];
let localLinksChecked=0;
for(const f of checkedDocuments){const body=await readFile(new URL(f,here),'utf8');for(const match of body.matchAll(/\]\(\.\/([^\)]+)\)/g)){await access(new URL(match[1].split('#')[0],here));localLinksChecked++;}assert.ok(body.length>1000);}
const locks=[];
async function scan(dir,depth=0){if(depth>10)return;for(const ent of await readdir(dir,{withFileTypes:true})){if(ent.isSymbolicLink())continue;const next=new URL(ent.name+(ent.isDirectory()?'/':''),dir);if(ent.isFile()&&/^LOCK.*\.json$/i.test(ent.name))locks.push(fileURLToPath(next));if(ent.isDirectory()&&!['node_modules','.git','.next','.wrangler','.cache','.venv','venv','.playwright','.openai'].includes(ent.name))await scan(next,depth+1);}}
for(const dir of [root,new URL('.project-continuity/',root),new URL('.project-continuity/runtime/',root),new URL('site/',root)])await scan(dir,10);
const result={checkedAt:new Date().toISOString(),result:'PASS',meaning:'Report structure, cited file existence, generated counts and audit-data consistency only. Not product/browser validation.',issueCount:64,publicRoutes:37,publicHTTP200:36,initialServerButtons:20,missingFragmentLinks:28,syntheticProbes:7,localDocumentLinksChecked:localLinksChecked,sourceEvidenceFilesExist:true,collaborationLocksFound:locks.length,lockScanScope:'Nonrecursive workspace root, .project-continuity, its runtime, and site root. Symlinks skipped; no B drive access. Prior broader scan stopped without a completed result.',browserTasksPassed:0,androidTasksPassed:0,productModifiedDuringAudit:false};
await writeFile(new URL('report-validation.json',here),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
