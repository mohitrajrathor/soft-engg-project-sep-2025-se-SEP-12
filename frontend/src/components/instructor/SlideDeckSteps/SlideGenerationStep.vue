<template>
  <div class="w-full">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="font-extrabold text-4xl text-slate-900 tracking-tight">Generated Slides</h1>
      <p class="text-slate-500 mt-2">Step 3: Review, edit, and save your presentation</p>
      <div class="mt-4 flex gap-1">
        <div class="flex-1 h-1 bg-blue-600 rounded-full"></div>
        <div class="flex-1 h-1 bg-blue-600 rounded-full"></div>
        <div class="flex-1 h-1 bg-blue-600 rounded-full"></div>
      </div>
    </div>

    <!-- Two-Column Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-6">
      <!-- Sidebar with Slides List -->
      <div class="lg:col-span-1">
        <div class="bg-white rounded-xl border border-slate-200 sticky top-6 max-h-[calc(100vh-200px)] overflow-y-auto">
          <div class="p-4 border-b border-slate-200 bg-slate-50">
            <h3 class="font-bold text-slate-900">Slides ({{ slides.length }})</h3>
          </div>
          <div class="p-2 space-y-1">
            <button
              v-for="(slide, idx) in slides"
              :key="idx"
              @click="selectedSlideIndex = idx"
              :class="[
                'w-full text-left p-3 rounded-lg transition font-medium text-sm',
                selectedSlideIndex === idx
                  ? 'bg-blue-100 text-blue-900 border-l-4 border-blue-600'
                  : 'text-slate-700 hover:bg-slate-50'
              ]"
            >
              <div class="flex items-start gap-2">
                <span class="flex-shrink-0 w-6 h-6 rounded-full bg-blue-600 text-white text-xs flex items-center justify-center font-bold">
                  {{ idx + 1 }}
                </span>
                <span class="truncate">{{ slide.title }}</span>
              </div>
            </button>
          </div>
        </div>
      </div>

      <!-- Main Slide Viewer -->
      <div class="lg:col-span-3">
        <div v-if="currentSlide" class="space-y-6">
          <!-- Slide Card -->
          <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <!-- Slide Content -->
            <div class="p-8 min-h-96 bg-gradient-to-br from-slate-50 to-white">
              <div class="max-w-4xl mx-auto prose prose-sm max-w-none">
                <h2 class="text-2xl font-bold text-slate-900 mb-4">{{ currentSlide.title }}</h2>
                <div v-html="renderMarkdown(currentSlide.content)" class="text-slate-700 leading-relaxed"></div>
              </div>

              <!-- Graph Display -->
              <GraphRenderer
                v-if="currentSlide.graph_data"
                :graphData="currentSlide.graph_data"
                class="mt-8 pt-8 border-t border-slate-200"
              />
            </div>

            <!-- Slide Actions -->
            <div class="p-4 border-t border-slate-200 bg-slate-50 flex gap-2 flex-wrap">
              <button
                @click="openEditModal(selectedSlideIndex)"
                class="px-4 py-2 bg-amber-100 text-amber-800 font-semibold rounded-lg hover:bg-amber-200 transition text-sm"
              >
                ✏️ Edit Content
              </button>
              <button
                v-if="currentSlide.graph_data"
                @click="showGraphSettings = !showGraphSettings"
                class="px-4 py-2 bg-purple-100 text-purple-800 font-semibold rounded-lg hover:bg-purple-200 transition text-sm"
              >
                📊 Graph
              </button>
              <div class="flex-1"></div>
              <button
                v-if="selectedSlideIndex > 0"
                @click="selectedSlideIndex--"
                class="px-4 py-2 border border-slate-300 text-slate-700 font-semibold rounded-lg hover:bg-slate-100 transition text-sm"
              >
                ← Previous
              </button>
              <button
                v-if="selectedSlideIndex < slides.length - 1"
                @click="selectedSlideIndex++"
                class="px-4 py-2 border border-slate-300 text-slate-700 font-semibold rounded-lg hover:bg-slate-100 transition text-sm"
              >
                Next →
              </button>
            </div>
          </div>

          <!-- Graph Settings (if exists) -->
          <div v-if="showGraphSettings && currentSlide.graph_data" class="bg-purple-50 border border-purple-200 rounded-xl p-4">
            <p class="text-xs font-bold text-purple-900 uppercase mb-2">Graph Details</p>
            <pre class="text-xs text-purple-800 bg-white p-3 rounded border border-purple-100 overflow-x-auto">{{ JSON.stringify(currentSlide.graph_data, null, 2) }}</pre>
          </div>
        </div>
      </div>
    </div>

    <!-- Summary Bar -->
    <div class="bg-slate-100 rounded-lg p-4 mb-6 flex items-center justify-between">
      <div class="text-sm">
        <p class="font-semibold text-slate-900">{{ config.title }}</p>
        <p class="text-xs text-slate-600">{{ slides.length }} slides • {{ config.format }} • {{ config.topics.join(', ') }}</p>
      </div>
      <button
        @click="showDetails = !showDetails"
        class="text-xs font-bold text-slate-600 hover:text-slate-900"
      >
        {{ showDetails ? 'Hide' : 'Show' }} Details
      </button>
    </div>

    <!-- Details (if shown) -->
    <div v-if="showDetails" class="bg-slate-50 rounded-lg p-4 mb-6 space-y-2 text-sm">
      <div><span class="font-semibold text-slate-700">Format:</span> <span class="text-slate-600 capitalize">{{ config.format }}</span></div>
      <div><span class="font-semibold text-slate-700">Description:</span> <span class="text-slate-600">{{ config.description || 'None' }}</span></div>
      <div><span class="font-semibold text-slate-700">Topics:</span> <span class="text-slate-600">{{ config.topics.join(', ') }}</span></div>
      <div><span class="font-semibold text-slate-700">With Graphs:</span> <span class="text-slate-600">{{ config.includeGraphs ? 'Yes' : 'No' }}</span></div>
    </div>

    <!-- Action Buttons -->
    <div class="flex gap-3 justify-end">
      <button
        @click="$emit('back')"
        :disabled="isSaving"
        class="px-6 py-3 border border-slate-300 text-slate-700 font-bold rounded-lg hover:bg-slate-50 transition disabled:opacity-50"
      >
        ← Back
      </button>
      <button
        @click="saveToDatabase"
        :disabled="isSaving"
        class="px-8 py-3 bg-green-600 text-white font-bold rounded-lg hover:bg-green-700 transition disabled:opacity-50 flex items-center gap-2"
      >
        <span v-if="isSaving" class="animate-spin">⟳</span>
        <span>{{ isSaving ? 'Saving...' : '💾 Save to Database' }}</span>
      </button>
    </div>

    <!-- Edit Modal -->
    <div
      v-if="showEditModal"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
      @click.self="showEditModal = false"
    >
      <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-slate-200 sticky top-0 bg-white">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-bold text-slate-900">Edit Slide {{ editingSlideIndex + 1 }}</h3>
            <button
              @click="showEditModal = false"
              class="text-slate-400 hover:text-slate-600 text-2xl"
            >
              ✕
            </button>
          </div>
        </div>

        <div class="p-6 space-y-4">
          <!-- Title -->
          <div>
            <label class="block text-sm font-bold text-slate-700 mb-2">Slide Title</label>
            <input
              v-model="editForm.title"
              type="text"
              class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
            />
          </div>

          <!-- Content -->
          <div>
            <label class="block text-sm font-bold text-slate-700 mb-2">Content (Markdown)</label>
            <textarea
              v-model="editForm.content"
              rows="6"
              class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none font-mono text-sm"
            ></textarea>
          </div>

          <!-- Regeneration Notes -->
          <div>
            <label class="block text-sm font-bold text-slate-700 mb-2">
              Custom Notes for Regeneration
            </label>
            <textarea
              v-model="editForm.regenerationNotes"
              rows="3"
              placeholder="Describe specific changes you want for this slide (optional)..."
              class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-sm"
            ></textarea>
          </div>

          <!-- Preview -->
          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs font-bold text-slate-600 uppercase mb-2">Preview</p>
            <div v-html="renderMarkdown(editForm.content)" class="prose prose-sm max-w-none"></div>
          </div>
        </div>

        <div class="p-6 border-t border-slate-200 flex gap-3 justify-end">
          <button
            @click="showEditModal = false"
            class="px-4 py-2 border border-slate-300 text-slate-700 font-bold rounded-lg hover:bg-slate-50 transition"
          >
            Cancel
          </button>
          <button
            @click="saveSlideEdit"
            class="px-4 py-2 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 transition"
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import MarkdownIt from 'markdown-it'
import GraphRenderer from '@/components/instructor/GraphRenderer.vue'
import { api } from '@/api'

const props = defineProps({
  slides: {
    type: Array,
    required: true
  },
  config: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['back', 'saved'])

const md = new MarkdownIt({ html: true, linkify: true })

const selectedSlideIndex = ref(0)
const showGraphSettings = ref(false)
const showDetails = ref(false)
const showEditModal = ref(false)
const editingSlideIndex = ref(null)
const isSaving = ref(false)

const editForm = ref({
  title: '',
  content: '',
  regenerationNotes: ''
})

const currentSlide = computed(() => props.slides[selectedSlideIndex.value])

function renderMarkdown(content) {
  return md.render(content || '')
}

function openEditModal(idx) {
  editingSlideIndex.value = idx
  const slide = props.slides[idx]
  editForm.value = {
    title: slide.title,
    content: slide.content,
    regenerationNotes: ''
  }
  showEditModal.value = true
}

function saveSlideEdit() {
  const slide = props.slides[editingSlideIndex.value]
  slide.title = editForm.value.title
  slide.content = editForm.value.content
  showEditModal.value = false
}

async function saveToDatabase() {
  isSaving.value = true
  try {
    const response = await api.post('/slide-decks/', {
      course_id: props.config.courseId,
      title: props.config.title,
      description: props.config.description || '',
      topics: props.config.topics,
      num_slides: props.config.numSlides,
      format: props.config.format,
      include_graphs: props.config.includeGraphs,
      graph_types: props.config.graphTypes,
      slides: props.slides
    })

    emit('saved', response.data)
  } catch (error) {
    console.error('Save failed:', error)
    alert('Failed to save: ' + (error.response?.data?.detail || error.message))
  } finally {
    isSaving.value = false
  }
}
</script>

<style scoped></style>
