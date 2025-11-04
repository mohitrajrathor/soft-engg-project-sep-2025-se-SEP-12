<script setup>
import { ref, computed } from 'vue'
import { VueDraggableNext } from 'vue-draggable-next'
import TASidebar from '../layout/TaLayout/TASidebar.vue'
import TaHeaderBar from '../layout/TaLayout/TaHeaderBar.vue'

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
  <div class="flex">
  <TASidebar class="fixed top-0 left-0 h-screen w-[250px]" />
    <main class="flex-1 flex flex-col min-h-screen ml-[250px] bg-gray-50">
      <TaHeaderBar searchPlaceholder="Search dashboard, queries, resources" />

      <!-- Export + Share Buttons -->
      <div class="px-8 pt-6 flex flex-col lg:flex-row gap-8">
        <button
          class="px-5 py-2 rounded-lg bg-blue-900 text-white font-semibold hover:bg-blue-700 transition">
          Export to PDF
        </button>
        <button
          class="px-5 py-2 rounded-lg bg-blue-50 text-blue-900 font-medium border hover:bg-blue-100 transition">
          Share Link
        </button>
      </div>

      <!-- Slide Control Area -->
      <section class="flex flex-col gap-4 flex-1 px-8 pt-4 pb-10">
        <!-- Current Slide -->
        <div class="bg-white rounded-t-2xl shadow-2xl p-7 relative">
          <div class="flex items-center justify-between mb-3">
            <h2 class="font-bold text-lg text-black">
              Current Slide: <span class="text-indigo-700">{{ currentSlide?.title }}</span>
            </h2>
            <div class="flex gap-2">
              <button @click="prevSlide" :disabled="currentIndex === 0"
                class="px-4 py-2 rounded-lg bg-gray-100 text-gray-600 font-semibold hover:bg-gray-200 transition disabled:opacity-50 disabled:cursor-not-allowed">
                Prev
              </button>
              <button @click="nextSlide" :disabled="currentIndex === slides.length - 1"
                class="px-4 py-2 rounded-lg bg-gray-100 text-gray-600 font-semibold hover:bg-gray-200 transition disabled:opacity-50 disabled:cursor-not-allowed">
                Next
              </button>
            </div>
          </div>

          <!-- Auto-expanding textarea for prompt -->
          <textarea
            v-model="slidePrompt"
            @input="e => {e.target.style.height = 'auto'; e.target.style.height = e.target.scrollHeight + 'px'}"
            class="w-full p-3 border rounded-lg resize-none focus:ring-2 focus:ring-indigo-500 focus:outline-none text-gray-800 text-sm"
            placeholder="Type your prompt here to generate or refine slides..."
            rows="2">
          </textarea>

          <button
            @click="generateSlidesFromPrompt"
            class="mt-3 px-5 py-2 rounded-lg bg-indigo-600 text-white font-semibold hover:bg-indigo-700 transition">
            Generate Slides
          </button>

          <!-- Editable Slide Content -->
          <textarea
            v-model="currentSlide.content"
            @input="e =>{ e.target.style.height = 'auto'; e.target.style.height = e.target.scrollHeight + 'px'}"
            class="w-full p-4 border rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:outline-none text-gray-900 mt-5"
            placeholder="Edit current slide content..."
            rows="3">
          </textarea>
        </div>

        <!-- Reorder Slides -->
        <div class="bg-white rounded-b-2xl shadow-2xl p-7 border-t border-gray-200">
          <h2 class="font-bold text-lg text-black mb-5">Reorder Slides (Drag & Drop)</h2>
          <VueDraggableNext v-model="slides" @end="onDragEnd" animation="200" handle=".drag-handle">
            <transition-group name="fade" tag="div" class="grid grid-cols-1 gap-3">
              <div
                v-for="slide in slides"
                :key="slide.id"
                class="flex items-center gap-4 p-4 bg-indigo-50 rounded-xl cursor-grab hover:bg-indigo-100 transition">
                <i class="bi bi-grip-vertical text-gray-500 text-lg drag-handle"></i>
                <span
                  class="bg-indigo-600 text-white font-extrabold rounded-lg w-10 h-10 flex items-center justify-center">{{ slide.order }}</span>
                <div>
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
.fade-enter-active, .fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
