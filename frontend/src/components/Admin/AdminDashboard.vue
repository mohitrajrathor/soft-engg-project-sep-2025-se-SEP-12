<template>
  <div class="min-h-screen bg-gray-100 py-10 px-4">
    <div class="max-w-6xl mx-auto">
      <!-- Banner -->
      <div class="rounded-xl bg-gradient-to-r from-indigo-500 to-indigo-700 text-white p-8 mb-8 shadow">
        <h1 class="text-3xl font-bold mb-2">Welcome back, Admin! 👋</h1>
        <div class="text-lg">Here's a birds-eye view of your institution for today.</div>
        <button
          v-if="!isLoading"
          @click="refreshData"
          class="mt-4 px-4 py-2 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg text-sm transition-all"
        >
          🔄 Refresh Data
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading && !overview" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        <p class="mt-4 text-gray-600">Loading dashboard...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-xl p-6 mb-8">
        <h3 class="text-red-800 font-semibold mb-2">⚠️ Error Loading Dashboard</h3>
        <p class="text-red-600 text-sm">{{ error }}</p>
        <button @click="refreshData" class="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">
          Try Again
        </button>
      </div>

      <!-- Dashboard Content -->
      <template v-else-if="overview">
        <!-- Top Metrics -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center hover:shadow-lg transition-shadow">
            <div class="text-2xl font-bold text-indigo-600">{{ formatNumber(usage?.usage_stats?.active_users_week || 0) }}</div>
            <div class="text-gray-700 mt-2">Active Users (Week)</div>
            <div class="text-xs text-gray-500 mt-1">
              {{ overview.active_users_today || 0 }} today
            </div>
          </div>
          <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center hover:shadow-lg transition-shadow">
            <div class="text-2xl font-bold text-yellow-500">{{ overview.open_queries || 0 }}</div>
            <div class="text-gray-700 mt-2">Open Queries</div>
            <div class="text-xs text-gray-500 mt-1">
              {{ overview.queries_today || 0 }} created today
            </div>
          </div>
          <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center hover:shadow-lg transition-shadow">
            <div class="text-2xl font-bold text-pink-600">{{ overview.total_queries || 0 }}</div>
            <div class="text-gray-700 mt-2">Total Queries</div>
            <div class="text-xs text-gray-500 mt-1">
              {{ overview.resolved_queries || 0 }} resolved
            </div>
          </div>
          <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center hover:shadow-lg transition-shadow">
            <div class="text-2xl font-bold text-green-700">
              {{ performance ? Math.round(performance.resolution_rate_percentage) : 0 }}%
            </div>
            <div class="text-gray-700 mt-2">Resolution Rate</div>
            <div class="text-xs text-gray-500 mt-1">
              Avg: {{ formatHours(overview.average_resolution_time_hours) }}
            </div>
          </div>
        </div>

        <!-- Main Analytics + Tables -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div class="lg:col-span-2 grid gap-8">
            <!-- Charts Section -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- FAQ Analytics -->
              <div class="bg-white rounded-lg shadow p-6">
                <h2 class="text-lg font-semibold text-indigo-700 mb-2">FAQ Analytics</h2>
                <div v-if="faqs && faqs.faqs.length > 0" class="space-y-2">
                  <div v-for="(faq, index) in faqs.faqs.slice(0, 5)" :key="index" class="text-sm">
                    <div class="flex justify-between items-center">
                      <span class="text-gray-700 truncate flex-1">{{ faq.question }}</span>
                      <span class="text-indigo-600 font-bold ml-2">{{ faq.count }}</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-1 mt-1">
                      <div
                        class="bg-indigo-600 h-1 rounded-full"
                        :style="{ width: (faq.count / faqs.faqs[0].count * 100) + '%' }"
                      ></div>
                    </div>
                  </div>
                </div>
                <p class="mt-3 text-gray-500 text-sm">Top-asked questions and frequency.</p>
              </div>

              <!-- Performance Metrics -->
              <div class="bg-white rounded-lg shadow p-6">
                <h2 class="text-lg font-semibold text-indigo-700 mb-2">Performance Metrics</h2>
                <div v-if="performance" class="space-y-3">
                  <div class="flex justify-between items-center">
                    <span class="text-gray-600 text-sm">With Responses</span>
                    <span class="text-green-600 font-bold">{{ performance.queries_with_responses }}</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-600 text-sm">Without Responses</span>
                    <span class="text-orange-600 font-bold">{{ performance.queries_without_responses }}</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-gray-600 text-sm">Avg Response Time</span>
                    <span class="text-blue-600 font-bold">{{ formatMinutes(performance.average_response_time_minutes) }}</span>
                  </div>
                </div>
                <p class="mt-3 text-gray-500 text-sm">Monitor response coverage and speed.</p>
              </div>
            </div>

            <!-- Recent Queries Table -->
            <div class="bg-white rounded-lg shadow p-6">
              <div class="flex items-center justify-between mb-4">
                <h2 class="text-lg font-semibold text-indigo-700">Top FAQs</h2>
                <span class="text-sm text-gray-600">Last 30 days</span>
              </div>
              <div v-if="faqs && faqs.faqs.length > 0" class="overflow-x-auto">
                <table class="min-w-full text-sm">
                  <thead>
                    <tr class="bg-indigo-100 text-gray-700">
                      <th class="p-2 font-semibold text-left">Question</th>
                      <th class="p-2 font-semibold">Category</th>
                      <th class="p-2 font-semibold">Count</th>
                      <th class="p-2 font-semibold">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(faq, index) in faqs.faqs.slice(0, 10)" :key="index" class="text-gray-700 border-b">
                      <td class="p-2">{{ faq.question }}</td>
                      <td class="p-2 text-center">
                        <span class="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">
                          {{ faq.category }}
                        </span>
                      </td>
                      <td class="p-2 text-center font-bold text-indigo-600">{{ faq.count }}</td>
                      <td class="p-2 text-center">
                        <span
                          :class="[
                            'px-2 py-1 rounded-full text-xs font-bold',
                            faq.status === 'OPEN'
                              ? 'bg-yellow-100 text-yellow-800'
                              : faq.status === 'IN_PROGRESS'
                                ? 'bg-blue-100 text-blue-700'
                                : 'bg-green-100 text-green-700'
                          ]"
                        >{{ faq.status }}</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="text-center py-8 text-gray-500">
                No FAQ data available
              </div>
            </div>

            <!-- User Statistics by Role -->
            <div class="bg-white rounded-lg shadow p-6">
              <div class="flex items-center justify-between mb-4">
                <h2 class="text-lg font-semibold text-indigo-700">Users by Role</h2>
                <span class="text-sm text-gray-600">Total: {{ overview.total_users || 0 }}</span>
              </div>
              <div v-if="usage && usage.users_by_role.length > 0" class="overflow-x-auto">
                <table class="min-w-full text-sm">
                  <thead>
                    <tr class="bg-gray-200 text-gray-700">
                      <th class="p-2 font-semibold text-left">Role</th>
                      <th class="p-2 font-semibold">Total Users</th>
                      <th class="p-2 font-semibold">Active (Week)</th>
                      <th class="p-2 font-semibold">Activity Rate</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="role in usage.users_by_role" :key="role.role" class="text-gray-700 border-b">
                      <td class="p-2 capitalize">
                        <span
                          :class="[
                            'px-2 py-1 rounded-full text-xs font-semibold',
                            role.role === 'student'
                              ? 'bg-indigo-100 text-indigo-700'
                              : role.role === 'ta'
                                ? 'bg-blue-100 text-blue-700'
                                : role.role === 'instructor'
                                  ? 'bg-green-100 text-green-700'
                                  : 'bg-purple-100 text-purple-700'
                          ]"
                        >{{ role.role }}</span>
                      </td>
                      <td class="p-2 text-center font-bold">{{ role.count }}</td>
                      <td class="p-2 text-center text-green-600 font-bold">{{ role.active_count }}</td>
                      <td class="p-2 text-center">
                        <span class="text-indigo-600 font-semibold">
                          {{ Math.round((role.active_count / role.count) * 100) }}%
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="text-center py-8 text-gray-500">
                No user data available
              </div>
            </div>
          </div>

          <!-- Quick Actions & Stats -->
          <div class="flex flex-col gap-8">
            <!-- Sentiment Analysis -->
            <div class="bg-white rounded-lg shadow p-6">
              <h2 class="text-lg font-semibold text-indigo-700 mb-4">Sentiment Analysis</h2>
              <div v-if="sentiment" class="space-y-3">
                <div class="text-center mb-4">
                  <div class="text-3xl font-bold text-indigo-600">
                    {{ sentiment.average_rating ? sentiment.average_rating.toFixed(1) : 'N/A' }}
                  </div>
                  <div class="text-xs text-gray-600">Average Rating</div>
                </div>
                <div>
                  <div class="flex justify-between text-xs mb-1">
                    <span class="text-gray-600">😊 Positive</span>
                    <span class="font-semibold text-green-600">{{ Math.round(sentiment.positive_percentage) }}%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-green-500 h-2 rounded-full" :style="{ width: sentiment.positive_percentage + '%' }"></div>
                  </div>
                </div>
                <div>
                  <div class="flex justify-between text-xs mb-1">
                    <span class="text-gray-600">😐 Neutral</span>
                    <span class="font-semibold text-gray-600">{{ Math.round(sentiment.neutral_percentage) }}%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-gray-400 h-2 rounded-full" :style="{ width: sentiment.neutral_percentage + '%' }"></div>
                  </div>
                </div>
                <div>
                  <div class="flex justify-between text-xs mb-1">
                    <span class="text-gray-600">😞 Negative</span>
                    <span class="font-semibold text-red-600">{{ Math.round(sentiment.negative_percentage) }}%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-red-500 h-2 rounded-full" :style="{ width: sentiment.negative_percentage + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Usage Statistics -->
            <div class="bg-white rounded-lg shadow p-6">
              <h2 class="text-lg font-semibold text-indigo-700 mb-4">Usage Statistics</h2>
              <div v-if="usage" class="space-y-3">
                <div class="flex justify-between items-center">
                  <span class="text-gray-600 text-sm">Active Today</span>
                  <span class="text-indigo-600 font-bold">{{ usage.usage_stats.active_users_today }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-600 text-sm">Active This Week</span>
                  <span class="text-indigo-600 font-bold">{{ usage.usage_stats.active_users_week }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-600 text-sm">Active This Month</span>
                  <span class="text-indigo-600 font-bold">{{ usage.usage_stats.active_users_month }}</span>
                </div>
                <div class="pt-2 border-t">
                  <div class="flex justify-between items-center">
                    <span class="text-gray-600 text-sm">Growth Rate</span>
                    <span class="text-green-600 font-bold">+{{ usage.usage_stats.user_growth_rate_percentage }}%</span>
                  </div>
                </div>
                <div class="pt-2 border-t">
                  <div class="flex justify-between items-center">
                    <span class="text-gray-600 text-sm">Peak Hour</span>
                    <span class="text-orange-600 font-bold">{{ usage.usage_stats.peak_usage_hour }}:00</span>
                  </div>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-600 text-sm">Chat Sessions</span>
                  <span class="text-purple-600 font-bold">{{ usage.usage_stats.total_chat_sessions }}</span>
                </div>
              </div>
            </div>

            <!-- Quick Actions -->
            <div class="bg-white rounded-lg shadow p-6">
              <h2 class="text-lg font-semibold text-indigo-700 mb-4">System Info</h2>
              <div class="space-y-2 text-sm text-gray-700">
                <div class="flex justify-between">
                  <span>Total Knowledge Sources</span>
                  <span class="font-bold">{{ overview.total_knowledge_sources || 0 }}</span>
                </div>
                <div class="flex justify-between">
                  <span>Total Responses</span>
                  <span class="font-bold">{{ overview.total_responses || 0 }}</span>
                </div>
                <div class="flex justify-between">
                  <span>Chat Sessions</span>
                  <span class="font-bold">{{ overview.total_chat_sessions || 0 }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>

      <!-- Footer -->
      <div class="h-8"></div>
      <div class="text-center text-gray-400 text-sm">
        &copy; 2025 Institute Admin Panel | Last updated: {{ lastUpdated }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { analyticsAPI } from '@/api'

// State
const overview = ref(null)
const faqs = ref(null)
const performance = ref(null)
const sentiment = ref(null)
const usage = ref(null)
const isLoading = ref(false)
const error = ref(null)
const lastUpdated = ref('')

// Load analytics data
const loadDashboardData = async () => {
  isLoading.value = true
  error.value = null

  try {
    const data = await analyticsAPI.getAllAnalytics({ faqLimit: 10, faqDays: 30 })

    overview.value = data.overview
    faqs.value = data.faqs
    performance.value = data.performance
    sentiment.value = data.sentiment
    usage.value = data.usage

    lastUpdated.value = new Date().toLocaleString()
  } catch (err) {
    console.error('Error loading dashboard:', err)
    error.value = err.response?.data?.detail || err.message || 'Failed to load dashboard data'
  } finally {
    isLoading.value = false
  }
}

const refreshData = () => {
  loadDashboardData()
}

// Helper functions
const formatNumber = (num) => {
  if (!num) return '0'
  return num.toLocaleString()
}

const formatHours = (hours) => {
  if (!hours) return 'N/A'
  return `${hours.toFixed(1)}h`
}

const formatMinutes = (minutes) => {
  if (!minutes) return 'N/A'
  return `${minutes.toFixed(0)}m`
}

// Lifecycle
onMounted(() => {
  loadDashboardData()
})
</script>

<style scoped>
/* Add any custom styles here */
</style>
