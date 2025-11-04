<script setup>
import { ref, onMounted } from 'vue'
import TASidebar from '@/components/layout/TaLayout/TASideBar.vue'
import { FunnelIcon, ArrowDownTrayIcon, ChatBubbleLeftRightIcon, ExclamationTriangleIcon, EnvelopeIcon, ClipboardDocumentListIcon, DocumentTextIcon } from '@heroicons/vue/24/outline'

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

// === MOCK API CALL ===
const fetchSummary = async () => {
  // Real endpoint: POST /api/doubt-summarizer
  console.log('Fetching AI-powered doubt summary...')
}
onMounted(fetchSummary)

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
    <!-- Sidebar (from teammates) -->
    <TASidebar class="fixed top-0 left-0 h-screen w-[250px]"/>

    <!-- Main Layout -->
    <main class="flex-1 flex flex-col min-h-screen ml-[250px] bg-gray-50">
      <!-- Header -->
      <header class="bg-white shadow-sm px-8 py-5 flex items-center justify-between">
        <h1 class="text-2xl font-extrabold text-black">TA Doubt Summarizer</h1>
        <button @click="exportSummary" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-800 flex items-center font-semibold shadow-sm transition-colors">
          <ArrowDownTrayIcon class="w-5 h-5 mr-2" />
          Export Summary
        </button>
      </header>

      <!-- Content Area -->
      <div class="flex-1 p-8 gap-6 flex">
        <!-- Main Panel -->
        <div class="flex-1 space-y-6">
          <!-- Filter Controls -->
          <div class="bg-white rounded-2xl shadow-2xl p-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Summary Period</label>
                <div class="flex space-x-2">
                  <button
                    v-for="period in ['daily', 'weekly', 'monthly']"
                    :key="period"
                    @click="selectedPeriod = period"
                    :class="[
                      'flex-1 px-4 py-2 rounded-lg text-sm font-semibold transition-colors',
                      selectedPeriod === period
                        ? 'bg-blue-600 text-white shadow-sm'
                        : 'bg-blue-50 text-blue-700 hover:bg-blue-100'
                    ]"
                  >
                    {{ period.charAt(0).toUpperCase() + period.slice(1) }}
                  </button>
                </div>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Source</label>
                <select
                  v-model="selectedSource"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 bg-blue-50"
                >
                  <option value="all">All Sources</option>
                  <option value="forum">Forum Posts</option>
                  <option value="email">Emails</option>
                  <option value="chat">Chat Logs</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Course</label>
                <select
                  v-model="selectedCourse"
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 bg-blue-50"
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
            <div class="bg-white rounded-2xl shadow-2xl p-5">
              <p class="text-sm font-medium text-gray-500 mb-1">Total Queries</p>
              <p class="text-3xl font-bold text-black">{{ summaryStats.totalQueries }}</p>
              <p class="text-xs text-green-600 mt-1 font-semibold">↑ {{ summaryStats.percentageChange }}% from last week</p>
            </div>
            <div class="bg-white rounded-2xl shadow-2xl p-5">
              <p class="text-sm font-medium text-gray-500 mb-1">Topic Clusters</p>
              <p class="text-3xl font-bold text-black">{{ summaryStats.topicClusters }}</p>
              <p class="text-xs text-gray-500 mt-1">Major confusion areas</p>
            </div>
            <div class="bg-white rounded-2xl shadow-2xl p-5">
              <p class="text-sm font-medium text-gray-500 mb-1">Recurring Doubts</p>
              <p class="text-3xl font-bold text-black">{{ summaryStats.recurringDoubts }}</p>
              <p class="text-xs text-orange-600 mt-1 font-semibold">Need attention</p>
            </div>
            <div class="bg-white rounded-2xl shadow-2xl p-5">
              <p class="text-sm font-medium text-gray-500 mb-1">Learning Gaps</p>
              <p class="text-3xl font-bold text-black">{{ summaryStats.learningGaps }}</p>
              <p class="text-xs text-red-600 mt-1 font-semibold">Critical issues</p>
            </div>
          </div>

          <!-- AI Summary Brief -->
          <div class="bg-gradient-to-r from-blue-100 to-purple-100 border-2 border-blue-300 rounded-2xl p-6 shadow-2xl">
            <div class="flex items-start">
              <div class="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center mr-4 flex-shrink-0">
                <ChatBubbleLeftRightIcon class="text-white w-6 h-6" />
              </div>
              <div class="flex-1">
                <h4 class="font-bold text-black mb-2 text-lg">AI Summary Brief (Oct 24 - Oct 31, 2024)</h4>
                <p class="text-sm text-gray-800 mb-3">
                  This week, <strong>{{ summaryStats.totalQueries }} student queries</strong> were received across your assigned courses. 
                  The AI has identified <strong>{{ summaryStats.topicClusters }} major topic clusters</strong> with 
                  <strong>{{ doubtSummary.topicClusters[0].topic }}</strong> being the most challenging 
                  ({{ doubtSummary.topicClusters[0].count }} queries). There's a significant increase in questions about 
                  Factory Pattern implementation and Abstract Classes. <strong>{{ summaryStats.recurringDoubts }} recurring doubts</strong> 
                  suggest students need additional clarification on these concepts. Forum activity is up 
                  <strong>{{ summaryStats.percentageChange }}%</strong> compared to last week.
                </p>
                <div class="flex items-center space-x-4 text-sm">
                  <span class="text-blue-700 font-semibold">Detailed insights below</span>
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
                class="border-2 border-gray-200 rounded-xl p-5 hover:shadow-lg transition-shadow bg-blue-50"
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
                      <strong>{{ cluster.count }} queries</strong> identified from forum posts, emails, and chat logs
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
                  <button @click="viewAllQueries(cluster)" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-800 text-sm font-semibold shadow-sm">
                    View All {{ cluster.count }} Queries
                  </button>
                  <button @click="generateResponseTemplate(cluster)" class="px-4 py-2 border-2 border-blue-600 text-blue-700 rounded-lg hover:bg-blue-50 text-sm font-semibold">
                    Generate Response Template
                  </button>
                  <button @click="markAsAddressed(cluster)" class="px-4 py-2 border-2 border-gray-300 text-gray-700 rounded-lg hover:bg-gray-100 text-sm font-semibold">
                    Mark as Addressed
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
              These issues appear repeatedly across multiple students, indicating fundamental learning gaps
            </p>
            <div class="space-y-3">
              <div
                v-for="(item, index) in doubtSummary.commonIssues"
                :key="index"
                class="p-4 bg-orange-50 border-2 border-orange-300 rounded-lg"
              >
                <div class="flex items-start justify-between">
                  <div class="flex items-start flex-1">
                    <span class="flex items-center justify-center w-7 h-7 bg-orange-600 text-white rounded-full text-sm font-bold mr-3">
                      {{ index + 1 }}
                    </span>
                    <div class="flex-1">
                      <p class="font-bold text-black">{{ item.issue }}</p>
                      <p class="text-sm text-gray-700 mt-1">
                        Mentioned by <strong>{{ item.students }} students</strong> across forum and emails
                      </p>
                    </div>
                  </div>
                  <button @click="createFAQ(item.issue)" class="ml-4 px-4 py-2 bg-orange-600 text-white rounded-lg text-sm hover:bg-orange-700 font-semibold shadow-sm">
                    Create FAQ
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Source Breakdown -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="bg-white rounded-2xl shadow-2xl p-5">
              <div class="flex items-center justify-between mb-3">
                <h5 class="font-bold text-black">Forum Posts</h5>
                <ChatBubbleLeftRightIcon class="text-blue-600 w-6 h-6" />
              </div>
              <p class="text-3xl font-bold text-black mb-1">{{ doubtSummary.sourceBreakdown.forum.count }}</p>
              <p class="text-sm text-gray-600">{{ doubtSummary.sourceBreakdown.forum.percentage }}% of total queries</p>
            </div>
            <div class="bg-white rounded-2xl shadow-2xl p-5">
              <div class="flex items-center justify-between mb-3">
                <h5 class="font-bold text-black">Emails</h5>
                <EnvelopeIcon class="text-green-600 w-6 h-6" />
              </div>
              <p class="text-3xl font-bold text-black mb-1">{{ doubtSummary.sourceBreakdown.email.count }}</p>
              <p class="text-sm text-gray-600">{{ doubtSummary.sourceBreakdown.email.percentage }}% of total queries</p>
            </div>
            <div class="bg-white rounded-2xl shadow-2xl p-5">
              <div class="flex items-center justify-between mb-3">
                <h5 class="font-bold text-black">Chat Logs</h5>
                <ChatBubbleLeftRightIcon class="text-purple-600 w-6 h-6" />
              </div>
              <p class="text-3xl font-bold text-black mb-1">{{ doubtSummary.sourceBreakdown.chat.count }}</p>
              <p class="text-sm text-gray-600">{{ doubtSummary.sourceBreakdown.chat.percentage }}% of total queries</p>
            </div>
          </div>

          <!-- Quick Actions -->
          <div classeaf class="bg-white rounded-2xl shadow-2xl p-6">
            <h4 class="font-bold text-black mb-4 text-lg">Quick Actions</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <button @click="sendToInstructor" class="px-5 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-800 font-semibold text-left shadow-sm">
                Send Summary to Instructor
              </button>
              <button @click="createOfficeHoursAgenda" class="px-5 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 font-semibold text-left shadow-sm">
                Create Office Hours Agenda
              </button>
              <button @click="generateWeeklyReport" class="px-5 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 font-semibold text-left shadow-sm">
                Generate Weekly Report (PDF)
              </button>
              <button @click="getAIResponseSuggestions" class="px-5 py-3 bg-orange-600 text-white rounded-lg hover:bg-orange-700 font-semibold text-left shadow-sm">
                Get AI Response Suggestions
              </button>
            </div>
          </div>
        </div>

        <!-- Right Side Panel -->
        <aside class="w-[320px] flex flex-col gap-6">
          <!-- Summary Statistics -->
          <div class="bg-white rounded-2xl shadow-2xl p-5">
            <div class="font-bold mb-4 text-base text-black">Summary Statistics</div>
            <div class="space-y-3">
              <div class="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                <span class="text-gray-700 text-sm font-medium">Total Queries</span>
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

          <!-- Export Options -->
          <div class="bg-white rounded-2xl shadow-2xl p-5">
            <div class="font-bold mb-4 text-base text-black">Export Options</div>
            <button class="w-full mb-2 px-4 py-3 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-800 shadow-sm">
              <DocumentTextIcon class="w-5 h-5 inline mr-2" />
              Export as PDF
            </button>
            <button class="w-full mb-2 px-4 py-3 rounded-lg bg-blue-50 text-blue-700 font-medium border-2 border-blue-200 hover:bg-blue-100">
              <ClipboardDocumentListIcon class="w-5 h-5 inline mr-2" />
              Export as CSV
            </button>
            <button class="w-full px-4 py-3 rounded-lg bg-blue-50 text-blue-700 font-medium border-2 border-blue-200 hover:bg-blue-100">
              <EnvelopeIcon class="w-5 h-5 inline mr-2" />
              Email Report
            </button>
          </div>

          <!-- AI Insights -->
          <div class="bg-gradient-to-br from-purple-100 to-blue-100 rounded-2xl shadow-2xl p-5 border-2 border-purple-300">
            <div class="font-bold mb-3 text-base text-black">AI Insights</div>
            <p class="text-sm text-gray-800 mb-3">
              Design Patterns queries have increased by 40% this week. Consider scheduling a special session.
            </p>
            <button class="w-full px-4 py-2 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700 text-sm shadow-sm">
              Get More Insights
            </button>
          </div>
        </aside>
      </div>
    </main>
  </div>
</template>