<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, Upload, Loader2, CheckCircle, FileText, X, AlertCircle } from 'lucide-vue-next'
import { adminService } from '@/api/admin'

const router = useRouter()

const uploadMode = ref('file') // 'file' or 'text'
const selectedFile = ref(null)
const isDragging = ref(false)
const loading = ref(false)
const success = ref(false)
const error = ref('')

const form = ref({
  title: '',
  content: '',
  category: 'General',
  description: ''
})

const categories = [
  'General',
  'Admission',
  'Courses',
  'Placement',
  'Fees',
  'Exam'
]

const fileInfo = computed(() => {
  if (!selectedFile.value) return null
  const size = selectedFile.value.size
  const sizeKB = (size / 1024).toFixed(2)
  const sizeMB = (size / (1024 * 1024)).toFixed(2)
  
  return {
    name: selectedFile.value.name,
    size: size < 1024 * 1024 ? `${sizeKB} KB` : `${sizeMB} MB`,
    type: selectedFile.value.type
  }
})

const acceptedFileTypes = '.pdf,.docx,.txt,.xlsx,.xls,.csv'
const maxFileSize = 10 * 1024 * 1024 // 10 MB

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    validateAndSetFile(file)
  }
}

const handleDrop = (event) => {
  isDragging.value = false
  const file = event.dataTransfer.files[0]
  if (file) {
    validateAndSetFile(file)
  }
}

const validateAndSetFile = (file) => {
  error.value = ''
  
  // Check file type
  const validTypes = [
    'application/pdf', 
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'text/plain',
    'text/csv'
  ]
  const validExtensions = /\.(pdf|docx|txt|xlsx|xls|csv)$/i
  
  if (!validTypes.includes(file.type) && !file.name.match(validExtensions)) {
    error.value = 'Invalid file type. Please upload PDF, DOCX, TXT, XLSX, XLS, or CSV files.'
    return
  }
  
  // Check file size
  if (file.size > maxFileSize) {
    error.value = `File too large. Maximum size is ${maxFileSize / (1024 * 1024)} MB.`
    return
  }
  
  selectedFile.value = file
  
  // Auto-fill title from filename if empty
  if (!form.value.title) {
    form.value.title = file.name.replace(/\.[^/.]+$/, '')
  }
}

const removeFile = () => {
  selectedFile.value = null
  error.value = ''
}

const handleSubmit = async () => {
  error.value = ''
  
  if (uploadMode.value === 'file') {
    if (!selectedFile.value) {
      error.value = 'Please select a file to upload'
      return
    }
    if (!form.value.title) {
      error.value = 'Please enter a title'
      return
    }
    
    await uploadFile()
  } else {
    if (!form.value.title || !form.value.content) {
      error.value = 'Please fill in all required fields'
      return
    }
    
    await uploadText()
  }
}

const uploadFile = async () => {
  loading.value = true
  try {
    await adminService.uploadKnowledgeFile(
      selectedFile.value,
      form.value.title,
      form.value.category,
      form.value.description
    )
    success.value = true
    setTimeout(() => {
      router.push('/admin/knowledge')
    }, 1500)
  } catch (err) {
    console.error('Error uploading file:', err)
    error.value = err.response?.data?.detail || 'Failed to upload file'
  } finally {
    loading.value = false
  }
}

const uploadText = async () => {
  loading.value = true
  try {
    await adminService.ingestKnowledge(form.value)
    success.value = true
    setTimeout(() => {
      router.push('/admin/knowledge')
    }, 1500)
  } catch (err) {
    console.error('Error ingesting knowledge:', err)
    error.value = err.response?.data?.detail || 'Failed to ingest knowledge'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-3xl mx-auto space-y-6 p-6">
    <div class="flex items-center gap-4">
      <button 
        @click="router.back()"
        class="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full transition-colors"
      >
        <ArrowLeft class="h-5 w-5 text-gray-600 dark:text-gray-400" />
      </button>
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Add Knowledge Source</h1>
        <p class="text-sm text-gray-500 dark:text-gray-400">Upload a file or paste text content</p>
      </div>
    </div>

    <!-- Upload Mode Tabs -->
    <div class="flex gap-2 p-1 bg-gray-100 dark:bg-gray-800 rounded-lg">
      <button
        @click="uploadMode = 'file'"
        :class="[
          'flex-1 py-2 px-4 rounded-md font-medium transition-all',
          uploadMode === 'file' 
            ? 'bg-white dark:bg-gray-700 text-indigo-600 dark:text-indigo-400 shadow-sm' 
            : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
        ]"
      >
        <Upload class="h-4 w-4 inline mr-2" />
        Upload File
      </button>
      <button
        @click="uploadMode = 'text'"
        :class="[
          'flex-1 py-2 px-4 rounded-md font-medium transition-all',
          uploadMode === 'text' 
            ? 'bg-white dark:bg-gray-700 text-indigo-600 dark:text-indigo-400 shadow-sm' 
            : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
        ]"
      >
        <FileText class="h-4 w-4 inline mr-2" />
        Paste Text
      </button>
    </div>

    <!-- Error Alert -->
    <div v-if="error" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 flex items-start gap-3">
      <AlertCircle class="h-5 w-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
      <div class="flex-1">
        <p class="text-sm font-medium text-red-800 dark:text-red-200">{{ error }}</p>
      </div>
      <button @click="error = ''" class="text-red-600 dark:text-red-400 hover:text-red-800">
        <X class="h-4 w-4" />
      </button>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      <form @submit.prevent="handleSubmit" class="space-y-6">
        
        <!-- File Upload Mode -->
        <div v-if="uploadMode === 'file'" class="space-y-6">
          <!-- File Drop Zone -->
          <div
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleDrop"
            :class="[
              'relative border-2 border-dashed rounded-lg p-8 text-center transition-all cursor-pointer',
              isDragging 
                ? 'border-indigo-500 bg-indigo-50 dark:bg-indigo-900/20' 
                : 'border-gray-300 dark:border-gray-600 hover:border-indigo-400 dark:hover:border-indigo-500'
            ]"
            @click="$refs.fileInput.click()"
          >
            <input
              ref="fileInput"
              type="file"
              :accept="acceptedFileTypes"
              @change="handleFileSelect"
              class="hidden"
            />
            
            <div v-if="!selectedFile">
              <Upload class="h-12 w-12 mx-auto text-gray-400 dark:text-gray-500 mb-4" />
              <p class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Drop your file here, or <span class="text-indigo-600 dark:text-indigo-400">browse</span>
              </p>
              <p class="text-xs text-gray-500 dark:text-gray-400">
                Supports PDF, DOCX, TXT, XLSX, XLS, CSV (max 10 MB)
              </p>
            </div>
            
            <div v-else class="flex items-center justify-between bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
              <div class="flex items-center gap-3">
                <div class="p-2 bg-indigo-100 dark:bg-indigo-900/30 rounded-lg">
                  <FileText class="h-6 w-6 text-indigo-600 dark:text-indigo-400" />
                </div>
                <div class="text-left">
                  <p class="text-sm font-medium text-gray-900 dark:text-white">{{ fileInfo.name }}</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">{{ fileInfo.size }}</p>
                </div>
              </div>
              <button
                type="button"
                @click.stop="removeFile"
                class="p-2 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-full transition-colors"
              >
                <X class="h-4 w-4 text-gray-600 dark:text-gray-400" />
              </button>
            </div>
          </div>
        </div>

        <!-- Text Paste Mode -->
        <div v-if="uploadMode === 'text'">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Content
          </label>
          <textarea 
            v-model="form.content"
            required
            rows="8"
            class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-transparent focus:ring-2 focus:ring-indigo-500 dark:focus:ring-indigo-400 font-mono text-sm"
            placeholder="Paste text content here..."
          ></textarea>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-2">
            The system will automatically process and chunk this content for RAG.
          </p>
        </div>

        <!-- Common Fields -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Title <span class="text-red-500">*</span>
            </label>
            <input 
              v-model="form.title"
              type="text"
              required
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-transparent focus:ring-2 focus:ring-indigo-500"
              placeholder="e.g., Admission Guidelines 2025"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Category
            </label>
            <select 
              v-model="form.category"
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-transparent focus:ring-2 focus:ring-indigo-500"
            >
              <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
            </select>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Description (Optional)
          </label>
          <input 
            v-model="form.description"
            type="text"
            class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-transparent focus:ring-2 focus:ring-indigo-500"
            placeholder="Brief description of the content"
          />
        </div>

        <!-- Submit Button -->
        <div class="pt-4">
          <button 
            type="submit"
            :disabled="loading || success"
            class="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 disabled:cursor-not-allowed text-white py-3 rounded-lg transition-colors font-medium shadow-sm"
          >
            <span v-if="success" class="flex items-center gap-2">
              <CheckCircle class="h-5 w-5" />
              {{ uploadMode === 'file' ? 'Uploaded' : 'Ingested' }} Successfully!
            </span>
            <span v-else-if="loading" class="flex items-center gap-2">
              <Loader2 class="h-5 w-5 animate-spin" />
              Processing...
            </span>
            <span v-else class="flex items-center gap-2">
              <Upload class="h-5 w-5" />
              {{ uploadMode === 'file' ? 'Upload File' : 'Ingest Content' }}
            </span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
