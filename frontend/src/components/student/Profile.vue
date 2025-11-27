<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { queriesAPI, chatbotAPI } from '@/api'
import Sidebar from '@/components/layout/StudentLayout/SideBar.vue'
import HeaderBar from '@/components/layout/StudentLayout/HeaderBar.vue'

import {
  UserCircleIcon,
  EnvelopeIcon,
  KeyIcon,
  Cog6ToothIcon,
  TrashIcon,
  CheckCircleIcon,
  ArrowRightOnRectangleIcon,
  ExclamationCircleIcon
} from "@heroicons/vue/24/outline"

const userStore = useUserStore()

// State
const isLoading = ref(false)
const error = ref(null)
const userStats = ref({
  total_queries: 0,
  open_queries: 0,
  resolved_queries: 0,
  active_tasks: 0
})
const profileData = ref({
  full_name: '',
  email: '',
  role: ''
})

// Computed
const formattedRole = computed(() => {
  if (!profileData.value.role) return 'Student'
  return profileData.value.role.charAt(0).toUpperCase() + profileData.value.role.slice(1)
})

const memberSince = computed(() => {
  // You can add a created_at field to User model if needed
  // For now, return a default
  return 'Recently joined'
})

// API Functions
const loadProfileData = async () => {
  isLoading.value = true
  error.value = null

  try {
    // Get user info from store
    const user = userStore.user
    if (user) {
      profileData.value = {
        full_name: user.full_name || user.name || 'User',
        email: user.email || '',
        role: user.role || 'student'
      }
    }

    // Get query statistics
    try {
      const queryStats = await queriesAPI.getStatistics()
      userStats.value.total_queries = queryStats.total_queries || 0
      userStats.value.open_queries = queryStats.by_status?.open || 0
      userStats.value.resolved_queries = queryStats.by_status?.resolved || 0
    } catch (err) {
      console.warn('Failed to load query stats:', err)
    }

    // Get user context for additional stats
    try {
      const context = await chatbotAPI.getUserContext()
      if (context.user_context) {
        userStats.value.active_tasks = context.user_context.active_tasks_count || 0
      }
    } catch (err) {
      console.warn('Failed to load user context:', err)
    }

  } catch (err) {
    console.error('Failed to load profile data:', err)
    error.value = 'Failed to load profile data. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const handleLogout = () => {
  userStore.logout()
  // Will redirect to login via auth guard
}

// Lifecycle
onMounted(() => {
  loadProfileData()
})
</script>

<template>
  <div class="flex min-h-screen bg-gray-50">
    <Sidebar class="fixed top-0 left-0 h-screen w-[250px]" />
    <main class="flex-1 p-8 ml-[250px] overflow-y-auto">
      <HeaderBar searchPlaceholder="Search courses, threads, resources" />
      <h2 class="font-bold text-2xl mb-6">Settings</h2>

      <!-- Loading State -->
      <div v-if="isLoading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">Loading your profile...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-xl p-6 mb-6">
        <div class="flex items-center gap-3">
          <ExclamationCircleIcon class="w-6 h-6 text-red-600" />
          <div>
            <h3 class="text-red-800 font-semibold mb-1">Error</h3>
            <p class="text-red-600 text-sm">{{ error }}</p>
          </div>
        </div>
        <button
          @click="loadProfileData"
          class="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
        >
          Retry
        </button>
      </div>

      <!-- Profile Content -->
      <div v-else class="grid grid-cols-12 gap-8">
        <!-- Left main content -->
        <div class="col-span-8 space-y-8">
          <!-- Profile Card -->
          <div class="bg-white rounded-2xl p-6 shadow cursor-pointer flex flex-col sm:flex-row items-start gap-8 hover:shadow-xl transition group">
            <div class="flex flex-col items-center min-w-[120px]">
              <div class="w-20 h-20 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white text-2xl font-bold border-4 border-blue-100 shadow mb-3 transition group-hover:scale-110">
                {{ profileData.full_name.charAt(0).toUpperCase() }}
              </div>
              <button
                class="px-4 py-1 bg-blue-100 text-blue-700 font-semibold rounded-lg text-xs hover:bg-blue-200 active:scale-95 transition"
              >Change avatar</button>
              <span class="mt-2 text-xs bg-blue-100 text-blue-800 rounded-full px-2 py-1 font-semibold">{{ formattedRole }}</span>
            </div>
            <form class="flex-1 w-full grid grid-cols-1 gap-3">
              <div class="grid md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-xs text-gray-700 mb-1">Full name</label>
                  <input
                    type="text"
                    class="w-full border rounded-lg p-2 mb-3 focus:ring focus:border-blue-400 hover:border-blue-400 transition"
                    :value="profileData.full_name"
                    readonly
                  />
                  <label class="block text-xs text-gray-700 mb-1">University email</label>
                  <input
                    type="email"
                    class="w-full border rounded-lg p-2 mb-3 focus:ring focus:border-blue-400 hover:border-blue-400 transition"
                    :value="profileData.email"
                    readonly
                  />
                  <label class="block text-xs text-gray-700 mb-1">Role</label>
                  <input
                    type="text"
                    class="w-full border rounded-lg p-2 mb-3 focus:ring focus:border-blue-400 hover:border-blue-400 transition bg-gray-50"
                    :value="formattedRole"
                    readonly
                  />
                </div>
                <div class="flex flex-col items-start gap-3 justify-center">
                  <label class="hidden sm:block text-xs text-gray-700 mb-1">&nbsp;</label>
                  <button
                    type="button"
                    class="w-full py-2 bg-gray-300 text-gray-600 font-semibold rounded-lg shadow cursor-not-allowed"
                    disabled
                  >Upload (Coming Soon)</button>
                  <button
                    type="button"
                    class="w-full py-2 flex items-center justify-center gap-2 bg-gray-300 text-gray-600 font-semibold rounded-lg shadow cursor-not-allowed"
                    disabled
                  >
                    <CheckCircleIcon class="w-5 h-5" />Save changes (Coming Soon)
                  </button>
                </div>
              </div>
            </form>
          </div>

          <!-- Notifications Card -->
          <div class="bg-white rounded-2xl p-6 shadow space-y-2 hover:shadow-lg transition">
            <div class="font-bold mb-2">Notifications</div>
            <div class="flex flex-col gap-3">
              <label class="flex items-center cursor-pointer hover:bg-blue-50 px-2 py-1 rounded transition">
                <input type="checkbox" checked class="mr-2 accent-blue-600"> All notifications
              </label>
              <label class="flex items-center cursor-pointer hover:bg-blue-50 px-2 py-1 rounded transition">
                <input type="checkbox" checked class="mr-2 accent-blue-600"> Thread replies
              </label>
              <label class="flex items-center cursor-pointer hover:bg-blue-50 px-2 py-1 rounded transition">
                <input type="checkbox" checked class="mr-2 accent-blue-600"> Office hour reminders
              </label>
            </div>
          </div>

          <!-- Preferences Card -->
          <div class="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition">
            <div class="font-bold mb-2">Preferences</div>
            <div class="flex gap-6 flex-wrap mb-2">
              <div>
                <div class="text-xs mb-1">Theme</div>
                <button class="border rounded-lg px-4 py-2 mr-2 bg-gray-50 focus:bg-blue-50 hover:border-blue-400 hover:bg-blue-50 active:scale-95 transition">System</button>
                <button class="border rounded-lg px-4 py-2 bg-gray-50 focus:bg-blue-50 hover:border-blue-400 hover:bg-blue-50 active:scale-95 transition">Light</button>
                <button class="border rounded-lg px-4 py-2 bg-gray-50 focus:bg-blue-50 hover:border-blue-400 hover:bg-blue-50 active:scale-95 transition">Dark</button>
              </div>
              <div>
                <div class="text-xs mb-1">Language</div>
                <button class="border rounded-lg px-4 py-2 bg-gray-50 focus:bg-blue-50 hover:border-blue-400 hover:bg-blue-50 active:scale-95 transition">English</button>
                <button class="border rounded-lg px-4 py-2 bg-gray-50 focus:bg-blue-50 hover:border-blue-400 hover:bg-blue-50 active:scale-95 transition">Hindi</button>
                <button class="border rounded-lg px-4 py-2 bg-gray-50 focus:bg-blue-50 hover:border-blue-400 hover:bg-blue-50 active:scale-95 transition">Other</button>
              </div>
              <div>
                <div class="text-xs mb-1">Time zone</div>
                <button class="border rounded-lg px-4 py-2 bg-gray-50 focus:bg-blue-50 hover:border-blue-400 hover:bg-blue-50 active:scale-95 transition">UTC+05:00</button>
                <button class="border rounded-lg px-4 py-2 bg-gray-50 focus:bg-blue-50 hover:border-blue-400 hover:bg-blue-50 active:scale-95 transition">UTC+01:00</button>
              </div>
            </div>
          </div>

          <!-- Connected services Card -->
          <div class="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition">
            <div class="font-bold mb-2">Connected Services</div>
            <div class="flex flex-wrap gap-6">
              <div>
                <span class="font-semibold">GitHub</span>
                <button class="text-gray-400 ml-2">Not linked</button>
              </div>
              <div>
                <span class="font-semibold">LinkedIn</span>
                <button class="text-gray-400 ml-2">Not linked</button>
              </div>
              <div>
                <span class="font-semibold">Twitter</span>
                <button class="text-gray-400 ml-2">Not linked</button>
              </div>
              <div>
                <span class="font-semibold">Cloud Storage</span>
                <button class="text-gray-400 ml-2">Not linked</button>
              </div>
            </div>
          </div>

          <!-- Danger Zone Card -->
          <div class="bg-white rounded-2xl p-6 shadow flex items-center justify-between hover:shadow-lg transition">
            <div>
              <div class="font-bold text-red-600 mb-2">Danger zone</div>
              <div>Delete account</div>
              <div class="text-xs text-gray-400">This action is irreversible</div>
            </div>
            <button class="bg-red-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-red-700 active:scale-95 transition">
              <TrashIcon class="w-5 h-5" />Delete
            </button>
          </div>
        </div>

        <!-- Sidebar (Right) for summary, shortcuts, session -->
        <div class="col-span-4 space-y-6">
          <!-- Account Summary (Dynamic) -->
          <div class="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition">
            <div class="font-bold mb-3">Account summary</div>
            <div class="space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-600">Email:</span>
                <span class="text-xs font-mono text-gray-800">{{ profileData.email }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-600">Role:</span>
                <span class="text-xs font-semibold text-blue-600">{{ formattedRole }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-600">Member since:</span>
                <span class="text-xs text-gray-800">{{ memberSince }}</span>
              </div>
            </div>

            <div class="mt-4 pt-4 border-t space-y-2">
              <div class="font-semibold text-sm mb-2">Statistics</div>
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-600">Total Queries:</span>
                <span class="text-sm font-bold text-blue-600">{{ userStats.total_queries }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-600">Open Queries:</span>
                <span class="text-sm font-bold text-yellow-600">{{ userStats.open_queries }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-600">Resolved:</span>
                <span class="text-sm font-bold text-green-600">{{ userStats.resolved_queries }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-600">Active Tasks:</span>
                <span class="text-sm font-bold text-purple-600">{{ userStats.active_tasks }}</span>
              </div>
            </div>
          </div>

          <!-- Shortcuts -->
          <div class="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition">
            <div class="font-bold mb-2">Shortcuts</div>
            <div class="space-y-2">
              <button class="flex items-center gap-2 w-full text-left text-sm hover:text-blue-700 hover:bg-blue-50 rounded-lg px-2 py-2 transition">
                <Cog6ToothIcon class="w-4 h-4" />Customize AI Assistant
              </button>
              <button class="flex items-center gap-2 w-full text-left text-sm hover:text-blue-700 hover:bg-blue-50 rounded-lg px-2 py-2 transition">
                <CheckCircleIcon class="w-4 h-4" />Notification settings
              </button>
              <button class="flex items-center gap-2 w-full text-left text-sm hover:text-blue-700 hover:bg-blue-50 rounded-lg px-2 py-2 transition">
                <EnvelopeIcon class="w-4 h-4" />Help & Support
              </button>
            </div>
          </div>

          <!-- Session -->
          <div class="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition">
            <div class="font-bold mb-2">Session</div>
            <div class="text-xs text-gray-700 mb-3">
              <div class="mb-1">Currently logged in as:</div>
              <div class="font-mono text-blue-600">{{ profileData.email }}</div>
            </div>
            <button
              @click="handleLogout"
              class="mt-2 px-3 py-2 border border-red-600 bg-red-50 rounded-lg text-red-700 font-semibold w-full flex items-center justify-center gap-2 hover:bg-red-100 hover:border-red-800 active:scale-95 transition"
            >
              <ArrowRightOnRectangleIcon class="w-5 h-5" />Sign out
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
/* Interactive styling already included in classes above */
</style>
