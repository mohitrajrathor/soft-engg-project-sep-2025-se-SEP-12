<script setup>
import { ref } from "vue"
import Sidebar from "@/components/layout/StudentLayout/SideBar.vue"
import HeaderBar from "@/components/layout/StudentLayout/HeaderBar.vue" 

// State
const videoLink = ref("")
const summary = ref("")
const isLoading = ref(false)

const getSummary = async () => {
  if (!videoLink.value.trim()) {
    alert("Please enter a video link!")
    return
  }

  isLoading.value = true
  summary.value = ""

  try {
    await new Promise((r) => setTimeout(r, 2000))
    summary.value = `Summary for: ${videoLink.value}
- Covers basics of Dijkstra’s Algorithm
- Explains priority queue and complexity
- Includes visualization examples and use-cases
- Duration: 12 minutes
`
  } catch (e) {
    summary.value = "Error generating summary."
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="flex h-screen bg-gray-50 overflow-hidden">
    <!-- Sidebar -->
    <Sidebar class="fixed top-0 left-0 h-screen w-[250px]" />

    <!-- Main Content Area -->
    <div class="flex flex-col flex-1 ml-[250px]">
      <!-- Navbar -->
      <HeaderBar class="sticky top-0 z-20" />

      <!-- Page Content -->
      <main class="flex-1 p-8 overflow-y-auto bg-gray-50">
        <h1 class="text-2xl font-bold mb-6">Video Summary Generator</h1>

        <!-- Input Section -->
        <div class="bg-white shadow rounded-2xl p-6 mb-6">
          <label class="block font-semibold text-gray-700 mb-2">
            Enter Video Link (YouTube, Vimeo, etc.)
          </label>
          <div class="flex gap-3">
            <input
              v-model="videoLink"
              type="text"
              placeholder="https://www.youtube.com/watch?v=..."
              class="flex-1 border border-gray-300 rounded-xl px-4 py-2 focus:ring focus:ring-blue-200 outline-none"
            />
            <button
              @click="getSummary"
              class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-5 py-2 rounded-xl transition"
              :disabled="isLoading"
            >
              {{ isLoading ? "Summarizing..." : "Generate" }}
            </button>
          </div>
        </div>

        <!-- Output Section -->
        <div class="bg-white shadow rounded-2xl p-6">
          <h2 class="text-lg font-semibold mb-3 text-gray-800">📝 Summary</h2>

          <div v-if="!summary && !isLoading" class="text-gray-400">
            Enter a video link above to get the summary.
          </div>

          <div v-else-if="isLoading" class="text-blue-500 animate-pulse">
            Generating summary, please wait...
          </div>

          <pre
            v-else
            class="whitespace-pre-wrap bg-blue-50 p-4 rounded-xl text-gray-700 text-sm"
          >
{{ summary }}
          </pre>
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
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

