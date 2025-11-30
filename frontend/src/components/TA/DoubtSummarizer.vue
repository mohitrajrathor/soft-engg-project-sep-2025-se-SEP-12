<script setup>
import { ref, onMounted, watch } from 'vue'
import TASidebar from '@/components/layout/TaLayout/TASideBar.vue'
import doubtsAPI from '@/api/doubts'
import ExportOptions from '@/components/shared/ExportOptions.vue'
import { 
  ArrowDownTrayIcon, 
  ChatBubbleLeftRightIcon, 
  ExclamationTriangleIcon, 
  EnvelopeIcon, 
  ClipboardDocumentListIcon, 
  DocumentTextIcon 
} from '@heroicons/vue/24/outline'

// === STATE ===
const isLoading = ref(false)
const error = ref(null)

// === FILTERS ===
const selectedPeriod = ref('weekly')
const selectedSource = ref('all')
const selectedCourse = ref('all')

// === SUMMARY STATS ===
const summaryStats = ref({
  totalQueries: 45,
  topicClusters: 3,
  recurringDoubts: 18,
  learningGaps: 5,
  percentageChange: 12
})

// === FULL DOUBT SUMMARY ===
const doubtSummary = ref({
  topicClusters: [
    {
      topic: 'Design Patterns',
      count: 12,
      trend: 'up',
      samples: [
        'How to implement Factory Pattern in Java?',
        'Difference between Factory and Abstract Factory?',
        'When should I use which design pattern?'
      ]
    },
    {
      topic: 'Neural Networks',
      count: 8,
      trend: 'stable',
      samples: [
        'Why is my neural network not converging?',
        'How to choose the right activation function?',
        'Batch size impact on training?'
      ]
    },
    {
      topic: 'Database Queries',
      count: 6,
      trend: 'down',
      samples: [
        'Explain JOIN operations with examples',
        'How to optimize SQL queries?',
        'Difference between WHERE and HAVING?'
      ]
    }
  ],
  commonIssues: [
    { issue: 'Implementation of Factory Pattern', students: 8 },
    { issue: 'Training convergence problems', students: 6 },
    { issue: 'SQL JOIN operations', students: 5 }
  ],
  sourceBreakdown: {
    forum: { count: 28, percentage: 62 },
    email: { count: 12, percentage: 27 },
    chat: { count: 5, percentage: 11 }
  }
})

// === DATA FETCH ===
const normalizeTrend = (t) => {
  const v = (t || '').toString().toLowerCase()
  if (v.startsWith('inc')) return 'up'
  if (v.startsWith('dec')) return 'down'
  return 'stable'
}

const fetchSummary = async () => {
  const courseCode = selectedCourse.value === 'all' ? 'CS101' : selectedCourse.value
  isLoading.value = true
  error.value = null

  try {
    const params = { period: selectedPeriod.value, source: selectedSource.value === 'all' ? null : selectedSource.value }
    
    // Fetch summary and source breakdown in parallel
    const [res, breakdownRes] = await Promise.all([
      doubtsAPI.getSummary(courseCode, params),
      doubtsAPI.getSourceBreakdown(courseCode, { period: selectedPeriod.value })
    ])

    // Map backend -> UI
    const topics = Array.isArray(res.topics) ? res.topics : []
    const learningGaps = Array.isArray(res.learning_gaps) ? res.learning_gaps : []
    const stats = res.stats || {}

    // Build summary stats from backend computed values
    summaryStats.value = {
      totalQueries: stats.total_messages || breakdownRes.total || 0,
      topicClusters: stats.topic_clusters || topics.length,
      recurringDoubts: stats.recurring_issues || 0,  // Now using proper recurring issues count
      learningGaps: stats.learning_gaps || learningGaps.length,
      percentageChange: 0 // TODO: compute from historical data
    }

    doubtSummary.value = {
      topicClusters: topics.map(t => ({
        topic: t.label || 'Unknown',
        count: t.count || 0,
        trend: normalizeTrend(t.trend),
        samples: t.sample_questions || []
      })),
      commonIssues: learningGaps.map(g => ({
        issue: g.issue_title || 'Unlabeled Gap',
        students: g.student_count || 0
      })),
      // Use real source breakdown from backend (prefer summary response, fallback to breakdown endpoint)
      sourceBreakdown: {
        forum: res.source_breakdown?.forum || breakdownRes.breakdown?.forum || { count: 0, percentage: 0 },
        email: res.source_breakdown?.email || breakdownRes.breakdown?.email || { count: 0, percentage: 0 },
        chat: res.source_breakdown?.chat || breakdownRes.breakdown?.chat || { count: 0, percentage: 0 }
      }
    }
  } catch (e) {
    console.error('Failed to load doubt summary', e)
    error.value = e.response?.data?.detail || e.message || 'Failed to load summary. Please try again.'
  } finally {
    isLoading.value = false
  }
}
onMounted(fetchSummary)

// Debounced watch to avoid rapid API calls during filter changes
let debounceTimer = null
watch([selectedPeriod, selectedSource, selectedCourse], () => {
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(fetchSummary, 300) // 300ms debounce
})

// === ACTION HANDLERS ===
const exportSummary = () => alert('Exporting summary as PDF...')
const viewAllQueries = (cluster) => alert(`Viewing all ${cluster.count} queries for ${cluster.topic}`)
const generateResponseTemplate = (cluster) => alert(`Generating AI response template for ${cluster.topic}...`)
const markAsAddressed = (cluster) => alert(`Marked ${cluster.topic} as addressed`)
const createFAQ = (issue) => alert(`Creating FAQ entry for: ${issue}`)
const sendToInstructor = () => alert('Sending summary email to instructor...')
const createOfficeHoursAgenda = () => alert('Creating office hours agenda based on doubts...')
const generateWeeklyReport = () => alert('Generating weekly PDF report...')
const getAIResponseSuggestions = () => alert('Getting AI-powered response suggestions...')

// === HELPER FUNCTIONS ===
const getTrendColor = (trend) => {
  if (trend === 'up') return 'bg-red-500 animate-pulse'
  if (trend === 'down') return 'bg-green-500'
  return 'bg-yellow-500'
}
const getTrendBadgeColor = (trend) => {
  if (trend === 'up') return 'bg-red-100 text-red-700'
  if (trend === 'down') return 'bg-green-100 text-green-700'
  return 'bg-yellow-100 text-yellow-700'
}
const getTrendText = (trend) => {
  if (trend === 'up') return 'Increasing'
  if (trend === 'down') return 'Decreasing'
  return 'Stable'
}
</script>

<template>
  <div class="flex min-h-screen bg-[#f8fafc]">
    <!-- Sidebar -->
    <TASidebar class="fixed top-0 left-0 h-screen w-[250px]" />

    <!-- Main Layout -->
    <main class="flex-1 flex flex-col min-h-screen ml-[250px] bg-gray-50">
      <!-- Header -->
      <header class="bg-white shadow-sm px-8 py-3 flex items-center justify-between">
        <h1 class="text-2xl font-extrabold text-black">TA Doubt Summarizer</h1>
        <button @click="exportSummary" class="px-4 py-2 bg-gray-100 text-black rounded-lg hover:bg-gray-200 flex items-center font-semibold shadow-sm transition-colors border border-gray-300">
          <ArrowDownTrayIcon class="w-5 h-5 mr-2" />
          Export Summary
        </button>
      </header>

      <!-- Content Area -->
      <div class="flex-1 p-8 gap-6 flex">
        <!-- Error State (full overlay) -->
        <div v-if="error && !isLoading" class="flex-1 flex items-center justify-center">
          <div class="bg-red-50 border-2 border-red-200 rounded-2xl p-8 max-w-md text-center">
            <ExclamationTriangleIcon class="w-16 h-16 text-red-500 mx-auto mb-4" />
            <h3 class="text-xl font-bold text-red-800 mb-2">Error Loading Summary</h3>
            <p class="text-red-600 mb-4">{{ error }}</p>
            <button @click="fetchSummary" class="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 font-semibold shadow-sm">
              Try Again
            </button>
          </div>
        </div>

        <!-- Main Panel (with loading overlay) -->
        <div class="flex-1 space-y-6 relative transition-opacity duration-300" :class="{ 'opacity-60 pointer-events-none': isLoading }">
          <!-- Loading Indicator (small, non-intrusive) -->
          <div v-if="isLoading" class="absolute top-0 left-0 right-0 z-10 flex justify-center">
            <div class="bg-blue-600 text-white px-6 py-3 rounded-b-xl shadow-lg flex items-center gap-3 animate-pulse">
              <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span class="font-semibold">Updating summary...</span>
            </div>
          </div>
          <!-- Filter Controls -->
          <div class="bg-white rounded-2xl shadow-2xl p-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-x-6 gap-y-6">
              <!-- Summary Period (Dropdown) -->
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Summary Period</label>
                <select
                  v-model="selectedPeriod"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 bg-white"
                >
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
              </div>

              <!-- Source -->
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Source</label>
                <select
                  v-model="selectedSource"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 bg-white"
                >
                  <option value="all">All Sources</option>
                  <option value="forum">Forum Posts</option>
                  <option value="email">Emails</option>
                  <option value="chat">Chat Logs</option>
                </select>
              </div>

              <!-- Course -->
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Course</label>
                <select
                  v-model="selectedCourse"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 bg-white"
                >
                  <option value="all">All Courses</option>
                  <option value="bscs3001">BSCS3001 - Software Engineering</option>
                  <option value="bscs3003">BSCS3003 - Machine Learning</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Summary Stats Cards -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <!-- Most Active Channel -->
            <div class="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl shadow-2xl p-5 border border-blue-200">
              <div class="flex items-center justify-between mb-2">
                <p class="text-sm font-semibold text-blue-900">Most Active Channel</p>
                <ChatBubbleLeftRightIcon class="w-5 h-5 text-blue-600" />
              </div>
              <p class="text-2xl font-bold text-blue-900 mb-1">
                {{ Object.entries(doubtSummary.sourceBreakdown).sort((a, b) => b[1].count - a[1].count)[0][0].charAt(0).toUpperCase() + Object.entries(doubtSummary.sourceBreakdown).sort((a, b) => b[1].count - a[1].count)[0][0].slice(1) }}
              </p>
              <p class="text-xs text-blue-700">{{ Object.entries(doubtSummary.sourceBreakdown).sort((a, b) => b[1].count - a[1].count)[0][1].percentage }}% of all queries</p>
            </div>
            
            <!-- Top Concern -->
            <div class="bg-gradient-to-br from-orange-50 to-orange-100 rounded-2xl shadow-2xl p-5 border border-orange-200">
              <div class="flex items-center justify-between mb-2">
                <p class="text-sm font-semibold text-orange-900">Top Concern</p>
                <ExclamationTriangleIcon class="w-5 h-5 text-orange-600" />
              </div>
              <p class="text-2xl font-bold text-orange-900 mb-1 truncate" :title="doubtSummary.topicClusters[0]?.topic">
                {{ doubtSummary.topicClusters[0]?.topic || 'N/A' }}
              </p>
              <p class="text-xs text-orange-700">{{ doubtSummary.topicClusters[0]?.count || 0 }} queries this period</p>
            </div>
            
            <!-- Response Time Target -->
            <div class="bg-gradient-to-br from-green-50 to-green-100 rounded-2xl shadow-2xl p-5 border border-green-200">
              <div class="flex items-center justify-between mb-2">
                <p class="text-sm font-semibold text-green-900">Avg Response Time</p>
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <p class="text-2xl font-bold text-green-900 mb-1">< 2 hrs</p>
              <p class="text-xs text-green-700">Within SLA targets</p>
            </div>
            
            <!-- Trend Indicator -->
            <div class="bg-gradient-to-br from-purple-50 to-purple-100 rounded-2xl shadow-2xl p-5 border border-purple-200">
              <div class="flex items-center justify-between mb-2">
                <p class="text-sm font-semibold text-purple-900">Activity Trend</p>
                <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
              <p class="text-2xl font-bold text-purple-900 mb-1">
                {{ summaryStats.percentageChange > 0 ? '+' : '' }}{{ summaryStats.percentageChange }}%
              </p>
              <p class="text-xs text-purple-700">vs previous period</p>
            </div>
          </div>

          <!-- AI Summary Brief -->
          <div class="bg-white rounded-2xl shadow-2xl p-6 border border-gray-200">
            <div class="flex items-start">
              <div class="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center mr-4 flex-shrink-0">
                <ChatBubbleLeftRightIcon class="text-white w-6 h-6" />
              </div>
              <div class="flex-1">
                <h4 class="font-bold text-black mb-2 text-lg">AI Summary Brief (Oct 24 - Oct 31, 2024)</h4>
                <p class="text-sm text-gray-800 mb-3">
                  This week, <strong>{{ summaryStats.totalQueries }} student queries</strong> were received. 
                  The AI identified <strong>{{ summaryStats.topicClusters }} major clusters</strong>, with 
                  <strong>{{ doubtSummary.topicClusters[0].topic }}</strong> leading at 
                  {{ doubtSummary.topicClusters[0].count }} queries. Forum activity up 
                  <strong>{{ summaryStats.percentageChange }}%</strong>.
                </p>
                <div class="flex items-center space-x-4 text-sm">
                  <span class="text-gray-700 font-semibold">Detailed insights below</span>
                  <span class="text-gray-500">•</span>
                  <span class="text-gray-600">Generated by AI on Nov 4, 2024</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Topic Clustering Analysis -->
          <div class="bg-white rounded-2xl shadow-2xl p-6">
            <h4 class="text-xl font-bold text-black mb-4">Topic Clustering Analysis</h4>
            <div class="space-y-4">
              <div
                v-for="(cluster, index) in doubtSummary.topicClusters"
                :key="index"
                class="border border-gray-200 rounded-xl p-5 hover:shadow-lg transition-shadow bg-gray-50"
              >
                <div class="flex items-start justify-between mb-3">
                  <div class="flex-1">
                    <div class="flex items-center mb-2">
                      <div :class="['w-3 h-3 rounded-full mr-3', getTrendColor(cluster.trend)]"></div>
                      <h5 class="font-bold text-black text-lg">{{ cluster.topic }}</h5>
                      <span :class="['ml-3 px-3 py-1 rounded-full text-xs font-bold', getTrendBadgeColor(cluster.trend)]">
                        {{ getTrendText(cluster.trend) }}
                      </span>
                    </div>
                    <p class="text-sm text-gray-700 mb-2">
                      <strong>{{ cluster.count }} queries</strong> from forum, email, and chat
                    </p>
                    
                    <!-- Sample Queries -->
                    <div class="mt-3 p-4 bg-white rounded-lg border border-gray-200">
                      <p class="text-xs font-bold text-gray-700 mb-2">Sample Queries:</p>
                      <ul class="text-xs text-gray-600 space-y-1">
                        <li v-for="(sample, idx) in cluster.samples" :key="idx">• {{ sample }}</li>
                      </ul>
                    </div>
                  </div>
                </div>
                
                <div class="flex flex-wrap gap-2 mt-4">
                  <button @click="viewAllQueries(cluster)" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-semibold shadow-sm">
                    View All {{ cluster.count }} Queries
                  </button>
                  <button @click="generateResponseTemplate(cluster)" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-semibold shadow-sm">
                    Generate Template
                  </button>
                  <button @click="markAsAddressed(cluster)" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-semibold shadow-sm">
                    Mark Addressed
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Recurring Doubts & Learning Gaps -->
          <div class="bg-white rounded-2xl shadow-2xl p-6">
            <h4 class="text-xl font-bold text-black mb-2 flex items-center">
              <ExclamationTriangleIcon class="w-6 h-6 text-orange-600 mr-2" />
              Recurring Doubts & Learning Gaps
            </h4>
            <p class="text-sm text-gray-600 mb-4">
              Repeated issues across multiple students
            </p>
            <div class="space-y-3">
              <div
                v-for="(item, index) in doubtSummary.commonIssues"
                :key="index"
                class="p-4 bg-gray-50 border border-gray-200 rounded-lg"
              >
                <div class="flex items-start justify-between">
                  <div class="flex items-start flex-1">
                    <span class="flex items-center justify-center w-7 h-7 bg-blue-600 text-white rounded-full text-sm font-bold mr-3">
                      {{ index + 1 }}
                    </span>
                    <div class="flex-1">
                      <p class="font-bold text-black">{{ item.issue }}</p>
                      <p class="text-sm text-gray-700 mt-1">
                        Mentioned by <strong>{{ item.students }} students</strong>
                      </p>
                    </div>
                  </div>
                  <button @click="createFAQ(item.issue)" class="ml-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-semibold shadow-sm">
                    Create FAQ
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Source Breakdown -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="bg-white rounded-2xl shadow-2xl p-5 border border-gray-200">
              <div class="flex items-center justify-between mb-3">
                <h5 class="font-bold text-black">Forum Posts</h5>
                <ChatBubbleLeftRightIcon class="text-blue-600 w-6 h-6" />
              </div>
              <p class="text-3xl font-bold text-black mb-1">{{ doubtSummary.sourceBreakdown.forum.count }}</p>
              <p class="text-sm text-gray-600">{{ doubtSummary.sourceBreakdown.forum.percentage }}% of total</p>
            </div>
            <div class="bg-white rounded-2xl shadow-2xl p-5 border border-gray-200">
              <div class="flex items-center justify-between mb-3">
                <h5 class="font-bold text-black">Emails</h5>
                <EnvelopeIcon class="text-blue-600 w-6 h-6" />
              </div>
              <p class="text-3xl font-bold text-black mb-1">{{ doubtSummary.sourceBreakdown.email.count }}</p>
              <p class="text-sm text-gray-600">{{ doubtSummary.sourceBreakdown.email.percentage }}% of total</p>
            </div>
            <div class="bg-white rounded-2xl shadow-2xl p-5 border border-gray-200">
              <div class="flex items-center justify-between mb-3">
                <h5 class="font-bold text-black">Chat Logs</h5>
                <ChatBubbleLeftRightIcon class="text-blue-600 w-6 h-6" />
              </div>
              <p class="text-3xl font-bold text-black mb-1">{{ doubtSummary.sourceBreakdown.chat.count }}</p>
              <p class="text-sm text-gray-600">{{ doubtSummary.sourceBreakdown.chat.percentage }}% of total</p>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="bg-white rounded-2xl shadow-2xl p-6">
            <h4 class="font-bold text-black mb-4 text-lg">Quick Actions</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <button @click="sendToInstructor" class="px-5 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold text-left shadow-sm">
                Send to Instructor
              </button>
              <button @click="createOfficeHoursAgenda" class="px-5 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold text-left shadow-sm">
                Create Office Hours Agenda
              </button>
              <button @click="generateWeeklyReport" class="px-5 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold text-left shadow-sm">
                Generate Weekly Report
              </button>
              <button @click="getAIResponseSuggestions" class="px-5 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold text-left shadow-sm">
                AI Response Suggestions
              </button>
            </div>
          </div>
        </div>

        <!-- Right Side Panel -->
        <aside class="w-[320px] flex flex-col gap-6 relative transition-opacity duration-300" :class="{ 'opacity-60 pointer-events-none': isLoading }">
          <!-- Summary Statistics -->
          <div class="bg-white rounded-2xl shadow-2xl p-5 border border-gray-200">
            <div class="font-bold mb-4 text-base text-black">Summary Statistics</div>
            <div class="space-y-3">
              <div class="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                <span class="text-gray-700 text-sm font-medium">Total Messages</span>
                <span class="bg-blue-600 text-white px-3 py-1 rounded-full font-bold text-sm">{{ summaryStats.totalQueries }}</span>
              </div>
              <div class="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                <span class="text-gray-700 text-sm font-medium">Topics Identified</span>
                <span class="bg-blue-600 text-white px-3 py-1 rounded-full font-bold text-sm">{{ summaryStats.topicClusters }}</span>
              </div>
              <div class="flex justify-between items-center p-3 bg-orange-50 rounded-lg">
                <span class="text-gray-700 text-sm font-medium">Recurring Issues</span>
                <span class="bg-orange-600 text-white px-3 py-1 rounded-full font-bold text-sm">{{ summaryStats.recurringDoubts }}</span>
              </div>
              <div class="flex justify-between items-center p-3 bg-red-50 rounded-lg">
                <span class="text-gray-700 text-sm font-medium">Learning Gaps</span>
                <span class="bg-red-600 text-white px-3 py-1 rounded-full font-bold text-sm">{{ summaryStats.learningGaps }}</span>
              </div>
            </div>
          </div>

          <!-- Export Options Component -->
          <ExportOptions 
            :course-code="selectedCourse === 'all' ? 'CS101' : selectedCourse"
            :period="selectedPeriod"
            :source="selectedSource"
          />

          <!-- AI Insights -->
          <div class="bg-white rounded-2xl shadow-2xl p-5 border border-gray-200">
            <div class="font-bold mb-3 text-base text-black">AI Insights</div>
            <p class="text-sm text-gray-800 mb-3">
              Design Patterns queries up 40%. Consider a special session.
            </p>
            <button class="w-full px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 text-sm shadow-sm">
              Get More Insights
            </button>
          </div>
        </aside>
      </div>
    </main>
  </div>
</template>