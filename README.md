# Multimodal AI Customer Support Copilot

A local portfolio demo with synthetic policies and customer data.

[Setup](#local-installation--setup-guide) · [Architecture](#architecture--system-design-diagram) · [Detailed guide](PROJECT_GUIDE.md) · [Repository standard](docs/REPOSITORY_STANDARD.md)

## Visuals

![Architecture](<docs/architecture.png>)

Existing project visual; diagrams and illustrative graphics are not evidence of a deployed application.

## Live Link / Demo

Run the local demo using the setup guide below. No public deployment URL has been verified for this documentation update.

## Key Features

Text/PDF extraction, Tesseract screenshot OCR, cited TF-IDF retrieval, editable drafts, SQLite tickets and agent approval/escalation. Approval does not send a message.

Optional audio: install `requirements-audio.txt` and allow the Whisper model download.
Optional neural embeddings: install `requirements-semantic.txt` and set `SEMANTIC_SEARCH=1`.
Optional LLM: install Ollama and a chat model, set `OLLAMA_MODEL` to its installed name and enable drafting in the UI. Live Transformers, Whisper and neural-retrieval smoke tests now pass. See [model results](reports/model_validation.json) and [model setup](docs/DEPLOYMENT.md). Ollama remains untested. The default response is evidence extraction, not generation.

## Tech Stack

![Python](https://img.shields.io/badge/Python-334155?style=flat-square) ![scikit-learn](https://img.shields.io/badge/scikit--learn-334155?style=flat-square) ![NumPy](https://img.shields.io/badge/NumPy-334155?style=flat-square) ![Docker](https://img.shields.io/badge/Docker-334155?style=flat-square)

Dependency versions and optional packages are defined in the repository manifests.

## Architecture / System Design Diagram

[Architecture documentation / diagram](<docs/architecture.png>)

## Local Installation & Setup Guide

```bash
git clone https://github.com/harshakavali81-collab/A-Multimodal-AI-Customer-Support-Copilot.git
cd A-Multimodal-AI-Customer-Support-Copilot
```

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```
Open http://127.0.0.1:8000. Ask `My payment failed with PAY-402`.
On macOS/Linux use `python3 -m venv .venv` and `.venv/bin/python`.

## Challenges & Solutions

**Repository organization:** this project uses its existing project-specific entry points. Keeping those paths stable avoids breaking imports, asset links and deployment commands while the documentation follows a shared format. Project-specific technical limitations and prior release evidence are retained in [Project guide](PROJECT_GUIDE.md).

## Future Improvements

- Capture a reproducible end-to-end demo with runtime versions and sample inputs.
- Expand regression checks for invalid inputs and documented edge cases.
- Record measured results, data provenance and deployment limitations alongside each release.

## Scope and supporting evidence

A local portfolio demo with synthetic policies and customer data.

## Repository Structure

| Location | Purpose |
| --- | --- |
| `tests/` | Tests |
| `docs/` | Documentation |
| `data/` | Data and samples |
| `scripts/` | Automation scripts |
| `.github/` | Issue forms, PR template and automated checks |

[Complete file inventory and workflow](docs/REPOSITORY_STANDARD.md). Runtime entry points retain their existing paths.

## Workflow & Tracking

Use the [bug and feature forms](https://github.com/harshakavali81-collab/A-Multimodal-AI-Customer-Support-Copilot/issues/new/choose) to define work with acceptance criteria. Keep tasks in Todo → In progress → Review → Done, and link a pull request with `Closes #<number>`. See [the maintenance workflow](docs/REPOSITORY_STANDARD.md#workflow).

## License

Original project software is available under the [MIT License](LICENSE). See [licensing scope](docs/LICENSING.md) for third-party and data exclusions.

