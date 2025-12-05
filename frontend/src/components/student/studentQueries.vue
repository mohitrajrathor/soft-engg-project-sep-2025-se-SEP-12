<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useThemeStore } from '@/stores/theme'
import { queriesAPI } from '@/api'
import Sidebar from '@/components/layout/StudentLayout/SideBar.vue'
import HeaderBar from '@/components/layout/StudentLayout/HeaderBar.vue'
import BottomBar from '@/components/layout/StudentLayout/BottomBar.vue'
import ChatBubble from '@/components/shared/ChatBubble.vue'
import {
  MagnifyingGlassIcon,
  PlusCircleIcon,
  CheckCircleIcon,
  AcademicCapIcon,
  ChatBubbleLeftRightIcon,
  UserCircleIcon,
  PaperClipIcon,
  CubeIcon,
  ExclamationCircleIcon,
  ClockIcon,
} from "@heroicons/vue/24/outline"

const userStore = useUserStore()
const themeStore = useThemeStore()

// State
const queries = ref([])
const selectedQuery = ref(null)
const statusFilter = ref('all')  // 'all', 'open', 'resolved'
const isLoading = ref(false)
const isLoadingDetail = ref(false)
const error = ref(null)
const searchQuery = ref('')
const showNewQueryModal = ref(false)

// Message input state
const message = ref('')
const attachedFile = ref(null)
const fileInput = ref(null)

const triggerFilePicker = () => fileInput.value.click()

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) attachedFile.value = file
}

const removeAttachment = () => {
  attachedFile.value = null
  fileInput.value.value = ''
}

// Computed
const filteredQueries = computed(() => {
  let result = queries.value

  // Filter by status
  if (statusFilter.value === 'open') {
    result = result.filter(q => q.status === 'OPEN')
  } else if (statusFilter.value === 'resolved') {
    result = result.filter(q => q.status === 'RESOLVED')
  }

  // Filter by search query
  if (searchQuery.value.trim()) {
    const search = searchQuery.value.toLowerCase()
    result = result.filter(q =>
      q.title.toLowerCase().includes(search) ||
      q.description.toLowerCase().includes(search)
    )
  }

  return result
})

const recentQueries = computed(() => {
  // Show last 10 queries for sidebar
  return queries.value.slice(0, 10)
})

const openQueriesCount = computed(() => {
  return queries.value.filter(q => q.status === 'OPEN').length
})

// Helper functions
const getStatusColor = (status) => {
  switch (status) {
    case 'OPEN':
      return 'bg-blue-50 text-blue-700'
    case 'IN_PROGRESS':
      return 'bg-yellow-50 text-yellow-700'
    case 'RESOLVED':
      return 'bg-green-50 text-green-700'
    default:
      return 'bg-gray-50 text-gray-700'
  }
}

const getStatusLabel = (status) => {
  switch (status) {
    case 'OPEN':
      return 'Open'
    case 'IN_PROGRESS':
      return 'In Progress'
    case 'RESOLVED':
      return 'Resolved'
    default:
      return status
  }
}

const getCategoryIcon = (category) => {
  // For now, use CubeIcon for all categories
  return CubeIcon
}

const formatTimeAgo = (isoString) => {
  if (!isoString) return ''

  const date = new Date(isoString)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)

  if (diffMins < 60) {
    return `${diffMins}m ago`
  } else if (diffHours < 24) {
    return `${diffHours}h ago`
  } else if (diffDays === 1) {
    return 'Yesterday'
  } else if (diffDays < 7) {
    return `${diffDays}d ago`
  } else {
    return date.toLocaleDateString()
  }
}

// API functions
const loadQueries = async () => {
  isLoading.value = true
  error.value = null

  try {
    const response = await queriesAPI.getQueries({ limit: 100 })
    queries.value = response.queries || []

    // Auto-select first query if none selected
    if (queries.value.length > 0 && !selectedQuery.value) {
      await selectQuery(queries.value[0].id)
    }
  } catch (err) {
    console.error('Failed to load queries:', err)
    error.value = 'Failed to load queries. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const selectQuery = async (queryId) => {
  isLoadingDetail.value = true

  try {
    const query = await queriesAPI.getQuery(queryId)
    selectedQuery.value = query
  } catch (err) {
    console.error('Failed to load query details:', err)
    error.value = 'Failed to load query details.'
  } finally {
    isLoadingDetail.value = false
  }
}

const setStatusFilter = (filter) => {
  statusFilter.value = filter
}

const sendMessage = async () => {
  if (message.value.trim() === '' && !attachedFile.value) return
  if (!selectedQuery.value) return

  try {
    await queriesAPI.addResponse(selectedQuery.value.id, {
      content: message.value,
      is_solution: false
    })

    // Reload query to show new response
    await selectQuery(selectedQuery.value.id)
    await loadQueries()  // Refresh list

    message.value = ''
    removeAttachment()
  } catch (err) {
    console.error('Failed to send message:', err)
    error.value = 'Failed to send message. Please try again.'
  }
}

// Lifecycle
onMounted(() => {
  loadQueries()
})
</script>

<template>
  <div class="flex h-screen overflow-hidden">
    <!-- Sidebar -->
    <Sidebar class="sticky top-0 h-screen flex-shrink-0" />

    <!-- Main Content -->
    <div class="flex-1 flex flex-col ml-[250px]" :style="{ background: 'var(--bg-primary)' }">
      <!-- Header -->
      <HeaderBar class="sticky top-0 z-50" searchPlaceholder="Search queries..." :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }" />

      <!-- Page content -->
      <div class="flex-1 overflow-y-auto p-6 pb-28" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
        <!-- Top Filter Bar -->
        <div class="flex items-center justify-between gap-6 mb-6" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
          <div class="flex gap-3">
            <button
              @click="setStatusFilter('all')"
              class="rounded-[18px] px-6 py-2 text-base font-semibold border-2 shadow transition"
              :class="statusFilter === 'all' ? 'text-blue-700 bg-section border-blue-500' : 'text-gray-700 bg-section border-gray-200 hover:bg-gray-100'"
            >
              All
            </button>
            <button
              @click="setStatusFilter('open')"
              class="rounded-[18px] px-6 py-2 text-base font-semibold border-2 shadow transition"
              :class="statusFilter === 'open' ? 'text-blue-700 bg-blue-100 border-blue-500' : 'text-gray-700 bg-section border-gray-200 hover:bg-gray-100'"
            >
              Open
            </button>
            <button
              @click="setStatusFilter('resolved')"
              class="rounded-[18px] px-6 py-2 text-base border-2 transition"
              :class="statusFilter === 'resolved' ? 'text-green-700 bg-green-100 border-green-500 font-semibold' : 'text-gray-700 bg-section border-gray-200 hover:bg-gray-100'"
            >
              Resolved
            </button>
          </div>

          <router-link
            to="/student/new-query"
            class="flex items-center gap-2 px-5 py-2 rounded-[18px] bg-blue-600 font-semibold shadow hover:bg-blue-700 transition text-base"
            :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }"
          >
            <PlusCircleIcon class="w-6 h-6" />
            New Query
          </router-link>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p class="mt-4" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Loading your queries...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-xl p-6 mb-6">
          <div class="flex items-center gap-3">
            <ExclamationCircleIcon class="w-6 h-6 text-red-600" />
            <div>
              <h3 class="font-semibold mb-1" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Error</h3>
              <p class="text-sm" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ error }}</p>
            </div>
          </div>
          <button
            @click="loadQueries"
            class="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
          >
            Retry
          </button>
        </div>

        <!-- Empty State -->
        <div v-else-if="queries.length === 0" class="text-center py-16">
          <ChatBubbleLeftRightIcon class="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 class="text-xl font-semibold mb-2" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">No queries yet</h3>
          <p class="mb-6" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Start by creating your first query</p>
          <router-link
            to="/student/new-query"
            class="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-blue-600 font-semibold shadow hover:bg-blue-700 transition"
            :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }"
          >
            <PlusCircleIcon class="w-5 h-5" /> Create New Query
          </router-link>
        </div>

        <!-- Grid Layout -->
        <div v-else class="grid grid-cols-12 gap-6">
          <!-- Left: Recent Queries -->
          <aside class="col-span-3 overflow-y-auto max-h-[calc(100vh-160px)] pr-1" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
            <div class="font-bold mb-3 text-lg">
              Recent queries
              <span class="text-xs ml-1" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">{{ queries.length }} total</span>
            </div>
            <div class="space-y-3">
              <div
                v-for="query in recentQueries"
                :key="query.id"
                @click="selectQuery(query.id)"
                :class="[
                  'rounded-2xl px-4 py-3 shadow border hover:shadow-md cursor-pointer transition',
                  selectedQuery && selectedQuery.id === query.id ? 'ring-2 ring-blue-500' : ''
                ]"
                :style="{ background: 'var(--color-bg-card)', borderColor: 'var(--color-border)' }"
              >
                <div class="font-semibold leading-tight line-clamp-2">{{ query.title }}</div>
                <div class="flex items-center gap-1 text-xs mt-1 mb-1" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
                  <component :is="getCategoryIcon(query.category)" class="w-4 h-4" />
                  {{ query.category }} · {{ formatTimeAgo(query.created_at) }}
                  <span :class="['ml-auto rounded-lg px-2 py-0.5', getStatusColor(query.status)]">
                    {{ getStatusLabel(query.status) }}
                  </span>
                </div>
                <div class="text-xs line-clamp-2" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
                  {{ query.description }}
                </div>
                <div v-if="query.response_count > 0" class="text-xs mt-1" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
                  {{ query.response_count }} {{ query.response_count === 1 ? 'reply' : 'replies' }}
                </div>
              </div>

              <!-- No queries message -->
              <div v-if="recentQueries.length === 0" class="text-center py-8 text-sm" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
                No queries match your filter
              </div>
            </div>
          </aside>

          <!-- Center: Main Thread -->
          <section class="col-span-5 flex flex-col relative rounded-2xl shadow-lg border overflow-hidden" :style="{ background: 'var(--color-bg-card)', color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
            <!-- Loading state for detail -->
            <div v-if="isLoadingDetail" class="flex-1 flex items-center justify-center">
              <div class="text-center">
                <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-2"></div>
                <p class="text-sm" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Loading query...</p>
              </div>
            </div>

            <!-- No query selected -->
            <div v-else-if="!selectedQuery" class="flex-1 flex items-center justify-center" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
              <div class="text-center">
                <ChatBubbleLeftRightIcon class="w-12 h-12 text-gray-300 mx-auto mb-3" />
                <p>Select a query to view details</p>
              </div>
            </div>

            <!-- Query detail -->
            <div v-else class="flex-1 flex flex-col">
              <!-- Scrollable Conversation -->
              <div class="flex-1 overflow-y-auto p-7">
                <div class="flex items-center gap-2 text-xs mb-3" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
                  <component :is="getCategoryIcon(selectedQuery.category)" class="w-5 h-5 text-blue-400" />
                  <span class="font-semibold">{{ selectedQuery.category }}</span>
                  <span class="mx-2 rounded-lg px-2 py-0.5 bg-slate-100" :style="{ color: themeStore.currentTheme === 'dark' ? 'black' : 'black' }">
                    {{ selectedQuery.priority }}
                  </span>
                  <span
                    v-if="selectedQuery.status === 'OPEN'"
                    class="ml-auto rounded-lg px-2 py-0.5 bg-green-100 text-green-700 flex items-center gap-1 cursor-pointer hover:bg-green-200"
                  >
                    <CheckCircleIcon class="w-4 h-4" /> Mark Resolved
                  </span>
                  <span
                    v-else
                    :class="['ml-auto rounded-lg px-2 py-0.5', getStatusColor(selectedQuery.status)]"
                  >
                    {{ getStatusLabel(selectedQuery.status) }}
                  </span>
                </div>

                <div class="font-black text-xl mb-1">{{ selectedQuery.title }}</div>
                <div class="text-xs mb-3" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
                  Created {{ formatTimeAgo(selectedQuery.created_at) }} · Query ID:
                  <span class="font-mono">Q-{{ selectedQuery.id }}</span>
                </div>

                <div class="text-sm mb-5 p-4 rounded-lg" :style="{ backgroundColor: 'var(--color-bg-section)', color: 'var(--color-text-primary)' }">
                  {{ selectedQuery.description }}
                </div>

                <!-- Messages/Responses -->
                <div class="space-y-5">
                  <!-- Original query as first message (rendered with ChatBubble) -->
                  <ChatBubble
                    v-if="selectedQuery"
                    :message="{ content: selectedQuery.description, timestamp: new Date(selectedQuery.created_at) }"
                    :isUser="true"
                    :isDark="themeStore.currentTheme === 'dark'"
                  />

                  <!-- Responses rendered with ChatBubble for consistent separation -->
                  <ChatBubble
                    v-for="response in selectedQuery.responses || []"
                    :key="response.id"
                    :message="{ content: response.content, timestamp: new Date(response.created_at), user_role: response.user_role }"
                    :isUser="response.user_role === 'student'"
                    :isDark="themeStore.currentTheme === 'dark'"
                  />

                  <!-- No responses yet -->
                  <div v-if="!selectedQuery.responses || selectedQuery.responses.length === 0" class="text-center py-8 text-sm" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
                    No responses yet. Be the first to respond!
                  </div>
                </div>
              </div>

              <!-- Message Input (only for open/in-progress queries) -->
              <div
                v-if="selectedQuery.status !== 'RESOLVED'"
                class="border-t p-4"
                :style="{ background: 'var(--color-bg-card)', borderColor: 'var(--color-border)' }"
              >
                <div class="flex items-center gap-3">
                  <input
                    v-model="message"
                    @keyup.enter="sendMessage"
                    type="text" 
                    placeholder="Add a response..."
                    class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <button
                    @click="sendMessage"
                    :disabled="!message.trim()"
                    :class="[
                      'px-4 py-2 rounded-lg font-semibold transition',
                      message.trim()
                        ? 'bg-blue-600 text-white hover:bg-blue-700' 
                        : 'bg-gray-300 text-gray-500 cursor-not-allowed',
                    ]"
                  >
                    Send
                  </button>
                </div>
              </div>
            </div>
          </section>

          <!-- Right: Filters & Info -->
          <aside class="col-span-4 overflow-y-auto max-h-[calc(100vh-160px)] space-y-5" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
            <div class="rounded-2xl border shadow p-5 flex flex-col gap-3" :style="{ background: 'var(--color-bg-card)', borderColor: 'var(--color-border)' }">
              <div class="font-bold">Quick Stats</div>
              <div class="grid grid-cols-2 gap-3" :style="{ color: 'var(--color-text-primary)' }">
                <div class="rounded-lg p-3 text-center" :style="{ backgroundColor: 'var(--color-bg-section)' }">
                  <div class="text-2xl font-bold text-blue-600">{{ queries.length }}</div>
                  <div class="text-xs text-gray-600" :style="{ color: 'var(--color-text-secondary)' }">Total Queries</div>
                </div> 
                <div class="bg-green-50 rounded-lg p-3 text-center">
                  <div class="text-2xl font-bold text-green-600">{{ openQueriesCount }}</div>
                  <div class="text-xs" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">Open</div>
                </div>
              </div>
            </div>

            <div v-if="selectedQuery" class="rounded-2xl border shadow p-5 flex flex-col gap-3" :style="{ background: 'var(--color-bg-card)', borderColor: 'var(--color-border)' }">
              <div class="font-bold">Query Details</div>
              <div class="space-y-2 text-sm" :style="{ color: 'var(--color-text-primary)' }">
                <div>
                  <span :style="{ color: 'var(--color-text-secondary)' }">Status:</span>
                  <span :class="['ml-2 px-2 py-1 rounded text-xs', getStatusColor(selectedQuery.status)]">
                    {{ getStatusLabel(selectedQuery.status) }}
                  </span>
                </div>
                <div>
                  <span :style="{ color: 'var(--color-text-secondary)' }">Priority:</span>
                  <span class="ml-2 font-semibold">{{ selectedQuery.priority }}</span>
                </div>
                <div>
                  <span :style="{ color: 'var(--color-text-secondary)' }">Category:</span>
                  <span class="ml-2">{{ selectedQuery.category }}</span>
                </div>
                <div>
                  <span :style="{ color: 'var(--color-text-secondary)' }">Created:</span>
                  <span class="ml-2">{{ formatTimeAgo(selectedQuery.created_at) }}</span>
                </div>
                <div v-if="selectedQuery.tags && selectedQuery.tags.length > 0">
                  <span :style="{ color: 'var(--color-text-secondary)' }">Tags:</span>
                  <div class="flex flex-wrap gap-1 mt-1">
                    <span
                      v-for="tag in selectedQuery.tags"
                      :key="tag"
                      class="px-2 py-1 bg-gray-100 rounded text-xs"
                      :style="{ color: themeStore.currentTheme === 'dark' ? 'black' : 'black' }"
                    >
                      #{{ tag }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </aside>
        </div>
      </div>

      <!-- Bottom Bar -->
      <BottomBar />
    </div>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  line-clamp: 2;
  -webkit-line-clamp: 2;
  overflow: hidden;
}
</style>
