<script setup>
import { ref, nextTick, watch } from "vue"
import Sidebar from '@/components/layout/StudentLayout/SideBar.vue'
import HeaderBar from '@/components/layout/StudentLayout/HeaderBar.vue'
import { api } from '@/api'
import MarkdownIt from 'markdown-it'

// Setup Markdown Renderer
const md = new MarkdownIt({ html: true, linkify: true })

const videoLink = ref("")
const summary = ref("")
const relatedVideos = ref([]) // Now dynamic!
const isLoading = ref(false)
const showChat = ref(false)

// Chat State
const chatInput = ref("")
const chatHistory = ref([])
const chatContainer = ref(null)

const getSummary = async () => {
  if (!videoLink.value.trim()) return alert("Please enter a valid YouTube link!")

  isLoading.value = true
  showChat.value = false
  chatHistory.value = []
  summary.value = ""
  relatedVideos.value = []

  try {
    // Call Backend
    const res = await api.post('/video/summarize', { url: videoLink.value },
      { timeout: 60000 })

    // Update State from JSON Response
    summary.value = res.data.summary

    // Map related topics to visual cards
    // Inside your getSummary function, replace the current "related_videos" block with this:

    if (res.data.related_videos && res.data.related_videos.length > 0) {
      relatedVideos.value = res.data.related_videos.map(topic => {
        // Clean the topic string just in case
        const cleanTopic = topic.trim();

        return {
          title: cleanTopic,
          // Creates a specific YouTube Search Link for this topic
          link: `https://www.youtube.com/results?search_query=${encodeURIComponent(cleanTopic)}`,
          // Generates a nice placeholder image with the text on it
          thumbnail: `https://placehold.co/600x400/2563eb/FFFFFF/png?text=${encodeURIComponent(cleanTopic)}&font=roboto`
        }
      })
    }

    showChat.value = true
    chatHistory.value.push({ role: 'ai', text: "Summary generated! Ask me any follow-up questions." })

  } catch (err) {
    console.error(err)
    summary.value = "Failed to generate summary. Please ensure the video has captions."
  } finally {
    isLoading.value = false
  }
}

const askQuestion = async () => {
  if (!chatInput.value.trim()) return
  const question = chatInput.value
  chatHistory.value.push({ role: 'user', text: question })
  chatInput.value = ""
  scrollToBottom()

  chatHistory.value.push({ role: 'ai', text: '...', loading: true })

  try {
    const context = `Summary Context:\n${summary.value}\n\nUser Question: ${question}`
    const res = await api.post('/chatbot/chat', { message: context, mode: 'academic' })
    chatHistory.value.pop()
    chatHistory.value.push({ role: 'ai', text: res.data.response })
  } catch (e) {
    chatHistory.value.pop()
    chatHistory.value.push({ role: 'ai', text: "Error connecting to chat." })
  }
  scrollToBottom()
}

function scrollToBottom() {
  nextTick(() => { if (chatContainer.value) chatContainer.value.scrollTop = chatContainer.value.scrollHeight })
}
</script>

<template>
  <div class="flex h-screen bg-gray-50 overflow-hidden font-sans">
    <Sidebar class="fixed top-0 left-0 h-screen w-[250px] z-30" />

    <div class="flex flex-col flex-1 ml-[250px]">
      <HeaderBar class="sticky top-0 z-20" />

      <main class="flex-1 p-6 lg:p-8 overflow-y-auto bg-gray-50 flex flex-col lg:flex-row gap-6">

        <div class="flex-1 space-y-6 h-full overflow-y-auto pr-2 custom-scrollbar">

          <div class="bg-white shadow-sm border border-gray-200 rounded-2xl p-6">
            <h1 class="text-2xl font-bold mb-1 text-gray-800">Video Learning Assistant</h1>
            <p class="text-sm text-gray-500 mb-5">Paste a YouTube link to generate notes & recommendations.</p>

            <div class="flex gap-3">
              <div class="relative w-full">

                <div class="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round"
                      d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                </div>

                <input v-model="videoLink" @keyup.enter="getSummary" type="text"
                  placeholder="https://www.youtube.com/watch?v=..."
                  class="w-full pl-12 pr-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition" />
              </div>

              <button @click="getSummary"
                class="bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-2 rounded-xl transition shadow-sm flex items-center gap-2 disabled:opacity-70"
                :disabled="isLoading">
                <span v-if="isLoading" class="animate-spin">⟳</span> {{ isLoading ? "Analyzing..." : "Summarize" }}
              </button>
            </div>
          </div>

          <div v-if="summary || isLoading"
            class="bg-white shadow-sm border border-gray-200 rounded-2xl p-8 min-h-[200px]">
            <div class="flex items-center justify-between mb-4 border-b border-gray-100 pb-2">
              <h2 class="text-lg font-bold text-gray-800">✨ Key Insights</h2>
              <span v-if="!isLoading"
                class="text-xs font-medium bg-green-100 text-green-700 px-2 py-1 rounded">Success</span>
            </div>
            <div v-if="isLoading" class="animate-pulse space-y-4">
              <div class="h-4 bg-gray-100 rounded w-3/4"></div>
              <div class="h-4 bg-gray-100 rounded w-full"></div>
              <div class="h-4 bg-gray-100 rounded w-5/6"></div>
            </div>
            <div v-else class="prose prose-blue prose-sm max-w-none text-gray-600 leading-relaxed"
              v-html="md.render(summary)"></div>
          </div>

          <div v-if="relatedVideos.length > 0" class="mt-6 bg-white shadow-sm border border-gray-200 rounded-2xl p-6">
            <div class="flex items-center gap-2 mb-4">
              <div class="p-1.5 bg-red-100 rounded-lg text-red-600">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path
                    d="M2 6a2 2 0 012-2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V6zM14.553 7.106A1 1 0 0014 8v4a1 1 0 00.553.894l2 1A1 1 0 0018 13V7a1 1 0 00-1.447-.894l-2 1z" />
                </svg>
              </div>
              <h2 class="text-lg font-bold text-gray-800">Related Videos & Topics</h2>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4">
              <a v-for="(video, index) in relatedVideos" :key="index" :href="video.link" target="_blank"
                class="group flex gap-4 p-3 border border-gray-100 rounded-xl hover:bg-gray-50 hover:border-blue-200 cursor-pointer transition-all duration-200">
                <div class="relative w-32 h-20 flex-shrink-0 bg-gray-200 rounded-lg overflow-hidden shadow-sm">
                  <img :src="video.thumbnail"
                    class="w-full h-full object-cover group-hover:scale-105 transition duration-500" alt="Thumbnail" />
                  <div
                    class="absolute inset-0 bg-black/10 group-hover:bg-black/0 transition flex items-center justify-center">
                    <div class="bg-black/60 text-white rounded-full p-1.5 backdrop-blur-sm">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 pl-0.5" viewBox="0 0 20 20"
                        fill="currentColor">
                        <path fill-rule="evenodd"
                          d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z"
                          clip-rule="evenodd" />
                      </svg>
                    </div>
                  </div>
                </div>

                <div class="flex flex-col justify-center min-w-0">
                  <h3 class="text-sm font-bold text-gray-800 leading-tight group-hover:text-blue-600 line-clamp-2">
                    {{ video.title }}
                  </h3>
                  <div class="flex items-center gap-2 mt-2">
                    <span
                      class="text-xs font-medium text-gray-500 bg-gray-100 px-2 py-0.5 rounded-md group-hover:bg-white">Watch
                      on YouTube ↗</span>
                  </div>
                </div>
              </a>
            </div>
          </div>

          <div v-if="relatedVideos.length > 0" class="bg-white shadow-sm border border-gray-200 rounded-2xl p-6">
            <h2 class="text-lg font-bold mb-4 text-gray-800">Recommended Next Steps</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="(vid, i) in relatedVideos" :key="i"
                class="group flex gap-3 p-3 border border-gray-100 rounded-xl hover:bg-gray-50 cursor-pointer transition">
                <img :src="vid.thumbnail" class="w-24 h-16 object-cover rounded-lg bg-gray-200" />
                <div class="flex flex-col justify-center">
                  <h3 class="text-sm font-bold text-gray-800 group-hover:text-blue-600 line-clamp-2">{{ vid.title }}
                  </h3>
                  <a :href="`https://www.youtube.com/results?search_query=${encodeURIComponent(vid.title)}`"
                    target="_blank" class="text-xs text-gray-500 hover:underline mt-1">Search on YouTube ↗</a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="showChat"
          class="w-full lg:w-[400px] bg-white shadow-lg shadow-gray-200/50 border border-gray-200 rounded-2xl flex flex-col h-[calc(100vh-140px)] sticky top-6">
          <div class="p-4 border-b border-gray-100 flex justify-between items-center bg-gray-50/50 rounded-t-2xl">
            <h3 class="font-bold text-gray-700">Chat with Video</h3>
            <span class="text-xs bg-blue-100 text-blue-600 px-2 py-0.5 rounded-full font-bold">AI Active</span>
          </div>
          <div ref="chatContainer" class="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
            <div v-for="(msg, i) in chatHistory" :key="i" class="flex"
              :class="msg.role === 'user' ? 'justify-end' : 'justify-start'">
              <div class="max-w-[85%] p-3.5 rounded-2xl text-sm leading-relaxed shadow-sm"
                :class="msg.role === 'user' ? 'bg-blue-600 text-white rounded-tr-none' : 'bg-gray-100 text-gray-800 rounded-tl-none'">
                <div v-if="msg.loading" class="flex items-center gap-2 py-1">
                  <svg class="animate-spin h-4 w-4 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none"
                    viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                    </path>
                  </svg>

                  <span class="text-gray-500 text-sm font-medium italic animate-pulse">Thinking...</span>
                </div>
                <div v-else v-html="md.render(msg.text)"></div>
              </div>
            </div>
          </div>
          <div class="p-4 border-t border-gray-100 bg-white rounded-b-2xl flex gap-2">
            <input v-model="chatInput" @keyup.enter="askQuestion" type="text" placeholder="Ask follow-up..."
              class="flex-1 bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-blue-500" />
            <button @click="askQuestion"
              class="p-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition">➤</button>
          </div>
        </div>

      </main>
    </div>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 5px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}

:deep(.prose h1),
:deep(.prose h2),
:deep(.prose h3) {
  margin-top: 1em;
  margin-bottom: 0.5em;
  color: #1f2937;
  font-weight: 700;
}

:deep(.prose ul) {
  list-style-type: disc;
  padding-left: 1.5em;
}

:deep(.prose strong) {
  font-weight: 700;
  color: #111827;
}
</style>