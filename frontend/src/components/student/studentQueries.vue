<script setup>
import { ref } from 'vue'
import Sidebar from '@/components/layout/StudentLayout/SideBar.vue'
import HeaderBar from '@/components/layout/StudentLayout/HeaderBar.vue'
import BottomBar from '@/components/layout/StudentLayout/BottomBar.vue'
import {
  MagnifyingGlassIcon,
  PlusCircleIcon,
  CheckCircleIcon,
  AcademicCapIcon,
  ChatBubbleLeftRightIcon,
  UserCircleIcon,
  PaperClipIcon,
  CubeIcon,
} from "@heroicons/vue/24/outline"

// State for message and file
const message = ref('')
const attachedFile = ref(null)
const fileInput = ref(null)

const triggerFilePicker = () => fileInput.value.click()

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) attachedFile.value = file
}

const removeAttachment = () => {
  attachedFile.value = null
  fileInput.value.value = ''
}

const sendMessage = () => {
  if (message.value.trim() === '' && !attachedFile.value) return
  console.log('Message sent:', message.value)
  if (attachedFile.value) console.log('Attached file:', attachedFile.value)
  message.value = ''
  removeAttachment()
}
</script>

<template>
  <div class="flex h-screen overflow-hidden">
    <!-- Sidebar -->
    <Sidebar class="sticky top-0 h-screen flex-shrink-0" />

    <!-- Main Content -->
    <div class="flex-1 flex flex-col bg-gray-50 ml-[250px]">
      <!-- Header -->
      <HeaderBar class="sticky top-0 z-50" searchPlaceholder="Search courses, threads, resources" />

      <!-- Page content -->
      <div class="flex-1 overflow-y-auto p-6 pb-28"> <!-- extra bottom padding for BottomBar -->
        <!-- Top Filter Bar -->
        <div class="flex items-center justify-between gap-6 mb-6">
          <div class="flex gap-3">
            <button class="rounded-[18px] px-6 py-2 text-base font-semibold text-blue-700 bg-white border-2 border-blue-500 shadow hover:bg-blue-50 transition">
              Search My Queries
            </button>
            <button class="rounded-[18px] px-6 py-2 text-base text-gray-700 bg-white border-2 border-gray-200 hover:bg-gray-100 transition">
              All
            </button>
            <button class="rounded-[18px] px-6 py-2 text-base font-semibold text-blue-700 bg-blue-100 border-2 border-blue-500 shadow-inner">
              Open
            </button>
            <button class="rounded-[18px] px-6 py-2 text-base text-gray-700 bg-white border-2 border-gray-200 hover:bg-gray-100 transition">
              Resolved
            </button>
          </div>

          <router-link
            to="/student/new-query"
            class="flex items-center gap-2 px-5 py-2 rounded-[18px] bg-blue-600 text-white font-semibold shadow hover:bg-blue-700 transition text-base"
          >
            <PlusCircleIcon class="w-6 h-6" /> New Query
          </router-link>
        </div>

        <!-- Grid Layout -->
        <div class="grid grid-cols-12 gap-6">
          <!-- Left: Recent Queries -->
          <aside class="col-span-3 overflow-y-auto max-h-[calc(100vh-160px)] pr-1">
            <div class="font-bold mb-3 text-lg">
              Recent queries
              <span class="text-xs text-gray-400 ml-1">7 this month</span>
            </div>
            <div class="space-y-3">
              <div class="bg-white rounded-2xl px-4 py-3 shadow border hover:shadow-md cursor-pointer transition">
                <div class="font-semibold leading-tight">Help with Dijkstra complexity</div>
                <div class="flex items-center gap-1 text-xs text-gray-500 mt-1 mb-1">
                  <CubeIcon class="w-4 h-4" /> CS 301 · 2h ago
                  <span class="ml-auto rounded-lg bg-blue-50 text-blue-700 px-2 py-0.5">Open</span>
                </div>
                <div class="text-xs text-gray-400 line-clamp-2">
                  I implemented the algorithm but still see O(n²)...
                </div>
              </div>

              <div class="bg-white rounded-2xl px-4 py-3 shadow border hover:shadow-md cursor-pointer transition">
                <div class="font-semibold leading-tight">Systems lab Docker error</div>
                <div class="flex items-center gap-1 text-xs text-gray-500 mt-1 mb-1">
                  <CubeIcon class="w-4 h-4" /> CS 210 · Yesterday
                  <span class="ml-auto rounded-lg bg-green-50 text-green-700 px-2 py-0.5">Resolved</span>
                </div>
                <div class="text-xs text-gray-400 line-clamp-2">
                  Docker build fails on ARM machine...
                </div>
              </div>

              <div class="bg-white rounded-2xl px-4 py-3 shadow border hover:shadow-md cursor-pointer transition">
                <div class="font-semibold leading-tight">Office hour booking confirmation</div>
                <div class="flex items-center gap-1 text-xs text-gray-500 mt-1 mb-1">
                  <CubeIcon class="w-4 h-4" /> HOST · 1d ago
                  <span class="ml-auto rounded-lg bg-blue-50 text-blue-700 px-2 py-0.5">Open</span>
                </div>
                <div class="text-xs text-gray-400 line-clamp-2">
                  Want to confirm the location for Friday...
                </div>
              </div>
            </div>
          </aside>

          <!-- Center: Main Thread -->
          <section class="col-span-5 flex flex-col relative bg-white rounded-2xl shadow-lg border overflow-hidden">
            <!-- Scrollable Conversation -->
            <div class="flex-1 overflow-y-auto p-7">
              <div class="flex items-center gap-2 text-xs text-gray-500 mb-3">
                <CubeIcon class="w-5 h-5 text-blue-400" /> <span class="font-semibold">CS 301</span>
                <span class="mx-2 rounded-lg px-2 py-0.5 bg-slate-100 text-gray-700">Algorithms</span>
                <span class="rounded-lg px-2 py-0.5 bg-slate-100 text-gray-700">Share</span>
                <span class="ml-auto rounded-lg px-2 py-0.5 bg-green-100 text-green-700 flex items-center gap-1 cursor-pointer hover:bg-green-200">
                  <CheckCircleIcon class="w-4 h-4" /> Mark Resolved
                </span>
              </div>

              <div class="font-black text-xl mb-1">Dijkstra complexity on dense graphs</div>
              <div class="text-xs text-gray-400 mb-3">
                Created 2h ago · Query ID: <span class="font-mono">Q-87314</span>
              </div>

              <!-- Messages -->
              <div class="space-y-5">
                <!-- User -->
                <div class="flex items-start gap-4 mb-1">
                  <UserCircleIcon class="w-7 h-7 text-blue-600" />
                  <div>
                    <span class="font-semibold text-blue-900 flex items-center gap-2">
                      You <span class="rounded-md px-2 py-0.5 bg-blue-50 text-blue-700 text-xs">Open</span>
                    </span>
                    <div class="text-base">
                      I used adjacency matrix + binary heap and got O(n²). Is this expected for dense graphs?
                    </div>
                    <div class="text-xs text-gray-400 mt-0.5">45 min ago</div>
                  </div>
                </div>

                <!-- AI -->
                <div class="flex items-start gap-4 mb-1 bg-blue-50 rounded-xl p-4">
                  <ChatBubbleLeftRightIcon class="w-7 h-7 text-blue-500" />
                  <div>
                    <span class="font-semibold text-blue-700">AI Assistant</span>
                    <div class="text-base">
                      Yes. With an adjacency matrix the edge scans dominate at O(n²)... Use adjacency lists; on dense
                      graphs, a Fibonacci heap won’t help asymptotically versus array/heap implementations.
                    </div>
                    <div class="text-xs text-gray-400 mt-0.5">45 min ago</div>
                  </div>
                </div>

                <!-- TA -->
                <div class="flex items-start gap-4 mb-1">
                  <AcademicCapIcon class="w-7 h-7 text-green-500" />
                  <div>
                    <span class="font-semibold text-green-700">TA Lee</span>
                    <div class="text-base">
                      Check that you don’t relax edges finalized. Expect O(n²) for matrix + array.
                    </div>
                    <div class="text-xs text-gray-400 mt-0.5">31 min ago</div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- Right: Filters & Suggestions -->
          <aside class="col-span-4 overflow-y-auto max-h-[calc(100vh-160px)] space-y-5">
            <div class="bg-white rounded-2xl border shadow p-5 flex flex-col gap-3">
              <div class="font-bold">Filters</div>
              <button class="w-full flex justify-between items-center text-sm px-4 py-2 rounded-lg hover:bg-blue-50 border mb-1">
                Course <span class="font-mono text-gray-500">All</span>
              </button>
              <button class="w-full flex justify-between items-center text-sm px-4 py-2 rounded-lg hover:bg-blue-50 border mb-1">
                Status <span class="font-mono text-gray-500">Open</span>
              </button>
              <button class="w-full flex justify-between items-center text-sm px-4 py-2 rounded-lg hover:bg-blue-50 border">
                Date <span class="font-mono text-gray-500">This month</span>
              </button>
            </div>

            <div class="bg-white rounded-2xl border shadow p-5 flex flex-col gap-2">
              <div class="font-bold">Suggested articles</div>
              <button class="flex justify-between items-center gap-2 px-4 py-2 rounded-lg hover:bg-blue-50 border text-sm">
                Dijkstra variants <CubeIcon class="w-4 h-4" />
              </button>
              <button class="flex justify-between items-center gap-2 px-4 py-2 rounded-lg hover:bg-blue-50 border text-sm">
                Dense vs sparse graphs <CubeIcon class="w-4 h-4" />
              </button>
            </div>

            <div class="bg-white rounded-2xl border shadow p-5 flex flex-col gap-2">
              <div class="font-bold">Continue where you left</div>
              <button class="flex items-center gap-2 px-4 py-2 rounded-lg hover:bg-blue-50 border text-sm">
                <CubeIcon class="w-4 h-4 text-green-500" /> Docker error thread
              </button>
              <button class="flex items-center gap-2 px-4 py-2 rounded-lg hover:bg-blue-50 border text-sm">
                <CubeIcon class="w-4 h-4 text-blue-500" /> Office hour confirmation
              </button>
            </div>
          </aside>
        </div>
      </div>

      <!-- ✅ Bottom Bar -->
      <BottomBar />
    </div>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  line-clamp: 2;
  -webkit-line-clamp: 2;
  overflow: hidden;
}
</style>
