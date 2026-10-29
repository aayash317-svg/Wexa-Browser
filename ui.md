# Wexa Browser — Implement the Approved UI Design

## Objective
Implement the existing Wexa Browser frontend to closely match the approved dark-premium UI mockup.

## 1. Overview & Brand Identity (Black + White Edition)

**Wexa Browser** features an integrated, high-contrast, strictly monochromatic black-and-white minimalist developer interface (`#000000`, `#080808`, `#121212`, `#1e1e1e`, `#ffffff`). Zero colors are used—ensuring a pure, distraction-free architectural aesthetic.

- **Design Philosophy**: Pure Black + White High-Contrast Architectural UI.
### 3. Logo
Create a consistent WEXA brand identity:
- Geometric W symbol.
- Electric-blue outline or accent.
- WEXA wordmark.
- Browser sub-label.
- Reuse the same branding throughout the application.

### 4. Functional requirements
- Analyse Page must call the existing page-analysis functionality when available.
- Datasets must use the existing dataset pipeline.
- Permission controls must require approval before editing webpage content.
- Code editor and testing actions must connect to existing backend APIs where supported.
- Offline status must reflect the actual model state, not a hardcoded success indicator.
- Add loading, success, empty, and error states.
- Keep the interface responsive.

### 5. Strict project-preservation rules
1. Inspect the existing repository before changing files.
2. Preserve the current backend, API contracts, dataset downloads, and training pipeline.
3. Do not replace working functionality with mock data.
4. Do not integrate Qwen, Llama, or any other existing local model.
5. Do not claim that code execution or tests succeeded unless verified.
6. Implement the frontend in small stages and report changed files and test results.
7. If an API is not ready, create a clear integration boundary rather than inventing its behaviour.

```
+---------------------------------------------------------------------------------------------------------+
| Window Titlebar: Traffic Lights (Red/Yellow/Green) | Tab: WEXA — Two Sum | [+]   | [—] [▢] [✕]          |
+---------------------------------------------------------------------------------------------------------+
| Browser Navigation: [←] [→] [↻] | [🔒 https://leetcode.com/problems/two-sum/ ★ ⎘]               | [W]  |
+--------+--------------------------------------------------------------+---------------------------------+
| Side-  | Embedded Browser Workspace                                   | AI Assistant Side Panel (Beta)  |
| bar    |                                                              |                                 |
|        | [Problem Pane]           | [Monaco / Code Editor]            | [User Message Bubble]           |
| [Home] | 1. Two Sum [Medium]      | Python3 v        [▶ Run] [Submit] | "Analyse this page and solve..."|
| [Brow] | Given an array of ints...| class Solution:                   |                                 |
| [AI]   |                          |     def twoSum(self, nums...):    | [Page Analysis Checklist]       |
| [Down] | Example 1:               |         # Write your code here    | ✓ Page Analysis Complete        |
| [Data] |   nums=[2,7,11,15], t=9  |         pass                      | ✓ Problem: Two Sum              |
| [Set]  |   Output: [0, 1]         |                                   | ✓ Language: Python              |
|        |                          +-----------------------------------+ ✓ Editor: Monaco                |
|        |                          | [Testcases Deck]                  | ✓ Target: Complete missing code |
|        |                          | Testcase | Result     [Run All]   | ✓ Permission: Required          |
| [●Off] |                          | ✓ Test Case 1: nums = [2,7,11,15] |                                 |
|        |                          | ○ Test Case 2: nums = [3,2,4]     | [Callout & Action Buttons]      |
|        |                          | ○ Test Case 3: nums = [3,3]       | [Generate Solution] [View Diff] |
|        |                          |                                   |                                 |
|        |                          |                                   | [Ask me anything... input]      |
|        |                          |                                   | [⚡ Analyse] [⎘ Insert] [▶ Test] |
+--------+--------------------------+-----------------------------------+---------------------------------+
| Bottom Control Deck                                                                                     |
| [1. Page Analysis: Done]  | [2. Permission Control: Allowed] | [3. Quick Actions]   | [4. WEXA Brand]   |
| ✓ Page type: Coding Plat. | Status: Allowed                  | > Analyse Current... | WEXA BROWSER      |
| ✓ Question: Detected      | [Allow] [Deny] [Ask Later]       | > Find Questions...  | Build•Learn•Grow  |
| ✓ Editor: Found (Python)  |                                  | > Dataset Manager... |                   |
| ✓ Action status: Ready    |                                  | > Settings...        |                   |
+---------------------------+----------------------------------+----------------------+-------------------+
```

---

## 3. Detailed Component Specifications

### 3.1 Left Navigation Sidebar
- **Wexa Logo**: Gradient squircle with custom white "W" monogram.
- **Navigation Items**:
  - `Home`: Dashboard & practice history.
  - `Browser` *(Active glowing blue pill)*: Active split-pane browser & coding workspace.
  - `AI Assistant`: Direct conversational assistant & autonomous tasks.
  - `Downloads`: Exported solution patches, benchmark data, and models.
  - `Datasets`: Automated telemetry collector and fine-tuning dataset manager.
  - `Settings`: Model selection (embedded GGUF engine), hardware threads, offline security boundaries.
- **Footer Badge**:
  - `● Offline Mode`: "Model running locally, No internet required."
  - Version label: `Wexa Browser v1.0.0`

### 3.2 Center Split Workspace (Browser & Practice Environment)
- **Problem Pane**:
  - Problem title: `1. Two Sum`, difficulty pill: `Medium`, interaction stats (`122K Likes`, `5.4K Comments`).
  - Company tags button (`🏢 Companies`).
  - Formatted problem statement, examples, and constraints.
- **Code Editor Pane**:
  - Header: Language selector (`Python3`, `Java`, `C++`), action buttons (`▶ Run`, `☁ Submit`).
  - Monaco / Textarea editor with line numbers, code highlighting, and starter function signature.
- **Testcases Tray**:
  - Tabs: `Testcase` and `Result`.
  - Batch action: `Run All`.
  - Live testcase items with status icons (`✓` green passing, `○` pending).

### 3.3 Right AI Assistant Panel
- **Header**: Sparkle icon, `AI Assistant`, `Beta` badge, and dismiss button (`✕`).
- **User Prompt Bubble**: Displays prompt ("Analyse this page and solve the coding question.").
- **Page Analysis Checklist**:
  - `✓ Page Analysis Complete`
  - `✓ Problem: Two Sum`
  - `✓ Language: Python`
  - `✓ Editor: Monaco`
  - `✓ Target: Complete missing code`
  - `✓ Permission: Required`
- **Callout Card**:
  - Explains the detected problem and asks user authorization before touching editor.
  - Primary button: `Generate Solution` (with loading spinner).
  - Secondary button: `View Details` (opens unified diff preview).
- **Footer Bar**:
  - Chat input box: "Ask me anything..." with send arrow.
  - Quick action pills: `[⚡ Analyse Page]`, `[⎘ Insert Code]`, `[▶ Run Tests]`.

### 3.4 Bottom Control Deck
- **Card 1: Page Analysis [Done]**: Summarizes page classification, question detection, and editor discovery.
- **Card 2: Permission Control [Allowed]**: Non-bypassable approval status with explicit `[Allow]`, `[Deny]`, and `[Ask Later]` controls.
- **Card 3: Quick Actions**: Direct links to analyse current page, find questions, manage datasets, or adjust settings.
- **Card 4: Brand Emblem**: WEXA logo with "Build • Learn • Grow" motto.

---

## 4. Design Tokens & Color Palette (Strictly Black & White)

| Token | Hex / Value | Description |
| :--- | :--- | :--- |
| `--bg-pure-black` | `#000000` | Window frame, code editor, deepest canvas |
| `--bg-deep` | `#080808` | Secondary navigation, problem pane background |
| `--bg-surface` | `#0F0F0F` | Headers, active cards, tab background |
| `--bg-elevated` | `#161616` | Active states, hover surfaces, inputs |
| `--border-subtle` | `#262626` | Structural borders, splitters, dividers |
| `--border-medium` | `#363636` | Card borders, interactive element strokes |
| `--border-bright` | `#FFFFFF` | Focus rings, active tab indicators, modals |
| `--text-white` | `#FFFFFF` | Primary headers, active buttons, code keywords |
| `--text-primary` | `#EDEDED` | Problem descriptions, editor text |
| `--text-secondary`| `#9E9E9E` | Muted subtitles, labels, secondary metadata |
| `--text-muted` | `#616161` | Inactive icons, line numbers |
| `--font-sans` | `Inter`, sans-serif | General UI typography |
| `--font-mono` | `JetBrains Mono`, monospace | Code editor, diff viewer, testcase logs |
