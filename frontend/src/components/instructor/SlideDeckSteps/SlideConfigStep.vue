<template>
  <div class="w-full">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="font-extrabold text-4xl text-slate-900 tracking-tight">Create Slide Deck</h1>
      <p class="text-slate-500 mt-2">Step 1: Configure your presentation settings</p>
      <div class="mt-4 flex gap-1">
        <div class="flex-1 h-1 bg-blue-600 rounded-full"></div>
        <div class="flex-1 h-1 bg-slate-200 rounded-full"></div>
        <div class="flex-1 h-1 bg-slate-200 rounded-full"></div>
      </div>
    </div>

    <!-- Config Form -->
    <form @submit.prevent="handleNext" class="space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Course ID -->
        <div>
          <label class="block text-sm font-bold text-slate-700 mb-2">
            Course ID <span class="text-red-500">*</span>
          </label>
          <input
            v-model.number="form.courseId"
            type="number"
            min="1"
            placeholder="Enter course ID"
            required
            class="w-full px-4 py-3 bg-white border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition text-slate-800 placeholder-slate-400"
          />
        </div>

        <!-- Format -->
        <div>
          <label class="block text-sm font-bold text-slate-700 mb-2">
            Format <span class="text-red-500">*</span>
          </label>
          <select
            v-model="form.format"
            required
            class="w-full px-4 py-3 bg-white border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition text-slate-800"
          >
            <option value="presentation">Presentation (Concise)</option>
            <option value="document">Document (Detailed)</option>
          </select>
        </div>
      </div>

      <!-- Title -->
      <div>
        <label class="block text-sm font-bold text-slate-700 mb-2">
          Deck Title <span class="text-red-500">*</span>
        </label>
        <input
          v-model="form.title"
          type="text"
          placeholder="e.g., Python Fundamentals 101"
          required
          minlength="3"
          maxlength="100"
          class="w-full px-4 py-3 bg-white border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition text-slate-800 placeholder-slate-400 font-semibold"
        />
      </div>

      <!-- Description -->
      <div>
        <label class="block text-sm font-bold text-slate-700 mb-2">
          Context / Description
        </label>
        <textarea
          v-model="form.description"
          placeholder="Provide specific focus areas, learning objectives, or any special requirements..."
          rows="3"
          maxlength="500"
          class="w-full px-4 py-3 bg-white border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition text-slate-800 placeholder-slate-400 resize-none"
        ></textarea>
        <p class="text-xs text-slate-400 mt-1">{{ form.description.length }}/500</p>
      </div>

      <!-- Number of Slides -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label class="block text-sm font-bold text-slate-700 mb-2">
            Number of Slides <span class="text-red-500">*</span>
          </label>
          <input
            v-model.number="form.numSlides"
            type="number"
            min="2"
            max="20"
            required
            class="w-full px-4 py-3 bg-white border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition text-slate-800"
          />
          <p class="text-xs text-slate-400 mt-1">Between 2-20 slides</p>
        </div>

        <!-- Include Graphs -->
        <div>
          <label class="block text-sm font-bold text-slate-700 mb-2">
            Enhancements
          </label>
          <label class="flex items-center gap-3 p-3 border border-slate-300 rounded-xl hover:bg-blue-50 cursor-pointer transition">
            <input
              v-model="form.includeGraphs"
              type="checkbox"
              class="w-5 h-5 text-blue-600 rounded cursor-pointer"
            />
            <span class="text-sm font-medium text-slate-700">Include AI-Generated Graphs</span>
          </label>
        </div>
      </div>

      <!-- Graph Types -->
      <div v-if="form.includeGraphs" class="p-4 bg-blue-50 border border-blue-200 rounded-xl">
        <p class="text-sm font-bold text-slate-700 mb-3">Select Graph Types:</p>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <label
            v-for="type in graphTypeOptions"
            :key="type.value"
            class="flex items-center gap-2 p-2 border border-blue-200 rounded-lg hover:bg-white cursor-pointer transition"
          >
            <input
              :value="type.value"
              v-model="form.graphTypes"
              type="checkbox"
              class="w-4 h-4 text-blue-600 rounded"
            />
            <span class="text-sm text-slate-700">{{ type.label }}</span>
          </label>
        </div>
      </div>

      <!-- Topics Section -->
      <div class="border-t pt-6">
        <div class="flex items-center justify-between mb-3">
          <label class="block text-sm font-bold text-slate-700">
            Topics to Cover <span class="text-red-500">*</span>
          </label>
          <button
            type="button"
            @click="addTopic"
            class="text-xs font-bold text-blue-600 hover:text-blue-700 px-2 py-1"
          >
            + Add Topic
          </button>
        </div>

        <div class="space-y-2">
          <div v-for="(topic, idx) in form.topics" :key="idx" class="flex gap-2">
            <input
              v-model="form.topics[idx]"
              type="text"
              placeholder="Enter a topic..."
              class="flex-1 px-4 py-2 bg-white border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition text-slate-800 placeholder-slate-400"
            />
            <button
              v-if="form.topics.length > 1"
              type="button"
              @click="removeTopic(idx)"
              class="px-3 py-2 text-red-500 hover:bg-red-50 rounded-lg transition font-bold"
            >
              ✕
            </button>
          </div>
        </div>

        <p class="text-xs text-slate-400 mt-2">{{ form.topics.filter(t => t.trim()).length }} topic(s) added</p>
      </div>

      <!-- Action Buttons -->
      <div class="flex gap-3 justify-end pt-6">
        <button
          type="button"
          @click="$emit('cancel')"
          class="px-6 py-3 border border-slate-300 text-slate-700 font-bold rounded-lg hover:bg-slate-50 transition"
        >
          Cancel
        </button>
        <button
          type="submit"
          :disabled="isLoading || !isFormValid"
          class="px-8 py-3 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          <span v-if="!isLoading">Next: Preview</span>
          <span v-else class="animate-spin">⟳</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  initialConfig: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['next', 'cancel'])

const graphTypeOptions = [
  { value: 'bar', label: 'Bar Chart' },
  { value: 'line', label: 'Line Chart' },
  { value: 'pie', label: 'Pie Chart' },
  { value: 'scatter', label: 'Scatter Plot' }
]

const form = ref({
  courseId: props.initialConfig.courseId || null,
  title: props.initialConfig.title || '',
  description: props.initialConfig.description || '',
  format: props.initialConfig.format || 'presentation',
  numSlides: props.initialConfig.numSlides || 5,
  includeGraphs: props.initialConfig.includeGraphs || false,
  graphTypes: props.initialConfig.graphTypes || [],
  topics: props.initialConfig.topics || ['']
})

const isLoading = ref(false)

const isFormValid = computed(() => {
  return (
    form.value.courseId &&
    form.value.title.trim().length >= 3 &&
    form.value.numSlides >= 2 &&
    form.value.numSlides <= 20 &&
    form.value.topics.filter(t => t.trim()).length > 0
  )
})

function addTopic() {
  form.value.topics.push('')
}

function removeTopic(idx) {
  form.value.topics.splice(idx, 1)
}

async function handleNext() {
  isLoading.value = true
  try {
    emit('next', {
      courseId: form.value.courseId,
      title: form.value.title,
      description: form.value.description,
      format: form.value.format,
      numSlides: form.value.numSlides,
      includeGraphs: form.value.includeGraphs,
      graphTypes: form.value.graphTypes,
      topics: form.value.topics.filter(t => t.trim())
    })
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
input:focus,
textarea:focus,
select:focus {
  @apply shadow-lg;
}
</style>
