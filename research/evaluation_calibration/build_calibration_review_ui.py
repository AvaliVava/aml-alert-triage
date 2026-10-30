"""Build a local-only G02 calibration worksheet from the verified, frozen catalog."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from hybrid_calibration import load_catalog,validate_catalog,DEFAULT_CATALOG,DEFAULT_PACKET
from hybrid_review_preview import load_packet


def build_html(packet_path=DEFAULT_PACKET, catalog_path=DEFAULT_CATALOG):
    """Render frozen text and proposed evidence links without approvals or I/O writes."""
    raw, docs = load_packet(packet_path)
    catalog=load_catalog(catalog_path)
    checks=validate_catalog(catalog,raw,docs,packet_path)
    selected_ids={unit['unit_id'] for bundle in catalog['calibration_bundles']
                  for unit in bundle['source_units']}
    payload={
       'status':'AI_DRAFT_UNADJUDICATED',
       'frozen_packet_sha256':catalog['frozen_packet_sha256'],
       'packet_identity':checks['packet_identity'],
       'input_file_sha256':catalog['input_file_sha256'],
       'candidate_source_hashes':catalog['candidate_source_hashes'],
       'bundles':catalog['calibration_bundles'],
       'checks':{'verified_bundles':checks['selected_bundles'],
                 'selected_units':checks['selected_review_units']},
       'case_level_items':catalog['selected_case_level_items'],
       'source_records':docs['source_inventory.draft.json']['source_records'],
       'unit_evidence_for_review':{
           unit['unit_id']:{field:unit.get(field) for field in (
               'supporting_input','context_input','opposing_or_alternative_reading_input',
               'input_scope_evidence','implementation_context',
           )} for unit in docs['claim_annotations.draft.json']['units']
           if unit['unit_id'] in selected_ids
       },
    }
    js_json=json.dumps(payload,ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    html=r'''<!doctype html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>G02 — Seven-bundle Calibration Lab (draft)</title>
<style>
:root{color-scheme:light;--bg:#f3f5f8;--white:#fff;--text:#142437;--secondary:#506175;--border:#dce2ea;--primary:#174c68;--accent:#00b4a0;--warn:#8b5315}
*{box-sizing:border-box}body{margin:0;background:var(--bg);font:15px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--text)}
header{background:#132b3e;color:#fff;padding:22px 30px}header h1{font-size:23px;margin:0 0 5px}header p{margin:0;color:#cfdae4;max-width:800px}
.wrap{max-width:1440px;margin:auto;display:grid;grid-template-columns:280px 1fr;gap:22px;padding:22px}
nav{background:white;border:1px solid var(--border);border-radius:13px;padding:15px;align-self:start;position:sticky;top:12px}
nav h2{font-size:13px;color:var(--secondary);margin:4px 8px 12px;letter-spacing:1px;text-transform:uppercase}
nav button{width:100%;text-align:left;background:transparent;border:0;border-radius:9px;padding:11px 12px;cursor:pointer;color:var(--text);margin:2px 0;line-height:1.3}
nav button:hover{background:#f1f7f9}nav button.active{background:#e4f4f4;border-left:4px solid var(--accent);font-weight:700}
main{min-width:0}.panel{background:var(--white);border:1px solid var(--border);border-radius:13px;padding:22px;margin-bottom:18px}
.small{font-size:12px;color:var(--secondary)}h2{margin:0 0 5px;font-size:22px}h3{font-size:16px;margin:18px 0 6px}h4{font-size:14px;margin:14px 0 5px}
.eyebrow{letter-spacing:.09em;font-size:11px;text-transform:uppercase;color:var(--primary);font-weight:750}
.tag{display:inline-block;font-size:11px;padding:4px 9px;border-radius:100px;border:1px solid #c9dae0;color:#214e62;background:#f0f7fa;margin:4px 5px 4px 0}
.draft{border:1px solid #f2d7a4;color:#704800;background:#fff7e8}
.rule{padding:12px 15px;border-left:3px solid var(--accent);background:#f3f9f9;border-radius:6px;margin:10px 0}
.statement{white-space:pre-wrap;font-size:14px;padding:13px 14px;background:#f5f7fa;border-radius:8px;border:1px solid var(--border)}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:13px}.quote{font-size:14px;margin:5px 0 15px}
.sourceUnit{border-top:1px solid var(--border);padding:14px 0}.sourceUnit:first-of-type{border-top:0}
code{font-family:ui-monospace,Consolas,monospace;font-size:12px;overflow-wrap:anywhere}
textarea{width:100%;font:14px system-ui;min-height:110px;border:1px solid #bfcbd8;border-radius:8px;padding:12px;resize:vertical}
pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}summary{cursor:pointer}
button.export{background:var(--primary);color:white;border:0;border-radius:8px;padding:11px 16px;cursor:pointer;font-weight:650}
button.export:hover{background:#0a344e}.warning{background:#fff9ef;border:1px solid #e9d6b3;padding:12px;border-radius:9px;font-size:13px}
@media(max-width:850px){.wrap{grid-template-columns:1fr}nav{position:static}.pair{grid-template-columns:1fr}header{padding:20px}}
</style></head><body>
<header><div class="eyebrow" style="color:#60d9cc">RESEARCH / EVALUATION DESIGN</div><h1>G02 Hybrid Calibration Lab</h1>
<p>Seven source-anchored design bundles from Codex's independent review. This is a draft review worksheet, not a semantic evaluator, approval system or performance dashboard.</p></header>
<div class="wrap"><nav><h2>Calibration bundles</h2><div id="nav"></div></nav><main>
<div class="panel"><span class="tag draft">AI-prepared · Unreviewed</span><span class="tag" id="counts"></span><span class="tag">No model calls · Offline</span>
<p class="small">Source documents and candidates are frozen. Proposed normalized claims may be semantically wrong even when their exact text pointers are valid. Notes stay in this browser tab until exported. No automatic semantic scores.</p>
<button class="export" id="export">Export draft notes (JSON)</button></div><div id="contents"></div>
<section class="panel"><details><summary>Frozen input record inventory (supplied records, not authenticated facts)</summary><pre id="sourceRecords"></pre></details></section>
</main></div>
<script>const DATA=__PAYLOAD__;
const notes={}; let current=0;
const el=(tag,content,cls)=>{let e=document.createElement(tag);if(content!==undefined)e.textContent=content;if(cls)e.className=cls;return e};
const add=(parent,tag,text,cls)=>{let n=el(tag,text,cls);parent.appendChild(n);return n};
const split=(text,max=125)=>text.length>max?text.slice(0,max)+'…':text;
function render(){const b=DATA.bundles[current], nav=document.getElementById('nav');nav.replaceChildren();
DATA.bundles.forEach((x,i)=>{let btn=el('button',(i+1)+'. '+x.name);btn.className=i===current?'active':'';btn.onclick=()=>{saveCurrent();current=i;render()};nav.appendChild(btn)});
const host=document.getElementById('contents');host.replaceChildren();let top=add(host,'section','','panel');add(top,'div','BUNDLE '+b.id+' / '+b.status.toUpperCase(),'eyebrow');add(top,'h2',b.name);add(top,'p',b.flaw);for(const r of b.rule_ids)add(top,'span',r,'tag');add(top,'h3','Design decision under review');add(top,'p',b.decision,'rule');add(top,'div','Authorities to inspect: '+b.authority.join(' / '),'small');
let items=add(host,'section','','panel');add(items,'h3','Frozen original statements and proposed units');
const byStatement=new Map();for(const u of b.source_units){const key=u.candidate_id+' | '+u.json_pointer;if(!byStatement.has(key))byStatement.set(key,[]);byStatement.get(key).push(u)}
for(const [location,units] of byStatement){add(items,'div',location,'eyebrow');add(items,'div',units[0].exact_statement,'statement');for(const u of units){const block=add(items,'div','','sourceUnit');add(block,'strong',u.unit_id+' — Original selected span');add(block,'div',u.exact_span,'quote');add(block,'div','Proposed normalized proposition (not approved)','small');add(block,'div',u.atomic_proposition_as_proposed,'rule');add(block,'div','Proposed input support: '+String(u.proposed_support_category_not_approved)+' | proposed citation adequacy: '+String(u.proposed_citation_category_not_approved),'small');add(block,'div','Submitted citations: '+(u.submitted_citations.length?u.submitted_citations.map(c=>c.record_type+':'+c.record_id).join(', '):'(none; may be permitted by the contract)'),'small');add(block,'div','Pointer: '+u.json_pointer+' | SHA-256: '+u.statement_sha256,'small');let evidence=add(block,'details');add(evidence,'summary','Proposed source links, exact field values and scoped inventory');add(evidence,'pre',JSON.stringify(DATA.unit_evidence_for_review[u.unit_id],null,2))}}
let tests=add(host,'section','','panel');add(tests,'h3','Proposed adversarial challenges');for(const t of b.tests){let x=add(tests,'div','','sourceUnit');add(x,'strong',t.id+' — '+t.change);add(x,'p','Fixed: '+t.fixed);add(x,'p','Proposed behavior: '+t.expected);add(x,'div','Method: '+t.method+' (not executed as a semantic test)','small')}
let work=add(host,'section','','panel');add(work,'h3','Human review preparation — draft notes only');add(work,'p','Inspect exact wording versus normalized propositions and evidence before writing. No choice here approves a verdict.','warning');let ta=add(work,'textarea');ta.placeholder='Evidence checked; which normalizations lose meaning; competing interpretations; proposed general rule; disagreements; next test...';ta.id='reviewNotes';ta.value=notes[b.id]||'';ta.oninput=()=>{notes[b.id]=ta.value};add(work,'p','Draft notes only. Reviewer qualification, D-07 adjudicator, scoring and final decisions remain unset.','small')}
function saveCurrent(){let ta=document.getElementById('reviewNotes');if(ta)notes[DATA.bundles[current].id]=ta.value}
document.getElementById('export').onclick=()=>{saveCurrent();let exportObj={format:'G02_CALIBRATION_NOTES_DRAFT_V0_1',status:'UNREVIEWED_NOTES_ONLY',frozen_packet_sha256:DATA.frozen_packet_sha256,packet_identity:DATA.packet_identity,input_file_sha256:DATA.input_file_sha256,candidate_source_hashes:DATA.candidate_source_hashes,reviewer_id:null,adjudicator_id:null,approved_rules:[],scores:null,notes:DATA.bundles.map(b=>({bundle_id:b.id,draft_notes:notes[b.id]||'',human_review_state:'not_reviewed'}))};let blob=new Blob([JSON.stringify(exportObj,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='G02_calibration_draft_notes.json';document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(url)};
document.getElementById('sourceRecords').textContent=JSON.stringify(DATA.source_records,null,2);
document.getElementById('counts').textContent=DATA.checks.verified_bundles+' bundles · '+DATA.checks.selected_units+' review units';render();
</script></body></html>'''.replace('__PAYLOAD__',js_json)
    return html


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet',default=str(DEFAULT_PACKET))
    parser.add_argument('--catalog',default=str(DEFAULT_CATALOG))
    parser.add_argument('--output',required=True,help='New HTML path; existing files are refused')
    args=parser.parse_args()
    html=build_html(args.packet,args.catalog)
    target=Path(args.output)
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('x',encoding='utf-8',newline='\n') as f:
        f.write(html)
    print('Created offline draft review:',target)
if __name__=='__main__':main()
