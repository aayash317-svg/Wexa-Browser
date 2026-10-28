# Wexa Browser — UI & Interface Specification

![WEXA AI Browser Interface Mockup](./WEXA%20AI%20Browser%20Interface%20Mockup.png)

## 1. Overview & Brand Identity

**Wexa Browser** features an integrated, high-contrast, modern dark cyberpunk/developer UI (`#070D1B`, `#0B132B`, `#111C38`) with electric neon blue (`#1E6FFF`) and cyan/glow (`#38BDF8`) accents.

- **Brand Statement**: "Your AI-Powered Browser: Read • Analyse • Code • Solve."
- **Tagline**: "SMARTER BROWSING. FASTER SOLUTIONS."
- **Motto**: "Build • Learn • Grow"

---

## 2. Layout & Viewport Breakdown

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

## 4. Design Tokens & Color Palette

| Token | Hex / Value | Description |
| :--- | :--- | :--- |
| `--bg-darkest` | `#070D1B` | Window frame, main application background |
| `--bg-surface` | `#0B132B` | Navigation sidebar, titlebar, bottom deck |
| `--bg-card` | `#111C38` | AI Assistant panel, card containers |
| `--border-color` | `#1C2A4A` | Structural borders, splitters, dividers |
| `--primary-blue` | `#1E6FFF` | Primary action buttons, active navigation item |
| `--accent-glow` | `#38BDF8` | Brand glow, status checkmarks, active badges |
| `--success-green` | `#10B981` | Passing tests, allowed permissions, success tags |
| `--warning-yellow`| `#F59E0B` | Medium difficulty badge, review notices |
| `--text-primary` | `#F8FAFC` | Main headings, code text, active labels |
| `--text-secondary`| `#94A3B8` | Descriptions, problem body, muted subtitles |
| `--font-sans` | `Inter`, sans-serif | General UI typography |
| `--font-mono` | `JetBrains Mono`, monospace | Code editor, diff viewer, testcase logs |
