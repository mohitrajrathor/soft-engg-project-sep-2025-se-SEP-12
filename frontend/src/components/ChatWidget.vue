<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { MessageCircle, X, Minimize2, Maximize2, Bot } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const props = defineProps({
  position: {
    type: String,
    default: 'bottom-right',
    validator: (value) => ['bottom-right', 'bottom-left'].includes(value)
  },
  defaultOpen: {
    type: Boolean,
    default: false
  }
})

const router = useRouter()
const isOpen = ref(props.defaultOpen)
const isMinimized = ref(false)
const hasNewMessage = ref(false)
let timer = null

// Show notification after a delay
onMounted(() => {
  if (!isOpen.value) {
    timer = setTimeout(() => {
      hasNewMessage.value = true
    }, 10000) // Show after 10 seconds
  }
})

onUnmounted(() => {
  if (timer) clearTimeout(timer)
})

const toggleOpen = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    hasNewMessage.value = false
  }
}

const toggleMinimize = () => {
  isMinimized.value = !isMinimized.value
}

const startConversation = () => {
  isOpen.value = false
  router.push('/chat')
}

const positionClasses = {
  'bottom-right': 'bottom-4 right-4',
  'bottom-left': 'bottom-4 left-4'
}
</script>

<template>
  <div>
    <!-- Floating Button -->
    <div
      v-if="!isOpen"
      class="fixed z-50"
      :class="positionClasses[position]"
    >
      <div class="relative">
        <div v-if="hasNewMessage" class="absolute -top-12 -left-2 animate-in slide-in-from-bottom-2">
          <div class="bg-white dark:bg-gray-800 px-3 py-2 shadow-lg rounded-lg border border-gray-200 dark:border-gray-700">
            <p class="text-sm font-medium text-gray-900 dark:text-white">Need help? Chat with AURA!</p>
          </div>
          <div class="absolute bottom-0 left-6 w-3 h-3 bg-white dark:bg-gray-800 rotate-45 -mb-1.5 border-b border-r border-gray-200 dark:border-gray-700" />
        </div>

        <button
          @click="toggleOpen"
          class="bg-blue-600 hover:bg-blue-700 text-white rounded-full h-14 w-14 shadow-lg hover:scale-110 transition-transform flex items-center justify-center"
        >
          <MessageCircle class="h-6 w-6" />
          <span v-if="hasNewMessage" class="absolute -top-1 -right-1 h-3 w-3 bg-red-500 rounded-full animate-pulse" />
        </button>
      </div>
    </div>

    <!-- Chat Window -->
    <div
      v-if="isOpen"
      class="fixed z-50 animate-in slide-in-from-bottom-5 duration-300"
      :class="positionClasses[position]"
    >
      <div
        class="bg-white dark:bg-gray-900 shadow-2xl border border-gray-200 dark:border-gray-800 rounded-lg overflow-hidden transition-all duration-300"
        :class="isMinimized ? 'w-80' : 'w-96 h-[600px]'"
      >
        <!-- Header -->
        <div class="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="relative">
                <Bot class="h-6 w-6" />
                <span class="absolute -bottom-1 -right-1 h-2 w-2 bg-green-400 rounded-full" />
              </div>
              <div>
                <h3 class="font-semibold">AURA Support</h3>
                <p class="text-xs text-blue-100">Always here to help</p>
              </div>
            </div>

            <div class="flex items-center gap-1">
              <button
                @click="toggleMinimize"
                class="p-1 hover:bg-white/20 rounded text-white transition-colors"
              >
                <Maximize2 v-if="isMinimized" class="h-4 w-4" />
                <Minimize2 v-else class="h-4 w-4" />
              </button>
              <button
                @click="toggleOpen"
                class="p-1 hover:bg-white/20 rounded text-white transition-colors"
              >
                <X class="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>

        <!-- Content -->
        <div v-if="!isMinimized" class="flex flex-col h-[536px]">
          <div class="flex-1 p-6 flex flex-col items-center justify-center text-center">
            <div class="w-16 h-16 rounded-full bg-blue-100 dark:bg-blue-900/20 flex items-center justify-center mb-4">
              <Bot class="h-8 w-8 text-blue-600" />
            </div>

            <h3 class="text-lg font-semibold mb-2 text-gray-900 dark:text-white">
              Welcome to AURA Chat
            </h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-6">
              Get instant answers about IITM BS Degree program in your preferred language
            </p>

            <div class="space-y-3 w-full">
              <div class="w-full py-2 px-3 border border-gray-200 dark:border-gray-700 rounded-full text-xs font-medium text-gray-700 dark:text-gray-300">
                🌐 Support in 13+ Indian Languages
              </div>
              <div class="w-full py-2 px-3 border border-gray-200 dark:border-gray-700 rounded-full text-xs font-medium text-gray-700 dark:text-gray-300">
                ⚡ Instant AI-Powered Responses
              </div>
              <div class="w-full py-2 px-3 border border-gray-200 dark:border-gray-700 rounded-full text-xs font-medium text-gray-700 dark:text-gray-300">
                📚 Complete IITM BS Degree Info
              </div>
            </div>

            <div class="w-full mt-6">
              <button
                @click="startConversation"
                class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
              >
                Start Conversation
              </button>
            </div>
          </div>

          <div class="border-t border-gray-200 dark:border-gray-800 p-4 bg-gray-50 dark:bg-gray-900/50">
            <p class="text-xs text-center text-gray-500 dark:text-gray-400">
              Powered by Gemini AI • Available 24/7
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.animate-in {
  animation-duration: 300ms;
  animation-fill-mode: both;
}

.slide-in-from-bottom-2 {
  animation-name: slideInFromBottom2;
}

.slide-in-from-bottom-5 {
  animation-name: slideInFromBottom5;
}

@keyframes slideInFromBottom2 {
  from {
    transform: translateY(0.5rem);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes slideInFromBottom5 {
  from {
    transform: translateY(1.25rem);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
