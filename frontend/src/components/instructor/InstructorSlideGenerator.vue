<script setup>
import { ref, computed } from 'vue'
import { VueDraggableNext } from 'vue-draggable-next'
import instructorSidebar from '@/components/layout/instructorLayout/instructorSideBar.vue';

// Slides data
const slides = ref([
  { id: 1, title: "Introduction to EduSlide Gen", content: "Welcome slide!", order: 1 },
  { id: 2, title: "Agenda", content: "Topics covered ...", order: 2 },
  { id: 3, title: "Core Concepts", content: "Explain concepts ...", order: 3 },
  { id: 4, title: "Example Problems", content: "Practice slides ...", order: 4 },
  { id: 5, title: "Summary & Next Steps", content: "Wrap up ...", order: 5 }
])

// Prompt input
const slidePrompt = ref("")

// Current selected slide
const currentIndex = ref(0)
const currentSlide = computed(() => slides.value[currentIndex.value] || slides.value[0])

function prevSlide() {
  if (currentIndex.value > 0) currentIndex.value--
}

function nextSlide() {
  if (currentIndex.value < slides.value.length - 1) currentIndex.value++
}

function onDragEnd() {
  slides.value = slides.value.map((s, index) => ({ ...s, order: index + 1 }))
}

function generateSlidesFromPrompt() {
  if (!slidePrompt.value.trim()) return
  alert(`Generating slides based on: "${slidePrompt.value}"`)
  // TODO: Call AI API or slide generation logic here
  slidePrompt.value = ''
}
</script>

<template>
  <div class="flex min-h-screen bg-[#f8fafc]">
    <!-- Fixed Sidebar -->
    <div class="fixed top-0 left-0 h-screen w-64 z-10">
      <instructorSidebar />
    </div>

    <!-- Main Content -->
    <main class="flex-1 ml-48 bg-gray-50 overflow-auto">
      <!-- Header Section -->
      <div class="px-8 pt-6 pb-4 bg-white border-b border-gray-200">
        <h1 class="text-2xl font-bold text-gray-800 mb-2">Slide Deck Generator</h1>
        <p class="text-gray-500 text-sm">Create and manage your presentation slides</p>
      </div>

      <!-- Export + Share Buttons -->
      <div class="px-8 pt-6 flex flex-wrap gap-4">
        <button
          class="px-5 py-2 rounded-lg bg-blue-900 text-white font-semibold hover:bg-blue-700 transition shadow-sm">
          Export to PDF
        </button>
        <button
          class="px-5 py-2 rounded-lg bg-blue-50 text-blue-900 font-medium border border-blue-200 hover:bg-blue-100 transition">
          Share Link
        </button>
        <button
          class="px-5 py-2 rounded-lg bg-gray-50 text-gray-700 font-medium border border-gray-200 hover:bg-gray-100 transition">
          Export to PowerPoint
        </button>
      </div>

      <!-- Slide Control Area -->
      <section class="flex flex-col gap-6 px-8 pt-6 pb-10">
        <!-- Current Slide Editor -->
        <div class="bg-white rounded-xl shadow-lg p-7">
          <div class="flex items-center justify-between mb-5">
            <h2 class="font-bold text-lg text-gray-800">
              Current Slide: <span class="text-indigo-700">{{ currentSlide?.title }}</span>
            </h2>
            <div class="flex gap-2">
              <button 
                @click="prevSlide" 
                :disabled="currentIndex === 0"
                class="px-4 py-2 rounded-lg bg-gray-100 text-gray-600 font-semibold hover:bg-gray-200 transition disabled:opacity-50 disabled:cursor-not-allowed">
                ← Prev
              </button>
              <button 
                @click="nextSlide" 
                :disabled="currentIndex === slides.length - 1"
                class="px-4 py-2 rounded-lg bg-gray-100 text-gray-600 font-semibold hover:bg-gray-200 transition disabled:opacity-50 disabled:cursor-not-allowed">
                Next →
              </button>
            </div>
          </div>

          <!-- Prompt Input Section -->
          <div class="mb-6 p-4 bg-gradient-to-r from-indigo-50 to-blue-50 rounded-lg border border-indigo-100">
            <label class="block text-sm font-semibold text-gray-700 mb-2">
              AI Slide Generator
            </label>
            <textarea
              v-model="slidePrompt"
              @input="e => {e.target.style.height = 'auto'; e.target.style.height = e.target.scrollHeight + 'px'}"
              class="w-full p-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-indigo-500 focus:outline-none text-gray-800 text-sm"
              placeholder="Type your prompt here to generate or refine slides... (e.g., 'Create 5 slides about Machine Learning basics')"
              rows="2">
            </textarea>

            <button
              @click="generateSlidesFromPrompt"
              class="mt-3 px-5 py-2 rounded-lg bg-indigo-600 text-white font-semibold hover:bg-indigo-700 transition shadow-sm flex items-center gap-2">
              <i class="bi bi-magic"></i>
              Generate Slides
            </button>
          </div>

          <!-- Editable Slide Content -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">
              Slide Content
            </label>
            <textarea
              v-model="currentSlide.content"
              @input="e => {e.target.style.height = 'auto'; e.target.style.height = e.target.scrollHeight + 'px'}"
              class="w-full p-4 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:outline-none text-gray-900"
              placeholder="Edit current slide content..."
              rows="4">
            </textarea>
          </div>
        </div>

        <!-- Reorder Slides Section -->
        <div class="bg-white rounded-xl shadow-lg p-7">
          <div class="flex items-center justify-between mb-5">
            <h2 class="font-bold text-lg text-gray-800">Slide Order</h2>
            <span class="text-sm text-gray-500">Drag to reorder</span>
          </div>
          
          <VueDraggableNext 
            v-model="slides" 
            @end="onDragEnd" 
            animation="200" 
            handle=".drag-handle"
            class="space-y-3">
            <transition-group name="fade" tag="div">
              <div
                v-for="slide in slides"
                :key="slide.id"
                class="flex items-center gap-4 p-4 bg-indigo-50 rounded-xl cursor-grab hover:bg-indigo-100 transition border border-indigo-100">
                <i class="bi bi-grip-vertical text-gray-400 text-xl drag-handle hover:text-gray-600"></i>
                <span
                  class="bg-indigo-600 text-white font-bold rounded-lg w-10 h-10 flex items-center justify-center flex-shrink-0 shadow-sm">
                  {{ slide.order }}
                </span>
                <div class="flex-1 min-w-0">
                  <div class="font-bold text-indigo-800">{{ slide.title }}</div>
                  <div class="text-sm text-gray-500 truncate">{{ slide.content }}</div>
                </div>
              </div>
            </transition-group>
          </VueDraggableNext>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
.drag-handle {
  cursor: grab;
}

.drag-handle:active {
  cursor: grabbing;
}

.fade-enter-active, 
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from, 
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* Custom scrollbar */
main::-webkit-scrollbar {
  width: 8px;
}

main::-webkit-scrollbar-track {
  background: #f1f1f1;
}

main::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

main::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>