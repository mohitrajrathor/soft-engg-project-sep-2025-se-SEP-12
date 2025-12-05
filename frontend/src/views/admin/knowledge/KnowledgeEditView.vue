<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  ArrowLeft, 
  Save,
  Loader2,
  AlertCircle
} from 'lucide-vue-next'
import { adminService } from '@/api/admin'

const router = useRouter()
const route = useRoute()

const loading = ref(true)
const saving = ref(false)
const error = ref(null)
const successMessage = ref(null)

// Form data
const form = ref({
  title: '',
  description: '',
  category: '',
  is_active: true
})

// Available categories (from CategoryEnum)
const categories = ref([
  'General',
  'Assessment',
  'Assignments',
  'Exams',
  'Grading',
  'Policies',
  'Resources',
  'Schedule'
])

const fetchSource = async () => {
  loading.value = true
  error.value = null
  try {
    const data = await adminService.getKnowledgeSourceDetail(route.params.id)
    form.value = {
      title: data.title,
      description: data.description || '',
      category: data.category,
      is_active: data.is_active
    }
  } catch (err) {
    console.error('Error fetching source:', err)
    error.value = err.response?.data?.detail || 'Failed to load source'
  } finally {
    loading.value = false
  }
}

const handleSave = async () => {
  // Validation
  if (!form.value.title.trim()) {
    error.value = 'Title is required'
    return
  }
  if (!form.value.category) {
    error.value = 'Category is required'
    return
  }

  saving.value = true
  error.value = null
  successMessage.value = null

  try {
    await adminService.updateKnowledgeSource(route.params.id, {
      title: form.value.title.trim(),
      description: form.value.description.trim() || null,
      category: form.value.category,
      is_active: form.value.is_active
    })
    
    successMessage.value = 'Knowledge source updated successfully!'
    
    // Redirect back to detail view after a short delay
    setTimeout(() => {
      router.push(`/admin/knowledge/${route.params.id}`)
    }, 1500)
  } catch (err) {
    console.error('Error updating source:', err)
    error.value = err.response?.data?.detail || 'Failed to update source'
  } finally {
    saving.value = false
  }
}

const handleCancel = () => {
  router.push(`/admin/knowledge/${route.params.id}`)
}

onMounted(() => {
  fetchSource()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center gap-4">
      <button 
        @click="handleCancel"
        class="p-2 text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-800 rounded-lg transition-colors"
      >
        <ArrowLeft class="h-5 w-5" />
      </button>
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Edit Knowledge Source</h1>
        <p class="text-sm text-gray-500 dark:text-gray-400">Update source information</p>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <Loader2 class="h-8 w-8 animate-spin text-gray-400" />
    </div>

    <!-- Error State -->
    <div v-else-if="error && !form.title" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
      <div class="flex items-center gap-2 text-red-800 dark:text-red-400">
        <AlertCircle class="h-5 w-5" />
        <p>{{ error }}</p>
      </div>
    </div>

    <!-- Edit Form -->
    <div v-else class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      <!-- Success Message -->
      <div v-if="successMessage" class="mb-6 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
        <p class="text-green-800 dark:text-green-400">{{ successMessage }}</p>
      </div>

      <!-- Error Message -->
      <div v-if="error && form.title" class="mb-6 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
        <div class="flex items-center gap-2 text-red-800 dark:text-red-400">
          <AlertCircle class="h-5 w-5" />
          <p>{{ error }}</p>
        </div>
      </div>

      <form @submit.prevent="handleSave" class="space-y-6">
        <!-- Title -->
        <div>
          <label for="title" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Title <span class="text-red-500">*</span>
          </label>
          <input
            id="title"
            v-model="form.title"
            type="text"
            required
            class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            placeholder="Enter source title"
          />
        </div>

        <!-- Category -->
        <div>
          <label for="category" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Category <span class="text-red-500">*</span>
          </label>
          <select
            id="category"
            v-model="form.category"
            required
            class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          >
            <option value="">Select a category</option>
            <option v-for="cat in categories" :key="cat" :value="cat">
              {{ cat }}
            </option>
          </select>
        </div>

        <!-- Description -->
        <div>
          <label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Description
          </label>
          <textarea
            id="description"
            v-model="form.description"
            rows="4"
            class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            placeholder="Enter description (optional)"
          ></textarea>
        </div>

        <!-- Active Status -->
        <div class="flex items-center gap-3">
          <input
            id="is_active"
            v-model="form.is_active"
            type="checkbox"
            class="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
          />
          <label for="is_active" class="text-sm font-medium text-gray-700 dark:text-gray-300">
            Active (visible in search results)
          </label>
        </div>

        <!-- Action Buttons -->
        <div class="flex items-center gap-3 pt-4 border-t border-gray-200 dark:border-gray-700">
          <button
            type="submit"
            :disabled="saving"
            class="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Save class="h-4 w-4" />
            {{ saving ? 'Saving...' : 'Save Changes' }}
          </button>
          <button
            type="button"
            @click="handleCancel"
            :disabled="saving"
            class="px-6 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Cancel
          </button>
        </div>
      </form>

      <!-- Info Note -->
      <div class="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
        <p class="text-sm text-blue-800 dark:text-blue-400">
          <strong>Note:</strong> You can only edit the metadata (title, description, category, and status). 
          The original content and chunks cannot be modified. To update the content, delete this source and re-upload the file.
        </p>
      </div>
    </div>
  </div>
</template>
