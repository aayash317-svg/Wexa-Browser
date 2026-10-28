# Wexa Browser — UI & UX Specification

*Derived directly from the official interface mockup (`WEXA AI Browser Interface Mockup.png`).*

---

## 1. Visual Theme & Color Palette

| Token Name | Hex Code | Usage |
| :--- | :--- | :--- |
| **Background Darkest** | `#070D1B` | App outer window frame, root background |
| **Surface Dark (Sidebar/Deck)**| `#0B132B` | Left sidebar, bottom deck cards, header |
| **Surface Card / Active** | `#111C38` | AI Assistant panel, card backgrounds |
| **Border / Subtle Divider** | `#1C2A4A` | Card borders, splitters, tab dividers |
| **Primary Accent Blue** | `#1E6FFF` | Primary buttons (`Generate Solution`, `Allow`), active pills |
| **Accent Glow / Neon** | `#38BDF8` | Brand glow, status checkmarks, active icons |
| **Success Green** | `#10B981` | Verification pills, checkmarks, passing tests |
| **Warning / Notice Yellow** | `#F59E0B` | Permission required alerts, diff notices |
| **Text Primary** | `#F8FAFC` | Headings, active labels, code |
| **Text Secondary / Muted** | `#94A3B8` | Subtitles, hints, constraints |

---

## 2. Layout Grid & Structure

```
+--------------------------------------------------------------------------------------------------------+
| Top Window Bar: Traffic Lights | Tab ("WEXA") | +                                | Min | Max | Close   |
+--------------------------------------------------------------------------------------------------------+
| Browser Navigation: [<-] [->] [Refresh] [ URL: https://...                         ] [Star] [Share] [W]|
+--------+-----------------------------------------------------------+-----------------------------------+
| Side-  | Embedded Browser / Webview Area                           | Right AI Assistant Panel          |
| bar    |                                                           | - Header: AI Assistant (Beta) [X] |
|        | - Problem Statement Area (Title, Difficulty, Constraints) | - Conversation / Execution Feed   |
| [Home] | - Interactive Code Editor (Monaco / Textarea)             | - Status Checklist:               |
| [Brows]| - Testcases Deck (Run, Test Case 1, 2, 3)                 |   * Page Analysis Complete        |
| [AI]   |                                                           |   * Language: Python              |
| [Down] |                                                           |   * Editor: Monaco                |
| [Data] |                                                           |   * Permission: Required          |
| [Set]  |                                                           | - Action Callout Card:            |
|        |                                                           |   [Generate Solution] [View Diff] |
| [●Off] |                                                           | - Prompt Bar & Quick Action Pills:|
|        |                                                           |   [Analyse Page] [Insert] [Test]  |
+--------+-----------------------------------------------------------+-----------------------------------+
| Bottom Control Deck                                                                                    |
| [ Page Analysis: Done ] | [ Permission Control: Allowed ] | [ Quick Actions ] | [ WEXA Brand Card ]    |
+--------------------------------------------------------------------------------------------------------+
```

---

## 3. Core Component Specifications

### 3.1 Left Navigation Sidebar
- **Wexa Logo**: Gradient icon with bold typography.
- **Nav Items**:
  - `Home`: Overview & recent practice history.
  - `Browser` *(Active)*: Main split-view workspace.
  - `AI Assistant`: Direct conversational / agent control.
  - `Downloads`: Exported code patches, local datasets.
  - `Datasets`: Automated training telemetry manager.
  - `Settings`: Model selection (GGUF runner), offline limits.
- **Status Indicator**:
  - `● Offline Mode`: "Model running locally, No internet required."
  - `Wexa Browser v1.0.0` version string.

### 3.2 Right AI Assistant Sidecar Panel
- **State 1: Initial Page Inspection**
  - Displays structured breakdown: Problem title, language, editor type, missing region.
  - Explains proposal and asks for authorization.
- **State 2: Solution Preview & Approval**
  - Unified diff view showing original starter code vs proposed replacement.
  - Explicit `[Generate Solution]` / `[Allow]` button triggering code insertion.
- **State 3: Verification & Test Execution**
  - Real-time status: Editor write verified $\rightarrow$ Sandboxed test runner status (`PASS` / `FAIL`).
- **Quick Action Pills**:
  - `Analyse Page`: Sends page text and starter code to `/api/analyze-page`.
  - `Insert Code`: Triggers approval and writes into the active editor.
  - `Run Tests`: Executes isolated test suite in sandbox.

### 3.3 Bottom Control Deck
- **Page Analysis Card**: Shows page type detection (Coding Platform) and editor detection status.
- **Permission Control Card**: Clear status tag (`Allowed`, `Pending`, `Denied`) with primary `[Allow]`, `[Deny]`, `[Ask Later]` controls.
- **Quick Actions Deck**: Fast-path shortcuts to analyse, find problems, or open dataset manager.
