# Wexa Browser — Website Restrictions and Offline Operation

## 1. Objective

Wexa Browser should detect website restrictions, understand what actions are permitted, and handle restricted situations intelligently. The browser should work offline wherever possible, using our own trained model without depending on external AI APIs or other local model integrations.

## 2. Website Restriction Detection

Wexa should identify restrictions such as:

- Disabled text editors or input fields.
- Websites that block automated browser interactions.
- Copy-and-paste restrictions.
- Read-only pages and protected form fields.
- CAPTCHA and human-verification challenges.
- Login requirements and permission errors.
- Rate limits and temporary access restrictions.
- Websites that prohibit automated editing or code submission.
- Restricted examinations and coding assessments.

Wexa should distinguish between ordinary interface limitations and security or policy restrictions.

## 3. Restriction Handling

When Wexa encounters a restriction, it should:

1. Detect the restriction.
2. Identify the affected element or browser action.
3. Determine whether the action is permitted.
4. Use an available, authorized alternative when one exists.
5. Ask the user for clarification or permission when necessary.
6. Stop the restricted action when authorization is unavailable.
7. Explain the restriction and offer a legitimate alternative.

Wexa must not assume that a restriction can be ignored merely because the user requests it.

## 4. Authorized Alternatives

Where permitted, Wexa may:

- Use supported accessibility interfaces.
- Interact with normal form fields and editors.
- Use an official API or documented integration.
- Save generated code locally for manual insertion.
- Explain how the user can complete an action manually.
- Retry a failed action when it is a temporary interface or technical error.
- Ask the user to complete a legitimate verification step themselves.

Wexa must not circumvent CAPTCHA, authentication, authorization checks, access controls, anti-bot protections, or assessment safeguards.

## 5. Offline Model Operation

Wexa's own trained model should support offline operation.

Requirements:

- Run the model locally without external AI API calls.
- Analyse locally available webpage information.
- Classify detected restrictions.
- Decide whether an action is allowed, requires confirmation, or must stop.
- Generate code and explanations when supported by the trained model.
- Store datasets, model weights, and evaluation reports locally.
- Avoid uploading webpage content, source code, credentials, cookies, or personal information to external services.
- Provide a clear error message when a required resource is unavailable offline.

**Important:** Offline operation does not automatically grant permission to bypass a website's restrictions.

## 6. Permission and Safety Rules

- Obtain user approval before modifying webpage content or code editors.
- Respect website terms, access permissions, and applicable assessment rules.
- Never steal, extract, or expose authentication tokens, cookies, or credentials.
- Never disable security protections to force an action.
- Never claim that an action succeeded without verifying its result.
- Keep an audit record of restriction detection and the resulting decision without storing secrets.

## 7. Expected Behaviour

| Situation | Wexa behaviour |
|---|---|
| Editor is empty and editing is permitted | Ask permission, then insert code |
| Editor is read-only | Explain the limitation and offer a local code file |
| Paste is disabled | Use another supported method only if authorized |
| CAPTCHA appears | Ask the user to complete verification |
| Login is required | Ask the user to sign in through the legitimate process |
| Access is denied | Stop and explain the denial |
| Automation is prohibited | Do not automate the restricted action |
| Website is unavailable offline | Explain which feature requires connectivity |
| Browser action fails unexpectedly | Diagnose and retry only when appropriate |

## 8. Acceptance Criteria

Wexa is ready for restriction-handling testing when it can:

- Detect common interface and access restrictions.
- Distinguish technical failures from authorization restrictions.
- Operate its own trained model offline when its local resources are available.
- Offer legitimate alternatives for blocked actions.
- Request permission before editing.
- Stop prohibited actions safely.
- Verify successful actions and report failures honestly.
