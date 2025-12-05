<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Send, User, Loader2, ArrowLeft, Bot } from 'lucide-vue-next'
import { chatService } from '@/api/chat'

const router = useRouter()
const route = useRoute()

const messages = ref([])
const inputText = ref('')
const isLoading = ref(false)
const session = ref(null)
const showSamples = ref(true)
const messagesEndRef = ref(null)
const textareaRef = ref(null)

const SAMPLE_QUESTIONS = [
  "What is the admission process for IITM BS Degree?",
  "Tell me about the course structure and subjects",
  "What are the fee details and payment options?",
  "What are the eligibility criteria for IITM BS program?",
  "How to apply for the IITM BS Degree program?",
  "What is the exam pattern and schedule?"
]

// Simple Markdown Parser
const parseMarkdown = (text) => {
  if (!text) return ''
  let html = text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
    .replace(/\*(.*?)\*/g, '<em>$1</em>') // Italic
    .replace(/`(.*?)`/g, '<code class="bg-gray-100 dark:bg-gray-800 px-1 rounded text-sm font-mono">$1</code>') // Inline Code
    .replace(/\n/g, '<br>') // Line breaks
  return html
}

const scrollToBottom = async () => {
  await nextTick()
  messagesEndRef.value?.scrollIntoView({ behavior: 'smooth' })
}

watch(messages, () => {
  scrollToBottom()
}, { deep: true })

const restoreSession = async (chatId) => {
  try {
    const history = await chatService.getChatHistory(chatId)
    
    const restoredMessages = history.queries.flatMap(query => [
      {
        id: `${query.query_id}-user`,
        text: query.input_text,
        sender: 'user',
        timestamp: new Date(query.created_at),
        language: query.language
      },
      {
        id: `${query.query_id}-assistant`,
        text: query.answer_text || "I couldn't find an answer to that question.",
        sender: 'assistant',
        timestamp: new Date(query.created_at),
        language: query.language,
        confidence: query.confidence
      }
    ])

    messages.value = restoredMessages

    if (restoredMessages.length > 0) {
      showSamples.value = false
    }

    if (history.queries.length > 0) {
      session.value = {
        chatId,
        createdAt: new Date(history.queries[0].created_at)
      }
    }
  } catch (error) {
    console.error('Failed to restore session:', error)
    // toast.error('Failed to restore chat history.')
  }
}

onMounted(() => {
  const chatId = route.query.chat_id
  if (chatId) {
    restoreSession(chatId)
  }
})

const sendMessage = async (text) => {
  const messageText = text || inputText.value.trim()
  if (!messageText || isLoading.value) return

  showSamples.value = false
  
  const userMessage = {
    id: `user-${Date.now()}`,
    text: messageText,
    sender: 'user',
    timestamp: new Date()
  }

  const loadingMessage = {
    id: `loading-${Date.now()}`,
    text: "Processing your request...",
    sender: 'assistant',
    timestamp: new Date(),
    isLoading: true
  }

  messages.value.push(userMessage, loadingMessage)
  inputText.value = ''
  isLoading.value = true

  try {
    let result
    
    if (!session.value) {
      // First query
      result = await chatService.sendFirstQueryAndWait(messageText)
      
      session.value = {
        chatId: result.task.chat_id,
        createdAt: new Date()
      }
      
      // Update URL without reloading
      router.replace({ query: { ...route.query, chat_id: result.task.chat_id } })
    } else {
      // Subsequent query
      result = await chatService.sendQueryAndWait(session.value.chatId, messageText)
    }

    // Remove loading message
    messages.value = messages.value.filter(msg => !msg.isLoading)

    const finalStatus = result.finalStatus
    const actualAnswer = finalStatus.metadata?.answer_text || 
                        (finalStatus.metadata?.has_answered ? "I processed your request successfully." : 
                        "I don't have specific information about your question.")

    const assistantMessage = {
      id: finalStatus.metadata?.query_id || `assistant-${Date.now()}`,
      text: actualAnswer,
      sender: 'assistant',
      timestamp: new Date(),
      language: finalStatus.metadata?.language || 'en',
      confidence: finalStatus.metadata?.confidence || 0
    }

    messages.value.push(assistantMessage)

  } catch (error) {
    console.error('Chat error:', error)
    messages.value = messages.value.filter(msg => !msg.isLoading)
    
    const errorMessage = {
      id: `error-${Date.now()}`,
      text: "Sorry, I encountered an error. Please try again.",
      sender: 'assistant',
      timestamp: new Date(),
      isError: true
    }
    messages.value.push(errorMessage)
  } finally {
    isLoading.value = false
    await nextTick()
    textareaRef.value?.focus()
  }
}

const handleKeyPress = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}

const startNewChat = () => {
  router.push('/chat')
  messages.value = []
  session.value = null
  showSamples.value = true
}
</script>

<template>
  <div class="h-screen bg-white dark:bg-gray-900 flex flex-col overflow-hidden">
    <div class="max-w-4xl mx-auto w-full flex flex-col h-full overflow-hidden">
      <!-- Header -->
      <div class="border-b border-gray-200 dark:border-gray-800 px-4 py-6 flex-shrink-0">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <button 
              @click="router.back()"
              class="flex items-center text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white transition-colors"
            >
              <ArrowLeft class="h-4 w-4 mr-2" />
              Back
            </button>
            <div>
              <h1 class="text-2xl font-light text-gray-900 dark:text-white">Chat</h1>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                Ask anything about IITM BS Degree
              </p>
            </div>
          </div>

          <button
            v-if="session"
            @click="startNewChat"
            class="text-sm text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white px-3 py-1.5 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            New Chat
          </button>
        </div>
      </div>

      <!-- Messages Area -->
      <div class="flex-1 w-full overflow-y-auto p-4 space-y-6 scroll-smooth">
        <div v-if="messages.length === 0" class="text-center py-16">
          <h2 class="text-xl font-light text-gray-900 dark:text-white mb-4">
            How can I help you today?
          </h2>
          <p class="text-gray-500 dark:text-gray-400 mb-8 max-w-md mx-auto">
            Ask me anything about the IITM BS Degree program in any language
          </p>

          <div v-if="showSamples" class="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto">
            <button
              v-for="question in SAMPLE_QUESTIONS"
              :key="question"
              @click="sendMessage(question)"
              class="text-left p-4 rounded-lg border border-gray-200 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors text-gray-600 dark:text-gray-300 text-sm"
            >
              {{ question }}
            </button>
          </div>
        </div>

        <div
          v-for="message in messages"
          :key="message.id"
          class="flex gap-3"
          :class="message.sender === 'user' ? 'justify-end' : 'justify-start'"
        >
          <div v-if="message.sender === 'assistant'" class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
            <span class="text-white font-bold text-sm">N</span>
          </div>

          <div
            class="max-w-[80%]"
            :class="message.sender === 'user' ? 'text-right' : 'text-left'"
          >
            <div
              class="inline-block px-4 py-3 rounded-lg text-sm"
              :class="[
                message.sender === 'user' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white',
                message.isError && 'bg-red-50 dark:bg-red-900/20 text-red-900 dark:text-red-100',
                message.isLoading && 'bg-gray-50 dark:bg-gray-700'
              ]"
            >
              <div v-if="message.isLoading" class="flex items-center gap-2">
                <Loader2 class="h-4 w-4 animate-spin" />
                <span>{{ message.text }}</span>
              </div>
              <div v-else v-html="parseMarkdown(message.text)"></div>
            </div>

            <div class="text-xs text-gray-400 mt-1">
              {{ message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }}
              <span v-if="message.confidence && message.sender === 'assistant'" class="ml-2">
                • {{ message.confidence }}% confidence
              </span>
            </div>
          </div>

          <div v-if="message.sender === 'user'" class="w-8 h-8 bg-gray-400 rounded-full flex items-center justify-center flex-shrink-0">
            <User class="h-4 w-4 text-white" />
          </div>
        </div>

        <div ref="messagesEndRef" />
      </div>

      <!-- Input Area -->
      <div class="border-t border-gray-200 dark:border-gray-800 px-4 py-6 flex-shrink-0 bg-white dark:bg-gray-900">
        <div class="flex gap-3">
          <div class="flex-1">
            <textarea
              ref="textareaRef"
              v-model="inputText"
              @keypress="handleKeyPress"
              placeholder="Ask me anything about IITM BS Degree..."
              class="w-full min-h-[60px] max-h-[120px] resize-none border border-gray-300 dark:border-gray-700 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-800 dark:text-white text-sm"
              :disabled="isLoading"
            ></textarea>
          </div>

          <button
            @click="sendMessage()"
            :disabled="!inputText.trim() || isLoading"
            class="self-end px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-lg transition-colors flex items-center justify-center"
          >
            <Loader2 v-if="isLoading" class="h-4 w-4 animate-spin" />
            <Send v-else class="h-4 w-4" />
          </button>
        </div>

        <div class="flex items-center justify-between mt-2 text-xs text-gray-500">
          <span>Press Enter to send, Shift+Enter for new line</span>
          <span>Powered by AI</span>
        </div>
      </div>
    </div>
  </div>
</template>
