import unittest, tempfile, threading, json, urllib.request, urllib.error, base64, shutil
from pathlib import Path
from unittest.mock import patch
from http.server import HTTPServer
import app
from copilot.core import Copilot, ROOT
from copilot.store import Store

class APITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        app.engine = Copilot()
        app.store = Store(Path(cls.temp.name) / 'tickets.db')
        cls.server = HTTPServer(('127.0.0.1', 0), app.Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.temp.cleanup()

    def request(self, path, body=None, token=True):
        headers = {'Content-Type': 'application/json'}
        if token: headers['X-Copilot-Token'] = app.TOKEN
        req = urllib.request.Request(self.base + path, data=None if body is None else json.dumps(body).encode(), headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=35) as r: return r.status, r.read()
        except urllib.error.HTTPError as e: return e.code, e.read()

    def test_page(self):
        status, body = self.request('/')
        self.assertEqual(status, 200)
        self.assertIn(b'Customer request', body)
        self.assertNotIn(b'__PUBLIC_DEMO__', body)

    def test_health(self):
        self.assertEqual(json.loads(self.request('/health')[1])['status'], 'ok')

    def test_missing_token(self):
        self.assertEqual(self.request('/api/assist', {'message': 'hello'}, False)[0], 403)

    def test_invalid_body(self):
        self.assertEqual(self.request('/api/assist', [])[0], 400)

    def test_invalid_message_type(self):
        self.assertEqual(self.request('/api/assist', {'message': 3})[0], 400)

    def test_invalid_base64(self):
        self.assertEqual(self.request('/api/assist', {'attachments': [{'name': 'a.txt', 'data': '!!!'}]})[0], 400)

    def attachment(self, name):
        f = ROOT / 'data/samples' / name
        status, body = self.request('/api/assist', {'attachments': [{'name': name, 'data': base64.b64encode(f.read_bytes()).decode()}]})
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)['sources'][0]['id'], 'payments:1')

    def test_pdf_request(self):
        self.attachment('customer_case.pdf')

    @unittest.skipUnless(shutil.which('tesseract'), 'Tesseract not installed')
    def test_screenshot_request(self):
        self.attachment('payment_error.png')

    def test_review(self):
        _, body = self.request('/api/assist', {'message': 'reset password'})
        id = json.loads(body)['ticket_id']
        self.assertEqual(self.request('/api/review', {'id': id, 'status': 'approved', 'reply': 'Use the reset link.'})[0], 200)
        rows = json.loads(self.request('/api/tickets')[1])
        self.assertEqual(next(r for r in rows if r['id'] == id)['status'], 'approved')

    def test_public_no_persistence(self):
        before = len(app.store.list())
        with patch.object(app, 'PUBLIC_DEMO', True):
            self.assertEqual(self.request('/api/assist', {'message': 'PAY-402'})[0], 200)
            self.assertEqual(json.loads(self.request('/api/tickets')[1]), [])
            self.assertEqual(self.request('/api/review', {'id': 'test', 'status': 'approved', 'reply': 'OK'})[0], 409)
        self.assertEqual(len(app.store.list()), before)
