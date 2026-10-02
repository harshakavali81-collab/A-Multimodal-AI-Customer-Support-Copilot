import sys,json,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from copilot.core import Copilot,ROOT
engine=Copilot();rows=[]
for c in json.loads((ROOT/'data/evaluation.json').read_text()):
    r=engine.answer(c['query']);actual=r['sources'][0]['id'] if r['sources'] else ''
    rows.append(dict(**c,actual_source=actual,passed=actual==c['expected_source'],latency_ms=r['latency_ms']))
result={'scope':'10 synthetic text cases; top-1 retrieval and no-evidence routing only; not end-to-end answer accuracy','passed':sum(r['passed'] for r in rows),'total':len(rows),'cases':rows}
(ROOT/'reports').mkdir(exist_ok=True);(ROOT/'reports/evaluation.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))

if result["passed"] != result["total"]: raise SystemExit(1)
