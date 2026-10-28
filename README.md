# Wexa Browser — Backend Core

Local-first, page-aware AI coding agent engine built without an external Ollama daemon.

## Architecture Highlights

1. **Embedded Inference Engine (`backend/engine/inference.py`):**
   - Directly loads quantized `.gguf` models (e.g. `Qwen2.5-Coder-1.5B-Instruct-Q4_K_M.gguf`) via embedded bindings (`llama.cpp`).
   - Self-contained and portable; no background Ollama service required.

2. **Automated Telemetry & Self-Training Pipeline (`backend/data/telemetry_logger.py`):**
   - Records every coding session where the user accepts an edit or tests pass: `<problem, starter_code, verified_code, test_status>`.
   - Automatically exports high-quality, verified pairs directly to instruction-tuning JSONL format for local LoRA/QLoRA fine-tuning.

3. **Approval State Machine (`backend/agent/state_machine.py`):**
   - Non-bypassable state machine enforcing strict single-action permissions before any browser editor is modified.

4. **Isolated Test Execution (`backend/execution/runner.py`):**
   - Subprocess sandbox with timeouts and output bounds to verify code before reporting results.

## Quickstart

### 1. Install dependencies
```powershell
pip install -r requirements.txt
```

### 2. Download a GGUF model
Place any compatible `.gguf` model (e.g., Qwen2.5-Coder) into `D:\Wexa Browser\models\`.

### 3. Start the API server
```powershell
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8765 --reload
```

### 4. Run backend tests
```powershell
pytest tests/
```
