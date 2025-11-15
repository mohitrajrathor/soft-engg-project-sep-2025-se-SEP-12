<script setup>
import { ref, nextTick, onMounted } from 'vue'
import Sidebar from '@/components/layout/StudentLayout/SideBar.vue'
import HeaderBar from '@/components/layout/StudentLayout/HeaderBar.vue'
import { sendEnhancedChatMessage, getChatbotStatus } from '@/api/chatbot'

// State
const messages = ref([])
const userInput = ref('')
const isLoading = ref(false)
const conversationId = ref(null)
const chatMode = ref('academic')
const chatMessagesContainer = ref(null)
const isChatbotAvailable = ref(true)

// Suggested prompts
const suggestedPrompts = [
  'Summarize last CS 301 lecture',
  'Explain Dijkstra with example',
  'Draft study plan for finals',
  'Help me understand recursion'
]

// Initialize with welcome message
onMounted(async () => {
  // Check chatbot status
  try {
    await getChatbotStatus()
    isChatbotAvailable.value = true
  } catch (error) {
    console.error('Chatbot not available:', error)
    isChatbotAvailable.value = false
  }

  // Add welcome message
  messages.value.push({
    type: 'assistant',
    content: 'Welcome! Ask about deadlines, resources, or concepts. I can summarize lectures and draft study plans.',
    timestamp: new Date()
  })
})

// Send message
const sendMessage = async () => {
  const messageText = userInput.value.trim()

  if (!messageText) return

  // Add user message to chat
  messages.value.push({
    type: 'user',
    content: messageText,
    timestamp: new Date()
  })

  // Clear input
  userInput.value = ''

  // Scroll to bottom
  await nextTick()
  scrollToBottom()

  // Show loading state
  isLoading.value = true

  // Add loading message
  const loadingMessageIndex = messages.value.length
  messages.value.push({
    type: 'assistant',
    content: 'Thinking...',
    isLoading: true,
    timestamp: new Date()
  })

  try {
    // Send to backend using enhanced endpoint with query detection
    const response = await sendEnhancedChatMessage({
      message: messageText,
      mode: chatMode.value,
      conversation_id: conversationId.value,
      use_knowledge_base: true
    })

    // Store conversation ID
    if (response.conversation_id) {
      conversationId.value = response.conversation_id
    }

    // Replace loading message with actual response
    messages.value[loadingMessageIndex] = {
      type: 'assistant',
      content: response.answer || 'I received your message but couldn\'t generate a response.',
      timestamp: new Date(),
      sources: response.sources || [],
      knowledgeSourcesUsed: response.knowledge_sources_used || 0
    }

  } catch (error) {
    console.error('Failed to send message:', error)

    // Replace loading message with error
    messages.value[loadingMessageIndex] = {
      type: 'assistant',
      content: 'Sorry, I encountered an error. Please try again.',
      isError: true,
      timestamp: new Date()
    }
  } finally {
    isLoading.value = false
    await nextTick()
    scrollToBottom()
  }
}

// Handle suggested prompt click
const useSuggestedPrompt = (prompt) => {
  userInput.value = prompt
  sendMessage()
}

// Scroll to bottom of chat
const scrollToBottom = () => {
  if (chatMessagesContainer.value) {
    chatMessagesContainer.value.scrollTop = chatMessagesContainer.value.scrollHeight
  }
}

// Handle Enter key
const handleKeyDown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}

// Clear conversation
const clearChat = () => {
  messages.value = [{
    type: 'assistant',
    content: 'Conversation cleared. How can I help you today?',
    timestamp: new Date()
  }]
  conversationId.value = null
}

// Change chat mode
const changeChatMode = (mode) => {
  chatMode.value = mode
}
</script>

<template>
  <div class="flex h-screen bg-gray-50 overflow-hidden">
    <!-- Sidebar -->
    <Sidebar class="sticky top-0 h-screen overflow-y-auto flex-shrink-0" />

    <!-- Main Content Area -->
    <div class="flex flex-col flex-1 overflow-hidden ml-[250px]">
      <!-- Header -->
      <HeaderBar />

      <!-- Main Body -->
      <main class="flex flex-1 overflow-hidden">
        <!-- Central Chat Section -->
        <section
          class="flex flex-col flex-1 bg-white m-4 rounded-2xl shadow relative overflow-hidden"
        >
          <!-- Chat Mode Selector -->
          <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200">
            <div class="flex gap-2">
              <button
                @click="changeChatMode('academic')"
                :class="[
                  'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                  chatMode === 'academic'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                ]"
              >
                Academic
              </button>
              <button
                @click="changeChatMode('doubt_clarification')"
                :class="[
                  'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                  chatMode === 'doubt_clarification'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                ]"
              >
                Doubt Clarification
              </button>
              <button
                @click="changeChatMode('study_help')"
                :class="[
                  'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                  chatMode === 'study_help'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                ]"
              >
                Study Help
              </button>
              <button
                @click="changeChatMode('general')"
                :class="[
                  'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                  chatMode === 'general'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                ]"
              >
                General
              </button>
            </div>
            <button
              @click="clearChat"
              class="px-4 py-2 rounded-lg text-sm font-medium text-red-600 hover:bg-red-50 transition-colors"
            >
              Clear Chat
            </button>
          </div>

          <!-- Chat Messages (Scrollable) -->
          <div
            ref="chatMessagesContainer"
            class="flex-1 overflow-y-auto px-6 py-4 space-y-4"
            style="scroll-behavior: smooth"
          >
            <!-- Message Loop -->
            <div
              v-for="(message, index) in messages"
              :key="index"
              :class="[
                'flex items-start',
                message.type === 'user' ? 'justify-end' : ''
              ]"
            >
              <!-- Assistant Message -->
              <template v-if="message.type === 'assistant'">
                <img
                  src="https://randomuser.me/api/portraits/lego/2.jpg"
                  class="w-10 h-10 rounded-full mr-3 mt-1 flex-shrink-0"
                  alt="AI Assistant"
                />
                <div class="flex-1 max-w-3xl">
                  <div
                    :class="[
                      'rounded-2xl px-5 py-4',
                      message.isError
                        ? 'bg-red-50 text-red-800'
                        : message.isLoading
                        ? 'bg-gray-100 text-gray-600'
                        : 'bg-gray-100 text-gray-800'
                    ]"
                  >
                    <div v-if="message.isLoading" class="flex items-center gap-2">
                      <div class="flex gap-1">
                        <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
                        <span
                          class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                          style="animation-delay: 0.2s"
                        ></span>
                        <span
                          class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                          style="animation-delay: 0.4s"
                        ></span>
                      </div>
                      <span class="text-sm">{{ message.content }}</span>
                    </div>
                    <div v-else class="whitespace-pre-wrap">{{ message.content }}</div>
                  </div>
                  <span class="text-xs text-gray-400 mt-1 block">
                    {{ message.timestamp.toLocaleTimeString() }}
                  </span>
                </div>
              </template>

              <!-- User Message -->
              <template v-else>
                <div class="flex flex-col items-end max-w-3xl">
                  <div
                    class="rounded-2xl bg-blue-600 text-white px-5 py-3 shadow text-sm whitespace-pre-wrap"
                  >
                    {{ message.content }}
                  </div>
                  <span class="text-xs text-gray-400 mt-1 block">
                    {{ message.timestamp.toLocaleTimeString() }}
                  </span>
                </div>
                <img
                  src="https://randomuser.me/api/portraits/men/36.jpg"
                  class="w-10 h-10 rounded-full ml-3 mt-1 flex-shrink-0"
                  alt="You"
                />
              </template>
            </div>

            <!-- Empty state -->
            <div
              v-if="messages.length === 1"
              class="flex flex-col items-center justify-center py-12 text-gray-400"
            >
              <svg
                class="w-16 h-16 mb-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                />
              </svg>
              <p class="text-sm">Start a conversation with AURA AI Assistant</p>
            </div>
          </div>

          <!-- Chat Input -->
          <div class="border-t border-gray-200 p-4 bg-white">
            <div class="flex items-end gap-3">
              <div class="flex-1">
                <textarea
                  v-model="userInput"
                  @keydown="handleKeyDown"
                  placeholder="Type your message... (Shift+Enter for new line)"
                  rows="1"
                  class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  :disabled="isLoading || !isChatbotAvailable"
                  style="max-height: 120px"
                ></textarea>
              </div>
              <button
                @click="sendMessage"
                :disabled="!userInput.trim() || isLoading || !isChatbotAvailable"
                class="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                <svg
                  v-if="!isLoading"
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                  />
                </svg>
                <span v-if="isLoading" class="flex gap-1">
                  <span class="w-2 h-2 bg-white rounded-full animate-bounce"></span>
                  <span
                    class="w-2 h-2 bg-white rounded-full animate-bounce"
                    style="animation-delay: 0.2s"
                  ></span>
                  <span
                    class="w-2 h-2 bg-white rounded-full animate-bounce"
                    style="animation-delay: 0.4s"
                  ></span>
                </span>
                <span v-else>Send</span>
              </button>
            </div>

            <!-- Chatbot status warning -->
            <div
              v-if="!isChatbotAvailable"
              class="mt-2 text-sm text-amber-600 flex items-center gap-2"
            >
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                  clip-rule="evenodd"
                />
              </svg>
              Chatbot is currently unavailable. Please try again later.
            </div>
          </div>
        </section>

        <!-- Right Sidebar -->
        <aside
          class="w-80 flex-shrink-0 flex flex-col gap-5 p-4 overflow-y-auto h-[calc(100vh-80px)]"
        >
          <!-- Suggested Prompts -->
          <div class="bg-white rounded-2xl shadow p-5">
            <h3 class="text-base font-semibold mb-3">Suggested Prompts</h3>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="(prompt, index) in suggestedPrompts"
                :key="index"
                @click="useSuggestedPrompt(prompt)"
                class="bg-gray-100 hover:bg-blue-100 text-gray-700 text-xs px-3 py-2 rounded-full transition"
                :disabled="isLoading"
              >
                {{ prompt }}
              </button>
            </div>
            <p class="text-xs text-gray-400 mt-3">
              Click to use these prompts or type your own question.
            </p>
          </div>

          <!-- Chat Mode Info -->
          <div class="bg-white rounded-2xl shadow p-5">
            <h3 class="text-base font-semibold mb-3">Current Mode</h3>
            <div class="flex flex-col gap-2 text-sm">
              <div class="flex items-center gap-2">
                <span class="font-medium text-gray-600">Mode:</span>
                <span
                  class="bg-blue-50 text-blue-700 font-semibold px-3 py-1 rounded-full text-xs capitalize"
                >
                  {{ chatMode.replace('_', ' ') }}
                </span>
              </div>
              <p class="text-xs text-gray-500 mt-2">
                <span v-if="chatMode === 'academic'">
                  Get clear, educational explanations with examples.
                </span>
                <span v-else-if="chatMode === 'doubt_clarification'">
                  Step-by-step help to clarify your doubts.
                </span>
                <span v-else-if="chatMode === 'study_help'">
                  Study strategies, time management, and learning techniques.
                </span>
                <span v-else>
                  General helpful responses for any question.
                </span>
              </p>
            </div>
          </div>

          <!-- Conversation Info -->
          <div class="bg-white rounded-2xl shadow p-5">
            <h3 class="text-base font-semibold mb-3">Conversation</h3>
            <div class="flex flex-col gap-2 text-sm">
              <div class="flex items-center justify-between">
                <span class="font-medium text-gray-600">Messages:</span>
                <span class="text-gray-700 font-semibold">{{ messages.length }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="font-medium text-gray-600">Status:</span>
                <span
                  :class="[
                    'font-semibold px-2 py-1 rounded-full text-xs',
                    isChatbotAvailable
                      ? 'bg-green-50 text-green-700'
                      : 'bg-red-50 text-red-700'
                  ]"
                >
                  {{ isChatbotAvailable ? 'Connected' : 'Disconnected' }}
                </span>
              </div>
            </div>
          </div>
        </aside>
      </main>
    </div>
  </div>
</template>

<style scoped>
/* Smooth scroll for chat section */
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 6px;
}
::-webkit-scrollbar-thumb:hover {
  background-color: #94a3b8;
}

/* Textarea auto-resize */
textarea {
  min-height: 48px;
  line-height: 1.5;
}

/* Animation for loading dots */
@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}

.animate-bounce {
  animation: bounce 1s infinite;
}
</style>
