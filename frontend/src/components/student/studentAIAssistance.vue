<script setup>
import Sidebar from '@/components/layout/StudentLayout/SideBar.vue'
import HeaderBar from '@/components/layout/StudentLayout/HeaderBar.vue'
import BottomBar from '@/components/layout/StudentLayout/BottomBar.vue'

</script>

<template>
  <div class="flex h-screen bg-gray-50 overflow-hidden">
    <!-- Sidebar -->
    <Sidebar class="sticky top-0 h-screen overflow-y-auto flex-shrink-0" />

    <!-- Main Content Area -->
    <div class="flex flex-col flex-1 overflow-hidden ml-[250px]">
      <!-- Header -->
      <HeaderBar />

      <!-- Main Body -->
      <main class="flex flex-1 overflow-hidden">
        <!-- Central Chat Section -->
        <section
          class="flex flex-col flex-1 bg-white m-4 rounded-2xl shadow p-6 relative overflow-hidden"
        >


          <!-- Chat Messages (Scrollable) -->
          <div
            class="flex-1 overflow-y-auto pr-2 space-y-6 mb-4"
            style="scroll-behavior: smooth;"
          >
            <!-- Welcome message -->
            <div class="flex items-start">
              <img
                src="https://randomuser.me/api/portraits/lego/2.jpg"
                class="w-10 h-10 rounded-full mr-3 mt-1"
              />
              <div class="flex-1">
                <div class="rounded-2xl bg-gray-100 px-5 py-4">
                  <span class="font-semibold block mb-1">Welcome!</span>
                  <span class="text-gray-500 text-sm">
                    Ask about deadlines, resources, or concepts. I can summarize lectures and
                    draft study plans.
                  </span>
                </div>
              </div>
            </div>

            <!-- Student message -->
            <div class="flex items-start justify-end">
              <div
                class="rounded-2xl bg-blue-600 text-white px-5 py-3 shadow text-sm max-w-xl ml-auto"
              >
                What are my upcoming deadlines this week?
              </div>
              <img
                src="https://randomuser.me/api/portraits/men/36.jpg"
                class="w-10 h-10 rounded-full ml-3 mt-1"
              />
            </div>

            <!-- Assistant reply -->
            <div class="flex items-start">
              <img
                src="https://randomuser.me/api/portraits/lego/2.jpg"
                class="w-10 h-10 rounded-full mr-3 mt-1"
              />
              <div class="flex-1">
                <div class="rounded-2xl bg-blue-50/75 px-5 py-4">
                  <span class="font-semibold block mb-2 text-gray-800">Upcoming deadlines</span>
                  <div class="space-y-2">
                    <div
                      class="flex items-center justify-between rounded-lg bg-blue-100 px-4 py-2"
                    >
                      <span class="font-medium text-gray-700 text-sm"
                        >CS 301 • Lab 2 writeup</span
                      >
                      <span
                        class="text-blue-700 bg-white border border-blue-200 rounded-lg px-2 py-1 text-xs font-semibold"
                        >Today</span
                      >
                    </div>
                    <div
                      class="flex items-center justify-between rounded-lg bg-blue-100 px-4 py-2"
                    >
                      <span class="font-medium text-gray-700 text-sm"
                        >CS 210 • Project 2 milestone</span
                      >
                      <span
                        class="text-blue-700 bg-white border border-blue-200 rounded-lg px-2 py-1 text-xs font-semibold"
                        >Mon 11:59 PM</span
                      >
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Fixed Chat Input -->
          <bottomBar />
        </section>

        <!-- Right Sidebar -->
        <aside
          class="w-80 flex-shrink-0 flex flex-col gap-5 p-4 overflow-y-auto h-[calc(100vh-80px)]"
        >
          <!-- Suggested Prompts -->
          <div class="bg-white rounded-2xl shadow p-5">
            <h3 class="text-base font-semibold mb-3">Suggested Prompts</h3>
            <div class="flex flex-wrap gap-2">
              <button
                class="bg-gray-100 hover:bg-blue-100 text-gray-700 text-xs px-3 py-2 rounded-full transition"
              >
                Summarize last CS 301 lecture
              </button>
              <button
                class="bg-gray-100 hover:bg-blue-100 text-gray-700 text-xs px-3 py-2 rounded-full transition"
              >
                Explain Dijkstra with example
              </button>
              <button
                class="bg-gray-100 hover:bg-blue-100 text-gray-700 text-xs px-3 py-2 rounded-full transition"
              >
                Draft study plan for finals
              </button>
              <button
                class="bg-gray-100 hover:bg-blue-100 text-gray-700 text-xs px-3 py-2 rounded-full transition"
              >
                Find office hours this week
              </button>
            </div>
            <p class="text-xs text-gray-400 mt-3">
              These are tailored to your enrolled courses.
            </p>
          </div>

          <!-- Context -->
          <div class="bg-white rounded-2xl shadow p-5">
            <h3 class="text-base font-semibold mb-3">Context</h3>
            <div class="flex flex-col gap-2 text-sm">
              <div class="flex items-center gap-2">
                <span class="font-medium text-gray-600">Active course</span>
                <span
                  class="bg-blue-50 text-blue-700 font-semibold px-3 py-1 rounded-full text-xs"
                  >CS 301</span
                >
              </div>
              <div class="flex items-center gap-2">
                <span class="font-medium text-gray-600">Preferred format</span>
                <span
                  class="bg-blue-50 text-blue-700 font-semibold px-3 py-1 rounded-full text-xs"
                  >Bullet points</span
                >
              </div>
            </div>
          </div>

          <!-- Recent Threads -->
          <div class="bg-white rounded-2xl shadow p-5">
            <h3 class="text-base font-semibold mb-3">Recent Threads</h3>
            <div class="flex flex-col gap-2">
              <button
                class="bg-gray-100 hover:bg-blue-50 text-gray-700 px-4 py-2 rounded-full text-left text-sm transition"
              >
                Graph algorithms recap
              </button>
              <button
                class="bg-gray-100 hover:bg-blue-50 text-gray-700 px-4 py-2 rounded-full text-left text-sm transition"
              >
                Lab 2 rubric clarifications
              </button>
            </div>
          </div>
        </aside>
      </main>
    </div>
  </div>
</template>

<style scoped>
/* Smooth scroll for chat section */
::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 6px;
}
::-webkit-scrollbar-thumb:hover {
  background-color: #94a3b8;
}
</style>
