<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl p-8 text-white shadow-lg mb-8">
        <h1 class="text-3xl font-bold mb-2">Analytics Dashboard</h1>
        <p class="text-lg opacity-90">Comprehensive system metrics and insights</p>
        <div class="mt-4 flex items-center space-x-4 text-sm">
          <span>Last updated: {{ lastUpdated }}</span>
          <button
            @click="refreshAnalytics"
            :disabled="isLoading"
            class="px-4 py-2 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg transition-all disabled:opacity-50"
          >
            {{ isLoading ? 'Refreshing...' : 'Refresh Data' }}
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading && !overview" class="text-center py-20">
        <div class="inline-block animate-spin rounded-full h-16 w-16 border-b-2 border-indigo-600"></div>
        <p class="mt-4 text-gray-600">Loading analytics...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-xl p-6">
        <h3 class="text-red-800 font-semibold mb-2">Error Loading Analytics</h3>
        <p class="text-red-600 text-sm">{{ error }}</p>
        <button @click="refreshAnalytics" class="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700">
          Retry
        </button>
      </div>

      <!-- Analytics Content -->
      <template v-else-if="overview">
        <!-- Overview Metrics -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <MetricCard
            title="Total Users"
            :value="overview.total_users"
            :subtitle="`${overview.active_users_week} active this week`"
            icon="users"
            color="blue"
          />
          <MetricCard
            title="Total Queries"
            :value="overview.total_queries"
            :subtitle="`${overview.queries_today} created today`"
            icon="messages"
            color="green"
          />
          <MetricCard
            title="Open Queries"
            :value="overview.open_queries"
            :subtitle="`${overview.resolved_queries} resolved total`"
            icon="alert"
            color="yellow"
          />
          <MetricCard
            title="Avg Resolution Time"
            :value="formatHours(overview.average_resolution_time_hours)"
            subtitle="hours to resolve"
            icon="clock"
            color="purple"
          />
        </div>

        <!-- Performance & Sentiment Row -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <!-- Performance Metrics -->
          <div class="bg-white rounded-xl shadow-lg p-6">
            <h2 class="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <span class="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              Performance Metrics
            </h2>
            <div v-if="performance" class="space-y-4">
              <div class="flex justify-between items-center py-2 border-b">
                <span class="text-gray-600">Resolution Rate</span>
                <span class="text-2xl font-bold text-green-600">{{ performance.resolution_rate_percentage }}%</span>
              </div>
              <div class="flex justify-between items-center py-2 border-b">
                <span class="text-gray-600">Avg Response Time</span>
                <span class="text-xl font-semibold text-gray-900">
                  {{ formatMinutes(performance.average_response_time_minutes) }}
                </span>
              </div>
              <div class="flex justify-between items-center py-2 border-b">
                <span class="text-gray-600">Avg Resolution Time</span>
                <span class="text-xl font-semibold text-gray-900">
                  {{ formatHours(performance.average_resolution_time_hours) }}
                </span>
              </div>
              <div class="flex justify-between items-center py-2">
                <span class="text-gray-600">Queries with Responses</span>
                <span class="text-xl font-semibold text-gray-900">
                  {{ performance.queries_with_responses }} / {{ performance.queries_with_responses + performance.queries_without_responses }}
                </span>
              </div>
            </div>
          </div>

          <!-- Sentiment Analysis -->
          <div class="bg-white rounded-xl shadow-lg p-6">
            <h2 class="text-xl font-bold text-gray-900 mb-4 flex items-center">
              <span class="w-2 h-2 bg-purple-500 rounded-full mr-2"></span>
              Sentiment Analysis
            </h2>
            <div v-if="sentiment" class="space-y-4">
              <div class="text-center mb-4">
                <div class="text-4xl font-bold text-purple-600">{{ sentiment.average_rating || 'N/A' }}</div>
                <div class="text-sm text-gray-600">Average Rating (out of 5)</div>
              </div>
              <div class="space-y-3">
                <div>
                  <div class="flex justify-between text-sm mb-1">
                    <span class="text-gray-600">Positive</span>
                    <span class="font-semibold text-green-600">{{ sentiment.positive_percentage }}%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-green-500 h-2 rounded-full" :style="{ width: sentiment.positive_percentage + '%' }"></div>
                  </div>
                </div>
                <div>
                  <div class="flex justify-between text-sm mb-1">
                    <span class="text-gray-600">Neutral</span>
                    <span class="font-semibold text-gray-600">{{ sentiment.neutral_percentage }}%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-gray-400 h-2 rounded-full" :style="{ width: sentiment.neutral_percentage + '%' }"></div>
                  </div>
                </div>
                <div>
                  <div class="flex justify-between text-sm mb-1">
                    <span class="text-gray-600">Negative</span>
                    <span class="font-semibold text-red-600">{{ sentiment.negative_percentage }}%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-red-500 h-2 rounded-full" :style="{ width: sentiment.negative_percentage + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- FAQs Section -->
        <div class="bg-white rounded-xl shadow-lg p-6 mb-8">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-xl font-bold text-gray-900 flex items-center">
              <span class="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
              Frequently Asked Questions
            </h2>
            <div class="text-sm text-gray-600">
              Top {{ faqs?.faqs?.length || 0 }} of {{ faqs?.total_unique_questions || 0 }} unique questions
            </div>
          </div>
          <div v-if="faqs && faqs.faqs.length > 0" class="space-y-3">
            <div
              v-for="(faq, index) in faqs.faqs"
              :key="index"
              class="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center space-x-2 mb-1">
                    <span class="text-lg font-semibold text-gray-900">{{ faq.question }}</span>
                    <span class="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">{{ faq.category }}</span>
                  </div>
                  <div class="text-sm text-gray-600">
                    Asked {{ faq.count }} times • Last asked: {{ formatDate(faq.last_asked) }}
                  </div>
                </div>
                <div class="ml-4">
                  <span
                    class="px-3 py-1 rounded-full text-xs font-semibold"
                    :class="getStatusClass(faq.status)"
                  >
                    {{ faq.status }}
                  </span>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-8 text-gray-500">
            No FAQ data available
          </div>
        </div>

        <!-- Usage Statistics -->
        <div class="bg-white rounded-xl shadow-lg p-6">
          <h2 class="text-xl font-bold text-gray-900 mb-6 flex items-center">
            <span class="w-2 h-2 bg-orange-500 rounded-full mr-2"></span>
            Usage Statistics
          </h2>
          <div v-if="usage" class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Active Users -->
            <div class="space-y-4">
              <h3 class="font-semibold text-gray-700 text-sm uppercase tracking-wide">Active Users</h3>
              <div class="space-y-2">
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Today</span>
                  <span class="text-lg font-bold text-orange-600">{{ usage.usage_stats.active_users_today }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">This Week</span>
                  <span class="text-lg font-bold text-orange-600">{{ usage.usage_stats.active_users_week }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">This Month</span>
                  <span class="text-lg font-bold text-orange-600">{{ usage.usage_stats.active_users_month }}</span>
                </div>
                <div class="pt-2 border-t">
                  <div class="text-sm text-gray-600">Growth Rate</div>
                  <div class="text-xl font-bold text-green-600">
                    +{{ usage.usage_stats.user_growth_rate_percentage }}%
                  </div>
                </div>
              </div>
            </div>

            <!-- Session Stats -->
            <div class="space-y-4">
              <h3 class="font-semibold text-gray-700 text-sm uppercase tracking-wide">Sessions</h3>
              <div class="space-y-2">
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Total</span>
                  <span class="text-lg font-bold text-indigo-600">{{ usage.usage_stats.total_chat_sessions }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Today</span>
                  <span class="text-lg font-bold text-indigo-600">{{ usage.usage_stats.chat_sessions_today }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">This Week</span>
                  <span class="text-lg font-bold text-indigo-600">{{ usage.usage_stats.chat_sessions_week }}</span>
                </div>
                <div class="pt-2 border-t">
                  <div class="text-sm text-gray-600">Peak Hour</div>
                  <div class="text-xl font-bold text-indigo-600">
                    {{ usage.usage_stats.peak_usage_hour }}:00
                  </div>
                </div>
              </div>
            </div>

            <!-- Users by Role -->
            <div class="space-y-4">
              <h3 class="font-semibold text-gray-700 text-sm uppercase tracking-wide">Users by Role</h3>
              <div class="space-y-2">
                <div
                  v-for="role in usage.users_by_role"
                  :key="role.role"
                  class="flex justify-between items-center"
                >
                  <span class="text-gray-600 capitalize">{{ role.role }}</span>
                  <div class="text-right">
                    <span class="text-lg font-bold text-gray-900">{{ role.count }}</span>
                    <span class="text-sm text-gray-500 ml-2">({{ role.active_count }} active)</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { analyticsAPI } from '@/api'

// Metric Card Component (inline for simplicity)
const MetricCard = {
  props: ['title', 'value', 'subtitle', 'icon', 'color'],
  template: `
    <div class="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow">
      <div class="flex items-center justify-between mb-2">
        <div :class="'text-' + color + '-600'" class="text-3xl font-bold">{{ value || '0' }}</div>
      </div>
      <h3 class="text-gray-700 font-semibold text-sm">{{ title }}</h3>
      <p class="text-gray-500 text-xs mt-1">{{ subtitle }}</p>
    </div>
  `
}

// State
const overview = ref(null)
const faqs = ref(null)
const performance = ref(null)
const sentiment = ref(null)
const usage = ref(null)
const isLoading = ref(false)
const error = ref(null)
const lastUpdated = ref('')

// Methods
const loadAnalytics = async () => {
  isLoading.value = true
  error.value = null

  try {
    const data = await analyticsAPI.getAllAnalytics({ faqLimit: 10, faqDays: 30 })

    overview.value = data.overview
    faqs.value = data.faqs
    performance.value = data.performance
    sentiment.value = data.sentiment
    usage.value = data.usage

    lastUpdated.value = new Date().toLocaleTimeString()
  } catch (err) {
    console.error('Error loading analytics:', err)
    error.value = err.response?.data?.detail || err.message || 'Failed to load analytics data'
  } finally {
    isLoading.value = false
  }
}

const refreshAnalytics = () => {
  loadAnalytics()
}

const formatHours = (hours) => {
  if (!hours) return 'N/A'
  return `${hours.toFixed(1)}h`
}

const formatMinutes = (minutes) => {
  if (!minutes) return 'N/A'
  return `${minutes.toFixed(0)}m`
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

const getStatusClass = (status) => {
  const statusMap = {
    'OPEN': 'bg-yellow-100 text-yellow-700',
    'IN_PROGRESS': 'bg-blue-100 text-blue-700',
    'RESOLVED': 'bg-green-100 text-green-700',
    'CLOSED': 'bg-gray-100 text-gray-700'
  }
  return statusMap[status] || 'bg-gray-100 text-gray-700'
}

// Lifecycle
onMounted(() => {
  loadAnalytics()
})
</script>

<style scoped>
/* Add any custom styles here */
</style>
