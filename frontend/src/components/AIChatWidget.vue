<template>
  <div class="ai-chat-widget" :class="{ expanded: isExpanded }">
    <div class="chat-header" @click="toggleExpand">
      <span>🤖 AI Security Assistant</span>
      <button class="toggle-btn">{{ isExpanded ? "−" : "+" }}</button>
    </div>

    <div v-if="isExpanded" class="chat-body">
      <div class="messages" ref="messagesContainer">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="`message ${msg.role}`"
        >
          <div class="message-content">{{ msg.content }}</div>
        </div>
        <div v-if="loading" class="message assistant">
          <div class="message-content typing">AI is thinking...</div>
        </div>
      </div>

      <div class="chat-input">
        <input
          v-model="userInput"
          @keyup.enter="sendMessage"
          placeholder="Ask about vulnerabilities, patches, or security..."
          :disabled="loading"
        />
        <button @click="sendMessage" :disabled="loading || !userInput">
          Send
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from "vue";
import { useAI } from "@/composables/useAI";

const { loading, chatWithAI } = useAI();

const isExpanded = ref(false);
const messages = ref([
  {
    role: "assistant",
    content:
      "Hello! I'm your AI security assistant. Ask me anything about vulnerabilities, patches, or security best practices.",
  },
]);
const userInput = ref("");
const messagesContainer = ref(null);

const toggleExpand = () => {
  isExpanded.value = !isExpanded.value;
};

const sendMessage = async () => {
  if (!userInput.value.trim() || loading.value) return;

  // Add user message
  messages.value.push({
    role: "user",
    content: userInput.value,
  });

  const query = userInput.value;
  userInput.value = "";

  // Scroll to bottom
  await nextTick();
  scrollToBottom();

  // Get AI response
  const response = await chatWithAI(query, messages.value.slice(0, -1));

  if (response) {
    messages.value.push({
      role: "assistant",
      content: response,
    });
  } else {
    messages.value.push({
      role: "assistant",
      content: "Sorry, I encountered an error. Please try again.",
    });
  }

  // Scroll to bottom again
  await nextTick();
  scrollToBottom();
};

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

// Watch for new messages and scroll
watch(
  () => messages.value.length,
  async () => {
    await nextTick();
    scrollToBottom();
  },
);
</script>

<style scoped>
.ai-chat-widget {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 350px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  transition: all 0.3s ease;
}

.ai-chat-widget.expanded {
  height: 500px;
}

.chat-header {
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 16px 16px 0 0;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.toggle-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.5rem;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-body {
  display: flex;
  flex-direction: column;
  height: calc(500px - 60px);
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.message {
  display: flex;
}

.message.user {
  justify-content: flex-end;
}

.message.assistant {
  justify-content: flex-start;
}

.message-content {
  max-width: 80%;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  word-wrap: break-word;
  white-space: pre-wrap;
}

.message.user .message-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.message.assistant .message-content {
  background: #f3f4f6;
  color: #1f2937;
}

.message-content.typing {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.chat-input {
  display: flex;
  padding: 1rem;
  border-top: 1px solid #e5e7eb;
  gap: 0.5rem;
}

.chat-input input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.875rem;
}

.chat-input input:focus {
  outline: none;
  border-color: #667eea;
}

.chat-input button {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.chat-input button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.chat-input button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Scrollbar styling */
.messages::-webkit-scrollbar {
  width: 6px;
}

.messages::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.messages::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 10px;
}

.messages::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
