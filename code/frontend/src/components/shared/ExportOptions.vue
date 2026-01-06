<script setup>
import { ref } from 'vue'
import { 
  DocumentTextIcon, 
  ClipboardDocumentListIcon, 
  EnvelopeIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'
import api from '@/api/axios'

const props = defineProps({
  title: {
    type: String,
    default: 'Export Options'
  },
  courseCode: {
    type: String,
    required: true
  },
  period: {
    type: String,
    default: 'weekly'
  },
  source: {
    type: String,
    default: 'all'
  }
})

// Email modal state
const showEmailModal = ref(false)
const emailAddress = ref('')
const emailError = ref('')
const isExporting = ref(false)
const exportSuccess = ref('')

// Export handlers
const exportAsPDF = async () => {
  try {
    isExporting.value = true
    const response = await api.get('/ta/doubts/export/pdf', {
      params: {
        course_code: props.courseCode,
        period: props.period,
        source: props.source
      },
      responseType: 'blob'
    })

    // Create download link
    const blob = new Blob([response.data], { type: 'application/pdf' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `doubt-summary-${props.courseCode}-${props.period}.pdf`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    exportSuccess.value = 'PDF exported successfully!'
    setTimeout(() => exportSuccess.value = '', 3000)
  } catch (error) {
    console.error('PDF export failed:', error)
    alert('Failed to export PDF. Please try again.')
  } finally {
    isExporting.value = false
  }
}

const exportAsCSV = async () => {
  try {
    isExporting.value = true
    const response = await api.get('/ta/doubts/export/csv', {
      params: {
        course_code: props.courseCode,
        period: props.period,
        source: props.source
      },
      responseType: 'blob'
    })

    // Create download link
    const blob = new Blob([response.data], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `doubt-summary-${props.courseCode}-${props.period}.csv`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    exportSuccess.value = 'CSV exported successfully!'
    setTimeout(() => exportSuccess.value = '', 3000)
  } catch (error) {
    console.error('CSV export failed:', error)
    alert('Failed to export CSV. Please try again.')
  } finally {
    isExporting.value = false
  }
}

const openEmailModal = () => {
  showEmailModal.value = true
  emailAddress.value = ''
  emailError.value = ''
}

const closeEmailModal = () => {
  showEmailModal.value = false
  emailAddress.value = ''
  emailError.value = ''
}

const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

const sendEmailReport = async () => {
  emailError.value = ''
  
  if (!emailAddress.value) {
    emailError.value = 'Email address is required'
    return
  }
  
  if (!validateEmail(emailAddress.value)) {
    emailError.value = 'Please enter a valid email address'
    return
  }

  try {
    isExporting.value = true
    const response = await api.post('/ta/doubts/export/email', {
      course_code: props.courseCode,
      period: props.period,
      source: props.source,
      recipient_email: emailAddress.value
    })

    exportSuccess.value = response.data.message || `Report is being sent to ${emailAddress.value}!`
    setTimeout(() => exportSuccess.value = '', 5000)
    closeEmailModal()
  } catch (error) {
    console.error('Email send failed:', error)
    const errorDetail = error.response?.data?.detail
    
    // Provide user-friendly error messages
    if (typeof errorDetail === 'string') {
      emailError.value = errorDetail
    } else if (error.response?.status === 503) {
      emailError.value = 'Email service is temporarily unavailable. Please try again later or contact support.'
    } else if (error.response?.status === 500) {
      emailError.value = 'An error occurred while sending the email. Please try again.'
    } else {
      emailError.value = 'Failed to send email. Please check your connection and try again.'
    }
  } finally {
    isExporting.value = false
  }
}
</script>

<template>
  <div class="bg-white rounded-2xl shadow-2xl p-5 border border-gray-200">
    <div class="font-bold mb-4 text-base text-black">{{ title }}</div>
    
    <!-- Success message -->
    <div v-if="exportSuccess" class="mb-3 p-2 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm">
      {{ exportSuccess }}
    </div>

    <!-- Export buttons -->
    <button 
      @click="exportAsPDF" 
      :disabled="isExporting"
      class="w-full mb-2 px-4 py-3 rounded-lg bg-gray-100 text-black font-semibold hover:bg-gray-200 shadow-sm transition-colors flex items-center justify-center gap-2 border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      <DocumentTextIcon class="w-5 h-5" />
      <span>{{ isExporting ? 'Exporting...' : 'Export as PDF' }}</span>
    </button>
    
    <button 
      @click="exportAsCSV" 
      :disabled="isExporting"
      class="w-full mb-2 px-4 py-3 rounded-lg bg-gray-100 text-black font-semibold hover:bg-gray-200 shadow-sm transition-colors flex items-center justify-center gap-2 border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      <ClipboardDocumentListIcon class="w-5 h-5" />
      <span>{{ isExporting ? 'Exporting...' : 'Export as CSV' }}</span>
    </button>
    
    <button 
      @click="openEmailModal" 
      :disabled="isExporting"
      class="w-full px-4 py-3 rounded-lg bg-gray-100 text-black font-semibold hover:bg-gray-200 shadow-sm transition-colors flex items-center justify-center gap-2 border border-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
    >
      <EnvelopeIcon class="w-5 h-5" />
      <span>Email Report</span>
    </button>

    <!-- Email Modal -->
    <Teleport to="body">
      <div v-if="showEmailModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50" @click.self="closeEmailModal">
        <div class="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-md mx-4">
          <!-- Modal Header -->
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-xl font-bold text-black">Email Report</h3>
            <button @click="closeEmailModal" class="text-gray-500 hover:text-gray-700">
              <XMarkIcon class="w-6 h-6" />
            </button>
          </div>

          <!-- Email Input -->
          <div class="mb-4">
            <label class="block text-sm font-semibold text-gray-700 mb-2">
              Recipient Email Address
            </label>
            <input 
              v-model="emailAddress"
              type="email" 
              placeholder="example@university.edu"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
              @keyup.enter="sendEmailReport"
            />
            <p v-if="emailError" class="mt-2 text-sm text-red-600">{{ emailError }}</p>
          </div>

          <!-- Modal Actions -->
          <div class="flex gap-3">
            <button 
              @click="closeEmailModal" 
              :disabled="isExporting"
              class="flex-1 px-4 py-2 bg-gray-200 text-black rounded-lg hover:bg-gray-300 font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Cancel
            </button>
            <button 
              @click="sendEmailReport" 
              :disabled="isExporting"
              class="flex-1 px-4 py-2 bg-blue-600 text-black rounded-lg hover:bg-blue-700 font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ isExporting ? 'Queueing...' : 'Send Report' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
