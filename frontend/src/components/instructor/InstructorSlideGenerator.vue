<script setup>
import { ref, computed } from 'vue'
import instructorSidebar from '@/components/layout/instructorLayout/instructorSideBar.vue'
import { api } from '@/api'
import MarkdownIt from 'markdown-it'

// renderer
const md = new MarkdownIt()

// Slide state (initial sample slides kept until generation)
const slides = ref([
  { id: 1, title: "Introduction to EduSlide Gen", content: "# Welcome\nThis is the *welcome* slide.", order: 1 },
  { id: 2, title: "Agenda", content: "## Agenda\n- Topic A\n- Topic B", order: 2 },
  { id: 3, title: "Core Concepts", content: "Explain concepts ...", order: 3 }
])

const slideOrderOption = ref('all')
const orderedSlides = computed(() => {
  if (slideOrderOption.value === 'even') return slides.value.filter(s => s.order % 2 === 0)
  if (slideOrderOption.value === 'odd') return slides.value.filter(s => s.order % 2 === 1)
  return slides.value
})
const currentIndex = ref(0)
const currentSlide = computed(() => orderedSlides.value[currentIndex.value] || orderedSlides.value[0])
function selectOrder(option) {
  slideOrderOption.value = option
  currentIndex.value = 0
}
function prevSlide() { if (currentIndex.value > 0) currentIndex.value-- }
function nextSlide() { if (currentIndex.value < orderedSlides.value.length - 1) currentIndex.value++ }

// Inputs for generation
const courseId = ref(null)
const title = ref('')
const topicsInput = ref([''])
const numSlides = ref(5)
const loading = ref(false)

function addTopic() { topicsInput.value.push('') }
function removeTopic(i) { topicsInput.value.splice(i,1) }

async function generateSlides() {
  if (!courseId.value || courseId.value <= 0) {
    alert('Please provide a valid Course ID (numeric).')
    return
  }
  if (!title.value) {
    alert('Please provide a title for the slide deck.')
    return
  }
  const topics = topicsInput.value.map(t => t.trim()).filter(Boolean)
  if (topics.length === 0) {
    alert('Please provide at least one topic.')
    return
  }

  loading.value = true
  try {
    const payload = {
      course_id: courseId.value,
      title: title.value,
      description: '',
      topics: topics,
      num_slides: numSlides.value
    }
    const res = await api.post('/slide-decks', payload)
    // backend returns SlideDeckResponse with `slides` list
    const deck = res.data
    if (deck && Array.isArray(deck.slides)) {
      // normalize to local slide objects
      slides.value = deck.slides.map((s, idx) => ({ id: s.id ?? idx+1, title: s.title ?? `Slide ${idx+1}`, content: s.content ?? '', order: idx+1 }))
      currentIndex.value = 0
      alert('Slide deck generated and saved.')
    } else {
      alert('Unexpected response from server.')
    }
  } catch (err) {
    console.error('Slide generation error', err)
    const msg = err.response?.data?.detail || err.message || 'Failed to generate slides.'
    alert(msg)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="flex min-h-screen bg-[#f8fafc]">
    <instructorSidebar />

    <!-- Main Content -->
    <main class="flex-1 p-10 ml-64">
      <!-- Header -->
      <!-- <div class="flex items-center justify-between mb-9">
        <h1 class="font-extrabold text-3xl tracking-tight text-indigo-700">Slide Deck Generator</h1>
        <button
          class="px-6 py-2 bg-blue-600 text-white rounded-xl shadow font-semibold hover:bg-blue-800 transition">New
          Deck</button>
      </div> -->
      <div class="flex flex-wrap gap-12">
        <!-- Central work area -->
        <section class="flex-1 min-w-[500px] max-w-[760px] flex flex-col gap-8">
          <!-- Slides Ordering Controls -->
          <div class="mb-2 flex items-center gap-3">
            <span class="font-semibold text-sm text-gray-500 mr-1">Slides Order:</span>
            <button
              class="px-4 py-1 rounded-lg text-sm font-semibold border border-indigo-300 bg-indigo-50 text-indigo-700 hover:bg-indigo-100 transition"
              :class="{ 'bg-indigo-600 text-white': slideOrderOption === 'all' }" @click="selectOrder('all')">
              All
            </button>
            <button
              class="px-4 py-1 rounded-lg text-sm font-semibold border border-blue-200 bg-blue-50 text-blue-700 hover:bg-blue-100 transition"
              :class="{ 'bg-blue-700 text-white': slideOrderOption === 'even' }" @click="selectOrder('even')">
              Even
            </button>
            <button
              class="px-4 py-1 rounded-lg text-sm font-semibold border border-yellow-200 bg-yellow-50 text-yellow-800 hover:bg-yellow-100 transition"
              :class="{ 'bg-yellow-400 text-white': slideOrderOption === 'odd' }" @click="selectOrder('odd')">
              Odd
            </button>
          </div>
          <!-- Current Slide Panel -->
          <div class="bg-white rounded-2xl shadow-2xl p-7 relative">
            <div class="flex items-center justify-between mb-3">
              <h2 class="font-bold text-lg text-black">
                Current Slide: <span class="text-indigo-700">{{ currentSlide?.title }}</span>
              </h2>
              <div class="flex gap-2">
                <button @click="prevSlide" :disabled="currentIndex === 0"
                  class="px-4 py-2 rounded-lg bg-gray-100 text-gray-600 font-semibold hover:bg-gray-200 transition disabled:opacity-50 disabled:cursor-not-allowed">Prev</button>
                <button @click="nextSlide" :disabled="currentIndex === orderedSlides.length - 1"
                  class="px-4 py-2 rounded-lg bg-gray-100 text-gray-600 font-semibold hover:bg-gray-200 transition disabled:opacity-50 disabled:cursor-not-allowed">Next</button>
              </div>
            </div>
            <div class="flex space-x-2 mb-4">
              <button class="px-5 py-2 font-semibold rounded-lg bg-blue-900 text-white">Content</button>
              <button
                class="px-5 py-2 font-semibold rounded-lg bg-blue-50 text-blue-700 hover:bg-blue-100 transition">Styles</button>
              <button
                class="px-5 py-2 font-semibold rounded-lg bg-blue-50 text-blue-700 hover:bg-blue-100 transition">Collaborators</button>
            </div>
            <div class="flex gap-3 mb-3">
              <button
                class="px-3 py-2 rounded bg-blue-50 text-blue-700 font-medium hover:bg-blue-100 transition">B</button>
              <button
                class="px-3 py-2 rounded bg-blue-50 text-blue-700 font-medium hover:bg-blue-100 transition">I</button>
              <button
                class="px-3 py-2 rounded bg-blue-50 text-blue-700 font-medium hover:bg-blue-100 transition">Image</button>
              <button
                class="px-3 py-2 rounded bg-blue-50 text-blue-700 font-medium hover:bg-blue-100 transition">Graph</button>
            </div>
            <div class="max-w-md w-full">
              <textarea v-model="currentSlide.content" class="w-full p-3 border rounded-lg resize-y" rows="6"
                placeholder="Type slide content here..."></textarea>

              <!-- Rendered Markdown Preview for current slide -->
              <div class="mt-4 p-4 bg-gray-50 rounded">
                <h3 class="font-semibold mb-2">Preview</h3>
                <div v-html="md.render(currentSlide.content)"></div>
              </div>
            </div>

          </div>
          <!-- Live Preview: Slide List (Ordered) -->
          <div class="bg-white rounded-2xl shadow-2xl p-7">
            <h2 class="font-bold text-lg text-black mb-5">Ordered Slides Preview</h2>
            <div class="grid grid-cols-1 gap-1">
              <div v-for="slide in orderedSlides" :key="slide.id"
                class="w-full mb-3 bg-indigo-50 rounded-xl p-4 flex items-center gap-4">
                <span
                  class="bg-indigo-600 text-white font-extrabold rounded-lg w-10 h-10 flex items-center justify-center mr-2">{{
                  slide.order }}</span>
                <div>
                  <div class="font-bold text-indigo-800">{{ slide.title }}</div>
                  <div class="text-sm text-gray-500">{{ slide.content }}</div>
                </div>
              </div>
            </div>
          </div>
        </section>
        <!-- Side options -->
        <aside class="w-full max-w-xs flex flex-col gap-8">
          <!-- Generate Slide Deck (API inputs) -->
          <div class="bg-white rounded-2xl shadow-2xl p-5">
            <h3 class="font-bold text-lg mb-3 text-black">Generate Slide Deck</h3>
            <div class="space-y-3">
              <div>
                <label class="block text-sm text-gray-600 mb-1">Course ID</label>
                <input v-model.number="courseId" type="number" min="1" placeholder="e.g., 1"
                  class="w-full p-2 border rounded-lg focus:ring-1 focus:ring-indigo-300" />
              </div>
              <div>
                <label class="block text-sm text-gray-600 mb-1">Deck Title</label>
                <input v-model="title" type="text" placeholder="e.g., Lecture 1: Intro"
                  class="w-full p-2 border rounded-lg focus:ring-1 focus:ring-indigo-300" />
              </div>
              <div>
                <label class="block text-sm text-gray-600 mb-1">Topics</label>
                <div class="space-y-2">
                  <div v-for="(t, i) in topicsInput" :key="i" class="flex gap-2">
                    <input v-model="topicsInput[i]" type="text" placeholder="Topic"
                      class="flex-1 p-2 border rounded-lg" />
                    <button @click.prevent="removeTopic(i)" class="px-3 rounded bg-red-100 text-red-600">✕</button>
                  </div>
                  <button @click.prevent="addTopic" class="text-indigo-700 text-sm font-medium">+ Add topic</button>
                </div>
              </div>
              <div>
                <label class="block text-sm text-gray-600 mb-1">Number of Slides</label>
                <input v-model.number="numSlides" type="number" min="1" max="20" class="w-full p-2 border rounded-lg" />
              </div>
              <div class="pt-2">
                <button @click.prevent="generateSlides" :disabled="loading"
                  class="w-full px-4 py-2 rounded-lg bg-indigo-700 text-white hover:bg-indigo-800 disabled:opacity-60">{{ loading ? 'Generating...' : 'Generate' }}</button>
              </div>
            </div>
          </div>

          <!-- Template Selection -->
          <div class="bg-white rounded-2xl shadow-2xl p-5">
            <h3 class="font-bold text-lg mb-4 text-black">Template Selection</h3>
            <div class="grid grid-cols-2 gap-4">
              <button
                class="flex flex-col items-center border-2 border-blue-700 rounded-lg p-3 bg-blue-50 shadow hover:bg-blue-100 transition">
                <div class="w-14 h-10 bg-blue-200 rounded mb-1"></div>
                <span class="font-medium text-blue-700 mt-1">Classic Academic</span>
              </button>
              <button
                class="flex flex-col items-center border-2 border-gray-300 rounded-lg p-3 bg-gray-50 shadow hover:bg-gray-100 transition">
                <div class="w-14 h-10 bg-gray-200 rounded mb-1"></div>
                <span class="font-medium text-gray-700 mt-1">Modern Pro</span>
              </button>
              <button
                class="flex flex-col items-center border-2 border-gray-300 rounded-lg p-3 bg-gray-50 shadow hover:bg-gray-100 transition">
                <div class="w-14 h-10 bg-blue-100 rounded mb-1"></div>
                <span class="font-medium text-blue-700 mt-1">Minimalist Blue</span>
              </button>
              <button
                class="flex flex-col items-center border-2 border-yellow-400 rounded-lg p-3 bg-yellow-50 shadow hover:bg-yellow-100 transition">
                <div class="w-14 h-10 bg-yellow-200 rounded mb-1"></div>
                <span class="font-medium text-yellow-800 mt-1">Vibrant Yellow</span>
              </button>
            </div>
          </div>
          <!-- Export Panel -->
          <div class="bg-white rounded-2xl shadow-2xl p-5 flex flex-col gap-2">
            <h3 class="font-bold text-lg mb-2 text-black">Export Options</h3>
            <button
              class="w-full px-4 py-3 rounded-lg bg-blue-900 text-white font-semibold shadow hover:bg-blue-700 transition mb-2">Export
              to PDF</button>
            <button
              class="w-full px-4 py-3 rounded-lg bg-blue-50 text-blue-900 font-medium border hover:bg-blue-100 transition">Export
              to PowerPoint</button>
            <button
              class="w-full px-4 py-3 rounded-lg bg-blue-50 text-blue-900 font-medium border hover:bg-blue-100 transition">Share
              Link</button>
          </div>
        </aside>
      </div>
      <!-- Footer -->
      <footer class="mt-12 flex justify-between items-center text-xs text-gray-400 border-t pt-5">
        <div class="flex gap-8">
          <a href="#" class="hover:text-blue-700 transition">Quick Links</a>
          <a href="#" class="hover:text-blue-700 transition">Resources</a>
          <a href="#" class="hover:text-blue-700 transition">Legal</a>
        </div>
        <div class="flex gap-4">
          <a href="#" class="hover:text-blue-700 transition"><i class="fab fa-facebook"></i></a>
          <a href="#" class="hover:text-blue-700 transition"><i class="fab fa-twitter"></i></a>
          <a href="#" class="hover:text-blue-700 transition"><i class="fab fa-linkedin"></i></a>
        </div>
      </footer>
    </main>
  </div>
</template>
