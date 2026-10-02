# Validation update: 2026-10-02

- 20 unit and HTTP integration tests passed, including actual screenshot OCR, PDF ingestion, approval, malformed input handling and public-mode non-persistence.
- Original 10/10 synthetic text retrieval cases passed; see evaluation.json.
- 3/3 live AI component tests passed: neural retrieval, speech transcription and Qwen generated drafting. See model_validation.json for measured times and scope.
- Citations label the evidence supplied to the model. They do not establish factual entailment. Human review remains necessary.
- Ollama is an optional alternative and was not live-tested. The verified LLM backend is Transformers.
- Public hosting requires a connected hosting account. It has not been deployed.
- New GitHub CI includes container build and health checks; consult the matching commit's Actions run for its final status.

- Actual headless Chromium UI test passed: submit a payment issue, review the draft, approve in public session mode, and check mobile overflow at 390px. Screenshots: UI_Desktop.png and UI_Mobile.png.
