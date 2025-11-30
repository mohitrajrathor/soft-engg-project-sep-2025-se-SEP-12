<template>
  <div class="flex min-h-screen bg-gray-50">
    <!-- Sidebar Navigation -->
    <instructorSideBar />

    <!-- Main Content -->
    <div class="flex-1 flex flex-col ml-[250px] pt-9 px-6 pb-8 min-h-screen" :style="{ background: 'var(--page-bg)' }">
      <!-- Welcome/Header -->
      <div class="w-full bg-gradient-to-r from-indigo-600 to-purple-600 rounded-b-2xl shadow px-8 py-7 mb-8">
        <h2 class="text-3xl sm:text-4xl font-extrabold text-white mb-1">Welcome back, Instructor! </h2>
        <p class="text-lg text-indigo-100">Here’s an overview of what’s happening in your courses today.</p>
      </div>

      <!-- Dashboard Main Grid -->
      <div class="flex-1 px-6 pb-8">
        <div class="grid lg:grid-cols-4 gap-8">
          <!-- Main Left: 3 columns -->
          <div class="lg:col-span-3 flex flex-col gap-8">
            <!-- Top Row: Chart & Heatmap -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
              <!-- Chart -->
              <div class="rounded-2xl shadow border p-6 flex flex-col" :style="{ background: 'var(--color-bg-card)', borderColor: 'var(--color-border)' }">
                <div class="flex items-center justify-between mb-3">
                  <h3 class="font-semibold text-xl text-gray-900">Student Engagement Over Time</h3>
                  <button class="text-blue-700 font-medium hover:underline transition">View Details</button>
                </div>
                <div class="flex-1 flex items-center justify-center bg-blue-50/70 rounded-xl text-gray-400 py-5">
                  
                </div>
                <EngagementLineChart />
              </div>
              <!-- Heatmap -->
              <div class="rounded-2xl shadow border p-6" :style="{ background: 'var(--color-bg-card)', borderColor: 'var(--color-border)' }">
                <div class="flex items-center justify-between mb-3">
                  <h3 class="font-semibold text-xl text-gray-900">Assignment Performance Heatmap</h3>
                  <button class="text-blue-700 font-medium hover:underline transition">View All Assignments</button>
                </div>
                <table class="w-full text-xs md:text-sm mt-2">
                  <thead>
                    <tr>
                      <th class="py-1 pr-2 text-left font-semibold">Student</th>
                      <th v-for="n in 5" :key="n" class="px-1 font-medium">A{{ n }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(student, idx) in performance" :key="student.name" :class="idx % 2 === 1 ? 'bg-gray-50' : ''">
                      <td class="pr-2 font-medium">{{ student.name }}</td>
                      <td v-for="s in student.scores" :key="s" class="text-center px-1">{{ s }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Bottom Row: Deadlines & Quiz Scores -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
              <!-- Deadlines -->
              <div class="rounded-2xl shadow border p-6 flex flex-col" :style="{ background: 'var(--color-bg-card)', borderColor: 'var(--color-border)' }">
                <div class="flex items-center justify-between mb-3">
                  <h3 class="font-semibold text-lg text-gray-900">Upcoming & Missed Deadlines</h3>
                  <button class="text-blue-700 font-medium hover:underline text-xs transition">Review All Deadlines</button>
                </div>
                <div class="space-y-2">
                  <div
                    v-for="item in deadlines"
                    :key="item.name"
                    class="flex items-center bg-gray-50 rounded-lg px-4 py-3 hover:bg-blue-50 transition"
                  >
                    <div class="flex-1">
                      <div class="font-medium text-gray-900">{{ item.name }}</div>
                      <div class="text-xs text-gray-500">{{ item.date }}</div>
                    </div>
                    <span
                      class="ml-3 px-2 py-1 rounded text-xs font-semibold"
                      :class="item.status === 'Overdue' ? 'bg-red-100 text-red-600' : 'bg-blue-100 text-blue-700'"
                      >{{ item.status }}</span
                    >
                  </div>
                </div>
              </div>
              <!-- Quiz Score Bar -->
              <div class="rounded-2xl shadow border p-6 flex flex-col" :style="{ background: 'var(--color-bg-card)', borderColor: 'var(--color-border)' }">
                <div class="flex items-center justify-between mb-3">
                  <h3 class="font-semibold text-lg text-gray-900">Quiz Score Distribution</h3>
                  <button class="text-blue-700 font-medium hover:underline text-xs transition">Analyze Scores</button>
                </div>
                <div class="h-48 flex items-end justify-between gap-4 mt-4 pb-4">
                  <div
                    v-for="bucket in quizBuckets"
                    :key="bucket.label"
                    class="flex flex-col items-center w-1/5 group transition"
                  >
                    <div
                      :class="['rounded-t-md', bucket.active ? 'bg-blue-600' : 'bg-gray-300']"
                      :style="{ height: `${bucket.height}px`, minHeight: '8px', width: '32px' }"
                      class="transition-all duration-300"
                    ></div>
                    <div class="text-xs mt-2 text-gray-700">{{ bucket.label }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Sidebar: Actions + Top Students -->
          <div class="flex flex-col gap-8 w-full max-w-xs mx-auto lg:mx-0">
            <!-- Quick Actions -->
            <div class="rounded-2xl shadow border p-6" :style="{ background: 'var(--color-bg-card)', borderColor: 'var(--color-border)' }">
              <h4 class="font-bold text-lg text-gray-900 mb-4">Quick Actions</h4>
              <ul class="space-y-3">
                <li v-for="action in quickActions" :key="action.label">
                  <button
                    class="w-full flex items-center gap-2 px-4 py-2 text-blue-700 bg-blue-50 hover:bg-blue-600 hover:text-white focus:bg-blue-600 focus:text-white rounded-lg font-semibold transition-all shadow"
                  >
                    <component :is="action.icon" class="w-5 h-5" />
                    {{ action.label }}
                  </button>
                </li>
              </ul>
            </div>
            <!-- Top Students -->
            <div class="rounded-2xl shadow border p-6" :style="{ background: 'var(--color-bg-card)', borderColor: 'var(--color-border)' }">
              <div class="flex items-center justify-between mb-2">
                <h4 class="font-bold text-gray-900 text-lg">Top Performing Students</h4>
                <button class="text-blue-700 hover:underline text-xs font-semibold">View All Students</button>
              </div>
              <div class="space-y-2">
                <div
                  v-for="student in topStudents"
                  :key="student.name"
                  class="flex items-center justify-between py-1"
                >
                  <span class="font-medium text-gray-700">{{ student.name }}</span>
                  <span class="bg-blue-50 px-2 py-0.5 rounded text-xs text-blue-700 font-bold shadow"
                    >Score: {{ student.score }}</span
                  >
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import instructorSideBar from '@/components/layout/instructorLayout/instructorSideBar.vue'
import { ref } from 'vue'
import { FileText, BarChart2, Users, PlusCircle } from 'lucide-vue-next'
import EngagementLineChart from '@/components/instructor/EngagementLineChart.vue'


// Dummy Data
const performance = ref([
  { name: 'Alice Smith', scores: [92, 88, 75, 98, 80] },
  { name: 'Bob Johnson', scores: [70, 85, 80, 70, 60] },
  { name: 'Carol White', scores: [85, 88, 80, 91, 91] },
  { name: 'David Green', scores: [55, 68, 50, 62, 62] },
  { name: 'Eve Black', scores: [95, 90, 90, 90, 97] }
]);

const deadlines = ref([
  { name: "Project Proposal", date: "Oct 28, 2024", status: "Overdue" },
  { name: "Mid-term Exam", date: "Nov 15, 2024", status: "Upcoming" },
  { name: "Research Paper Draft", date: "Nov 20, 2024", status: "Upcoming" },
  { name: "Final Project Submission", date: "Dec 05, 2024", status: "Upcoming" },
  { name: "Course Feedback", date: "Dec 10, 2024", status: "Upcoming" }
]);

const quizBuckets = ref([
  { label: "0-40%", height: 20 },
  { label: "41-60%", height: 60 },
  { label: "61-80%", height: 110, active: true },
  { label: "81-100%", height: 70 }
]);

const quickActions = ref([
  { label: "Generate Progress Report", icon: BarChart2 },
  { label: "Export Student Data", icon: FileText },
  { label: "View Student Overview", icon: Users },
  { label: "Create New Assignment", icon: PlusCircle },
]);

const topStudents = ref([
  { name: "Riya Sharma", score: 98 },
  { name: "Ananya Singh", score: 96 },
  { name: "Vikram Patel", score: 95 },
  { name: "Priya Mehta", score: 93 },
  { name: "Siddharth Rao", score: 92 }
]);
</script>

<style scoped>
/* All stylings match your themed dashboard—rounded, shadow, soft blues, font-bold headline, etc */
</style>
