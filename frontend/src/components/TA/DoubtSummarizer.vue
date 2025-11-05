<script setup>
import { ref, onMounted } from 'vue'
import TASidebar from '@/components/layout/TaLayout/TASideBar.vue'
import { 
  ArrowDownTrayIcon, 
  ChatBubbleLeftRightIcon, 
  ExclamationTriangleIcon, 
  EnvelopeIcon, 
  ClipboardDocumentListIcon, 
  DocumentTextIcon 
} from '@heroicons/vue/24/outline'

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
    <!-- Sidebar -->
    <TASidebar class="fixed top-0 left-0 h-screen w-[250px]" />

    <!-- Main Layout -->
    <main class="flex-1 flex flex-col min-h-screen ml-[250px] bg-gray-50">
      <!-- Header -->
      <header class="bg-white shadow-sm px-8 py-5 flex items-center justify-between">
        <h1 class="text-2xl font-extrabold text-black">TA Doubt Summarizer</h1>
        <button @click="exportSummary" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center font-semibold shadow-sm transition-colors">
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
            <div class="bg-white rounded-2xl shadow-2xl p-5 border border-gray-200">
              <p class="text-sm font-medium text-gray-500 mb-1">Total Queries</p>
              <p class="text-3xl font-bold text-black">{{ summaryStats.totalQueries }}</p>
              <p class="text-xs text-green-600 mt-1 font-semibold">up {{ summaryStats.percentageChange }}% from last week</p>
            </div>
            <div class="bg-white rounded-2xl shadow-2xl p-5 border border-gray-200">
              <p class="text-sm font-medium text-gray-500 mb-1">Topic Clusters</p>
              <p class="text-3xl font-bold text-black">{{ summaryStats.topicClusters }}</p>
              <p class="text-xs text-gray-500 mt-1">Major confusion areas</p>
            </div>
            <div class="bg-white rounded-2xl shadow-2xl p-5 border border-gray-200">
              <p class="text-sm font-medium text-gray-500 mb-1">Recurring Doubts</p>
              <p class="text-3xl font-bold text-black">{{ summaryStats.recurringDoubts }}</p>
              <p class="text-xs text-orange-600 mt-1 font-semibold">Need attention</p>
            </div>
            <div class="bg-white rounded-2xl shadow-2xl p-5 border border-gray-200">
              <p class="text-sm font-medium text-gray-500 mb-1">Learning Gaps</p>
              <p class="text-3xl font-bold text-black">{{ summaryStats.learningGaps }}</p>
              <p class="text-xs text-red-600 mt-1 font-semibold">Critical issues</p>
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
        <aside class="w-[320px] flex flex-col gap-6">
          <!-- Summary Statistics -->
          <div class="bg-white rounded-2xl shadow-2xl p-5 border border-gray-200">
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
              <div class="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                <span class="text-gray-700 text-sm font-medium">Recurring Issues</span>
                <span class="bg-blue-600 text-white px-3 py-1 rounded-full font-bold text-sm">{{ summaryStats.recurringDoubts }}</span>
              </div>
              <div class="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                <span class="text-gray-700 text-sm font-medium">Learning Gaps</span>
                <span class="bg-blue-600 text-white px-3 py-1 rounded-full font-bold text-sm">{{ summaryStats.learningGaps }}</span>
              </div>
            </div>
          </div>

          <!-- Export Options -->
          <div class="bg-white rounded-2xl shadow-2xl p-5 border border-gray-200">
            <div class="font-bold mb-4 text-base text-black">Export Options</div>
            <button class="w-full mb-2 px-4 py-3 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700 shadow-sm">
              <DocumentTextIcon class="w-5 h-5 inline mr-2" />
              Export as PDF
            </button>
            <button class="w-full mb-2 px-4 py-3 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700 shadow-sm">
              <ClipboardDocumentListIcon class="w-5 h-5 inline mr-2" />
              Export as CSV
            </button>
            <button class="w-full px-4 py-3 rounded-lg bg-blue-600 text-white font-semibold hover:bg-blue-700 shadow-sm">
              <EnvelopeIcon class="w-5 h-5 inline mr-2" />
              Email Report
            </button>
          </div>

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