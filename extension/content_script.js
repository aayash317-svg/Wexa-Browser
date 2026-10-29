/**
 * Wexa Browser Extension — Active Page Content Script
 * Observes the live page DOM, extracts accessible elements with BIDs,
 * and executes approved safe browser actions.
 */

(() => {
  let bidCounter = 1;

  function extractLivePageObservation() {
    const headings = Array.from(document.querySelectorAll("h1, h2, h3"))
      .map(h => h.innerText.trim())
      .filter(t => t.length > 0)
      .slice(0, 8);

    const interactiveElements = [];
    const candidates = document.querySelectorAll(
      "button, a[href], input, textarea, select, [role='button'], [role='link'], .monaco-editor, .CodeMirror"
    );

    for (const el of Array.from(candidates).slice(0, 40)) {
      const tag = el.tagName.toLowerCase();
      const isVisible = el.offsetWidth > 0 && el.offsetHeight > 0;
      if (!isVisible && tag !== "input" && tag !== "textarea") continue;

      let bid = el.getAttribute("data-wexa-bid");
      if (!bid) {
        bid = "ext-b" + (bidCounter++);
        el.setAttribute("data-wexa-bid", bid);
      }

      const text = (el.innerText || el.getAttribute("placeholder") || el.getAttribute("aria-label") || el.value || "").trim();
      const role = el.getAttribute("role") || tag;

      interactiveElements.push({
        element_id: bid,
        tag: tag,
        role: role,
        text: text.slice(0, 80),
        name: el.getAttribute("name") || null,
        selector: `[data-wexa-bid="${bid}"]`,
        input_type: el.getAttribute("type") || null,
        value: (tag === "input" || tag === "textarea") ? el.value : null,
        is_interactive: true,
        is_consequential: (role === "submit" || text.toLowerCase().includes("submit") || text.toLowerCase().includes("buy") || text.toLowerCase().includes("delete"))
      });
    }

    // Detect barriers
    const bodyText = (document.body ? document.body.innerText : "").toLowerCase();
    const barriers = [];
    if (bodyText.includes("recaptcha") || bodyText.includes("cloudflare") || bodyText.includes("verify you are human") || bodyText.includes("captcha")) {
      barriers.push("captcha");
    }
    if (bodyText.includes("sign in to continue") || bodyText.includes("login required") || bodyText.includes("enter password")) {
      barriers.push("login_required");
    }

    const hasEditor = Boolean(document.querySelector(".monaco-editor, .CodeMirror, textarea"));

    return {
      url: window.location.href,
      title: document.title,
      headings: headings,
      interactive_elements: interactiveElements,
      has_code_editor: hasEditor,
      barriers: barriers,
      visible_text_sample: (document.body ? document.body.innerText : "").slice(0, 2000)
    };
  }

  // Handle Action Execution Commands from Side Panel
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === "OBSERVE_PAGE") {
      const obs = extractLivePageObservation();
      sendResponse({ observation: obs });
      return true;
    }

    if (request.type === "EXECUTE_BROWSER_ACTION") {
      const action = request.action;
      try {
        if (action.action_type === "click") {
          const target = document.querySelector(action.target_selector || `[data-wexa-bid="${action.target_element_id}"]`);
          if (!target) throw new Error("Target element not found in DOM");
          target.click();
          sendResponse({ success: true, message: `Clicked element ${action.target_element_id}` });
        } else if (action.action_type === "type") {
          const target = document.querySelector(action.target_selector || `[data-wexa-bid="${action.target_element_id}"]`);
          if (!target) throw new Error("Target input not found in DOM");
          target.value = action.parameters.text || "";
          target.dispatchEvent(new Event("input", { bubbles: true }));
          target.dispatchEvent(new Event("change", { bubbles: true }));
          sendResponse({ success: true, message: `Typed into ${action.target_element_id}` });
        } else {
          sendResponse({ success: true, message: `Action ${action.action_type} recorded.` });
        }
      } catch (err) {
        sendResponse({ success: false, error: err.message });
      }
      return true;
    }
  });
})();

