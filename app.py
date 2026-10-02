"""Local single-agent demo. Do not expose directly to the internet."""
import base64,json,os,secrets,uuid,binascii
from http.server import HTTPServer,BaseHTTPRequestHandler
from pathlib import Path
from copilot.core import Copilot,ROOT
from copilot.ingest import extract
from copilot.store import Store
TOKEN=secrets.token_urlsafe(32)
engine=None;store=None
PUBLIC_DEMO=os.getenv('PUBLIC_DEMO')=='1'
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def send(self,status,body,kind='application/json'):
        blob=body if isinstance(body,bytes) else json.dumps(body).encode()
        self.send_response(status);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(blob)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('X-Frame-Options','DENY');self.end_headers();self.wfile.write(blob)
    def do_GET(self):
        if self.path=='/': self.send(200,(ROOT/'web/index.html').read_text().replace('__TOKEN__',TOKEN).replace('__PUBLIC_DEMO__','true' if PUBLIC_DEMO else 'false').encode(),'text/html; charset=utf-8')
        elif self.path=='/health': self.send(200,{'status':'ok'})
        elif self.path=='/api/tickets' and self.headers.get('X-Copilot-Token')==TOKEN: self.send(200,[] if PUBLIC_DEMO else store.list())
        else:self.send(404,{'error':'Not found'})
    def do_POST(self):
        if self.headers.get('X-Copilot-Token')!=TOKEN:return self.send(403,{'error':'Invalid session token'})
        try:
            length=int(self.headers.get('Content-Length','0'))
            if length<=0 or length>28*1024*1024: raise ValueError('Request size limit exceeded')
            body=json.loads(self.rfile.read(length))
            if not isinstance(body,dict): raise ValueError('Request must be a JSON object')
            if self.path=='/api/assist':
                text=body.get('message','')
                attachments=body.get('attachments',[])
                if not isinstance(text,str) or not isinstance(attachments,list): raise ValueError('Invalid message or attachments')
                if len(text)>25000: raise ValueError('Message exceeds 25,000 characters')
                if not isinstance(body.get('use_llm',False),bool): raise ValueError('use_llm must be a boolean')
                if len(attachments)>3: raise ValueError('Maximum three attachments')
                for a in attachments:
                    if not isinstance(a,dict) or not isinstance(a.get('name'),str) or not isinstance(a.get('data'),str): raise ValueError('Invalid attachment')
                    text+='\n'+extract(a['name'],base64.b64decode(a['data'],validate=True))
                result=engine.answer(text,bool(body.get('use_llm')));result['ticket_id']=str(uuid.uuid4()) if PUBLIC_DEMO else store.create(result);self.send(200,result)
            elif self.path=='/api/review':
                if PUBLIC_DEMO: return self.send(409,{'error':'Public demo reviews stay in this browser session'})
                if not all(isinstance(body.get(k),str) for k in ['id','status','reply']): raise ValueError('Invalid review fields')
                store.review(body['id'],body['status'],body['reply']);self.send(200,{'saved':True,'sent_to_customer':False})
            else:self.send(404,{'error':'Not found'})
        except (ValueError,KeyError,TypeError,binascii.Error) as e:self.send(400,{'error':str(e)})
        except Exception as e:self.send(500,{'error':f'Processing failed ({type(e).__name__}). Check dependencies and file format.'})
if __name__=='__main__':
    engine=Copilot(semantic=os.getenv('SEMANTIC_SEARCH')=='1');store=None if PUBLIC_DEMO else Store()
    port=int(os.getenv('PORT','8000'));print(f'Open http://127.0.0.1:{port}',flush=True)
    HTTPServer((os.getenv('BIND_HOST','127.0.0.1'),port),Handler).serve_forever()
