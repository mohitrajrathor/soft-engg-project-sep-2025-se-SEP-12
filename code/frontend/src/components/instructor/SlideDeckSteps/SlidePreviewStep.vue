<template>
  <div class="w-full">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="font-extrabold text-4xl text-slate-900 tracking-tight">Review Slide Outline</h1>
      <p class="text-slate-500 mt-2">Step 2: Confirm the slide structure before generation</p>
      <div class="mt-4 flex gap-1">
        <div class="flex-1 h-1 bg-blue-600 rounded-full"></div>
        <div class="flex-1 h-1 bg-blue-600 rounded-full"></div>
        <div class="flex-1 h-1 bg-slate-200 rounded-full"></div>
      </div>
    </div>

    <!-- Deck Summary -->
    <div class="bg-white rounded-2xl border border-slate-200 p-6 mb-6">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div>
          <p class="text-xs font-bold text-slate-500 uppercase">Title</p>
          <p class="text-lg font-semibold text-slate-900 truncate">{{ config.title }}</p>
        </div>
        <div>
          <p class="text-xs font-bold text-slate-500 uppercase">Format</p>
          <p class="text-lg font-semibold text-slate-900 capitalize">{{ config.format }}</p>
        </div>
        <div>
          <p class="text-xs font-bold text-slate-500 uppercase">Slides</p>
          <p class="text-lg font-semibold text-slate-900">{{ config.numSlides }}</p>
        </div>
        <div>
          <p class="text-xs font-bold text-slate-500 uppercase">Topics</p>
          <p class="text-lg font-semibold text-slate-900">{{ config.topics.length }}</p>
        </div>
      </div>
    </div>

    <!-- Outline Section -->
    <div class="bg-white rounded-2xl border border-slate-200 p-6 mb-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-bold text-slate-900">Slide Outline</h2>
        <span v-if="isLoadingPreview" class="text-sm text-slate-500 flex items-center gap-2">
          <span class="animate-spin">⟳</span> Generating preview...
        </span>
      </div>

      <div v-if="previewOutline && previewOutline.length > 0" class="space-y-3">
        <div
          v-for="(outline, idx) in previewOutline"
          :key="idx"
          class="flex gap-3 p-3 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-100"
        >
          <div class="flex-shrink-0 w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-sm">
            {{ idx + 1 }}
          </div>
          <div class="flex-1">
            <p class="text-sm text-slate-700">{{ outline }}</p>
          </div>
        </div>
      </div>

      <div v-else-if="!isLoadingPreview && previewError" class="p-4 bg-red-50 border border-red-200 rounded-lg">
        <p class="text-sm text-red-700">Failed to generate preview: {{ previewError }}</p>
      </div>

      <div v-else-if="!isLoadingPreview && !previewOutline" class="p-4 bg-slate-50 border border-slate-200 rounded-lg text-center text-slate-500">
        <p class="text-sm">No preview available. Click "Generate Preview" to see the outline.</p>
      </div>
    </div>

    <!-- Settings Summary -->
    <div v-if="config.description" class="bg-indigo-50 border border-indigo-200 rounded-lg p-4 mb-6">
      <p class="text-xs font-bold text-indigo-900 uppercase mb-1">Context</p>
      <p class="text-sm text-indigo-800">{{ config.description }}</p>
    </div>

    <!-- Topics List -->
    <div class="bg-slate-50 rounded-lg p-4 mb-6">
      <p class="text-xs font-bold text-slate-600 uppercase mb-2">Topics to Cover</p>
      <div class="flex flex-wrap gap-2">
        <span
          v-for="(topic, idx) in config.topics"
          :key="idx"
          class="inline-block px-3 py-1 bg-blue-100 text-blue-800 text-xs font-semibold rounded-full"
        >
          {{ topic }}
        </span>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="flex gap-3 justify-end pt-6">
      <button
        type="button"
        @click="$emit('back')"
        :disabled="isGenerating"
        class="px-6 py-3 border border-slate-300 text-slate-700 font-bold rounded-lg hover:bg-slate-50 transition disabled:opacity-50 disabled:cursor-not-allowed"
      >
        ← Back
      </button>
      <button
        v-if="!previewOutline"
        type="button"
        @click="generatePreview"
        :disabled="isLoadingPreview || isGenerating"
        class="px-6 py-3 bg-slate-600 text-white font-bold rounded-lg hover:bg-slate-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
      >
        <span v-if="isLoadingPreview" class="animate-spin">⟳</span>
        <span>Preview Outline</span>
      </button>
      <button
        v-else
        type="button"
        @click="$emit('generate')"
        :disabled="isGenerating || isLoadingPreview"
        class="px-8 py-3 bg-green-600 text-white font-bold rounded-lg hover:bg-green-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
      >
        <span v-if="isGenerating" class="animate-spin">⟳</span>
        <span>{{ isGenerating ? 'Generating Slides...' : 'Generate Slides' }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'

const props = defineProps({
  config: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['back', 'generate'])

const previewOutline = ref(null)
const isLoadingPreview = ref(false)
const isGenerating = ref(false)
const previewError = ref(null)

async function generatePreview() {
  isLoadingPreview.value = true
  previewError.value = null

  try {
    const response = await api.post('/slide-decks/preview', {
      course_id: props.config.courseId,
      title: props.config.title,
      description: props.config.description || '',
      topics: props.config.topics,
      num_slides: props.config.numSlides,
      format: props.config.format,
      include_graphs: props.config.includeGraphs,
      graph_types: props.config.graphTypes
    })

    previewOutline.value = response.data.outline || []
  } catch (error) {
    console.error('Preview generation failed:', error)
    previewError.value = error.response?.data?.detail || error.message
  } finally {
    isLoadingPreview.value = false
  }
}

onMounted(() => {
  generatePreview()
})
</script>

<style scoped></style>
