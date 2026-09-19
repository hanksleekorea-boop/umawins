// Read-only product-module probes. Synthetic objects only; no browser or user storage.
import { createPrediction, createCorrection } from '../../site/lib/domain/record-ledger.mjs';
import { LOCAL_PRIVACY_SCOPES } from '../../site/lib/privacy/controls.mjs';
import { ONBOARDING_KEY, ONBOARDING_DISMISSED_KEY, recommendOnboardingPath } from '../../site/lib/onboarding/preferences.mjs';
import { writeFile } from 'node:fs/promises';
const input = { subject:'AUDIT_SYNTHETIC_ONLY',source:'synthetic audit fixture',observedAt:'2026-09-05',dataStatus:'synthetic',uncertainty:'not a real race',reasonsFor:'synthetic positive',reasonsAgainst:'synthetic negative',confidence:70 };
const probes=[];
function probe(id,run){try{probes.push({id,...run()});}catch(error){probes.push({id,error:error.message});}}
probe('P01_CORRECTION_LICENSE_WITHOUT_GRANT',()=>{const item=createCorrection({predictionId:'audit',field:'dataStatus',correctedValue:'licensed',reason:'synthetic audit, no real grant'},{now:'2026-09-05T10:00:00Z'});return {accepted:item.correctedValue==='licensed',meaning:'Domain correction validates the label but does not require rights evidence. No real record was changed.'};});
probe('P02_IMPOSSIBLE_CALENDAR_DATE',()=>{const item=createPrediction({...input,observedAt:'2026-02-31'},{now:'2026-09-05T10:00:00Z'});return {accepted:item.observedAt==='2026-02-31',meaning:'Impossible calendar date accepted by domain API; HTML date control may constrain direct entry, but import/correction paths also need validation.'};});
probe('P03_FUTURE_OBSERVATION_DATE',()=>{const item=createPrediction({...input,observedAt:'2099-01-01'},{now:'2026-09-05T10:00:00Z'});return {accepted:item.observedAt==='2099-01-01',meaning:'No observation-versus-record-time constraint at this layer. Decide a documented future-date policy.'};});
probe('P04_PREVIEW_TIMESTAMP_CONTRACT',()=>{const item=createPrediction(input,{now:'2026-09-05T10:00:00Z'});return {sealedAt:item.sealedAt,fields:Object.keys(item).filter(x=>/race|deadline|scheduled|cutoff/i.test(x)),meaning:'Creation already sets sealedAt. records/page.tsx calls creation at preview and appends same object at confirmation. No independent race cutoff field.'};});
probe('P05_SETTINGS_DELETION_COVERAGE',()=>{const keys=LOCAL_PRIVACY_SCOPES.flatMap(x=>x.keys);return {omittedKeys:[ONBOARDING_KEY,ONBOARDING_DISMISSED_KEY].filter(x=>!keys.includes(x)),meaning:'General local settings deletion inventory omits both onboarding storage keys. No actual deletion was performed.'};});
probe('P06_ONBOARDING_ROUTE_VARIATION',()=>{const a=recommendOnboardingPath({goal:'record',experience:'new',density:'guided'});const b=recommendOnboardingPath({goal:'record',experience:'advanced',density:'detailed'});return {sameDestination:a.href===b.href,sameTitle:a.title===b.title,explanationChanges:a.explanation!==b.explanation,meaning:'Experience/density change explanatory copy, not destination; source search additionally finds no downstream preference consumer.'};});
probe('P07_FUTURE_RECENT_PERIOD',()=>{const now=Date.parse('2026-09-05T10:00:00Z'),future=Date.parse('2099-01-01T00:00:00Z');return {futureIncluded:now-future<=7*86400000,meaning:'Reproduces pro-tools recent-count expression, which lacks a lower bound; this is a formula probe, not a browser test.'};});
const result={observedAt:new Date().toISOString(),evidenceKind:'AUTOMATED_SYNTHETIC_MODULE_PROBES_NOT_BROWSER',productMutations:0,probes};
await writeFile(new URL('./domain-probe-results.json',import.meta.url),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
