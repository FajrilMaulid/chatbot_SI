// ==========================================
// CONFIGURATION
// ==========================================
const API_BASE_URL = window.location.origin;
const API_CHAT_ENDPOINT = `${API_BASE_URL}/api/chat`;

// ==========================================
// DOM ELEMENTS
// ==========================================
const chatForm = document.getElementById("chatForm");
const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");
const chatMessages = document.getElementById("chatMessages");
const chatContainer = document.getElementById("chatContainer");
const typingIndicator = document.getElementById("typingIndicator");

// ==========================================
// STATE
// ==========================================
let isProcessing = false;

// ==========================================
// UTILITY FUNCTIONS
// ==========================================

/**
 * Get current time in readable format
 */
function getCurrentTime() {
  const now = new Date();
  const hours = now.getHours().toString().padStart(2, "0");
  const minutes = now.getMinutes().toString().padStart(2, "0");
  return `${hours}:${minutes}`;
}

/**
 * Scroll chat to bottom with smooth animation
 */
function scrollToBottom() {
  setTimeout(() => {
    chatMessages.scrollTo({
      top: chatMessages.scrollHeight,
      behavior: "smooth",
    });
  }, 100);
}

/**
 * Show typing indicator
 */
function showTypingIndicator() {
  typingIndicator.style.display = "block";
  scrollToBottom();
}

/**
 * Hide typing indicator
 */
function hideTypingIndicator() {
  typingIndicator.style.display = "none";
}

/**
 * Create message element
 */
function createMessageElement(content, isUser = false) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${isUser ? "user-message" : "bot-message"}`;

  const avatar = document.createElement("div");
  avatar.className = "message-avatar";

  if (isUser) {
    avatar.innerHTML = `
            <img src="/static/images/user-icon.svg" alt="User Avatar">
        `;
  } else {
    avatar.innerHTML = `
            <img src="/static/images/robot-icon.svg" alt="Bot Avatar">
        `;
  }

  const messageContent = document.createElement("div");
  messageContent.className = "message-content";

  const messageBubble = document.createElement("div");
  messageBubble.className = "message-bubble";

  // Format content: handle line breaks
  const formattedContent = content
    .split("\n")
    .map((line) => {
      if (line.trim() === "") return "";
      return `<p>${escapeHtml(line)}</p>`;
    })
    .join("");

  messageBubble.innerHTML = formattedContent;

  const messageTime = document.createElement("span");
  messageTime.className = "message-time";
  messageTime.textContent = getCurrentTime();

  messageContent.appendChild(messageBubble);
  messageContent.appendChild(messageTime);

  messageDiv.appendChild(avatar);
  messageDiv.appendChild(messageContent);

  return messageDiv;
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Add message to chat
 */
function addMessage(content, isUser = false) {
  const messageElement = createMessageElement(content, isUser);
  chatMessages.appendChild(messageElement);

  // Trigger animation
  setTimeout(() => {
    messageElement.setAttribute("data-animate", "true");
  }, 10);

  scrollToBottom();
}

/**
 * Set processing state
 */
function setProcessing(processing) {
  isProcessing = processing;
  sendButton.disabled = processing;
  userInput.disabled = processing;

  if (processing) {
    showTypingIndicator();
  } else {
    hideTypingIndicator();
  }
}

// ==========================================
// API FUNCTIONS
// ==========================================

/**
 * Send message to chatbot API
 */
async function sendMessage(message) {
  try {
    const response = await fetch(API_CHAT_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (data.status === "success") {
      return data.response;
    } else {
      throw new Error(data.error || "Unknown error occurred");
    }
  } catch (error) {
    console.error("Error sending message:", error);
    throw error;
  }
}

// ==========================================
// EVENT HANDLERS
// ==========================================

/**
 * Handle form submission
 */
async function handleSubmit(e) {
  e.preventDefault();

  // Prevent multiple submissions
  if (isProcessing) return;

  const message = userInput.value.trim();

  // Validate input
  if (!message) return;

  // Clear input
  userInput.value = "";

  // Add user message to chat
  addMessage(message, true);

  // Set processing state
  setProcessing(true);

  try {
    // Send message to API
    const botResponse = await sendMessage(message);

    // Simulate typing delay for better UX
    await new Promise((resolve) => setTimeout(resolve, 500));

    // Add bot response to chat
    addMessage(botResponse, false);
  } catch (error) {
    // Show error message
    addMessage("Maaf, terjadi kesalahan. Silakan coba lagi.", false);
  } finally {
    // Reset processing state
    setProcessing(false);

    // Focus back to input
    userInput.focus();
  }
}

// ==========================================
// INITIALIZATION
// ==========================================

/**
 * Initialize application
 */
function init() {
  // Add event listeners
  chatForm.addEventListener("submit", handleSubmit);

  // Focus input on load
  userInput.focus();

  // Handle Enter key (without Shift for submit)
  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      chatForm.dispatchEvent(new Event("submit"));
    }
  });

  console.log("🤖 Chatbot initialized successfully!");
}

// Run initialization when DOM is ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
