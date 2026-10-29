/**
 * Wexa Browser Extension — Background Service Worker
 * Tracks active tabs, observes page navigation events, and coordinates
 * communication between the active web page, Wexa Side Panel, and local backend.
 */

const WEXA_BACKEND_URL = "http://127.0.0.1:8765";

// Open side panel on extension action click
chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true }).catch(console.error);

// Active Tab Tracking & Real-Time Sync
chrome.tabs.onActivated.addListener(async (activeInfo) => {
  notifySidePanelOfTabChange(activeInfo.tabId);
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.active) {
    notifySidePanelOfTabChange(tabId);
  }
});

async function notifySidePanelOfTabChange(tabId) {
  try {
    const tab = await chrome.tabs.get(tabId);
    if (!tab || !tab.url || tab.url.startsWith("chrome://")) return;

    // Send update to open side panel
    chrome.runtime.sendMessage({
      type: "ACTIVE_TAB_CHANGED",
      tab: {
        id: tab.id,
        url: tab.url,
        title: tab.title
      }
    }).catch(() => {
      // Side panel may not be open yet
    });
  } catch (err) {
    console.warn("Tab notification error:", err);
  }
}

// Message Dispatcher
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === "GET_ACTIVE_TAB_INFO") {
    chrome.tabs.query({ active: true, currentWindow: true }).then(([tab]) => {
      sendResponse({ tab });
    });
    return true;
  }

  if (request.type === "EXECUTE_BROWSER_ACTION") {
    // Forward action execution into the active tab's content script
    chrome.tabs.query({ active: true, currentWindow: true }).then(([tab]) => {
      if (!tab) return sendResponse({ success: false, error: "No active tab" });
      chrome.tabs.sendMessage(tab.id, request).then(sendResponse).catch(err => {
        sendResponse({ success: false, error: err.message });
      });
    });
    return true;
  }
});

