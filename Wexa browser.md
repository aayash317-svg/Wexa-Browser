# Wexa Browser
## Deep Implementation Specification: Page-Aware Coding Agent

**Document type:** Technical implementation and development roadmap  
**Project:** Wexa Browser  
**Primary objective:** Build a local-first AI browser agent that understands webpages, identifies missing code, asks for permission, interacts with supported code editors, and verifies solutions in authorized practice environments.

---

# 1. Project Vision

Wexa Browser is a desktop browser with an integrated AI agent that can understand the current webpage and carry out approved tasks.

Unlike a standard chatbot, Wexa should not merely explain how to perform a task. It should understand the page, plan the necessary actions, request permission, interact with supported browser elements, and verify the result.

The first major capability is a page-aware coding agent.

The user opens a permitted coding practice page. Wexa reads the question, identifies the programming language and editor, determines which code is missing, prepares a solution using a local model, asks the user for permission, inserts the approved code, and tests it when testing is permitted.

## 1.1 Core principles

1. Local-first inference.
2. Explicit user approval before editing.
3. No unnecessary cloud API dependencies.
4. Reliable page and editor understanding.
5. Verification using actual test results.
6. Safe execution of generated code.
7. Privacy-preserving data collection.
8. Modular architecture that supports multiple models and editors.
9. Reproducible dataset preparation.
10. Automated testing before adding new features.

## 1.2 Important development rule

Do not build every feature simultaneously.

First establish a reliable workflow using one programming language, one supported editor, and a small evaluation dataset.

Only expand the project after the existing workflow passes its tests.

---

# 2. Initial Development Environment

The development agent must inspect the existing machine before choosing dependencies or downloading large models.

Known development context:

- Operating system: Windows.
- Development environment: VS Code with Antigravity.
- Available RAM: approximately 16 GB.
- Processor: Intel Core i5-1235U.
- Storage: approximately 512 GB NVMe.
- Local model runtime: Ollama.
- Previously installed model: Qwen3 4B.
- Storage constraint: avoid unnecessarily filling the Windows system drive.

These are starting assumptions, not a substitute for checking the actual machine.

## 2.1 Initial inspection tasks

Before installation, inspect:

- Windows version.
- Available disk space on C: and E:.
- Python version.
- Node.js and npm versions.
- Git installation.
- Ollama installation and service status.
- Installed Ollama models.
- Current model storage location.
- GPU availability and memory.
- Existing project directories.
- Whether the terminal can access downloaded datasets.

Do not reinstall working software without identifying a concrete reason.

Do not download multiple large language models simultaneously.

## 2.2 Recommended initial commands

Run these commands in the VS Code terminal.

```powershell
python --version
node --version
npm --version
git --version
ollama --version
ollama list
```

Inspect available disk space:

```powershell
Get-PSDrive -PSProvider FileSystem
```

Inspect the current project directory:

```powershell
Get-Location
Get-ChildItem
```

If a command is unavailable, record the error and investigate it before continuing.

---

# 3. Product Scope

## 3.1 Initial release

The first release should implement:

- Desktop browser shell.
- Current-page inspection.
- Question and instruction extraction.
- Programming-language detection.
- Code-editor detection.
- Missing-code classification.
- Local model integration.
- Solution preview.
- Explicit approval dialog.
- One supported editor adapter.
- Code insertion and verification.
- Safe practice-environment testing.
- Compiler-output analysis.
- Basic correction workflow.
- Local logs and evaluation results.

## 3.2 Features deferred until the first release works

Do not initially prioritize:

- Training a foundation model from scratch.
- Supporting every website.
- Supporting every editor.
- Multiple large models running concurrently.
- Autonomous browsing without action limits.
- Complex multi-agent architectures.
- Automatic submission of assessments.
- Cloud-based inference as a hidden fallback.
- Large-scale dataset collection without quality checks.

The first goal is a reliable end-to-end workflow, not a large feature list.

---

# 4. High-Level Architecture

Wexa should consist of separate modules with explicit responsibilities.

```text
Wexa Browser Desktop
|
+-- Browser Interface
|   +-- Tabs
|   +-- Address Bar
|   +-- Current Page
|   +-- AI Side Panel
|
+-- Page Understanding
|   +-- DOM Inspection
|   +-- Accessibility Tree
|   +-- Visible Text Extraction
|   +-- Question Extraction
|   +-- Language Detection
|   +-- Editor Detection
|
+-- Agent Orchestrator
|   +-- Task Classification
|   +-- Planning
|   +-- Permission Management
|   +-- Action Execution
|   +-- Verification
|   +-- Recovery
|
+-- Local AI Service
|   +-- Model Discovery
|   +-- Model Benchmarking
|   +-- Coding Model
|   +-- Optional Embedding Model
|   +-- Structured Output Validation
|
+-- Editor Adapter Layer
|   +-- Textarea Adapter
|   +-- Monaco Adapter
|   +-- CodeMirror Adapter
|   +-- Ace Adapter
|   +-- Custom Practice Editor
|
+-- Test Execution
|   +-- Static Validation
|   +-- Isolated Runtime
|   +-- Test Results
|   +-- Error Analysis
|
+-- Data and Evaluation
    +-- Dataset Manifest
    +-- Downloaded Data
    +-- Cleaned Data
    +-- Evaluation Dataset
    +-- Training Dataset
    +-- Benchmark Reports
```

## 4.1 Architectural boundary

The AI model proposes interpretations and actions.

The orchestrator validates those proposals.

The permission system decides whether an action is authorized.

The editor adapter performs the approved edit.

The test runner executes code in an isolated environment.

The verification module determines whether the action actually succeeded.

Never give the language model unrestricted operating-system or browser-control access.

---

# 5. Recommended Technology Stack

| Component | Initial recommendation | Purpose |
|---|---|---|
| Desktop application | Electron | Desktop browser shell |
| Frontend | React + TypeScript | Browser interface and AI panel |
| Build system | Vite | Frontend development |
| Backend | Python + FastAPI | AI orchestration and services |
| Local inference | Ollama | Local model execution |
| Browser automation | Playwright for testing; controlled Electron APIs for the product | Browser interaction |
| Local database | SQLite | Preferences, history and metadata |
| Search | SQLite FTS5 initially | Local text retrieval |
| Validation | Pydantic | Structured data validation |
| Unit testing | pytest | Python tests |
| UI testing | Playwright | Browser and application tests |
| Dataset processing | Python, pandas, JSONL utilities | Cleaning and conversion |
| Optional fine-tuning | Transformers + PEFT + TRL | Compatible-model adaptation |

Choose compatible, stable dependency versions during implementation and pin them in lockfiles or requirements files.

Do not introduce a vector database until the project needs semantic retrieval. It is not necessary for the first page-aware coding workflow.

---

# 6. Page Understanding Engine

The page understanding engine converts the active webpage into structured information.

It should not automatically send the entire page, browser profile, cookies, or account data to the model.

## 6.1 Inspection process

1. Identify the current tab.
2. Confirm that the user has requested page analysis.
3. Extract the page title and origin.
4. Collect visible problem text.
5. Identify input/output instructions and constraints.
6. Extract examples and starter code.
7. Detect relevant buttons and editor elements.
8. Identify the supported editor type.
9. Build a structured page representation.
10. Report missing or ambiguous information.

## 6.2 Data to extract

```json
{
  "page_title": "Example Coding Problem",
  "origin": "https://practice.example",
  "task_type": "complete_missing_code",
  "language": "java",
  "problem_statement": "Implement a method that adds two integers.",
  "constraints": [],
  "examples": [],
  "starter_code": "class Solution { ... }",
  "editor_type": "supported_editor",
  "editable_region": "sum method body",
  "run_available": true,
  "submit_available": false,
  "analysis_confidence": 0.93
}
```

This is an illustrative schema. Values must be extracted and validated from the actual page. Confidence values must be calibrated from evaluation data rather than invented.

## 6.3 Page-content security

Page content is untrusted input.

A webpage might contain text that attempts to instruct the AI to reveal secrets, change settings, or ignore its rules.

Wexa must treat webpage content as task data, not as privileged instructions.

The page parser must not expose:

- Passwords.
- Authentication tokens.
- Cookies.
- Private browser storage.
- Unrelated open tabs.
- Sensitive account information.

Capture only the content necessary for the user's task.

---

# 7. Missing-Code Detection

Wexa must distinguish an empty editor from an incomplete program.

An empty editor does not automatically mean that the correct response is a complete program.

## 7.1 Supported classifications

### A. Empty editor

The page provides a problem statement, but the editor has no code.

Action:

1. Extract the required language.
2. Identify expected input/output behavior.
3. Generate a complete proposed solution.
4. Validate the proposed solution.
5. Ask permission before insertion.

### B. Starter code with a TODO marker

Example:

```java
class Solution {
    public int sum(int a, int b) {
        // TODO
    }
}
```

The model should produce a targeted implementation while preserving the class and method signature.

### C. Incomplete method

The code contains a method with a missing body or placeholder.

The agent must identify the intended editable region and preserve the rest of the file.

### D. Existing code with errors

The agent should diagnose the issue, prepare a patch, and show the change before applying it.

### E. Ambiguous problem

If the language, target region, expected behavior, or permissions are unclear, ask the user for clarification.

Do not guess and edit.

### F. Unsupported or restricted editor

If the editor cannot be accessed through a supported interface, report the limitation.

Do not bypass access controls, copy/paste restrictions, assessment safeguards, or site policies.

## 7.2 Detection signals

Use a combination of:

- Problem statement.
- Starter-code structure.
- TODO and placeholder markers.
- Function signatures.
- Syntax errors.
- Editor selection and cursor.
- Explicit editable-region markers.
- Available practice-test instructions.
- User-provided target region.

The model should not decide edit boundaries from a screenshot alone when reliable editor state is available.

---

# 8. Local Model Strategy

## 8.1 Current model problems

The existing Qwen3 4B installation is a useful starting baseline, but it may produce:

- Invalid code.
- Incorrect assumptions.
- Malformed structured output.
- Incorrect function signatures.
- Hallucinated APIs.
- Unnecessary explanations instead of code.
- Inconsistent tool-call formats.
- Slow responses.
- Out-of-memory errors.
- Incorrect fixes after compiler errors.

These problems require different solutions. Do not assume that fine-tuning will solve every problem.

A better prompt may improve formatting. A stronger coding model may improve reasoning. A smaller quantization may improve memory usage. A deterministic validator can catch schema errors. A sandbox can catch runtime failures.

## 8.2 Model selection procedure

The implementation agent must first inspect the models already installed.

```powershell
ollama list
```

For each candidate, record:

- Exact model name and version or digest.
- Quantization, where available.
- Model size.
- Context-window settings.
- Memory usage.
- Response latency.
- Coding benchmark accuracy.
- Structured-output reliability.
- Tool-use reliability.
- Runtime stability.

Do not assume that a model with a larger parameter count will perform better on this machine.

## 8.3 Candidate models to investigate

Investigate compatible local coding models from these families:

- Qwen coder models.
- DeepSeek Coder models.
- StarCoder2 models.
- Other currently available open-weight coding models that support the chosen runtime.

These are candidate families, not a guarantee that every model variant is compatible with Ollama or suitable for 16 GB RAM.

Before downloading a candidate:

1. Verify that the exact model exists in the intended registry.
2. Check its model-card licence and intended use.
3. Check quantized size and runtime memory requirements.
4. Estimate disk space and memory requirements.
5. Download one candidate at a time.
6. Run the benchmark.
7. Keep it only if the results justify its resource usage.

Avoid running multiple large models concurrently on the development machine.

## 8.4 Local model discovery

Use the runtime's documented API to retrieve installed models and test generation.

For Ollama, verify the local service and API availability using its documented endpoints. Do not assume a connection succeeded just because the command was issued.

Record the following outcomes:

- Service reachable.
- Model loaded.
- Test prompt completed.
- Response parses correctly.
- Code compiles.
- Tests pass.
- Memory remains within limits.

## 8.5 Model benchmark

Create a small, manually verified benchmark before selecting a replacement model.

Include tasks covering:

1. Empty-editor solution generation.
2. Completion of a missing function body.
3. Preservation of starter code.
4. Exact function signatures.
5. Input/output handling.
6. Edge cases.
7. Compiler-error correction.
8. Structured JSON output.
9. Page-instruction extraction.
10. Rejection of unsupported or ambiguous actions.

Use the same tasks for each model.

Measure:

- Compile success rate.
- Unit-test pass rate.
- Exact-signature compliance.
- Starter-code preservation.
- Valid structured-output rate.
- Median response time.
- Peak memory.
- Failed or timed-out requests.

Do not select a model using one successful example.

## 8.6 Recommended model decision

Begin with the existing model and build the evaluation harness around it.

Then compare one or two suitable coding-model alternatives.

Choose the model with the best balance of:

- Correctness.
- Stability.
- Response time.
- Memory usage.
- Local compatibility.
- Licence suitability.

The final choice must be based on actual results recorded on this computer.

## 8.7 Model fallback policy

Wexa must not silently switch to a cloud API when local inference fails.

If the selected local model fails:

1. Capture a sanitized error message.
2. Check whether the service is running.
3. Check model availability.
4. Retry only transient failures, with a limit.
5. Show the error and allow a user-approved alternative model.
6. Preserve the current page and proposed edit.
7. Never claim that code was tested if it was not.

---

# 9. User Approval System

No code should be written into a page before the user approves the proposed change.

## 9.1 Empty-editor approval

Suggested message:

> The editor appears to be empty. I have analysed the question and prepared a solution. Would you like me to write it into the current practice editor?

Show:

- Detected language.
- Problem summary.
- Target editor.
- Proposed code.
- Testing plan.
- Any uncertainty.

## 9.2 Existing-code approval

Suggested message:

> I found incomplete code. I propose changing the following region while preserving the surrounding program. Review the patch before approving.

Display a diff rather than silently replacing the entire file.

## 9.3 Approval lifecycle

An approval is valid only for the specific proposed action.

Invalidate approval if:

- The current page changes.
- The editor content changes.
- The target element changes.
- The proposed code changes.
- The user navigates to a different problem.
- The requested action changes materially.

Approval to write code does not authorize submitting a test, publishing a repository, purchasing an item, or modifying unrelated data.

## 9.4 Approval state machine

```text
ANALYSING
    |
    v
PROPOSAL_READY
    |
    v
WAITING_FOR_APPROVAL
    |
    +---- User cancels ----> CANCELLED
    |
    +---- Page changed ----> REANALYSE
    |
    +---- User approves ---> VALIDATE_APPROVAL
                                  |
                                  v
                              APPLY_EDIT
                                  |
                                  v
                              VERIFY_EDIT
                                  |
                                  v
                              TEST_IF_ALLOWED
```

The backend must enforce this state machine. A frontend button alone is not a security boundary.

---

# 10. Editor Adapter System

Each editor type should implement a common interface.

```python
from typing import Protocol


class EditorAdapter(Protocol):
    def detect(self, page) -> bool:
        ...

    def read_content(self, page) -> str:
        ...

    def prepare_edit(
        self,
        current: str,
        proposal: str
    ) -> dict:
        ...

    def apply_approved_edit(self, edit: dict) -> None:
        ...

    def verify_edit(self, expected: str) -> bool:
        ...
```

## 10.1 Initial adapter

Start with a purpose-built practice page containing a normal textarea or a documented editor API.

Implement:

- Editor detection.
- Reading current content.
- Creating a proposed patch.
- Approval validation.
- Writing the patch.
- Reading content again.
- Comparing actual and expected results.

## 10.2 Additional adapters

Add these only after the first adapter passes automated tests:

- Monaco.
- CodeMirror.
- Ace.
- Other documented editor integrations.

## 10.3 Important implementation details

A modern editor may maintain its own internal document state.

Changing the visible DOM element does not necessarily update that state.

Therefore:

1. Use a supported editor API when available.
2. Confirm that the editor's own state changed.
3. Verify the resulting text.
4. Detect stale element references.
5. Avoid relying solely on simulated keystrokes or DOM mutation.
6. Stop when the editor is unsupported or the site disallows automation.

---

# 11. Code Generation and Validation

## 11.1 Model input

Provide only the necessary context:

- Problem statement.
- Programming language.
- Required function signature.
- Starter code.
- Constraints.
- Examples.
- Target editable region.
- Required response format.

Do not send unrelated browser information.

## 11.2 Model output

Use a validated structured response.

```json
{
  "language": "java",
  "task_type": "complete_missing_code",
  "target": {
    "kind": "function_body",
    "name": "sum"
  },
  "proposed_code": "return a + b;",
  "explanation": "Returns the sum of the two integers.",
  "requires_review": true
}
```

This is a format example, not an actual solution for an arbitrary page.

Validate all fields using Pydantic or an equivalent schema validator.

Reject:

- Missing required fields.
- Unsupported languages.
- Unexpected tool actions.
- Invalid target regions.
- Excessively large output.
- Malformed patches.
- Unapproved actions.

## 11.3 Validation stages

1. Parse the response.
2. Validate its schema.
3. Confirm the target region exists.
4. Check the language and required signature.
5. Verify that the proposed edit preserves required surrounding code.
6. Run available static checks.
7. Show the proposal.
8. Wait for approval.
9. Apply the approved change.
10. Verify the actual editor state.

Never treat model-generated explanations as proof of correctness.

---

# 12. Safe Test Execution

Code generation and code execution must be separate modules.

Generated code is untrusted.

## 12.1 Initial testing approach

Start with a locally controlled practice environment.

Use an isolated execution process with:

- Execution timeout.
- Memory limit where supported.
- Restricted filesystem access.
- No network access by default.
- Temporary working directory.
- Controlled compiler invocation.
- Output-size limits.
- Cleanup after execution.

Do not execute arbitrary generated code in the privileged Electron main process.

For stronger isolation, use an appropriately configured container or sandbox. Do not assume that a normal subprocess is a complete security boundary.

## 12.2 Testing sequence

1. Check the generated source.
2. Compile or perform static validation.
3. Execute permitted sample tests.
4. Capture standard output and standard error.
5. Record the exit status.
6. Compare outputs with expected results.
7. Summarize failures.
8. Offer a revised patch.
9. Request approval before applying a new patch.
10. Repeat only within a configured attempt limit.

## 12.3 Truthful reporting

Use explicit result states:

- `PASS`: all required tests actually ran and passed.
- `FAIL`: at least one executed test failed.
- `PARTIAL`: some tests passed but not all required tests ran.
- `UNVERIFIED`: tests could not be run or results were inconclusive.
- `BLOCKED`: the environment did not permit the requested test.

Do not describe hidden tests as passed unless the environment provides verifiable results.

Do not submit answers automatically in restricted assessments. Use the agent in authorized practice environments and follow the target website's rules.

---

# 13. Dataset Strategy

Dataset preparation should improve model evaluation and later fine-tuning.

Do not start by downloading hundreds of gigabytes of code.

First create a small, curated evaluation dataset. Then identify what additional training examples would actually help.

## 13.1 Dataset categories

### A. Page-understanding examples

Teach the system to extract:

- Problem statements.
- Programming languages.
- Constraints.
- Starter code.
- Required function signatures.
- Editable regions.

### B. Coding examples

Include:

- Function completion.
- Small algorithmic tasks.
- Input/output handling.
- Edge cases.
- Compiler-error corrections.
- Code-preservation tasks.

### C. Browser-action examples

Include approved actions on purpose-built practice pages:

- Inspect a page.
- Locate an editor.
- Read current code.
- Prepare a patch.
- Wait for approval.
- Apply a patch.
- Verify the result.

### D. Recovery examples

Include:

- Unsupported editor.
- Missing model.
- Timeout.
- Compilation error.
- Invalid structured output.
- Stale page.
- Changed editor content.

### E. Safety examples

Include:

- Malicious instructions embedded in a page.
- Requests to expose credentials.
- Unapproved editing.
- Attempts to bypass website restrictions.
- Requests to submit restricted assessments.

## 13.2 Dataset record format

Use JSONL so that every record occupies one line.

Example:

```json
{
  "id": "practice_java_0001",
  "source_type": "synthetic_practice",
  "license": "original",
  "task_type": "complete_missing_code",
  "language": "java",
  "problem_statement": "Implement a method that adds two integers.",
  "starter_code": "class Solution { ... }",
  "target_region": "sum method body",
  "expected_behavior": "Return the sum of two integers.",
  "tests": [
    {
      "input": [2, 3],
      "expected_output": 5
    }
  ],
  "expected_action": "prepare_patch_then_request_approval",
  "verified": true
}
```

This example uses a synthetic task. Real examples must have accurate source and licensing metadata.

## 13.3 Data provenance

For every downloaded dataset, record:

- Dataset name.
- Original source.
- Source URL.
- Download date.
- Licence.
- Version or commit.
- File size.
- Checksums.
- Permitted uses.
- Required attribution.
- Preprocessing steps.
- Number of records.
- Known limitations.

Do not train on private coursework, account credentials, authentication tokens, or arbitrary visited webpages.

Do not assume that publicly accessible code is automatically licensed for unrestricted training.

## 13.4 Dataset splits

Maintain separate datasets for:

- Training.
- Validation.
- Final evaluation.

Avoid placing near-identical tasks in training and evaluation.

Where possible, split by source repository or problem family to reduce data leakage.

Never use the final evaluation set as training data.

---

# 14. Dataset Download and Terminal Workflow

Antigravity should make dataset preparation reproducible.

The goal is for the coding agent to download permitted datasets, verify them, prepare a local directory, and make the processed files accessible from the terminal.

## 14.1 Dataset directory structure

Prefer a project data directory on the drive with sufficient free space.

Example:

```text
E:\WexaData\
    downloads\
    raw\
    processed\
    manifests\
    evaluation\
    reports\
```

The actual location should be configured rather than hard-coded throughout the application.

Inside the repository:

```text
wexa-browser/
    data/
        manifests/
        samples/
        evaluation/
        README.md
    scripts/
        check_environment.ps1
        download_datasets.py
        validate_datasets.py
        prepare_datasets.py
        evaluate_models.py
```

Large downloaded datasets should normally remain outside Git. Commit the manifest, preprocessing scripts, documentation, and small permitted samples instead.

## 14.2 Dataset manifest

Create a manifest such as `data/manifests/datasets.json`.

Example:

```json
{
  "datasets": [
    {
      "id": "example_coding_dataset",
      "source_url": "VERIFIED_DATASET_URL",
      "license": "VERIFY_BEFORE_DOWNLOAD",
      "destination": "raw/example_coding_dataset",
      "format": "jsonl",
      "enabled": false
    }
  ]
}
```

The placeholder URL must be replaced with a verified official source before use.

The download script must refuse to download entries whose source or licence has not been verified.

## 14.3 Download workflow

For each approved dataset:

1. Verify the official source.
2. Verify the licence.
3. Estimate the download size.
4. Check available disk space.
5. Download to a temporary file.
6. Verify the HTTP response and expected format.
7. Calculate a checksum.
8. Validate the file.
9. Move it into the raw-data directory.
10. Record its metadata in the manifest.
11. Log success or a useful failure message.

Do not silently continue when a download is incomplete.

Do not repeatedly download a file that has already been verified unless its version changes or the user requests a refresh.

## 14.4 Example PowerShell workflow

After the scripts are implemented, the intended terminal workflow should look like this:

```powershell
# Enter the project directory
Set-Location "D:\Projects\wexa-browser"

# Inspect the environment
.\.venv\Scripts\python.exe scripts\check_environment.py

# Inspect approved datasets and their licences
.\.venv\Scripts\python.exe scripts\download_datasets.py --dry-run

# Download only verified, enabled datasets
.\.venv\Scripts\python.exe scripts\download_datasets.py

# Validate raw data
.\.venv\Scripts\python.exe scripts\validate_datasets.py

# Prepare normalized JSONL files
.\.venv\Scripts\python.exe scripts\prepare_datasets.py

# Evaluate the current local model
.\.venv\Scripts\python.exe scripts\evaluate_models.py
```

These commands describe the intended scripts. Antigravity must create and test the scripts before treating the workflow as operational.

Use the actual project directory discovered on the machine rather than assuming `D:\Projects\wexa-browser` exists.

## 14.5 Terminal visibility

The scripts should print:

- Resolved dataset directory.
- Files discovered.
- Number of valid records.
- Number of rejected records.
- Licence-validation status.
- Download status.
- Checksum status.
- Output paths.
- Warnings and errors.

Example output:

```text
Wexa Dataset Preparation
------------------------
Manifest loaded: yes
Approved datasets: 2
Files discovered: 4
Records processed: 12,450
Records rejected: 37
Licence checks: passed
Output directory: E:\WexaData\processed
Status: completed with warnings
```

These values are illustrative only. The real script must display actual results.

---

# 15. Data Cleaning and Validation

Before any model training, validate every record.

Checks should include:

- Valid JSON.
- Required fields.
- Supported language labels.
- Nonempty task descriptions.
- Reasonable source-code length.
- Correct licence metadata.
- No duplicate records.
- No obvious secrets or credentials.
- Valid input/output examples.
- Consistent target regions.
- Correct test-output types.
- No train/evaluation leakage.

Store rejected records separately with a reason.

Do not silently discard records without reporting why.

Create a dataset report containing:

- Total input records.
- Accepted records.
- Rejected records.
- Duplicate count.
- Missing-field count.
- Licence-review count.
- Language distribution.
- Source distribution.
- Output file paths.

---

# 16. Training and Fine-Tuning Strategy

Fine-tuning is optional for the first release.

First establish a reliable baseline with an existing local model.

## 16.1 Recommended sequence

### Stage 1: Prompting and structured outputs

Improve task extraction, output schemas, examples, and validation.

### Stage 2: Tool orchestration

Implement reliable editor and browser actions outside the model.

### Stage 3: Evaluation

Identify exactly which tasks the current model fails.

### Stage 4: Dataset preparation

Collect or create relevant, permitted examples that address the observed weaknesses.

### Stage 5: Fine-tuning feasibility

Check whether the chosen base model, licence, training framework, and available hardware support the intended method.

### Stage 6: Small experiment

If practical, use parameter-efficient fine-tuning such as LoRA or QLoRA on a compatible model.

### Stage 7: Compare against baseline

Evaluate the fine-tuned model on the same held-out tasks.

Keep the tuned model only if it provides measurable improvement without unacceptable regressions.

## 16.2 Hardware limitations

The available computer has approximately 16 GB RAM and a mobile-class processor.

Full training of a large language model is not an appropriate starting point.

Even fine-tuning a small model can require substantial memory and compatible hardware.

Before training:

- Inspect available GPU and VRAM.
- Inspect system RAM and free disk space.
- Check framework compatibility.
- Estimate dataset size.
- Estimate checkpoint size.
- Confirm the selected base model supports the training method.
- Start with a small experiment.

If local training is impractical, continue with local inference and focus on better data, prompts, deterministic validation, and orchestration. Do not make cloud training a hidden requirement.

---

# 17. Model Evaluation Framework

Create a repeatable evaluation script.

Each test case should have:

- Unique ID.
- Task category.
- Input page representation.
- Starter code.
- Expected target region.
- Expected behavior.
- Test cases.
- Expected action.
- Actual model output.
- Compilation result.
- Test result.
- Latency.
- Error details.

## 17.1 Primary metrics

### Task extraction accuracy

How often does Wexa correctly identify the task, language, and target region?

### Code compilation rate

How often does the generated code compile in the supported test environment?

### Functional correctness

How often does the solution pass the required tests?

### Edit preservation

How often does Wexa preserve all code outside the approved target region?

### Approval enforcement

Can any test path modify the editor without a valid approval?

The expected answer is no.

### Editor verification accuracy

How often does Wexa correctly distinguish a successful edit from a failed edit?

### Error-reporting accuracy

Does the agent report actual test results rather than hallucinating success?

### Resource usage

Measure peak memory, disk usage, and response latency.

## 17.2 Initial benchmark size

Start with a small manually verified benchmark, such as 50–100 tasks.

Include both successful and failure scenarios.

This is a starting target, not a claim that 100 tasks are sufficient to prove reliability.

Expand the benchmark based on failures found during development.

---

# 18. Security and Privacy

Security is part of the initial implementation, not a later optional feature.

## 18.1 Browser security

- Enable Electron context isolation.
- Enable renderer sandboxing.
- Use restrictive Content Security Policy.
- Validate all IPC messages.
- Expose only necessary preload methods.
- Restrict navigation and external links.
- Separate browser content from privileged application logic.

## 18.2 Agent security

- Treat webpage text as untrusted.
- Require approval for edits.
- Revalidate approvals before execution.
- Limit action counts and retries.
- Avoid exposing cookies and tokens.
- Log sanitized action metadata.
- Prevent arbitrary shell commands from model output.
- Require explicit permission for consequential actions.

## 18.3 Code execution security

- Run code outside the privileged browser process.
- Use isolation appropriate to the threat model.
- Set timeouts and resource limits.
- Restrict filesystem access.
- Disable network access by default.
- Limit output size.
- Clean up temporary files.
- Do not trust generated code.

## 18.4 Assessment restrictions

Use the coding agent in authorized practice and development environments.

Do not implement mechanisms to bypass assessment controls, anti-automation safeguards, or restrictions on copying and pasting.

If a site prohibits automated assistance, Wexa should stop automated editing and offer explanations or guided learning instead.

---

# 19. Recommended Repository Structure

```text
wexa-browser/
|
+-- apps/
|   +-- desktop/
|       +-- main/
|       +-- preload/
|       +-- renderer/
|           +-- components/
|           +-- panels/
|           +-- approval/
|
+-- services/
|   +-- ai_backend/
|       +-- api/
|       +-- agent/
|       +-- page_understanding/
|       +-- code_generation/
|       +-- editor_adapters/
|       +-- testing/
|       +-- security/
|       +-- evaluation/
|
+-- scripts/
|   +-- check_environment.py
|   +-- download_datasets.py
|   +-- validate_datasets.py
|   +-- prepare_datasets.py
|   +-- evaluate_models.py
|
+-- data/
|   +-- manifests/
|   +-- samples/
|   +-- evaluation/
|
+-- tests/
|   +-- unit/
|   +-- browser/
|   +-- editor/
|   +-- security/
|   +-- evaluation/
|
+-- docs/
|   +-- architecture.md
|   +-- implementation_spec.md
|   +-- editor_adapter_spec.md
|   +-- permissions.md
|   +-- dataset_card.md
|   +-- model_evaluation.md
|   +-- threat_model.md
|
+-- .gitignore
+-- README.md
+-- package.json
+-- pyproject.toml
```

The development agent should inspect the existing repository before creating this structure.

Do not duplicate files or replace an existing architecture without understanding the current implementation.

---

# 20. Development Milestones

## Milestone 0 — Environment audit

Tasks:

- Inspect the existing repository.
- Check installed tools and models.
- Check storage and memory.
- Identify the existing project state.
- Produce an environment report.

Exit criteria:

- No unnecessary reinstallation.
- A known working Python environment.
- A known working Node.js environment.
- A documented local model baseline.
- A verified data-storage directory.

## Milestone 1 — Desktop foundation

Tasks:

- Build the desktop shell.
- Implement navigation.
- Create the AI side panel.
- Add an Analyse Page button.
- Display extracted page information.

Exit criteria:

- The application launches.
- The user can inspect a permitted test page.
- The application does not edit the page automatically.

## Milestone 2 — Local model integration

Tasks:

- Discover installed models.
- Test the local inference endpoint.
- Add structured request and response schemas.
- Implement timeouts and error handling.
- Build the model benchmark.

Exit criteria:

- Model responses are validated.
- Errors are visible and actionable.
- No silent cloud fallback occurs.

## Milestone 3 — Page-aware coding

Tasks:

- Extract a problem statement.
- Detect language.
- Identify starter code.
- Identify the editable region.
- Generate a proposed solution.
- Show the proposal to the user.

Exit criteria:

- The task representation matches the test page.
- The proposed solution is available for review.
- The editor remains unchanged before approval.

## Milestone 4 — Permission and editor integration

Tasks:

- Implement the approval state machine.
- Create the first editor adapter.
- Apply approved edits.
- Verify actual editor state.
- Handle cancellation and stale pages.

Exit criteria:

- Cancellation produces no edit.
- Approval is required for each material change.
- Unsupported editors fail safely.

## Milestone 5 — Testing and recovery

Tasks:

- Build the isolated test runner.
- Collect compiler output.
- Parse test results.
- Offer a corrected patch after failure.
- Enforce retry limits.

Exit criteria:

- Test status is based on actual execution.
- Failures are reported accurately.
- Correction attempts remain bounded.

## Milestone 6 — Dataset pipeline

Tasks:

- Verify permitted data sources.
- Create a dataset manifest.
- Implement downloads.
- Validate and clean files.
- Produce reproducible JSONL outputs.
- Record checksums and provenance.

Exit criteria:

- Dataset preparation can be repeated from the terminal.
- Invalid or unlicensed sources are rejected.
- All output paths are reported.
- Large data files are excluded from Git unless explicitly required.

## Milestone 7 — Model comparison

Tasks:

- Benchmark the existing model.
- Evaluate compatible coding-model alternatives.
- Compare correctness and resource usage.
- Select a model based on recorded results.

Exit criteria:

- A benchmark report exists.
- The model choice is evidence-based.
- The application supports replacing the model without redesigning the agent.

## Milestone 8 — Fine-tuning feasibility

Tasks:

- Analyse observed model weaknesses.
- Determine whether a dataset addresses those weaknesses.
- Check hardware and framework requirements.
- Run a small fine-tuning experiment only if feasible.
- Compare the result against the baseline.

Exit criteria:

- Fine-tuning is optional.
- Improvements are measured on held-out data.
- The baseline model remains available for comparison.

---

# 21. Automated Test Plan

The implementation must include tests for:

1. Empty practice editor.
2. Existing starter code.
3. TODO-region completion.
4. Wrong language detection.
5. Ambiguous instructions.
6. Unsupported editor.
7. User cancellation.
8. Invalid approval.
9. Page change after approval.
10. Editor change after approval.
11. Failed code insertion.
12. Incorrect editor readback.
13. Compilation failure.
14. Runtime timeout.
15. Missing local model.
16. Malformed model output.
17. Dataset checksum mismatch.
18. Invalid dataset records.
19. Licence metadata missing.
20. Prompt injection inside page content.
21. Attempted unauthorized submission.
22. Local model unavailable without internet.
23. Repeated model errors.
24. Recovery attempt limit.
25. Incorrect success reporting.

Security tests must confirm that unapproved editing and unauthorized submission cannot be triggered by model-generated text.

---

# 22. Antigravity Implementation Instructions

The following instructions should guide the coding agent in VS Code.

## Step 1: Inspect before editing

- Read the repository.
- Read the current README.
- Inspect dependency files.
- Identify completed functionality.
- Identify broken tests.
- Identify available local models.
- Check available disk space.

Produce a concise audit before modifying files.

## Step 2: Implement incrementally

Work on one milestone at a time.

For each milestone:

1. Create or modify the smallest required set of files.
2. Explain the changes.
3. Run the relevant tests.
4. Inspect errors.
5. Fix regressions.
6. Update the documentation.
7. Report the result.

Do not claim completion without evidence.

## Step 3: Dataset workflow

- Verify source and licence.
- Estimate size before downloading.
- Use a configurable data directory.
- Download incrementally.
- Verify checksums.
- Validate the format.
- Clean the data.
- Report accepted and rejected records.
- Make the resulting path visible in terminal output.

Do not train a model automatically immediately after downloading data.

## Step 4: Model workflow

- Test the existing model first.
- Save baseline metrics.
- Test candidate models one at a time.
- Avoid unnecessary duplicate downloads.
- Monitor memory.
- Record failures.
- Select the model based on results.
- Do not assume that a model name guarantees quality.

## Step 5: Preserve working code

- Avoid broad rewrites.
- Use version control.
- Keep changes focused.
- Run regression tests after modifications.
- Do not delete data or repositories without approval.
- Ask before large downloads, expensive operations, or destructive changes.

## Step 6: Completion reports

For each milestone, report:

- Files created.
- Files modified.
- Dependencies added.
- Commands executed.
- Tests run.
- Test results.
- Dataset paths.
- Model results.
- Known limitations.
- Remaining tasks.
- The exact next step.

Separate verified facts from planned work.

---

# 23. Definition of Done

The initial version is complete only when the following workflow works end to end in a permitted practice environment:

1. The user opens a practice coding page.
2. Wexa analyses the page.
3. Wexa identifies the problem and language.
4. Wexa detects the missing-code region.
5. The local model prepares a solution.
6. Wexa validates the proposal.
7. Wexa asks for permission.
8. The user approves the edit.
9. Wexa writes the code into the supported editor.
10. Wexa verifies the editor's actual state.
11. Wexa runs the permitted tests.
12. Wexa reads the actual results.
13. Wexa reports success, failure, or an unverified outcome accurately.
14. The application remains usable if the local model fails.
15. Automated tests confirm that unapproved edits do not occur.

Do not describe Wexa as supporting all websites until individual adapters and site behaviours have been tested.

---

# 24. Immediate Next Steps

Follow this order:

**First:** Inspect the existing project and development environment.

**Second:** Verify Ollama and benchmark the current model.

**Third:** Create the evaluation harness and the first small set of manually verified practice tasks.

**Fourth:** Implement page analysis and structured problem extraction.

**Fifth:** Build a purpose-built practice page and the first editor adapter.

**Sixth:** Implement the approval dialog and verify insertion.

**Seventh:** Add isolated testing and recovery.

**Eighth:** Implement the dataset download and preparation pipeline.

**Ninth:** Benchmark alternative local coding models.

**Tenth:** Consider fine-tuning only after the baseline and evaluation results identify a real need.

## Final engineering principle

Wexa Browser should be built as a controlled browser agent with a replaceable local model, not as a language model with unrestricted access to the computer.

The model provides intelligence. The browser layer provides observations. The orchestrator controls the workflow. The approval system controls user-authorized actions. The editor adapters perform changes. The test runner verifies results.

That separation is the foundation for making Wexa reliable, maintainable, privacy-conscious, and practical on the available hardware.
