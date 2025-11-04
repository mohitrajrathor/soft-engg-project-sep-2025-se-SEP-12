<script setup>
import { ref } from 'vue'
import TASidebar from '@/components/layout/TaLayout/TASideBar.vue'
import { PaperAirplaneIcon } from '@heroicons/vue/24/outline'

const messages = ref([
  { role: 'ai', text: "Hello! I'm your AI Onboarding Mentor. I'm trained on IITM TA policies, senior TA interviews, and internal docs. Ask me anything about your role!" }
])
const userInput = ref('')
const isTyping = ref(false)

const sendMessage = () => {
  if (!userInput.value.trim()) return
  messages.value.push({ role: 'user', text: userInput.value })
  const query = userInput.value
  userInput.value = ''
  isTyping.value = true

  // Simulate RAG + LLM response
  setTimeout(() => {
    messages.value.push({
      role: 'ai',
      text: `Based on IITM TA Handbook and senior TA interviews:\n\n**For "${query}":**\n\n1. Check the course forum daily\n2. Use Doubt Summarizer to spot trends\n3. Escalate to instructor if >3 students ask the same\n4. Log in Query Tracker\n\nWant a response template or checklist?`
    })
    isTyping.value = false
  }, 1800)
}
</script>

<template>
  <div class="flex min-h-screen bg-[#f8fafc]">
    <TASidebar class="fixed top-0 left-0 h-screen w-[250px]"/>
    <main class="flex-1 flex flex-col min-h-screen ml-[250px] bg-gray-50">
      <header class="bg-white shadow-sm px-8 py-5">
        <h1 class="text-2xl font-extrabold text-black">AI Onboarding Mentor</h1>
      </header>

      <div class="flex-1 flex flex-col mx-8 my-6">
        <div class="flex-1 bg-white rounded-2xl shadow-2xl p-6 overflow-y-auto mb-4">
          <div v-for="(msg, i) in messages" :key="i" :class="['mb-4 flex', msg.role === 'user' ? 'justify-end' : 'justify-start']">
            <div :class="['max-w-xs lg:max-w-md px-4 py-3 rounded-2xl', msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-800']">
              <p class="text-sm whitespace-pre-wrap">{{ msg.text }}</p>
            </div>
          </div>
          <div v-if="isTyping" class="flex justify-start">
            <div class="bg-gray-100 px-4 py-3 rounded-2xl">
              <p class="text-sm text-gray-600">AI is typing...</p>
            </div>
          </div>
        </div>

        <form @submit.prevent="sendMessage" class="flex gap-3">
          <input
            v-model="userInput"
            type="text"
            placeholder="Ask about grading, escalation, tools..."
            class="flex-1 px-5 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-600"
          />
          <button type="submit" class="px-6 py-3 bg-blue-600 text-white rounded-full hover:bg-blue-800 flex items-center shadow-sm">
            <PaperAirplaneIcon class="w-5 h-5" />
          </button>
        </form>
      </div>
    </main>
  </div>
</template>