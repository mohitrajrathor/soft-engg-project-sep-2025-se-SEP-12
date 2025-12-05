<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  Plus, 
  RefreshCw, 
  Search, 
  Trash2, 
  Eye, 
  MoreHorizontal, 
  Database, 
  Calendar, 
  Layers, 
  CheckCircle, 
  XCircle,
  Loader2,
  ChevronLeft,
  ChevronRight
} from 'lucide-vue-next'
import { adminService } from '@/api/admin'

const router = useRouter()
const route = useRoute()

const sources = ref([])
const loading = ref(true)
const total = ref(0)
const pages = ref(1)
const deleting = ref(null)

// Filters
const filters = ref({
  page: parseInt(route.query.page) || 1,
  search: route.query.search || '',
  is_active: route.query.is_active || 'all',
  category: route.query.category || ''
})

const fetchSources = async () => {
  loading.value = true
  try {
    const params = {
      page: filters.value.page,
      size: 10,
      search: filters.value.search,
      is_active: filters.value.is_active !== 'all' ? filters.value.is_active : undefined,
      category: filters.value.category
    }
    
    const data = await adminService.getKnowledgeSources(params)
    sources.value = data.items
    total.value = data.total
    pages.value = data.pages
    filters.value.page = data.page
  } catch (error) {
    console.error('Error fetching sources:', error)
  } finally {
    loading.value = false
  }
}

// Watch filters to refetch
watch(filters, () => {
  // Update URL
  const query = { ...filters.value }
  if (query.is_active === 'all') delete query.is_active
  if (!query.search) delete query.search
  if (!query.category) delete query.category
  if (query.page === 1) delete query.page
  
  router.replace({ query })
  fetchSources()
}, { deep: true })

onMounted(() => {
  fetchSources()
})

const handlePageChange = (newPage) => {
  if (newPage >= 1 && newPage <= pages.value) {
    filters.value.page = newPage
  }
}

const handleDelete = async (id) => {
  if (!confirm('Are you sure you want to delete this source?')) return
  
  deleting.value = id
  try {
    await adminService.deleteKnowledgeSource(id)
    fetchSources()
  } catch (error) {
    console.error('Error deleting source:', error)
    alert('Failed to delete source')
  } finally {
    deleting.value = null
  }
}

const truncateText = (text, maxLength = 100) => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Knowledge Sources</h1>
        <p class="text-sm text-gray-500 dark:text-gray-400">Manage your knowledge base and semantic search</p>
      </div>
      <div class="flex items-center gap-2">
        <button 
          @click="router.push('/admin/knowledge/add')"
          class="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors"
        >
          <Plus class="h-4 w-4" />
          Add Source
        </button>
        <button 
          @click="fetchSources"
          class="p-2 text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-800 rounded-lg transition-colors"
          :disabled="loading"
        >
          <RefreshCw class="h-4 w-4" :class="{ 'animate-spin': loading }" />
        </button>
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 text-center">
        <div class="text-2xl font-bold text-gray-900 dark:text-white">{{ total }}</div>
        <div class="text-xs text-gray-500">Total Sources</div>
      </div>
      <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 text-center">
        <div class="text-2xl font-bold text-green-600">{{ sources.filter(s => s.is_active).length }}</div>
        <div class="text-xs text-gray-500">Active</div>
      </div>
      <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 text-center">
        <div class="text-2xl font-bold text-gray-600">{{ sources.filter(s => !s.is_active).length }}</div>
        <div class="text-xs text-gray-500">Inactive</div>
      </div>
      <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 text-center">
        <div class="text-2xl font-bold text-blue-600">{{ sources.reduce((acc, s) => acc + (s.chunk_count || 0), 0) }}</div>
        <div class="text-xs text-gray-500">Total Chunks</div>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 flex flex-col sm:flex-row gap-4">
      <div class="relative flex-1">
        <Search class="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
        <input 
          v-model.lazy="filters.search"
          type="text"
          placeholder="Search sources..."
          class="w-full pl-9 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-transparent focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
        >
      </div>
      <select 
        v-model="filters.is_active"
        class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-transparent focus:ring-2 focus:ring-indigo-500"
      >
        <option value="all">All Statuses</option>
        <option value="true">Active</option>
        <option value="false">Inactive</option>
      </select>
      <input 
        v-model.lazy="filters.category"
        type="text"
        placeholder="Category..."
        class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-transparent focus:ring-2 focus:ring-indigo-500"
      >
    </div>

    <!-- Table -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-sm text-left">
          <thead class="bg-gray-50 dark:bg-gray-700/50 text-gray-500 dark:text-gray-400 uppercase text-xs">
            <tr>
              <th class="px-6 py-3 font-medium">Title</th>
              <th class="px-6 py-3 font-medium">Category</th>
              <th class="px-6 py-3 font-medium">Status</th>
              <th class="px-6 py-3 font-medium">Chunks</th>
              <th class="px-6 py-3 font-medium">Created</th>
              <th class="px-6 py-3 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-if="loading">
              <td colspan="6" class="px-6 py-8 text-center">
                <Loader2 class="h-8 w-8 animate-spin mx-auto text-gray-400" />
              </td>
            </tr>
            <tr v-else-if="sources.length === 0">
              <td colspan="6" class="px-6 py-8 text-center text-gray-500">
                No sources found.
              </td>
            </tr>
            <tr v-for="source in sources" :key="source.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
              <td class="px-6 py-4">
                <div class="font-medium text-gray-900 dark:text-white">{{ source.title }}</div>
                <div class="text-xs text-gray-500 mt-1">{{ truncateText(source.description || source.content) }}</div>
              </td>
              <td class="px-6 py-4">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300">
                  <Layers class="h-3 w-3 mr-1" />
                  {{ source.category }}
                </span>
              </td>
              <td class="px-6 py-4">
                <span 
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                  :class="source.is_active ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-400'"
                >
                  <component :is="source.is_active ? CheckCircle : XCircle" class="h-3 w-3 mr-1" />
                  {{ source.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td class="px-6 py-4 text-gray-500">
                <div class="flex items-center gap-1">
                  <Database class="h-3 w-3" />
                  {{ source.chunk_count || 0 }}
                </div>
              </td>
              <td class="px-6 py-4 text-gray-500">
                <div class="flex items-center gap-1">
                  <Calendar class="h-3 w-3" />
                  {{ new Date(source.created_at).toLocaleDateString() }}
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center gap-2">
                  <button 
                    @click="router.push(`/admin/knowledge/${source.id}`)"
                    class="text-indigo-600 hover:text-indigo-900 dark:hover:text-indigo-400 transition-colors"
                    title="View Details"
                  >
                    <Eye class="h-4 w-4" />
                  </button>
                  <button 
                    @click="handleDelete(source.id)"
                    class="text-red-600 hover:text-red-900 dark:hover:text-red-400 transition-colors"
                    :disabled="deleting === source.id"
                    title="Delete"
                  >
                    <Trash2 class="h-4 w-4" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="pages > 1" class="px-6 py-4 border-t border-gray-200 dark:border-gray-700 flex items-center justify-between">
        <span class="text-sm text-gray-500">
          Page {{ filters.page }} of {{ pages }}
        </span>
        <div class="flex gap-2">
          <button 
            @click="handlePageChange(filters.page - 1)"
            :disabled="filters.page === 1"
            class="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50"
          >
            <ChevronLeft class="h-5 w-5" />
          </button>
          <button 
            @click="handlePageChange(filters.page + 1)"
            :disabled="filters.page === pages"
            class="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50"
          >
            <ChevronRight class="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
