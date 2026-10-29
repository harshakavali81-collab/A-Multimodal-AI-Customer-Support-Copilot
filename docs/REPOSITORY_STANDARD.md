# Repository standard

## Layout

This repository keeps its working source paths. A shared portfolio structure does not require moving a React application, Python package, BI workbook or Verilog project into identical runtime directories.

| Area | Convention |
| --- | --- |
| Landing page | `README.md`: purpose, visuals, demo, features, stack, architecture, setup, tradeoffs and roadmap |
| Detailed reference | `PROJECT_GUIDE.md`: retained project-specific explanation and historical release notes |
| Documentation | `docs/`: design, inventory, reproduction and evidence |
| Work intake | `.github/ISSUE_TEMPLATE/`: bug and feature forms |
| Review | `.github/PULL_REQUEST_TEMPLATE.md`: linked issue, behavior and validation |
| Automation | `.github/workflows/portfolio-docs.yml`: README section and local-link checks |
| Source and tests | Existing project-specific paths listed below; no empty source/test placeholders |

## Workflow

1. Open an issue describing the user problem and measurable acceptance criteria.
2. Add it to a GitHub Project with Todo, In progress, Review and Done states when a board is configured.
3. Use a focused branch and meaningful commits, such as `docs: correct local setup paths` or `fix(api): reject malformed input`.
4. Run the project's documented checks and `python scripts/check_portfolio_docs.py`.
5. Open a pull request with actual validation results and `Closes #<issue-number>`.
6. Merge after review; record release evidence and update the issue/board.

Board creation, profile pins, repository social previews and milestone settings require account-level configuration. This file does not claim those settings have been applied.

## Validation scope

The documentation check validates the landing-page headings and local link targets only. It does not execute models, certify test coverage, inspect Git history for secrets, verify external websites, or prove production readiness. Existing application workflows remain the source of runtime CI evidence.

Keep credentials in local environment variables. A gitignore rule does not remove secrets already tracked or committed. Use only permitted sample data in public demos.

## Inventory at standardization

The following are the pre-existing public project files. New standardization files are described above. Historical guides may mention external bundles that are not part of this list.

- [`Dockerfile`](<../Dockerfile>)
- [`Dockerfile.models`](<../Dockerfile.models>)
- [`README.md`](<../README.md>)
- [`app.py`](<../app.py>)
- [`copilot`](<../copilot>)
- [`copilot/__init__.py`](<../copilot/__init__.py>)
- [`copilot/core.py`](<../copilot/core.py>)
- [`copilot/generation.py`](<../copilot/generation.py>)
- [`copilot/ingest.py`](<../copilot/ingest.py>)
- [`copilot/store.py`](<../copilot/store.py>)
- [`data`](<../data>)
- [`data/evaluation.json`](<../data/evaluation.json>)
- [`data/kb`](<../data/kb>)
- [`data/kb/cancellation.md`](<../data/kb/cancellation.md>)
- [`data/kb/delivery.md`](<../data/kb/delivery.md>)
- [`data/kb/login.md`](<../data/kb/login.md>)
- [`data/kb/payments.md`](<../data/kb/payments.md>)
- [`data/kb/refunds.md`](<../data/kb/refunds.md>)
- [`data/kb/security.md`](<../data/kb/security.md>)
- [`data/kb/upload.md`](<../data/kb/upload.md>)
- [`data/samples`](<../data/samples>)
- [`data/samples/customer_case.pdf`](<../data/samples/customer_case.pdf>)
- [`data/samples/customer_message.txt`](<../data/samples/customer_message.txt>)
- [`data/samples/payment_error.png`](<../data/samples/payment_error.png>)
- [`data/samples/voice_transcript.txt`](<../data/samples/voice_transcript.txt>)
- [`docs`](<../docs>)
- [`docs/Completion_Update.pdf`](<../docs/Completion_Update.pdf>)
- [`docs/DEPLOYMENT.md`](<../docs/DEPLOYMENT.md>)
- [`docs/FULL_GUIDE.md`](<../docs/FULL_GUIDE.md>)
- [`docs/GITHUB.md`](<../docs/GITHUB.md>)
- [`docs/Project_Guide.pdf`](<../docs/Project_Guide.pdf>)
- [`docs/architecture.png`](<../docs/architecture.png>)
- [`docs/architecture.svg`](<../docs/architecture.svg>)
- [`docs/workflow.mmd`](<../docs/workflow.mmd>)
- [`render.yaml`](<../render.yaml>)
- [`reports`](<../reports>)
- [`reports/Project_Workbook.xlsx`](<../reports/Project_Workbook.xlsx>)
- [`reports/UI_Desktop.png`](<../reports/UI_Desktop.png>)
- [`reports/UI_Mobile.png`](<../reports/UI_Mobile.png>)
- [`reports/VALIDATION.md`](<../reports/VALIDATION.md>)
- [`reports/evaluation.json`](<../reports/evaluation.json>)
- [`reports/model_validation.json`](<../reports/model_validation.json>)
- [`requirements-audio.txt`](<../requirements-audio.txt>)
- [`requirements-models.txt`](<../requirements-models.txt>)
- [`requirements-semantic.txt`](<../requirements-semantic.txt>)
- [`requirements.txt`](<../requirements.txt>)
- [`scripts`](<../scripts>)
- [`scripts/download_models.py`](<../scripts/download_models.py>)
- [`scripts/evaluate.py`](<../scripts/evaluate.py>)
- [`scripts/test_models.py`](<../scripts/test_models.py>)
- [`start_models.bat`](<../start_models.bat>)
- [`start_models.sh`](<../start_models.sh>)
- [`tests`](<../tests>)
- [`tests/test_api.py`](<../tests/test_api.py>)
- [`tests/test_core.py`](<../tests/test_core.py>)
- [`web`](<../web>)
- [`web/index.html`](<../web/index.html>)
