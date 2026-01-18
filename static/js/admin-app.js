// Admin Dashboard JavaScript
// ==========================================

const API_BASE = window.location.origin;

// State
let currentPage = "overview";
let currentChatLogsPage = 0;
let chatLogsPerPage = 50;
let allIntents = [];

// ==========================================
// INITIALIZATION
// ==========================================

document.addEventListener("DOMContentLoaded", async () => {
  // Check authentication
  const isAuthenticated = await checkAuth();

  if (!isAuthenticated) {
    window.location.href = "/admin.html";
    return;
  }

  // Setup navigation
  setupNavigation();

  // Setup logout
  document.getElementById("logoutBtn").addEventListener("click", handleLogout);

  // Load initial data
  loadOverviewData();

  // Setup search
  const searchInput = document.getElementById("searchChatLogs");
  if (searchInput) {
    searchInput.addEventListener("input", debounce(loadChatLogs, 500));
  }

  // Setup forms
  setupForms();
});

// ==========================================
// AUTHENTICATION
// ==========================================

async function checkAuth() {
  try {
    const response = await fetch(`${API_BASE}/api/admin/check-auth`);
    const data = await response.json();

    if (data.authenticated) {
      // Update UI with user info
      const username = data.user.username || "Admin";
      document.getElementById("adminUsername").textContent = username;
      document.getElementById("welcomeText").textContent =
        `Welcome back, ${username}!`;
      return true;
    }

    return false;
  } catch (error) {
    console.error("Auth check error:", error);
    return false;
  }
}

async function handleLogout() {
  try {
    await fetch(`${API_BASE}/api/admin/logout`, { method: "POST" });
    window.location.href = "/admin.html";
  } catch (error) {
    console.error("Logout error:", error);
    showToast("Logout failed", "error");
  }
}

// ==========================================
// NAVIGATION
// ==========================================

function setupNavigation() {
  const navItems = document.querySelectorAll(".nav-item");

  navItems.forEach((item) => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      const page = item.dataset.page;
      navigateTo(page);
    });
  });
}

function navigateTo(page) {
  // Update nav active state
  document.querySelectorAll(".nav-item").forEach((item) => {
    item.classList.remove("active");
  });

  document.querySelector(`[data-page="${page}"]`)?.classList.add("active");

  // Hide all pages
  document.querySelectorAll(".page-content").forEach((content) => {
    content.classList.remove("active");
    content.classList.add("hidden");
  });

  // Show selected page
  const pageElement = document.getElementById(`${page}-page`);
  if (pageElement) {
    pageElement.classList.remove("hidden");
    pageElement.classList.add("active");
  }

  // Update page title
  const titles = {
    overview: "Dashboard Overview",
    "chat-logs": "Chat Logs",
    "manage-intents": "Manage Intents",
  };
  document.getElementById("pageTitle").textContent =
    titles[page] || "Dashboard";

  // Load page data
  currentPage = page;
  loadPageData(page);
}

function loadPageData(page) {
  switch (page) {
    case "overview":
      loadOverviewData();
      break;
    case "chat-logs":
      loadChatLogs();
      break;
    case "manage-intents":
      loadIntents();
      break;
  }
}

// ==========================================
// OVERVIEW PAGE
// ==========================================

async function loadOverviewData() {
  try {
    const response = await fetch(`${API_BASE}/api/admin/stats`);
    const data = await response.json();

    if (data.status === "success") {
      const stats = data.data;
      document.getElementById("totalConversations").textContent =
        stats.total_conversations || 0;
      document.getElementById("totalIntents").textContent =
        stats.total_intents || 0;
      document.getElementById("totalPatterns").textContent =
        stats.total_patterns || 0;
      document.getElementById("todayConversations").textContent =
        stats.today_conversations || 0;
    }
  } catch (error) {
    console.error("Error loading stats:", error);
    showToast("Failed to load statistics", "error");
  }
}

// ==========================================
// CHAT LOGS PAGE
// ==========================================

async function loadChatLogs(page = 0) {
  const tbody = document.getElementById("chatLogsBody");
  tbody.innerHTML =
    '<tr><td colspan="5" class="loading-cell">Loading...</td></tr>';

  try {
    const searchTerm = document.getElementById("searchChatLogs")?.value || "";
    const offset = page * chatLogsPerPage;

    let url = `${API_BASE}/api/admin/chat-logs?limit=${chatLogsPerPage}&offset=${offset}`;
    if (searchTerm) {
      url += `&search=${encodeURIComponent(searchTerm)}`;
    }

    const response = await fetch(url);
    const data = await response.json();

    if (data.status === "success") {
      const logs = data.data.logs;
      const total = data.data.total;

      if (logs.length === 0) {
        tbody.innerHTML =
          '<tr><td colspan="5" class="loading-cell">No conversations found</td></tr>';
        return;
      }

      tbody.innerHTML = logs
        .map(
          (log) => `
        <tr>
          <td>${log.created_at || "N/A"}</td>
          <td>${log.session_id ? log.session_id.substring(0, 8) + "..." : "N/A"}</td>
          <td>${escapeHtml(log.user_message)}</td>
          <td>${escapeHtml(log.bot_response.substring(0, 100) + (log.bot_response.length > 100 ? "..." : ""))}</td>
          <td>${log.detected_intent || "N/A"}</td>
        </tr>
      `
        )
        .join("");

      // Update pagination
      updatePagination(
        "chatLogsPagination",
        page,
        total,
        chatLogsPerPage,
        loadChatLogs
      );
    }
  } catch (error) {
    console.error("Error loading chat logs:", error);
    tbody.innerHTML =
      '<tr><td colspan="5" class="loading-cell">Error loading chat logs</td></tr>';
    showToast("Failed to load chat logs", "error");
  }
}

// ==========================================
// MANAGE INTENTS PAGE
// ==========================================

async function loadIntents() {
  const container = document.getElementById("intentsContainer");
  container.innerHTML = '<div class="loading-cell">Loading intents...</div>';

  try {
    const response = await fetch(`${API_BASE}/api/admin/intents`);
    const data = await response.json();

    if (data.status === "success") {
      allIntents = data.data;
      renderIntents(allIntents);
    }
  } catch (error) {
    console.error("Error loading intents:", error);
    container.innerHTML =
      '<div class="loading-cell">Error loading intents</div>';
    showToast("Failed to load intents", "error");
  }
}

function renderIntents(intents) {
  const container = document.getElementById("intentsContainer");

  if (intents.length === 0) {
    container.innerHTML = '<div class="loading-cell">No intents found</div>';
    return;
  }

  container.innerHTML = intents
    .map(
      (intent) => `
    <div class="intent-card" data-intent-id="${intent.id}">
      <div class="intent-header">
        <h3>${escapeHtml(intent.intent_name)}</h3>
        <div class="intent-actions">
          <button class="edit-btn" onclick="showEditIntentDialog(${intent.id})">✏️ Edit</button>
          <button class="delete-btn" onclick="deleteIntent(${intent.id})">🗑️ Delete</button>
        </div>
      </div>
      <div class="intent-content">
        <div class="patterns-section">
          <h4>
            Patterns (${intent.patterns.length})
            <button class="add-item-btn" onclick="showAddPatternDialog(${intent.id})">+ Add</button>
          </h4>
          <ul class="item-list">
            ${intent.patterns
              .map(
                (p) => `
              <li>
                <span>${escapeHtml(p.text)}</span>
                <button class="delete-item-btn" onclick="deletePattern(${p.id})">✕</button>
              </li>
            `
              )
              .join("")}
            ${intent.patterns.length === 0 ? "<li>No patterns yet</li>" : ""}
          </ul>
        </div>
        <div class="responses-section">
          <h4>
            Responses (${intent.responses.length})
            <button class="add-item-btn" onclick="showAddResponseDialog(${intent.id})">+ Add</button>
          </h4>
          <ul class="item-list">
            ${intent.responses
              .map(
                (r) => `
              <li>
                <span>${escapeHtml(r.text.substring(0, 50) + (r.text.length > 50 ? "..." : ""))}</span>
                <button class="delete-item-btn" onclick="deleteResponse(${r.id})">✕</button>
              </li>
            `
              )
              .join("")}
            ${intent.responses.length === 0 ? "<li>No responses yet</li>" : ""}
          </ul>
        </div>
      </div>
    </div>
  `
    )
    .join("");
}

// ==========================================
// INTENT CRUD OPERATIONS
// ==========================================

function setupForms() {
  // Create Intent Form
  document
    .getElementById("createIntentForm")
    .addEventListener("submit", async (e) => {
      e.preventDefault();

      const intentName = document.getElementById("newIntentName").value.trim();
      const tag = document.getElementById("newIntentTag").value.trim();

      try {
        const response = await fetch(`${API_BASE}/api/admin/intents`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ intent_name: intentName, tag }),
        });

        const data = await response.json();

        if (data.status === "success") {
          showToast("Intent created successfully", "success");
          closeModal("createIntentModal");
          loadIntents();
          document.getElementById("createIntentForm").reset();
        } else {
          showToast(data.error || "Failed to create intent", "error");
        }
      } catch (error) {
        console.error("Error creating intent:", error);
        showToast("Failed to create intent", "error");
      }
    });

  // Edit Intent Form
  document
    .getElementById("editIntentForm")
    .addEventListener("submit", async (e) => {
      e.preventDefault();

      const intentId = document.getElementById("editIntentId").value;
      const intentName = document.getElementById("editIntentName").value.trim();
      const tag = document.getElementById("editIntentTag").value.trim();

      try {
        const response = await fetch(
          `${API_BASE}/api/admin/intents/${intentId}`,
          {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ intent_name: intentName, tag }),
          }
        );

        const data = await response.json();

        if (data.status === "success") {
          showToast("Intent updated successfully", "success");
          closeModal("editIntentModal");
          loadIntents();
        } else {
          showToast(data.error || "Failed to update intent", "error");
        }
      } catch (error) {
        console.error("Error updating intent:", error);
        showToast("Failed to update intent", "error");
      }
    });

  // Add Pattern Form
  document
    .getElementById("addPatternForm")
    .addEventListener("submit", async (e) => {
      e.preventDefault();

      const intentId = document.getElementById("patternIntentId").value;
      const patternText = document
        .getElementById("newPatternText")
        .value.trim();

      try {
        const response = await fetch(
          `${API_BASE}/api/admin/intents/${intentId}/patterns`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ pattern_text: patternText }),
          }
        );

        const data = await response.json();

        if (data.status === "success") {
          showToast("Pattern added successfully", "success");
          closeModal("addPatternModal");
          loadIntents();
          document.getElementById("addPatternForm").reset();
        } else {
          showToast(data.error || "Failed to add pattern", "error");
        }
      } catch (error) {
        console.error("Error adding pattern:", error);
        showToast("Failed to add pattern", "error");
      }
    });

  // Add Response Form
  document
    .getElementById("addResponseForm")
    .addEventListener("submit", async (e) => {
      e.preventDefault();

      const intentId = document.getElementById("responseIntentId").value;
      const responseText = document
        .getElementById("newResponseText")
        .value.trim();

      try {
        const response = await fetch(
          `${API_BASE}/api/admin/intents/${intentId}/responses`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ response_text: responseText }),
          }
        );

        const data = await response.json();

        if (data.status === "success") {
          showToast("Response added successfully", "success");
          closeModal("addResponseModal");
          loadIntents();
          document.getElementById("addResponseForm").reset();
        } else {
          showToast(data.error || "Failed to add response", "error");
        }
      } catch (error) {
        console.error("Error adding response:", error);
        showToast("Failed to add response", "error");
      }
    });
}

function showCreateIntentDialog() {
  openModal("createIntentModal");
}

function showEditIntentDialog(intentId) {
  const intent = allIntents.find((i) => i.id === intentId);
  if (!intent) return;

  document.getElementById("editIntentId").value = intent.id;
  document.getElementById("editIntentName").value = intent.intent_name;
  document.getElementById("editIntentTag").value = intent.tag || "";

  openModal("editIntentModal");
}

async function deleteIntent(intentId) {
  if (
    !confirm(
      "Are you sure you want to delete this intent? This will also delete all associated patterns and responses."
    )
  ) {
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/api/admin/intents/${intentId}`, {
      method: "DELETE",
    });

    const data = await response.json();

    if (data.status === "success") {
      showToast("Intent deleted successfully", "success");
      loadIntents();
    } else {
      showToast(data.error || "Failed to delete intent", "error");
    }
  } catch (error) {
    console.error("Error deleting intent:", error);
    showToast("Failed to delete intent", "error");
  }
}

function showAddPatternDialog(intentId) {
  document.getElementById("patternIntentId").value = intentId;
  document.getElementById("newPatternText").value = "";
  openModal("addPatternModal");
}

async function deletePattern(patternId) {
  if (!confirm("Delete this pattern?")) return;

  try {
    const response = await fetch(
      `${API_BASE}/api/admin/patterns/${patternId}`,
      {
        method: "DELETE",
      }
    );

    const data = await response.json();

    if (data.status === "success") {
      showToast("Pattern deleted", "success");
      loadIntents();
    } else {
      showToast(data.error || "Failed to delete pattern", "error");
    }
  } catch (error) {
    console.error("Error deleting pattern:", error);
    showToast("Failed to delete pattern", "error");
  }
}

function showAddResponseDialog(intentId) {
  document.getElementById("responseIntentId").value = intentId;
  document.getElementById("newResponseText").value = "";
  openModal("addResponseModal");
}

async function deleteResponse(responseId) {
  if (!confirm("Delete this response?")) return;

  try {
    const response = await fetch(
      `${API_BASE}/api/admin/responses/${responseId}`,
      {
        method: "DELETE",
      }
    );

    const data = await response.json();

    if (data.status === "success") {
      showToast("Response deleted", "success");
      loadIntents();
    } else {
      showToast(data.error || "Failed to delete response", "error");
    }
  } catch (error) {
    console.error("Error deleting response:", error);
    showToast("Failed to delete response", "error");
  }
}

// ==========================================
// MODAL MANAGEMENT
// ==========================================

function openModal(modalId) {
  document.getElementById(modalId).classList.add("active");
}

function closeModal(modalId) {
  document.getElementById(modalId).classList.remove("active");
}

// Close modal on outside click
document.addEventListener("click", (e) => {
  if (e.target.classList.contains("modal")) {
    e.target.classList.remove("active");
  }
});

// ==========================================
// UTILITY FUNCTIONS
// ==========================================

function showToast(message, type = "success") {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.className = `toast ${type} show`;

  setTimeout(() => {
    toast.classList.remove("show");
  }, 3000);
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

function updatePagination(containerId, currentPage, total, perPage, loadFunc) {
  const container = document.getElementById(containerId);
  const totalPages = Math.ceil(total / perPage);

  if (totalPages <= 1) {
    container.innerHTML = "";
    return;
  }

  let html = "";

  // Previous button
  html += `<button ${currentPage === 0 ? "disabled" : ""} onclick="${loadFunc.name}(${currentPage - 1})">← Previous</button>`;

  // Page info
  html += `<span>Page ${currentPage + 1} of ${totalPages}</span>`;

  // Next button
  html += `<button ${currentPage >= totalPages - 1 ? "disabled" : ""} onclick="${loadFunc.name}(${currentPage + 1})">Next →</button>`;

  container.innerHTML = html;
}
