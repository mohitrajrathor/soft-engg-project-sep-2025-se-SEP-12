<script setup>
import InstructorSidebar from '@/components/layout/instructorLayout/instructorSideBar.vue'
import { ref } from 'vue'

// Example data for charts and tables
const engagementData = ref([140, 180, 210, 190, 220, 260, 280])
const deadlines = ref([
  { title: "Project Proposal", date: "Oct 28, 2024", status: "Overdue" },
  { title: "Mid-term Exam", date: "Nov 15, 2024", status: "Upcoming" },
  { title: "Research Paper Draft", date: "Nov 20, 2024", status: "Upcoming" },
  { title: "Final Project Submission", date: "Dec 05, 2024", status: "Upcoming" },
  { title: "Course Feedback", date: "Dec 10, 2024", status: "Upcoming" }
])
const students = ref([
  { name: "Alice Smith", scores: [92, 88, 75, 95, 80] },
  { name: "Bob Johnson", scores: [70, 65, 78, 82, 73] },
  { name: "Carol White", scores: [85, 90, 88, 70, 91] },
  { name: "David Green", scores: [55, 50, 68, 60, 62] },
  { name: "Eve Black", scores: [98, 95, 90, 99, 97] }
])
const topStudents = ref([
  { name: "Riya Sharma", score: 98 },
  { name: "Ananya Singh", score: 96 },
  { name: "Vikram Patel", score: 95 },
  { name: "Priya Mehta", score: 93 },
  { name: "Siddharth Rao", score: 92 }
])
</script>

<template>
  <div class="flex min-h-screen bg-white">
    <!-- Sidebar -->
    <InstructorSidebar class="fixed top-0 left-0 h-screen w-[250px]" />

    <!-- Main content -->
    <main class="flex-1 ml-[250px] p-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800">Instructor Dashboard</h1>
        <input
          type="text"
          placeholder="Search instructor dashboard..."
          class="border border-gray-300 rounded-lg px-4 py-2 w-80 focus:ring-2 focus:ring-blue-400 focus:outline-none"
        />
      </div>

      <!-- Dashboard Grid -->
      <div class="grid grid-cols-12 gap-6">
        <!-- Student Engagement -->
        <div class="col-span-8 bg-white rounded-2xl shadow p-6 border border-gray-100">
          <div class="flex justify-between items-center mb-4">
            <h2 class="font-semibold text-gray-700">Student Engagement Over Time</h2>
            <a href="#" class="text-sm text-blue-600 hover:underline">View Details</a>
          </div>
          <div class="h-40 flex items-end gap-2">
            <div
              v-for="(val, i) in engagementData"
              :key="i"
              class="flex-1 bg-blue-400 rounded-t-lg"
              :style="{ height: val / 3 + 'px' }"
            ></div>
          </div>
        </div>

        <!-- Assignment Heatmap -->
        <div class="col-span-4 bg-white rounded-2xl shadow p-6 border border-gray-100">
          <div class="flex justify-between items-center mb-4">
            <h2 class="font-semibold text-gray-700">Assignment Performance Heatmap</h2>
            <a href="#" class="text-sm text-blue-600 hover:underline">View All Assignments</a>
          </div>
          <table class="w-full text-sm">
            <thead>
              <tr class="text-left text-gray-500 border-b">
                <th class="py-1">Student</th>
                <th v-for="n in 5" :key="n" class="py-1 text-center">A{{ n }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in students" :key="student.name" class="border-b hover:bg-gray-50">
                <td class="py-1">{{ student.name }}</td>
                <td v-for="(score, i) in student.scores" :key="i" class="py-1 text-center">
                  {{ score }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Upcoming & Missed Deadlines -->
        <div class="col-span-6 bg-white rounded-2xl shadow p-6 border border-gray-100">
          <div class="flex justify-between items-center mb-4">
            <h2 class="font-semibold text-gray-700">Upcoming & Missed Deadlines</h2>
            <a href="#" class="text-sm text-blue-600 hover:underline">Review All Deadlines</a>
          </div>
          <div class="space-y-3">
            <div
              v-for="(item, i) in deadlines"
              :key="i"
              class="flex justify-between items-center border-b pb-2"
            >
              <div>
                <div class="font-medium text-gray-800">{{ item.title }}</div>
                <div class="text-xs text-gray-500">{{ item.date }}</div>
              </div>
              <span
                class="text-xs font-semibold px-2 py-1 rounded-full"
                :class="item.status === 'Overdue'
                  ? 'bg-red-200 text-red-700'
                  : 'bg-blue-200 text-blue-700'"
              >
                {{ item.status }}
              </span>
            </div>
          </div>
        </div>

        <!-- Quiz Score Distribution -->
        <div class="col-span-6 bg-white rounded-2xl shadow p-6 border border-gray-100">
          <div class="flex justify-between items-center mb-4">
            <h2 class="font-semibold text-gray-700">Quiz Score Distribution</h2>
            <a href="#" class="text-sm text-blue-600 hover:underline">Analyze Scores</a>
          </div>
          <div class="h-40 flex items-end justify-between">
            <div
              v-for="(height, i) in [15, 30, 60, 50]"
              :key="i"
              class="w-1/5 bg-yellow-400 rounded-t-lg"
              :style="{ height: height + 'px' }"
            ></div>
          </div>
          <div class="flex justify-between text-xs text-gray-500 mt-2">
            <span>0–40%</span><span>41–60%</span><span>61–80%</span><span>81–100%</span>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="col-span-4 bg-white rounded-2xl shadow p-6 border border-gray-100">
          <h2 class="font-semibold mb-3 text-gray-700">Quick Actions</h2>
          <div class="flex flex-col gap-2">
            <button class="py-2 border border-gray-300 rounded-lg hover:bg-blue-50 transition">Generate Progress Report</button>
            <button class="py-2 border border-gray-300 rounded-lg hover:bg-blue-50 transition">Export Student Data</button>
            <button class="py-2 border border-gray-300 rounded-lg hover:bg-blue-50 transition">View Student Overview</button>
            <button class="py-2 border border-gray-300 rounded-lg hover:bg-blue-50 transition">Create New Assignment</button>
          </div>
        </div>

        <!-- Top Performing Students -->
        <div class="col-span-4 bg-white rounded-2xl shadow p-6 border border-gray-100">
          <div class="flex justify-between items-center mb-3">
            <h2 class="font-semibold text-gray-700">Top Performing Students</h2>
            <a href="#" class="text-sm text-blue-600 hover:underline">View All</a>
          </div>
          <div class="space-y-2">
            <div
              v-for="(stu, i) in topStudents"
              :key="i"
              class="flex justify-between items-center border-b pb-1"
            >
              <span>{{ stu.name }}</span>
              <span class="text-xs bg-green-200 text-green-800 rounded-full px-2 py-0.5 font-semibold">
                Score: {{ stu.score }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
table {
  border-collapse: collapse;
}
</style>
