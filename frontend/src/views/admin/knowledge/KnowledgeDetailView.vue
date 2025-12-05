<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  ArrowLeft, 
  Edit, 
  Trash2, 
  CheckCircle, 
  XCircle,
  Loader2,
  Calendar,
  Database,
  Layers,
  FileText,
  Hash,
  Type
} from 'lucide-vue-next'
import { adminService } from '@/api/admin'

const router = useRouter()
const route = useRoute()

const source = ref(null)
const loading = ref(true)
const error = ref(null)
const deleting = ref(false)

const fetchSourceDetail = async () => {
  loading.value = true
  error.value = null
  try {
    const data = await adminService.getKnowledgeSourceDetail(route.params.id)
    source.value = data
  } catch (err) {
    console.error('Error fetching source detail:', err)
    error.value = err.response?.data?.detail || 'Failed to load source details'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchSourceDetail()
})

const handleDelete = async () => {
  if (!confirm('Are you sure you want to delete this source?')) return
  
  deleting.value = true
  try {
    await adminService.deleteKnowledgeSource(route.params.id)
    router.push('/admin/knowledge')
  } catch (err) {
    console.error('Error deleting source:', err)
    alert('Failed to delete source')
  } finally {
    deleting.value = false
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString()
}
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div class="flex items-center gap-4">
        <button 
          @click="router.push('/admin/knowledge')"
          class="p-2 text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-800 rounded-lg transition-colors"
        >
          <ArrowLeft class="h-5 w-5" />
        </button>
        <div>
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Knowledge Source Details</h1>
          <p class="text-sm text-gray-500 dark:text-gray-400">View source information and chunks</p>
        </div>
      </div>
      
      <div v-if="source" class="flex items-center gap-2">
        <button 
          @click="router.push(`/admin/knowledge/${route.params.id}/edit`)"
          class="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors"
        >
          <Edit class="h-4 w-4" />
          Edit
        </button>
        <button 
          @click="handleDelete"
          :disabled="deleting"
          class="flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors disabled:opacity-50"
        >
          <Trash2 class="h-4 w-4" />
          Delete
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-12">
      <Loader2 class="h-8 w-8 animate-spin text-gray-400" />
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6">
      <p class="text-red-800 dark:text-red-400">{{ error }}</p>
    </div>

    <!-- Content -->
    <div v-else-if="source" class="space-y-6">
      <!-- Source Information Card -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-4">Source Information</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Title -->
          <div>
            <label class="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Title</label>
            <p class="text-gray-900 dark:text-white">{{ source.title }}</p>
          </div>

          <!-- Category -->
          <div>
            <label class="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Category</label>
            <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300">
              <Layers class="h-4 w-4 mr-1" />
              {{ source.category }}
            </span>
          </div>

          <!-- Status -->
          <div>
            <label class="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Status</label>
            <span 
              class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
              :class="source.is_active ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-400'"
            >
              <component :is="source.is_active ? CheckCircle : XCircle" class="h-4 w-4 mr-1" />
              {{ source.is_active ? 'Active' : 'Inactive' }}
            </span>
          </div>

          <!-- Chunk Count -->
          <div>
            <label class="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Total Chunks</label>
            <div class="flex items-center gap-2">
              <Database class="h-4 w-4 text-gray-500" />
              <span class="text-gray-900 dark:text-white font-semibold">{{ source.chunk_count }}</span>
            </div>
          </div>

          <!-- Created At -->
          <div>
            <label class="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Created</label>
            <div class="flex items-center gap-2">
              <Calendar class="h-4 w-4 text-gray-500" />
              <span class="text-gray-900 dark:text-white text-sm">{{ formatDate(source.created_at) }}</span>
            </div>
          </div>

          <!-- Updated At -->
          <div>
            <label class="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Last Updated</label>
            <div class="flex items-center gap-2">
              <Calendar class="h-4 w-4 text-gray-500" />
              <span class="text-gray-900 dark:text-white text-sm">{{ formatDate(source.updated_at) }}</span>
            </div>
          </div>
        </div>

        <!-- Description -->
        <div v-if="source.description" class="mt-6">
          <label class="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Description</label>
          <p class="text-gray-900 dark:text-white">{{ source.description }}</p>
        </div>

        <!-- Original Content -->
        <div v-if="source.content" class="mt-6">
          <label class="block text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">Original Content</label>
          <div class="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 max-h-64 overflow-y-auto">
            <p class="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap">{{ source.content }}</p>
          </div>
        </div>
      </div>

      <!-- Chunks Section -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Chunks</h2>
          <span class="text-sm text-gray-500 dark:text-gray-400">{{ source.chunks.length }} total</span>
        </div>

        <div v-if="source.chunks.length === 0" class="text-center py-8 text-gray-500">
          No chunks found for this source.
        </div>

        <div v-else class="space-y-4">
          <div 
            v-for="chunk in source.chunks" 
            :key="chunk.id"
            class="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 border border-gray-200 dark:border-gray-700"
          >
            <!-- Chunk Header -->
            <div class="flex items-start justify-between mb-3">
              <div class="flex items-center gap-3 text-sm text-gray-500 dark:text-gray-400">
                <div class="flex items-center gap-1">
                  <Hash class="h-4 w-4" />
                  <span>Index: {{ chunk.index }}</span>
                </div>
                <div class="flex items-center gap-1">
                  <Type class="h-4 w-4" />
                  <span>{{ chunk.word_count }} words</span>
                </div>
                <div class="flex items-center gap-1">
                  <FileText class="h-4 w-4" />
                  <span>{{ chunk.token_count }} tokens</span>
                </div>
              </div>
              <span 
                class="px-2 py-1 rounded text-xs font-medium"
                :class="chunk.has_embedding ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' : 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'"
              >
                {{ chunk.has_embedding ? 'Embedded' : 'No Embedding' }}
              </span>
            </div>

            <!-- Chunk Text -->
            <div class="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
              <p class="whitespace-pre-wrap">{{ chunk.text }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
