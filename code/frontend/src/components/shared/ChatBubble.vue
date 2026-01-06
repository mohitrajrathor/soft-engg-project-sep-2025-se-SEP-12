<script setup>
import { computed } from 'vue'
import MarkdownIt from 'markdown-it'

const props = defineProps({
  message: { type: Object, required: true },
  isUser: { type: Boolean, default: false },
  isDark: { type: Boolean, default: false }
})

// Initialize markdown renderer
const md = new MarkdownIt({
  html: false, // Disable HTML tags for security
  linkify: true, // Convert URLs to links
  typographer: true // Smart quotes and dashes
})

// Render markdown content
const renderedContent = computed(() => {
  if (props.message.isLoading || props.message.isError) {
    return props.message.content
  }
  return md.render(props.message.content || '')
})

const isLoading = computed(() => !!props.message.isLoading)
const isError = computed(() => !!props.message.isError)

const bubbleClass = computed(() => {
  let base = 'rounded-2xl px-5 py-4 chat-bubble'
  if (isError.value) {
    base += ' chat-bubble-error'
  } else if (isLoading.value) {
    base += ' chat-bubble-loading'
  } else {
    base += ' chat-bubble-normal'
  }

  base += props.isDark ? ' blue-shadow' : ' default-shadow'
  return base
})

const userBubbleClass = computed(() => {
  let base = 'rounded-2xl px-5 py-3 text-sm chat-bubble-user'
  base += props.isDark ? ' blue-shadow' : ' default-shadow'
  return base
})
</script>

<template>
  <div :class="['flex items-start', isUser ? 'justify-end' : '']">
    <template v-if="!isUser">
      <img
        src="https://randomuser.me/api/portraits/lego/2.jpg"
        class="w-10 h-10 rounded-full mr-2 mt-1 flex-shrink-0"
        alt="AI Assistant"
      />
      <div class="flex-1 max-w-3xl">
        <div :class="bubbleClass">
          <div v-if="isLoading" class="flex items-center gap-2">
            <div class="flex gap-1">
              <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
              <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></span>
              <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></span>
            </div>
            <span class="text-sm">{{ message.content }}</span>
          </div>
          <div v-else v-html="renderedContent"></div>
        </div>
        <span class="text-xs text-gray-400 mt-1 block">
          {{ (message.timestamp && typeof message.timestamp === 'string') ? new Date(message.timestamp).toLocaleTimeString() : (message.timestamp ? message.timestamp.toLocaleTimeString() : '') }}
        </span>
      </div>
    </template>

    <template v-else>
      <div class="flex flex-col items-end max-w-3xl">
        <div :class="userBubbleClass">{{ message.content }}</div>
        <span class="text-xs text-gray-400 mt-1 block">
          {{ (message.timestamp && typeof message.timestamp === 'string') ? new Date(message.timestamp).toLocaleTimeString() : (message.timestamp ? message.timestamp.toLocaleTimeString() : '') }}
        </span>
      </div>
      <img
        src="https://randomuser.me/api/portraits/men/36.jpg"
        class="w-10 h-10 rounded-full ml-2 mt-1 flex-shrink-0"
        alt="You"
      />
    </template>
  </div>
</template>

<style scoped>
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}
.animate-bounce { animation: bounce 1s infinite; }

.blue-shadow {
  box-shadow: 0 2px 12px 0 rgba(37, 99, 235, 0.2), 0 1px 3px 0 rgba(37, 99, 235, 0.15);
}
.default-shadow {
  box-shadow: 0 2px 8px 0 rgba(0,0,0,0.08);
}

/* Theme-aware chat bubble styles */
.chat-bubble {
  background: var(--card-bg);
  color: var(--text-primary);
}

.chat-bubble-error {
  background: var(--error-bg);
  color: var(--error-text);
}

.chat-bubble-loading {
  background: var(--card-bg);
  color: var(--text-secondary);
}

.chat-bubble-normal {
  background: var(--card-bg);
  color: var(--text-primary);
}

.chat-bubble-user {
  background: var(--accent-blue);
  color: white;
}

/* Markdown content styling */
:deep(p) {
  margin-bottom: 0.5rem;
}

:deep(p:last-child) {
  margin-bottom: 0;
}

:deep(ul), :deep(ol) {
  margin-left: 1rem;
  margin-bottom: 0.5rem;
}

:deep(li) {
  margin-bottom: 0.25rem;
}

:deep(code) {
  background-color: rgba(0, 0, 0, 0.1);
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 0.875em;
}

:deep(pre) {
  background-color: rgba(0, 0, 0, 0.05);
  padding: 0.75rem;
  border-radius: 0.375rem;
  overflow-x: auto;
  margin: 0.5rem 0;
}

:deep(pre code) {
  background-color: transparent;
  padding: 0;
}

:deep(blockquote) {
  border-left: 3px solid rgba(0, 0, 0, 0.2);
  padding-left: 0.75rem;
  margin: 0.5rem 0;
  font-style: italic;
}

:deep(strong) {
  font-weight: 600;
}

:deep(em) {
  font-style: italic;
}

:deep(a) {
  color: #3b82f6;
  text-decoration: underline;
}

:deep(a:hover) {
  color: #2563eb;
}
</style>
