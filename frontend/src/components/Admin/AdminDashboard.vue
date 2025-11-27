<template>
  <div class="min-h-screen bg-gray-100 py-10 px-4">
    <div class="max-w-6xl mx-auto">
      <!-- Banner -->
      <div class="rounded-xl bg-gradient-to-r from-indigo-500 to-indigo-700 text-white p-8 mb-8 shadow">
        <h1 class="text-3xl font-bold mb-2">Welcome back, Admin! </h1>
        <div class="text-lg">Here's a birds-eye view of your institution for today.</div>
      </div>

      <!-- Top Metrics -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center">
          <div class="text-2xl font-bold text-indigo-600">1,276</div>
          <div class="text-gray-700 mt-2">Active Users</div>
        </div>
        <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center">
          <div class="text-2xl font-bold text-yellow-500">86</div>
          <div class="text-gray-700 mt-2">Open Queries</div>
        </div>
        <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center">
          <div class="text-2xl font-bold text-pink-600">19</div>
          <div class="text-gray-700 mt-2">Flagged Issues</div>
        </div>
        <div class="bg-white rounded-lg shadow p-6 flex flex-col items-center">
          <div class="text-2xl font-bold text-green-700">99%</div>
          <div class="text-gray-700 mt-2">System Health</div>
        </div>
      </div>

      <!-- Main Analytics + Tables -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 grid gap-8">
          <!-- Charts Section -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-white rounded-lg shadow p-6">
              <h2 class="text-lg font-semibold text-indigo-700 mb-2">FAQ Analytics</h2>
              <FAQAnalyticsChart />
              <p class="mt-3 text-gray-500 text-sm">Top-asked questions and answer accuracy.</p>
            </div>
            <div class="bg-white rounded-lg shadow p-6">
              <h2 class="text-lg font-semibold text-indigo-700 mb-2">Unresolved Queries</h2>
              <UnresolvedQueriesChart />
              <p class="mt-3 text-gray-500 text-sm">Monitor backlog and escalation rate.</p>
            </div>
          </div>
          <!-- Institutional Queries Table -->
          <div class="bg-white rounded-lg shadow p-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-semibold text-indigo-700">Recent Institutional Queries</h2>
              <button class="bg-indigo-500 text-white px-4 py-1 rounded hover:bg-indigo-600 text-sm">Export</button>
            </div>
            <div class="overflow-x-auto">
              <table class="min-w-full text-sm">
                <thead>
                  <tr class="bg-indigo-100 text-gray-700">
                    <th class="p-2 font-semibold">ID</th>
                    <th class="p-2 font-semibold">Topic</th>
                    <th class="p-2 font-semibold">Role</th>
                    <th class="p-2 font-semibold">Date</th>
                    <th class="p-2 font-semibold">Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="row in sampleQueries" :key="row.id" class="text-gray-700">
                    <td class="p-2">{{ row.id }}</td>
                    <td class="p-2">{{ row.topic }}</td>
                    <td class="p-2">{{ row.role }}</td>
                    <td class="p-2">{{ row.date }}</td>
                    <td class="p-2">
                      <span
                        :class="[
                          'px-2 py-1 rounded-full text-xs font-bold',
                          row.status === 'Pending'
                            ? 'bg-yellow-100 text-yellow-800'
                            : row.status === 'Escalated'
                              ? 'bg-pink-100 text-pink-700'
                              : 'bg-green-100 text-green-700'
                        ]"
                      >{{ row.status }}</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- User Management Table -->
          <div class="bg-white rounded-lg shadow p-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-semibold text-indigo-700">User Management</h2>
              <button class="bg-indigo-500 text-white px-4 py-1 rounded hover:bg-indigo-600 text-sm">Bulk Approve</button>
            </div>
            <div class="overflow-x-auto">
              <table class="min-w-full text-sm">
                <thead>
                  <tr class="bg-gray-200 text-gray-700">
                    <th class="p-2 font-semibold">User</th>
                    <th class="p-2 font-semibold">Email</th>
                    <th class="p-2 font-semibold">Role</th>
                    <th class="p-2 font-semibold">Status</th>
                    <th class="p-2 font-semibold">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="user in users" :key="user.email" class="text-gray-700">
                    <td class="p-2 flex items-center gap-2">
                      <img :src="user.avatar" alt="Avatar" class="w-7 h-7 rounded-full border" />
                      <span>{{ user.name }}</span>
                    </td>
                    <td class="p-2">{{ user.email }}</td>
                    <td class="p-2">
                      <span
                        :class="[
                          'px-2 py-1 rounded-full text-xs',
                          user.role === 'TA'
                            ? 'bg-blue-100 text-blue-700'
                            : user.role === 'Instructor'
                              ? 'bg-green-100 text-green-700'
                              : 'bg-indigo-100 text-indigo-700'
                        ]"
                      >{{ user.role }}</span>
                    </td>
                    <td class="p-2">
                      <span
                        :class="[
                          'px-2 py-1 rounded-full text-xs font-bold',
                          user.status === 'Pending'
                            ? 'bg-yellow-100 text-yellow-800'
                            : user.status === 'Blocked'
                              ? 'bg-pink-100 text-pink-700'
                              : 'bg-green-100 text-green-700'
                        ]"
                      >{{ user.status }}</span>
                    </td>
                    <td class="p-2">
                      <button class="bg-green-400 text-white rounded px-2 py-1 mr-1 text-xs hover:bg-green-500" v-if="user.status === 'Pending'">Approve</button>
                      <button class="bg-yellow-400 text-white rounded px-2 py-1 mr-1 text-xs hover:bg-yellow-500" v-if="user.status !== 'Blocked'">Block</button>
                      <button class="bg-pink-500 text-white rounded px-2 py-1 text-xs hover:bg-pink-600">Flag</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Quick Actions & Announcements -->
        <div class="flex flex-col gap-8">
          <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-lg font-semibold text-indigo-700 mb-4">Quick Actions</h2>
            <button class="w-full py-2 mb-2 bg-indigo-500 text-white rounded hover:bg-indigo-600">Send Announcement</button>
            <button class="w-full py-2 mb-2 bg-indigo-500 text-white rounded hover:bg-indigo-600">Export Reports</button>
            <button class="w-full py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600">Manage Roles</button>
          </div>
          <div class="bg-white rounded-lg shadow p-6">
            <h2 class="text-lg font-semibold text-indigo-700 mb-2">Recent System Announcements</h2>
            <ul class="text-gray-700 list-disc pl-6 text-sm">
              <li>Resource HUB update added for 'Advanced AI'</li>
              <li>New feature: AI Query Summarizer is now live!</li>
              <li>Scheduled Maintenance: Every Sunday, 12 AM – 2 AM</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="h-8"></div>
      <div class="text-center text-gray-400 text-sm">
        &copy; 2025 Institute Admin Panel
      </div>
    </div>
  </div>
</template>

<script setup>
import FAQAnalyticsChart from '@/components/Admin/FAQAnalyticsChart.vue'
import UnresolvedQueriesChart from '@/components/Admin/UnresolvedQueriesChart.vue'

const sampleQueries = [
  { id: 3012, topic: 'Exam Dates Change', role: 'Student', date: '2025-11-03', status: 'Pending' },
  { id: 1989, topic: 'Resource Access Issue', role: 'Instructor', date: '2025-11-02', status: 'Resolved' },
  { id: 2244, topic: 'Duplicate Queries', role: 'TA', date: '2025-11-01', status: 'Escalated' },
  { id: 2967, topic: 'Policy Suggestion', role: 'Student', date: '2025-11-01', status: 'Pending' }
]

const users = [
  { name: 'Jane Doe', email: 'jane@iitm.ac.in', role: 'TA', status: 'Pending', avatar: 'https://randomuser.me/api/portraits/women/1.jpg' },
  { name: 'Dr. S. Kalra', email: 'kalra@iitm.ac.in', role: 'Instructor', status: 'Active', avatar: 'https://randomuser.me/api/portraits/men/10.jpg' },
  { name: 'Ankur Sharma', email: 'ankur@iitm.ac.in', role: 'Student', status: 'Blocked', avatar: 'https://randomuser.me/api/portraits/men/12.jpg' },
  { name: 'Priya Mehta', email: 'priya@iitm.ac.in', role: 'Student', status: 'Active', avatar: 'https://randomuser.me/api/portraits/women/4.jpg' }
]
</script>
