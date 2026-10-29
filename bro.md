# Wexa Browser — Universal Web Page Analysis and Next-Step Intelligence

## Objective
Implement a feature in the existing Wexa Browser application that can analyse different web pages dynamically when a user provides a URL. The feature must work across different websites instead of being hardcoded for a single website.

## Required Functionality

1. **Accept Any URL**
   - Allow the user to enter a URL from different websites.
   - Open the requested page in the browser environment.
   - Support ordinary web pages, documentation, shopping pages, and coding practice pages where access is permitted.

2. **Automatically Analyse the Page**
   - Inspect the current page's visible text, headings, links, buttons, forms, input fields, and available accessibility information.
   - Detect the page's purpose and identify the main task or workflow.
   - For coding pages, inspect the visible question, instructions, programming language, and accessible code-editor context.
   - Use screenshots or visual analysis when DOM information is insufficient.

3. **Understand What Happens Next**
   - Determine the current page state and identify the likely next step based on the user's goal.
   - Recognise navigation options, task instructions, available actions, validation messages, and errors.
   - Handle navigation to subsequent pages by analysing each newly loaded page instead of relying on fixed selectors or predefined website workflows.

4. **Dynamic Page-Aware Reasoning**
   - Implement an observe → analyse → plan → act → verify loop.
   - After every navigation or meaningful interaction, inspect the updated page again.
   - Reconsider the next action based on the latest page state.
   - Detect failed actions, unexpected layouts, loading states, unsupported editors, and inaccessible content.
   - Never assume an action succeeded without checking the result.

5. **Use Wexa's Own Model**
   - Integrate this feature with Wexa's existing model interface.
   - Do not require OpenAI, GPT, or another external paid AI API.
   - Keep the model provider configurable so Wexa's own model can be connected as it develops.
   - Do not replace the existing model, backend, dataset pipeline, or project architecture.
   - Do not add unrelated model integrations or download large models automatically.

6. **Browser Interaction**
   - Where supported and permitted, allow the agent to navigate, click links, select options, and enter text.
   - Show the proposed action and its purpose in Wexa's interface.
   - Require explicit user approval before consequential actions, including submitting forms, uploading files, making purchases, or submitting coursework.
   - Do not bypass authentication, CAPTCHA, access restrictions, or website security controls.

7. **Universal Compatibility**
   - Avoid hardcoding behaviour for one domain.
   - Use DOM and accessibility information as the primary source, with visual analysis as a fallback.
   - Detect when a page uses a complex editor or another unsupported component and report the limitation honestly.
   - Support ordinary multi-page navigation and dynamically rendered content where technically feasible.

## Implementation Requirements

- Inspect the existing Wexa codebase before making changes.
- Reuse the current frontend, backend, model interface, and browser infrastructure wherever possible.
- Implement the smallest complete feature rather than rebuilding the application.
- Add appropriate loading, progress, error, and unsupported-page states.
- Add tests for URL handling, page analysis, navigation, action verification, and error recovery.
- Do not claim universal compatibility without testing it against multiple different websites.
- Preserve all existing features and dataset-related work.

## Expected Result

A user enters a URL into Wexa Browser. Wexa opens the page, analyses its content and current state, identifies the user's requested goal, determines the next appropriate step, and explains or performs permitted browser actions. It then analyses the updated page and continues until the goal is completed or a limitation requires user input.

Begin by inspecting the existing codebase, identifying the missing components, and implementing this feature without disrupting existing functionality.


he architecture should support this workflow:
1. Enter any URL

Article, shopping page, documentation, or coding practice page

2. Inspect the page

Read visible text, links, buttons, forms and editor context

3. Wexa's own model reasons

Understand the goal and choose the next action

4. Show a proposed action

Explain the next step and request approval where needed

5. Execute and verify

Navigate, click, type, inspect the updated page and recover from errors


What we should build into Wexa
- Universal URL support: no site-specific implementation required for every new page.
- Page understanding: use the DOM/accessibility tree and screenshots when needed.
- Action loop: observe → plan → act → verify → repeat.
- Own-model support: connect Wexa's reasoning engine to your own model, without requiring a GPT API.
- Safety: ask before submitting forms, uploading files, or taking other consequential actions.
- Fallbacks: detect unsupported editors, CAPTCHA, login barriers and failed actions instead of pretending the task succeeded.