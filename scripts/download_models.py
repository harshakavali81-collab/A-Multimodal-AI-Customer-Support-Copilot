"""Download model weights ahead of deployment. Requires internet."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from copilot.core import Copilot
from copilot.ingest import audio_model
from copilot.generation import load_model
Copilot(semantic=True)
audio_model()
load_model()
print('Speech, embedding and generation models cached')
