<template>
  <div class="flex h-screen bg-light">
    <!-- Sidebar -->
    <Sidebar />

    <!-- Main Content -->
    <div class="flex flex-col flex-1 min-h-screen">
      <HeaderBar />

      <!-- Body Section -->
      <div class="d-flex flex-grow-1 overflow-hidden">

        <!-- Main content container -->
        <main class="flex-1 overflow-y-auto p-6 ml-[250px]">
          <!-- DASHBOARD PAGE -->
          <section v-show="activePage === 'dashboard'" class="space-y-6">
            <!-- Hero -->
            <div class="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-6 text-white shadow">
              <h2 class="text-2xl font-bold mb-1">Welcome back, Aryan! 👋</h2>
              <p class="opacity-90">Here's what's happening with your academics today.</p>
            </div>

            <!-- Stats -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div v-for="s in stats" :key="s.title" class="bg-white border border-gray-200 rounded-xl p-5">
                <div class="flex items-center justify-between mb-2">
                  <component :is="s.icon" class="w-5 h-5" :class="s.color" />
                  <span class="text-2xl font-bold text-gray-900">{{ s.value }}</span>
                </div>
                <p class="text-gray-600 text-sm">{{ s.title }}</p>
                <p class="text-green-600 text-xs mt-1">This week</p>
              </div>
            </div>

            <!-- Two-column area -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <!-- Deadlines -->
              <div class="bg-white border border-gray-200 rounded-xl p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">Upcoming Deadlines</h3>
                <div class="space-y-3">
                  <div v-for="d in deadlines" :key="d.name" class="flex items-start p-3 bg-gray-50 rounded-lg">
                    <AlertCircle class="w-5 h-5 text-orange-600 mr-3 mt-1" />
                    <div class="flex-1">
                      <p class="font-medium text-gray-900">{{ d.name }}</p>
                      <p class="text-sm text-gray-600">{{ d.course }}</p>
                      <p class="text-xs text-gray-500 mt-1">Due: {{ d.due }}</p>
                    </div>
                    <span class="px-2 py-1 rounded text-xs bg-orange-100 text-orange-600">pending</span>
                  </div>
                </div>
              </div>

              <!-- Announcements -->
              <div class="bg-white border border-gray-200 rounded-xl p-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">Recent Announcements</h3>
                <div class="space-y-3">
                  <div v-for="a in announcements" :key="a.title" class="flex items-start p-3 bg-gray-50 rounded-lg">
                    <Bell class="w-5 h-5 text-blue-600 mr-3 mt-1" />
                    <div class="flex-1">
                      <p class="font-medium text-gray-900">{{ a.title }}</p>
                      <p class="text-sm text-gray-600">{{ a.course }}</p>
                      <p class="text-xs text-gray-500 mt-1">{{ a.time }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Course progress -->
            <div class="bg-white border border-gray-200 rounded-xl p-6">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Course Progress</h3>
              <div class="space-y-4">
                <div v-for="c in courses" :key="c.code">
                  <div class="flex items-center justify-between mb-2">
                    <div>
                      <p class="font-medium text-gray-900">{{ c.name }}</p>
                      <p class="text-sm text-gray-600">{{ c.code }}</p>
                    </div>
                    <span class="font-bold text-blue-600">{{ c.progress }}%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-blue-600 h-2 rounded-full" :style="{ width: c.progress + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- AI ASSISTANT PAGE -->
          <section v-show="activePage === 'ai-assistant'" class="h-full flex flex-col gap-4">
            <div class="bg-white border border-gray-200 rounded-xl p-4">
              <h3 class="font-semibold text-gray-900">RAG-based Multilingual AI Assistant</h3>
              <p class="text-sm text-gray-600">Ask something about the course, assignments or admin.</p>
            </div>

            <div class="flex-1 bg-white border border-gray-200 rounded-xl p-4 flex flex-col">
              <div id="chatMessages" class="flex-1 overflow-y-auto p-4 space-y-3">
                <div v-for="(m, i) in messages" :key="i"
                  :class="m.from === 'user' ? 'flex justify-end' : 'flex justify-start'">
                  <div
                    :class="['max-w-xs lg:max-w-md px-4 py-3 rounded-lg', m.from === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-900']">
                    <p class="text-sm" v-html="m.text"></p>
                  </div>
                </div>
              </div>

              <div class="p-4 border-t border-gray-200">
                <div class="flex gap-2">
                  <input v-model="chatInput" @keyup.enter="sendMessage" placeholder="Ask a question..."
                    class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600" />
                  <button @click="sendMessage"
                    class="px-5 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">Send</button>
                </div>
              </div>
            </div>
          </section>

          <!-- STUDY ASSISTANT PAGE -->
          <section v-show="activePage === 'study-assistant'" class="space-y-6">
            <div class="bg-white border border-gray-200 rounded-xl p-6">
              <h3 class="text-lg font-semibold text-gray-900">Study Assistant</h3>
              <p class="text-sm text-gray-600">Weekly summary, deadlines, and smart reminders will appear here.
                (API-ready)</p>
            </div>

            <!-- Example card -->
            <div class="bg-white border border-gray-200 rounded-xl p-6">
              <h4 class="font-medium">Weekly Summary</h4>
              <p class="text-sm text-gray-600 mt-2">This is a placeholder. Hook up the backend to fetch weekly
                summaries.</p>
            </div>
          </section>

          <!-- CONTENT RECOMMENDER / MY QUERIES / FORUM / PROFILE -->
          <section v-show="activePage === 'content-recommender'" class="space-y-6">
            <div class="bg-white border border-gray-200 rounded-xl p-6">
              <h3 class="text-lg font-semibold text-gray-900">Content Recommender</h3>
              <p class="text-sm text-gray-600">Placeholder for recommended readings.</p>
            </div>
          </section>

          <section v-show="activePage === 'my-queries'" class="space-y-6">
            <div class="bg-white border border-gray-200 rounded-xl p-6">
              <h3 class="text-lg font-semibold text-gray-900">My Queries</h3>
              <p class="text-sm text-gray-600">Placeholder — shows student queries and statuses.</p>
            </div>
          </section>

          <section v-show="activePage === 'forum'" class="space-y-6">
            <div class="bg-white border border-gray-200 rounded-xl p-6">
              <h3 class="text-lg font-semibold text-gray-900">Discussion Forum</h3>
              <p class="text-sm text-gray-600">Placeholder for forum threads and search.</p>
            </div>
          </section>

          <section v-show="activePage === 'profile'" class="space-y-6">
            <div class="bg-white border border-gray-200 rounded-xl p-6">
              <h3 class="text-lg font-semibold text-gray-900">Profile</h3>
              <p class="text-sm text-gray-600">User profile and settings go here.</p>
            </div>
          </section>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import Sidebar from '@/components/layout/StudentLayout/SideBar.vue'

import { ref } from 'vue'
import {
  Menu,
  Bell,
  LogOut,
  BookOpen,
  CheckCircle,
  FileText,
  Clock,
  AlertCircle,
} from 'lucide-vue-next'

// ------- state -------
const activePage = ref('dashboard')
const pageTitle = ref('Dashboard')

const pagesList = [
  { id: 'dashboard', label: 'Dashboard' },
  { id: 'ai-assistant', label: 'AI Assistant' },
  { id: 'study-assistant', label: 'Study Assistant' },
  { id: 'content-recommender', label: 'Content Recommender' },
  { id: 'my-queries', label: 'My Queries' },
  { id: 'forum', label: 'Discussion Forum' },
  { id: 'profile', label: 'Profile' },
]

function showPage(id) {
  activePage.value = id
  const titleMap = {
    dashboard: 'Dashboard',
    'ai-assistant': 'AI Assistant',
    'study-assistant': 'Study Assistant',
    'content-recommender': 'Content Recommender',
    'my-queries': 'My Queries',
    forum: 'Discussion Forum',
    profile: 'Profile',
  }
  pageTitle.value = titleMap[id] || 'Aura'
}

// ------- sample data -------
const stats = [
  { title: 'Lectures Watched', value: 12, icon: BookOpen, color: 'text-blue-600' },
  { title: 'Assignments Done', value: 3, icon: CheckCircle, color: 'text-green-600' },
  { title: 'Quizzes Taken', value: 2, icon: FileText, color: 'text-purple-600' },
  { title: 'Study Hours', value: 18, icon: Clock, color: 'text-orange-600' },
]

const deadlines = [
  { name: 'Software Engineering Project - Milestone 3', course: 'BSCS3001', due: '2025-11-05' },
  { name: 'Data Science Assignment - Module 2', course: 'BSCS3010', due: '2025-11-07' },
  { name: 'AI Quiz - Unit 4', course: 'BSCS3025', due: '2025-11-10' },
]

const announcements = [
  { title: 'Mid-term exam schedule updated', course: 'BSCS3001', time: '2 hours ago' },
  { title: 'New project guidelines released', course: 'BSCS3010', time: '1 day ago' },
  { title: 'Assignment 2 evaluation complete', course: 'BSCS3025', time: '3 days ago' },
]

const courses = [
  { name: 'Software Engineering', code: 'BSCS3001', progress: 75 },
  { name: 'Data Science Fundamentals', code: 'BSCS3010', progress: 60 },
  { name: 'Artificial Intelligence', code: 'BSCS3025', progress: 40 },
]

// ------- AI chat demo -------
const messages = ref([
  { from: 'bot', text: "Hello! I'm your AI Assistant. How can I help you today?" },
])
const chatInput = ref('')
function sendMessage() {
  const t = chatInput.value.trim()
  if (!t) return
  messages.value.push({ from: 'user', text: t })
  chatInput.value = ''
  // fake response
  setTimeout(() => {
    messages.value.push({ from: 'bot', text: "Processing... In a real app this would call the AI with course context and return an answer." })
  }, 700)
}

// ------- simple handlers -------
function handleLogout() {
  // placeholder
  alert('Logging out (placeholder)')
}
</script>

<style scoped>
/* minor polish to keep parity with the HTML look */
.page-title {
  letter-spacing: -0.02em;
}
</style>
