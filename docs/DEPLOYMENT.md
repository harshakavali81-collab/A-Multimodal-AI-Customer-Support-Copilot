# Deployment and model setup

## Verified model mode
The three live smoke tests in `reports/model_validation.json` passed on 2026-10-02:
- Sentence-transformer retrieval selected login:1 for a password paraphrase.
- faster-whisper transcribed the public Whisper JFK test fixture.
- Qwen2.5-0.5B-Instruct generated a payment reply; the application attached the supplied source ID when the model omitted it.
These are component smoke tests, not broad accuracy or safety benchmarks. The generated response still requires human review. Ollama remains an alternative adapter and was not live-tested.

On Python 3.11 or 3.12, create a virtual environment, then install:
```bash
python -m pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements-models.txt
python scripts/download_models.py
python scripts/test_models.py
```
The audio decoder is pinned to PyAV 15.1.0 to avoid the incompatible `metadata_errors` API change in PyAV 19. Model downloads require internet and several GB of disk/RAM. Model weights are cached separately and are not committed to GitHub or included in the ZIP.

PowerShell:
```powershell
$env:LLM_BACKEND="transformers"
$env:SEMANTIC_SEARCH="1"
python app.py
```
Enable **Use AI drafting** in the page. Audio files use the cached Whisper model automatically. No paid API key is needed for these local models.

## Public portfolio demo
`PUBLIC_DEMO=1` makes the app stateless on the server: customer input and review decisions are not written to SQLite, and `/api/tickets` returns no shared history. Reviews and history remain only in the current browser page's memory. Reloading the page clears them. This prevents visitors from reading other visitors' saved tickets.

`render.yaml` configures the lightweight text/PDF/OCR demo using the baseline Dockerfile. Connect the repository in a Render account and deploy the Blueprint. The model-enabled container uses `Dockerfile.models` and requires a larger memory allocation; it is not configured for the small free baseline service. Choose a suitable plan in the hosting account before enabling it.

```bash
docker build -f Dockerfile.models -t support-copilot:models .
docker run --rm -p 127.0.0.1:8000:8000 support-copilot:models
```
The full image downloads models during build and selects neural retrieval plus Transformers drafting. Baseline CI also builds and health-checks the lightweight Docker image.

A Render connection is not available in the current session. No live public URL is claimed. GitHub source publication is separate from application hosting. The built-in HTTP server is a portfolio service; production use still needs a hardened serving layer, per-user authentication, resource controls and operational monitoring.

## GitHub checks
The regular workflow runs unit/API tests, baseline retrieval evaluation, a Docker build and container health check. Run **Live model tests** manually from the Actions tab to repeat large model downloads and inference. The workflow publishes its JSON result as a downloadable artifact.
