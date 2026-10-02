"""Live model tests. Downloads public weights and a Whisper audio test fixture."""
import sys,os,json,time,tempfile,urllib.request,traceback
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from copilot.core import Copilot,ROOT
from copilot.ingest import extract
results=[]
def check(name,func):
    t=time.perf_counter()
    try: detail=func();results.append(dict(name=name,passed=True,seconds=round(time.perf_counter()-t,2),detail=detail))
    except Exception as e:results.append(dict(name=name,passed=False,seconds=round(time.perf_counter()-t,2),error=f'{type(e).__name__}: {e}'));traceback.print_exc()
    print(json.dumps(results[-1]),flush=True)
    (ROOT/'reports/model_validation.json').write_text(json.dumps(results,indent=2))
def semantic():
    e=Copilot(semantic=True);r=e.answer('I forgot the password for my account and cannot sign in')
    assert r['sources'] and r['sources'][0]['id']=='login:1',r
    return {'top_source':r['sources'][0]['id'],'model':'all-MiniLM-L6-v2'}
def audio():
    url='https://raw.githubusercontent.com/openai/whisper/main/tests/jfk.flac'
    with urllib.request.urlopen(url,timeout=30) as r:data=r.read()
    text=extract('jfk.flac',data)
    assert 'country' in text.lower() and 'americans' in text.lower(),text
    return {'fixture_url':url,'transcript':text,'model':'tiny','scope':'Audio transcription component only; historical speech, not customer support audio'}
def llm():
    os.environ['LLM_BACKEND']='transformers'
    e=Copilot();r=e.answer('What should I check for PAY-402 payment failed?',use_llm=True)
    assert r['mode']=='transformers',r
    assert '[payments:1]' in r['draft'],r
    return {'mode':r['mode'],'draft':r['draft'],'model':os.getenv('LOCAL_LLM_MODEL','Qwen/Qwen2.5-0.5B-Instruct'),'scope':'Single cited draft smoke test, not factual-accuracy benchmark'}
check('semantic_retrieval',semantic);check('audio_transcription',audio);check('generated_cited_draft',llm)
if not all(r['passed'] for r in results):raise SystemExit(1)
