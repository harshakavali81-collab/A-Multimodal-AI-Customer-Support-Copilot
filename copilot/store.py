import sqlite3,json,uuid
from datetime import datetime,timezone
from .core import ROOT,redact
class Store:
    def __init__(self,path=None):
        self.path=str(path or ROOT/'runtime'/'tickets.db')
        from pathlib import Path
        Path(self.path).parent.mkdir(parents=True,exist_ok=True)
        with self.connect() as c:
            c.execute('CREATE TABLE IF NOT EXISTS tickets(id TEXT PRIMARY KEY, created TEXT, status TEXT, payload TEXT, approved_reply TEXT)')
    def connect(self): return sqlite3.connect(self.path)
    def create(self,result):
        id=str(uuid.uuid4())
        with self.connect() as c: c.execute('INSERT INTO tickets VALUES(?,?,?,?,?)',(id,datetime.now(timezone.utc).isoformat(),result['status'],json.dumps(result),''))
        return id
    def review(self,id,status,reply):
        if status not in {'approved','rejected','escalated'}: raise ValueError('Invalid review state')
        if status=='approved' and not reply.strip(): raise ValueError('Approved reply cannot be empty')
        with self.connect() as c:
            cur=c.execute('UPDATE tickets SET status=?,approved_reply=? WHERE id=?',(status,redact(reply),id))
            if cur.rowcount!=1: raise ValueError('Ticket not found')
    def list(self):
        with self.connect() as c: return [dict(id=r[0],created=r[1],status=r[2],result=json.loads(r[3]),approved_reply=r[4]) for r in c.execute('SELECT * FROM tickets ORDER BY created DESC LIMIT 100')]
