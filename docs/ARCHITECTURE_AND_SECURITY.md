# Wexa Browser — Comprehensive Technical Specification & Security Architecture

**GitHub Repository:** [https://github.com/aayash317-svg/Wexa-Browser.git](https://github.com/aayash317-svg/Wexa-Browser.git)  
**Local Workspace:** `D:\Wexa Browser`  
**License:** Private / Local-First Development  
**Status:** Core Backend & Security Hardening Complete (All 15 Unit & Security Tests Passing)

---

## 1. Executive Summary & Purpose

**Wexa Browser** is an autonomous, page-aware AI browser specifically engineered for coding practice platforms (e.g., LeetCode, HackerRank, Codeforces, custom educational portals).

Unlike standard conversational chatbots that only give advice, Wexa:
1. **Understands Practice Webpages**: Extracts problem statements, constraints, expected method signatures, starter code, and active editor elements.
2. **Operates 100% Offline with Embedded Inference**: Employs an embedded GGUF engine (`llama.cpp` wrapper) without requiring external services or third-party background daemons like Ollama.
3. **Guarantees Zero API Key & Data Leakage**: Automatically detects and redacts any API keys, access tokens, credentials, or cookies. Webpages never send private data off the machine.
4. **Enforces Static AST Code Safety**: Scans all generated code for dangerous operations (`import os`, `subprocess`, `eval`, `exec`, filesystem deletion, network calls) before code can execute or be proposed.
5. **Defends Against Indirect Prompt Injections (IPI)**: Blocks adversarial text on untrusted webpages from overriding agent instructions or exfiltrating data.
6. **Maintains a Non-Bypassable Permission State Machine**: Code cannot be inserted or run without explicit single-action user authorization with unified diff previews.
7. **Compiles an Automated Continuous Self-Training Dataset**: Logs validated, passing interactions into structured JSONL format and exports instruction-tuning datasets for offline LoRA fine-tuning.

---

## 2. Multi-Layer Security Architecture

Security is deeply integrated at every layer of the system:

```
+---------------------------------------------------------------------------------------+
|                                1. UNTRUSTED WEBPAGE                                   |
| (Webpage HTML, DOM Text, Starter Code, Comments, Assessment Guardrails)               |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
|                           2. ZERO-LEAKAGE PRIVACY GUARD                               |
|                  (backend/security/offline_guard.py)                                  |
| - Strips & redacts: OpenAI/Anthropic keys, GitHub PATs, AWS keys, Slack tokens, JWTs  |
| - Scrubs passwords, session cookies, and bearer tokens from prompts & telemetry logs  |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
|                        3. ANTI-PROMPT INJECTION DEFENSE                               |
|                  (backend/security/injection_guard.py)                                |
| - Detects jailbreaks: "ignore all previous instructions", DAN mode, system prompt leaks|
| - Blocks markdown exfiltration attacks: ![exfil](http://attacker.com/...)             |
| - Neutralizes chat template delimiter collisions (<|im_start|>, <|im_end|>)           |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
|                     4. WEBSITE RESTRICTION & POLICY DETECTOR                          |
|                  (backend/security/restriction_detector.py)                           |
| - Distinguishes interface limits from policy locks                                    |
| - Read-only editor -> Produces safe alternative: export to local disk                 |
| - CAPTCHA challenge -> Pauses automated agent; prompts user to solve manually         |
| - Proctored assessment / Anti-automation -> Disables auto-edit; respects site policy  |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
|                    5. EMBEDDED OFFLINE INFERENCE (Wexa Coder)                         |
|                  (backend/engine/inference.py)                                        |
| - Direct GGUF loading via llama.cpp (e.g. Qwen2.5-Coder-1.5B/3B)                      |
| - Fully contained in-process; zero external network calls                             |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
|                      6. AST STATIC CODE SAFETY INSPECTOR                              |
|                  (backend/security/ast_safety.py)                                     |
| - Parses Python code into an Abstract Syntax Tree (AST) before insertion              |
| - Prohibits forbidden imports: os, subprocess, shutil, socket, requests, urllib, etc. |
| - Prohibits arbitrary calls: eval(), exec(), compile(), __import__()                  |
| - Prohibits sandbox escape attributes: __subclasses__, __globals__, __builtins__      |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
|                    7. PERMISSION & APPROVAL STATE MACHINE                             |
|                  (backend/agent/state_machine.py)                                     |
| - States: ANALYSING -> PROPOSAL_READY -> WAITING_FOR_APPROVAL -> APPLY -> VERIFY      |
| - Ephemeral, single-use token invalidated if user navigates away or modifies text     |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
|                    8. ISOLATED SUBPROCESS EXECUTION SANDBOX                           |
|                  (backend/execution/runner.py)                                        |
| - Strict execution timeout (8 seconds max)                                            |
| - Ephemeral isolated directory cleanup                                                |
| - Output capped at 2,000 characters                                                   |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
|                  9. AUTOMATED SELF-TRAINING DATA RECORDER                             |
|                  (backend/data/telemetry_logger.py)                                   |
| - Automatically logs verified passing tuples: <problem, starter, clean_code, PASS>    |
| - Exports standardized JSONL datasets for local PEFT/LoRA fine-tuning                 |
+---------------------------------------------------------------------------------------+
```

---

## 3. Directory Structure & Key Files

```text
D:\Wexa Browser\
|-- backend\
|   |-- agent\
|   |   |-- orchestrator.py             # Central controller coordinating all pipelines
|   |   |-- state_machine.py            # Non-bypassable approval lifecycle
|   |-- data\
|   |   |-- telemetry_logger.py         # Automated interaction recorder & JSONL exporter
|   |-- editor_adapters\
|   |   |-- base.py                     # EditorAdapter protocol
|   |   |-- textarea.py                 # Textarea adapter with unified diff generation
|   |-- engine\
|   |   |-- inference.py                # Embedded GGUF runner (llama.cpp wrapper)
|   |-- execution\
|   |   |-- runner.py                   # Isolated execution sandbox with AST checks
|   |-- page_parser\
|   |   |-- extractor.py                # Extracts problems, constraints, and TODO markers
|   |-- schemas\
|   |   |-- editor.py                   # Edit proposals and diff models
|   |   |-- feedback.py                 # Telemetry record schema
|   |   |-- restrictions.py             # Restriction types & authorized alternatives
|   |   |-- task.py                     # Page analysis requests & extracted task schemas
|   |-- security\
|   |   |-- ast_safety.py               # Abstract Syntax Tree static code analyzer
|   |   |-- injection_guard.py          # Anti-Prompt Injection defense
|   |   |-- offline_guard.py            # Comprehensive API key & credential redaction
|   |   |-- restriction_detector.py     # Detects read-only, CAPTCHAs, and policy limits
|   |-- config.py                       # App settings, paths, and timeouts
|   |-- main.py                         # FastAPI server for the frontend / sidecar
|
|-- frontend\
|   |-- index.html                      # Replicates the official UI mockup
|   |-- styles.css                      # Cyberpunk dark navy theme with glowing accents
|   |-- app.js                          # Client-side controller with offline fallback simulation
|
|-- scripts\
|   |-- dataset_downloader.py           # Ingestion & normalization script
|   |-- train_lora.py                   # Automated PEFT/LoRA fine-tuning training harness
|
|-- data\
|   |-- datasets\                       # Storage for normalized training datasets
|   |   |-- starter_coding_eval.jsonl   # Seed benchmark tasks
|   |-- automated_interactions.jsonl    # Live auto-collected user solutions
|
|-- tests\
|   |-- test_backend.py                 # Core workflow unit tests
|   |-- test_model_security.py          # AST safety, injection defense, API key redaction tests
|   |-- test_restrictions.py            # Website restriction handling tests
|
|-- .gitignore                          # Excludes large GGUF models, caches, and node_modules
|-- requirements.txt                    # Project Python dependencies
|-- ui.md                               # Formatted UI & interface specification
|-- ui_spec.md                          # Design tokens, layout grids, and component specs
|-- Restrictions and Offline Operation.md # Offline operation and restriction charter
|-- Wexa browser.md                     # Technical roadmap and architecture specification
```

---

## 4. API Reference (`backend/main.py`)

The backend exposes a local REST API over `http://127.0.0.1:8765`:

### `GET /health`
Returns system status, embedded model readiness, and active agent state.

### `POST /api/analyze-page`
Accepts `PageAnalysisRequest` containing `page_title`, `origin`, `visible_text`, `starter_code`, and `dom_metadata`.
- Checks restrictions (read-only, CAPTCHA, assessment rules).
- Scrubs API keys and prompt injections.
- Produces `PageTaskExtraction` and proposed code with a unified diff preview.

### `POST /api/approve`
Accepts `ApprovalRequest` with `proposal_id`, `origin`, and `user_approved: bool`.
- Validates the token against the single-action state machine.
- Rejects if origin changed or user cancelled.

### `POST /api/verify-and-test`
Accepts `VerifyTestRequest` with `actual_editor_content` and optional `test_harness_code`.
- Verifies editor content matches proposal.
- Runs static AST safety check.
- Executes in isolated subprocess sandbox.
- Automatically appends interaction to `data/automated_interactions.jsonl`.

### `GET /api/datasets/stats`
Returns total interaction count, verified passing count, and language distribution.

### `POST /api/datasets/export`
Converts verified interactions into standard instruction-tuning format (`data/datasets/wexa_coder_finetune.jsonl`).

---

## 5. Security Test Suite (All Passing)

Run the test suite at any time from PowerShell:
```powershell
$env:PYTHONPATH="D:\Wexa Browser"
python -m pytest "D:\Wexa Browser\tests" -v
```
