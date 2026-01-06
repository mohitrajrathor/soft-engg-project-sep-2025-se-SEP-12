<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { useThemeStore } from '@/stores/theme'
import { authAPI } from '@/api'
import InstructorSidebar from '@/components/layout/instructorLayout/instructorSideBar.vue'
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
  , AcademicCapIcon
} from "@heroicons/vue/24/outline"

const userStore = useUserStore()
const themeStore = useThemeStore()

// State
const isLoading = ref(false)
const error = ref(null)
const instructorStats = ref({
  total_courses: 0,
  total_students: 0,
  total_quizzes: 0,
  published_quizzes: 0
})
const profileData = ref({
  full_name: '',
  email: '',
  role: '',
  department: ''
})

// Computed
const formattedRole = computed(() => {
  if (!profileData.value.role) return 'Instructor'
  return profileData.value.role.charAt(0).toUpperCase() + profileData.value.role.slice(1)
})

const userInitial = computed(() => {
  return profileData.value.full_name.charAt(0).toUpperCase() || 'I'
})

const memberSince = computed(() => {
  return 'Recently joined'
})

// API Functions
const loadProfileData = async () => {
  isLoading.value = true
  error.value = null

  try {
    // Get user info from backend API
    const user = await authAPI.getCurrentUser()
    if (user) {
      profileData.value = {
        full_name: user.full_name || user.name || 'Instructor',
        email: user.email || '',
        role: user.role || 'instructor',
        department: user.department || 'Computer Science'
      }
      console.log('Loaded instructor profile from backend:', profileData.value)
    } else {
      console.warn('No user data returned from backend')
      error.value = 'No user information available'
    }

    // Get instructor courses stats (placeholder for future API)
    try {
      // Once instructor statistics API is available, update this
      instructorStats.value = {
        total_courses: 3,
        total_students: 45,
        total_quizzes: 12,
        published_quizzes: 10
      }
    } catch (err) {
      console.warn('Failed to load instructor stats:', err)
    }

  } catch (err) {
    console.error('Failed to load profile data:', err)
    error.value = err.response?.data?.detail || 'Failed to load profile data. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const handleLogout = () => {
  userStore.logout()
}

// Lifecycle
onMounted(() => {
  loadProfileData()
})

// Watch for user store changes
watch(
  () => userStore.user,
  (newUser) => {
    if (newUser) {
      profileData.value = {
        full_name: newUser.full_name || newUser.name || 'Instructor',
        email: newUser.email || '',
        role: newUser.role || 'instructor',
        department: newUser.department || 'Computer Science'
      }
    }
  },
  { immediate: true }
)
</script>

<template>
  <div class="flex min-h-screen" style="background-color: var(--page-bg);">
    <!-- Sidebar -->
    <InstructorSidebar class="fixed top-0 left-0 h-screen w-[250px]" />

    <!-- Main -->
    <main class="flex-1 p-8 ml-[250px] overflow-y-auto" style="background-color: var(--page-bg);">
      <HeaderBar searchPlaceholder="Search students, courses, or resources" />
      <h2 class="font-bold text-2xl mb-6">Instructor Settings</h2>

      <!-- Loading State -->
      <div v-if="isLoading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
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
          <div class="bg-white rounded-2xl p-6 shadow flex flex-col sm:flex-row items-start gap-8 hover:shadow-xl transition group">
            <div class="flex flex-col items-center min-w-[120px]">
              <div class="w-20 h-20 rounded-full bg-gradient-to-br from-green-400 to-green-600 flex items-center justify-center text-white text-2xl font-bold border-4 border-green-100 shadow mb-3 transition group-hover:scale-110">
                {{ userInitial }}
              </div>
              <button class="px-4 py-1 bg-green-100 text-green-700 font-semibold rounded-lg text-xs hover:bg-green-200 active:scale-95 transition">
                Change avatar
              </button>
              <span class="mt-2 text-xs bg-green-100 text-green-800 rounded-full px-2 py-1 font-semibold">{{ formattedRole }}</span>
            </div>

            <form class="flex-1 w-full grid grid-cols-1 gap-3">
              <div class="grid md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-xs text-gray-700 mb-1">Full name</label>
                  <input type="text" class="w-full border rounded-lg p-2 mb-3 focus:ring focus:border-green-400 hover:border-green-400 transition" :value="profileData.full_name" readonly />
                  <label class="block text-xs text-gray-700 mb-1">Institution email</label>
                  <input type="email" class="w-full border rounded-lg p-2 mb-3 focus:ring focus:border-green-400 hover:border-green-400 transition" :value="profileData.email" readonly />
                  <label class="block text-xs text-gray-700 mb-1">Department</label>
                  <input type="text" class="w-full border rounded-lg p-2 mb-3 focus:ring focus:border-green-400 hover:border-green-400 transition bg-gray-50" :value="profileData.department" readonly />
                </div>
                <div class="flex flex-col items-start gap-3 justify-center">
                  <label class="hidden sm:block text-xs text-gray-700 mb-1">&nbsp;</label>
                  <button type="button" class="w-full py-2 bg-gray-300 text-gray-600 font-semibold rounded-lg shadow cursor-not-allowed" disabled>
                    Upload (Coming Soon)
                  </button>
                  <button type="button" class="w-full py-2 flex items-center justify-center gap-2 bg-gray-300 text-gray-600 font-semibold rounded-lg shadow cursor-not-allowed" disabled>
                    <CheckCircleIcon class="w-5 h-5" /> Save changes (Coming Soon)
                  </button>
                </div>
              </div>
            </form>
          </div>

          <!-- Teaching Preferences -->
          <div class="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition">
            <div class="font-bold mb-2">Teaching Preferences</div>
            <div class="flex gap-2">
              <button 
                @click="themeStore.setTheme('light')"
                :class="[
                  'border-2 rounded-lg px-4 py-2 transition active:scale-95 font-semibold',
                  themeStore.currentTheme === 'light' 
                    ? 'border-blue-600 bg-blue-50 text-blue-600 shadow-sm' 
                    : 'border-gray-300 hover:border-blue-400'
                ]"
                :style="themeStore.currentTheme === 'light' 
                  ? {} 
                  : { backgroundColor: 'var(--card-bg)', color: 'var(--text-primary)' }"
              >
                Light
              </button>
              <button 
                @click="themeStore.setTheme('dark')"
                :class="[
                  'border-2 rounded-lg px-4 py-2 transition active:scale-95 font-semibold',
                  themeStore.currentTheme === 'dark' 
                    ? 'border-blue-600 bg-blue-50 text-blue-600 shadow-sm' 
                    : 'border-gray-300 hover:border-blue-400'
                ]"
                :style="themeStore.currentTheme === 'dark' 
                  ? {} 
                  : { backgroundColor: 'var(--card-bg)', color: 'var(--text-primary)' }"
              >
                Dark
              </button>
            </div>
            <div class="mt-4">
              <div class="text-xs mb-1 font-semibold">Language</div>
              <div class="flex gap-2">
                <button class="border rounded-lg px-4 py-2 bg-gray-100 text-gray-700 border-gray-300 hover:border-green-400 active:scale-95 transition">English</button>
                <button class="border rounded-lg px-4 py-2 bg-gray-100 text-gray-700 border-gray-300 hover:border-green-400 active:scale-95 transition">Hindi</button>
              </div>
            </div>
          </div>

          <!-- Connected Platforms -->
          <div class="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition">
            <div class="font-bold mb-2">Connected Platforms</div>
            <div class="flex flex-wrap gap-6">
              <div><span class="font-semibold">Google Classroom</span><button class="text-green-600 underline ml-2 hover:text-green-800 active:scale-95 transition">Linked</button></div>
              <div><span class="font-semibold">GitHub</span><button class="text-green-600 underline ml-2 hover:text-green-800 active:scale-95 transition">Linked</button></div>
              <div><span class="font-semibold">Zoom</span><button class="text-green-600 underline ml-2 hover:text-green-800 active:scale-95 transition">Linked</button></div>
            </div>
          </div>

          <!-- Theme Preferences Card -->
          <div class="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition" style="background-color: var(--card-bg); border: 1px solid var(--border-color);">
            <div class="font-bold mb-4">Appearance Preferences</div>
            <div class="flex gap-6 flex-wrap">
              <div>
                <div class="text-xs mb-2 font-semibold">Theme</div>
                <div class="flex gap-2">
                  <button 
                    @click="themeStore.setTheme('light')"
                    :class="[
                      'border-2 rounded-lg px-4 py-2 transition active:scale-95 font-semibold',
                      themeStore.currentTheme === 'light' 
                        ? 'border-blue-600 bg-blue-600 text-white shadow-lg' 
                        : 'border-gray-300 hover:border-blue-400'
                    ]"
                    :style="themeStore.currentTheme === 'light' 
                      ? {} 
                      : { backgroundColor: 'var(--card-bg)', color: 'var(--text-primary)' }"
                  >
                    Light
                  </button>
                  <button 
                    @click="themeStore.setTheme('dark')"
                    :class="[
                      'border-2 rounded-lg px-4 py-2 transition active:scale-95 font-semibold',
                      themeStore.currentTheme === 'dark' 
                        ? 'border-blue-600 bg-blue-600 text-white shadow-lg' 
                        : 'border-gray-300 hover:border-blue-400'
                    ]"
                    :style="themeStore.currentTheme === 'dark' 
                      ? {} 
                      : { backgroundColor: 'var(--card-bg)', color: 'var(--text-primary)' }"
                  >
                    Dark
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Danger Zone Card -->
          <div class="bg-white rounded-2xl p-6 shadow flex items-center justify-between hover:shadow-lg transition">
            <div>
              <div class="font-bold text-red-600 mb-2">Danger zone</div>
              <div>Delete instructor account</div>
              <div class="text-xs text-gray-400">This action cannot be undone</div>
            </div>
            <button class="bg-red-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-red-700 active:scale-95 transition">
              <TrashIcon class="w-5 h-5" /> Delete
            </button>
          </div>
        </div>

        <!-- Right Sidebar -->
        <div class="col-span-4 space-y-6">
          <!-- Account Summary -->
          <div class="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition">
            <div class="font-bold">Instructor Summary</div>
            <div class="text-xs text-gray-700 mt-1">Email: <span class="font-mono text-gray-800">{{ profileData.email }}</span></div>
            <div class="text-xs text-gray-700">Role: <span class="font-semibold text-green-600">{{ formattedRole }}</span></div>
            <div class="text-xs text-gray-700">Member since: {{ memberSince }}</div>

            <div class="mt-4 pt-4 border-t space-y-2">
              <div class="font-semibold text-sm mb-2">Statistics</div>
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-600">Active Courses:</span>
                <span class="text-sm font-bold text-green-600">{{ instructorStats.total_courses }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-600">Total Students:</span>
                <span class="text-sm font-bold text-blue-600">{{ instructorStats.total_students }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-600">Total Quizzes:</span>
                <span class="text-sm font-bold text-purple-600">{{ instructorStats.total_quizzes }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-xs text-gray-600">Published:</span>
                <span class="text-sm font-bold text-emerald-600">{{ instructorStats.published_quizzes }}</span>
              </div>
            </div>
          </div>

          <!-- Shortcuts -->
          <div class="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition">
            <div class="font-bold mb-2">Shortcuts</div>
            <div class="space-y-2">
              <button class="flex items-center gap-2 w-full text-left text-sm hover:text-green-700 hover:bg-green-50 rounded-lg px-2 py-2 transition">
                <Cog6ToothIcon class="w-4 h-4" /> Manage courses
              </button>
              <button class="flex items-center gap-2 w-full text-left text-sm hover:text-green-700 hover:bg-green-50 rounded-lg px-2 py-2 transition">
                <UserCircleIcon class="w-4 h-4" /> View enrolled students
              </button>
              <button class="flex items-center gap-2 w-full text-left text-sm hover:text-green-700 hover:bg-green-50 rounded-lg px-2 py-2 transition">
                <AcademicCapIcon class="w-4 h-4" /> Grade submissions
              </button>
            </div>
          </div>

          <!-- Session -->
          <div class="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition">
            <div class="font-bold mb-2">Session</div>
            <div class="text-xs text-gray-700 mb-3">
              <div class="mb-1">Currently logged in as:</div>
              <div class="font-mono text-green-600">{{ profileData.email }}</div>
            </div>
            <button
              @click="handleLogout"
              class="mt-2 px-3 py-2 border border-green-600 bg-green-50 rounded-lg text-green-700 font-semibold w-full flex items-center justify-center gap-2 hover:bg-green-100 hover:border-green-800 active:scale-95 transition"
            >
              <ArrowRightOnRectangleIcon class="w-5 h-5" /> Sign out
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
/* Instructor settings styling handled mostly via Tailwind */
</style>
