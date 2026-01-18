// ==========================================
// CONFIGURATION
// ==========================================
const API_BASE_URL = window.location.origin;
const API_CHAT_ENDPOINT = `${API_BASE_URL}/api/chat`;

// Quick reply suggestions
const QUICK_REPLIES = [
  "Apa saja mata kuliah di Sistem Informasi?",
  "Bagaimana prospek kerja lulusan SI?",
  "Siapa saja dosen di prodi SI?",
  "Berapa lama masa studi program SI?",
];

// ==========================================
// DOM ELEMENTS
// ==========================================
const chatForm = document.getElementById("chatForm");
const userInput = document.getElementById("userInput");
const sendButton = document.getElementById("sendButton");
const chatMessages = document.getElementById("chatMessages");
const chatContainer = document.getElementById("chatContainer");
const typingIndicator = document.getElementById("typingIndicator");
const quickRepliesContainer = document.getElementById("quickReplies");

// ==========================================
// STATE
// ==========================================
let isProcessing = false;
let messageCount = 0;

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
function scrollToBottom(instant = false) {
  setTimeout(
    () => {
      chatMessages.scrollTo({
        top: chatMessages.scrollHeight,
        behavior: instant ? "auto" : "smooth",
      });
    },
    instant ? 0 : 100
  );
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
 * Show quick replies
 */
function showQuickReplies() {
  if (messageCount === 0) {
    const buttonsContainer = quickRepliesContainer.querySelector(
      ".quick-reply-buttons"
    );
    buttonsContainer.innerHTML = "";

    QUICK_REPLIES.forEach((reply) => {
      const button = document.createElement("button");
      button.className = "quick-reply-btn";
      button.textContent = reply;
      button.type = "button"; // Prevent form submission

      // Use addEventListener instead of onclick
      button.addEventListener("click", async () => {
        await handleQuickReply(reply);
      });

      buttonsContainer.appendChild(button);
    });

    quickRepliesContainer.style.display = "block";

    // Auto-hide after first message
    messageCount++;
  }
}

/**
 * Hide quick replies
 */
function hideQuickReplies() {
  quickRepliesContainer.style.display = "none";
}

/**
 * Handle quick reply click - sends message directly
 */
async function handleQuickReply(text) {
  // Prevent if already processing
  if (isProcessing) return;

  // Validate input
  if (!text || !text.trim()) return;

  // Hide quick replies
  hideQuickReplies();

  // Add user message to chat
  await addMessage(text, true, false);

  // Set processing state
  setProcessing(true);

  try {
    // Send message to API
    const botResponse = await sendMessage(text);

    // Simulate typing delay for better UX
    await new Promise((resolve) => setTimeout(resolve, 800));

    // Add bot response to chat with typing animation
    await addMessage(botResponse, false, true);
  } catch (error) {
    // Show error message
    await addMessage(
      "Maaf, terjadi kesalahan. Silakan coba lagi.",
      false,
      false
    );
  } finally {
    // Reset processing state
    setProcessing(false);

    // Focus back to input
    userInput.focus();
  }
}

/**
 * Create typing animation effect
 */
async function typeText(element, text, speed = 30) {
  element.textContent = "";
  let i = 0;

  return new Promise((resolve) => {
    const interval = setInterval(() => {
      if (i < text.length) {
        element.textContent += text.charAt(i);
        i++;
        scrollToBottom();
      } else {
        clearInterval(interval);
        resolve();
      }
    }, speed);
  });
}

/**
 * Create message element
 */
function createMessageElement(content, isUser = false, useTyping = false) {
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
  const lines = content.split("\n").filter((line) => line.trim() !== "");

  if (useTyping && !isUser) {
    // Create paragraphs for typing animation
    lines.forEach((line) => {
      const p = document.createElement("p");
      messageBubble.appendChild(p);
    });
  } else {
    // Regular rendering
    const formattedContent = lines
      .map((line) => `<p>${escapeHtml(line)}</p>`)
      .join("");
    messageBubble.innerHTML = formattedContent;
  }

  const messageFooter = document.createElement("div");
  messageFooter.className = "message-footer";

  const messageTime = document.createElement("span");
  messageTime.className = "message-time";
  messageTime.textContent = getCurrentTime();

  messageFooter.appendChild(messageTime);

  // Add reactions for bot messages
  if (!isUser) {
    const reactionsDiv = document.createElement("div");
    reactionsDiv.className = "message-reactions";

    const reactions = ["👍", "❤️", "🎉"];
    reactions.forEach((emoji) => {
      const btn = document.createElement("button");
      btn.className = "reaction-btn";
      btn.setAttribute("data-reaction", emoji);
      btn.textContent = emoji;
      btn.title = getReactionTitle(emoji);
      btn.onclick = () => handleReaction(btn);
      reactionsDiv.appendChild(btn);
    });

    messageFooter.appendChild(reactionsDiv);
  }

  messageContent.appendChild(messageBubble);
  messageContent.appendChild(messageFooter);

  messageDiv.appendChild(avatar);
  messageDiv.appendChild(messageContent);

  return { element: messageDiv, bubble: messageBubble, lines };
}

/**
 * Get reaction title
 */
function getReactionTitle(emoji) {
  const titles = {
    "👍": "Helpful",
    "❤️": "Love it",
    "🎉": "Awesome",
  };
  return titles[emoji] || "";
}

/**
 * Handle reaction click
 */
function handleReaction(button) {
  button.classList.toggle("active");

  // Create floating emoji effect
  const emoji = document.createElement("div");
  emoji.textContent = button.getAttribute("data-reaction");
  emoji.style.position = "fixed";
  emoji.style.fontSize = "24px";
  emoji.style.pointerEvents = "none";
  emoji.style.zIndex = "10000";

  const rect = button.getBoundingClientRect();
  emoji.style.left = rect.left + "px";
  emoji.style.top = rect.top + "px";

  document.body.appendChild(emoji);

  // Animate
  emoji.animate(
    [
      { transform: "translateY(0) scale(1)", opacity: 1 },
      { transform: "translateY(-100px) scale(1.5)", opacity: 0 },
    ],
    {
      duration: 1000,
      easing: "ease-out",
    }
  ).onfinish = () => emoji.remove();
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
async function addMessage(content, isUser = false, useTyping = false) {
  const { element, bubble, lines } = createMessageElement(
    content,
    isUser,
    useTyping
  );
  chatMessages.appendChild(element);

  // Trigger animation
  setTimeout(() => {
    element.setAttribute("data-animate", "true");
  }, 10);

  scrollToBottom();

  // Typing animation for bot messages
  if (useTyping && !isUser) {
    const paragraphs = bubble.querySelectorAll("p");
    for (let i = 0; i < Math.min(lines.length, paragraphs.length); i++) {
      await typeText(paragraphs[i], lines[i], 20);
    }
  }
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

  // Hide quick replies after first message
  hideQuickReplies();

  // Add user message to chat
  await addMessage(message, true, false);

  // Set processing state
  setProcessing(true);

  try {
    // Send message to API
    const botResponse = await sendMessage(message);

    // Simulate typing delay for better UX
    await new Promise((resolve) => setTimeout(resolve, 800));

    // Add bot response to chat with typing animation
    await addMessage(botResponse, false, true);
  } catch (error) {
    // Show error message
    await addMessage(
      "Maaf, terjadi kesalahan. Silakan coba lagi.",
      false,
      false
    );
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

  // Show quick replies on first load
  setTimeout(() => {
    showQuickReplies();
  }, 1000);

  // Add input animation
  userInput.addEventListener("input", () => {
    if (userInput.value.length > 0) {
      sendButton.style.transform = "scale(1.1)";
    } else {
      sendButton.style.transform = "scale(1)";
    }
  });

  console.log("🤖 Enhanced Chatbot initialized successfully!");
  console.log("✨ Animations and interactions enabled!");
}

// Run initialization when DOM is ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
