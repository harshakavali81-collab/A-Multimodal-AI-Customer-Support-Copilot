import io, os, subprocess, tempfile
from pathlib import Path
from functools import lru_cache
from pypdf import PdfReader
from PIL import Image
MAX_BYTES=10*1024*1024
AUDIO={'.wav','.mp3','.m4a','.ogg','.flac'}
@lru_cache(maxsize=1)
def audio_model():
    from faster_whisper import WhisperModel
    return WhisperModel(os.getenv('WHISPER_MODEL','tiny'),device='cpu',compute_type='int8')
def extract(name,data):
    if len(data)>MAX_BYTES: raise ValueError('Each attachment must be at most 10 MB')
    ext=Path(name).suffix.lower()
    if ext in {'.txt','.md'}: text=data.decode('utf-8')
    elif ext=='.pdf':
        reader=PdfReader(io.BytesIO(data))
        if len(reader.pages)>30: raise ValueError('PDF limit is 30 pages')
        text='\n'.join(f'Page {i+1}: '+(p.extract_text() or '') for i,p in enumerate(reader.pages))
        if len(text.strip())<15: raise ValueError('Scanned PDF: convert pages to PNG and upload for OCR')
    elif ext in {'.png','.jpg','.jpeg'}:
        with Image.open(io.BytesIO(data)) as im:
            if im.width*im.height>20000000: raise ValueError('Image exceeds 20 megapixels')
            im.verify()
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/('input'+ext);path.write_bytes(data)
            try: text=subprocess.run(['tesseract',str(path),'stdout','--psm','6'],capture_output=True,text=True,check=True,timeout=30).stdout
            except FileNotFoundError: raise ValueError('Install the Tesseract OCR executable and add it to PATH')
    elif ext in AUDIO:
        try: from faster_whisper import WhisperModel
        except ImportError: raise ValueError('Audio requires: pip install -r requirements-audio.txt')
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/('input'+ext);path.write_bytes(data)
            model=audio_model()
            segments,info=model.transcribe(str(path),beam_size=3)
            if info.duration>120: raise ValueError('Audio limit is two minutes')
            text=' '.join(s.text for s in segments)
    else: raise ValueError('Unsupported attachment type')
    if not text.strip(): raise ValueError('No readable content found')
    return text
