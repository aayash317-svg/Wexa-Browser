/**
 * Wexa Browser Extension — Persistent Side Panel Controller
 * Connects directly to active tab content scripts and local Wexa backend.
 */

const BACKEND_URL = "http://127.0.0.1:8765";

let currentActiveTab = null;
let currentObservation = null;
let currentProposal = null;

document.addEventListener("DOMContentLoaded", async () => {
  const panelPageTitle = document.getElementById("panelPageTitle");
  const panelPageCategory = document.getElementById("panelPageCategory");
  const panelPageUrl = document.getElementById("panelPageUrl");
  const btnRefresh = document.getElementById("btnRefreshObservation");
  const backendStatusText = document.getElementById("backendStatusText");

  const statHeadings = document.getElementById("statHeadings");
  const statElements = document.getElementById("statElements");
  const statEditor = document.getElementById("statEditor");
  const statBarriers = document.getElementById("statBarriers");
  const panelSummaryText = document.getElementById("panelSummaryText");

  const actionHeading = document.getElementById("actionHeading");
  const actionExplanation = document.getElementById("actionExplanation");
  const actionConfidence = document.getElementById("actionConfidence");
  const btnExecuteAction = document.getElementById("btnExecuteAction");
  const btnRejectAction = document.getElementById("btnRejectAction");

  const verificationCard = document.getElementById("verificationCard");
  const verificationLog = document.getElementById("verificationLog");

  const panelChatInput = document.getElementById("panelChatInput");
  const panelSendBtn = document.getElementById("panelSendBtn");

  // Check Backend Connection
  async function checkBackend() {
    try {
      const res = await fetch(`${BACKEND_URL}/health`, { signal: AbortSignal.timeout(1500) });
      if (res.ok) {
        backendStatusText.innerText = "ONLINE (LOCAL)";
      } else {
        backendStatusText.innerText = "OFFLINE";
      }
    } catch {
      backendStatusText.innerText = "OFFLINE";
    }
  }

  // Observe Active Tab
  async function inspectActiveTab() {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      if (!tab) return;
      currentActiveTab = tab;

      panelPageTitle.innerText = tab.title || "Untitled Tab";
      panelPageUrl.innerText = tab.url || "about:blank";

      // Message content script in the active tab to extract DOM
      const response = await chrome.tabs.sendMessage(tab.id, { type: "OBSERVE_PAGE" }).catch(() => null);

      if (response && response.observation) {
        currentObservation = response.observation;
        renderObservation(currentObservation);
        planNextAction();
      } else {
        // Fallback: send URL to backend observer
        const backendRes = await fetch(`${BACKEND_URL}/api/browser/navigate`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ url: tab.url })
        }).catch(() => null);

        if (backendRes && backendRes.ok) {
          const data = await backendRes.json();
          currentObservation = data.observation;
          renderObservation(currentObservation);
          planNextAction();
        }
      }
    } catch (err) {
      panelSummaryText.innerText = "Could not observe active tab: " + err.message;
    }
  }

  function renderObservation(obs) {
    panelPageTitle.innerText = obs.title || currentActiveTab?.title || "Page";
    panelPageCategory.innerText = (obs.page_type || "PAGE").toUpperCase();

    statHeadings.innerText = obs.headings ? obs.headings.length : 0;
    statElements.innerText = obs.interactive_elements ? obs.interactive_elements.length : 0;
    statEditor.innerText = obs.has_code_editor ? "Yes" : "None";
    statBarriers.innerText = (obs.barriers && obs.barriers.length) ? obs.barriers.join(", ") : "None";

    panelSummaryText.innerText = obs.visible_summary || `Inspected ${obs.title}. Ready for instruction.`;
  }

  async function planNextAction(goal = null) {
    actionHeading.innerText = "Reasoning...";
    actionExplanation.innerText = "Synthesizing structured action plan via Wexa's local model...";

    try {
      const res = await fetch(`${BACKEND_URL}/api/browser/plan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_goal: goal })
      });

      if (res.ok) {
        const data = await res.json();
        currentProposal = data.proposed_action;
        actionHeading.innerText = `${currentProposal.action_type.toUpperCase()}: ${currentProposal.target_element_id || 'Page'}`;
        actionExplanation.innerText = currentProposal.explanation;
        actionConfidence.innerText = `${Math.round(currentProposal.confidence * 100)}% CONFIDENCE`;
        btnExecuteAction.disabled = false;
      }
    } catch (e) {
      actionHeading.innerText = "Manual Inspection Mode";
      actionExplanation.innerText = "Active page observed. You can interact directly or enter a goal below.";
    }
  }

  // Execute Action
  btnExecuteAction.addEventListener("click", async () => {
    if (!currentProposal) return;
    btnExecuteAction.disabled = true;
    btnExecuteAction.innerText = "Executing...";

    try {
      // 1. Try in-tab execution via content script
      const tabRes = await chrome.tabs.sendMessage(currentActiveTab.id, {
        type: "EXECUTE_BROWSER_ACTION",
        action: currentProposal
      }).catch(() => null);

      verificationCard.style.display = "block";
      if (tabRes && tabRes.success) {
        verificationLog.textContent = `[SUCCESS] ${tabRes.message}\nAction verified in live DOM context.\nRe-observing updated state...`;
      } else {
        // Fallback to backend execution
        const res = await fetch(`${BACKEND_URL}/api/browser/action`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ action: currentProposal, user_approved: true })
        });
        const data = await res.json();
        verificationLog.textContent = `[VERIFIED] ${data.result.message}\nState changed: ${data.result.state_changed}`;
      }

      setTimeout(inspectActiveTab, 800);
    } catch (e) {
      verificationCard.style.display = "block";
      verificationLog.textContent = `[ERROR] Failed to execute action: ${e.message}`;
    } finally {
      btnExecuteAction.disabled = false;
      btnExecuteAction.innerHTML = `<span>Execute Action</span> <span class="arrow">➔</span>`;
    }
  });

  btnRejectAction.addEventListener("click", () => {
    actionHeading.innerText = "Action Dismissed";
    actionExplanation.innerText = "The proposed action was dismissed. You can type another instruction below.";
    currentProposal = null;
  });

  btnRefresh.addEventListener("click", inspectActiveTab);

  // Chat bar
  panelSendBtn.addEventListener("click", () => {
    const text = panelChatInput.value.trim();
    if (!text) return;
    panelChatInput.value = "";
    planNextAction(text);
  });

  panelChatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") panelSendBtn.click();
  });

  // Quick Tags
  document.getElementById("tagSolveCode").addEventListener("click", () => planNextAction("solve coding problem"));
  document.getElementById("tagFindPricing").addEventListener("click", () => planNextAction("find price and compare options"));
  document.getElementById("tagSummarize").addEventListener("click", () => planNextAction("summarize main content"));

  // Listen for Tab Change Notifications from background.js
  chrome.runtime.onMessage.addListener((msg) => {
    if (msg.type === "ACTIVE_TAB_CHANGED") {
      inspectActiveTab();
    }
  });

  // Init
  checkBackend();
  inspectActiveTab();
});

