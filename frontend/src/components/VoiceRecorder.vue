<template>
  <div class="voice-recorder">
    <!-- Voice Mode Toggle -->
    <div class="mode-toggle mb-4">
      <button
        @click="$emit('toggle-mode')"  
        class="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200"
      >
        ← Back to text mode
      </button>
    </div>

    <!-- Recording Interface -->
    <div class="recording-container">
      <div class="flex flex-col items-center space-y-6">
        
        <!-- Status Display -->
        <div class="text-center">
          <p class="text-lg font-medium dark:text-gray-200">
            {{ statusText }}
          </p>
          <p v-if="transcript" class="text-sm text-gray-600 dark:text-gray-400 mt-2">
            "{{ transcript }}"
          </p>
        </div>

        <!-- Microphone Button -->
        <div class="relative">
          <!-- Pulsing Animation when recording -->
          <div
            v-if="isRecording"
            class="absolute inset-0 rounded-full bg-red-400 opacity-75 animate-ping"
          ></div>
          
          <button
            @click="toggleRecording"
            :disabled="isProcessing"
            :class="micButtonClass"
            class="relative z-10 w-24 h-24 rounded-full flex items-center justify-center transition-all duration-300 shadow-lg"
          >
            <Mic v-if="!isRecording" :size="40" />
            <Square v-else :size="30" />
          </button>
        </div>

        <!-- Recording Duration -->
        <div v-if="isRecording" class="text-2xl font-mono dark:text-gray-200">
          {{ formattedDuration }}
        </div>

        <!-- Instructions -->
        <div class="text-center max-w-md">
          <p class="text-sm text-gray-600 dark:text-gray-400">
            <template v-if="state === 'idle'">
              Click the microphone to start recording your question
            </template>
            <template v-else-if="state === 'requesting'">
              Requesting microphone permission...
            </template>
            <template v-else-if="state === 'recording'">
              Speak your question clearly. Click to stop recording.
            </template>
            <template v-else-if="state === 'processing'">
              Processing your query...
            </template>
          </p>
        </div>

        <!-- Error Display -->
        <div v-if="error" class="mt-4 p-4 bg-red-50 dark:bg-red-900/20 rounded-lg max-w-md">
          <p class="text-red-600 dark:text-red-400 text-sm">
            {{ error }}
          </p>
          <button
            @click="clearError"
            class="mt-2 text-sm text-red-700 dark:text-red-300 underline"
          >
            Dismiss
          </button>
        </div>

        <!-- Audio Player for Response -->
        <VoicePlayer
          v-if="audioResponse"
          :audioUrl="audioResponse"
          :transcript="answerText"
          @playback-end="handlePlaybackEnd"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import { Mic, Square } from 'lucide-vue-next'
import VoicePlayer from './VoicePlayer.vue'
import { chatService } from '@/api/chat'

const emit = defineEmits(['toggle-mode', 'voice-query-complete'])

// State management
const state = ref('idle') // idle, requesting, recording, processing, playing, error
const isRecording = computed(() => state.value === 'recording')
const isProcessing = computed(() => state.value === 'processing')

// Recording state
const mediaRecorder = ref(null)
const audioChunks = ref([])
const recordingStartTime = ref(null)
const recordingDuration = ref(0)
const durationInterval = ref(null)

// Response state
const transcript = ref('')
const audioResponse = ref(null)
const answerText = ref('')
const error = ref('')

// Status text
const statusText = computed(() => {
  switch (state.value) {
    case 'idle':
      return 'Ready to listen'
    case 'requesting':
      return 'Requesting microphone access...'
    case 'recording':
      return 'Listening...'
    case 'processing':
      return 'Thinking...'
    case 'playing':
      return 'Playing response'
    default:
      return 'Ready'
  }
})

// Mic button styling
const micButtonClass = computed(() => ({
  'bg-indigo-600 hover:bg-indigo-700 text-white': !isRecording.value && !isProcessing.value,
  'bg-red-600 hover:bg-red-700 text-white': isRecording.value,
  'bg-gray-400 text-gray-200 cursor-not-allowed': isProcessing.value
}))

// Formatted duration (MM:SS)
const formattedDuration = computed(() => {
  const minutes = Math.floor(recordingDuration.value / 60)
  const seconds = recordingDuration.value % 60
  return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
})

// Toggle recording
async function toggleRecording() {
  if (isRecording.value) {
    stopRecording()
  } else {
    await startRecording()
  }
}

// Start recording
async function startRecording() {
  try {
    state.value = 'requesting'
    error.value = ''
    
    // Request microphone permission
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    
    // Create MediaRecorder
    mediaRecorder.value = new MediaRecorder(stream)
    audioChunks.value = []
    
    // Handle data available
    mediaRecorder.value.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.value.push(event.data)
      }
    }
    
    // Handle recording stop
    mediaRecorder.value.onstop = async () => {
      // Stop all tracks
      stream.getTracks().forEach(track => track.stop())
      
      // Create audio blob
      const audioBlob = new Blob(audioChunks.value, { type: 'audio/webm' })
      
      // Send to backend
      await processVoiceQuery(audioBlob)
    }
    
    // Start recording
    mediaRecorder.value.start()
    state.value = 'recording'
    recordingStartTime.value = Date.now()
    recordingDuration.value = 0
    
    // Start duration counter
    durationInterval.value = setInterval(() => {
      recordingDuration.value = Math.floor((Date.now() - recordingStartTime.value) / 1000)
    }, 1000)
    
  } catch (err) {
    console.error('Failed to start recording:', err)
    state.value = 'idle'
    
    if (err.name === 'NotAllowedError') {
      error.value = 'Microphone permission denied. Please allow microphone access and try again.'
    } else if (err.name === 'NotFoundError') {
      error.value = 'No microphone found. Please connect a microphone and try again.'
    } else {
      error.value = `Failed to start recording: ${err.message}`
    }
  }
}

// Stop recording
function stopRecording() {
  if (mediaRecorder.value && mediaRecorder.value.state === 'recording') {
    mediaRecorder.value.stop()
    
    // Clear duration counter
    if (durationInterval.value) {
      clearInterval(durationInterval.value)
      durationInterval.value = null
    }
  }
}

// Process voice query
async function processVoiceQuery(audioBlob) {
  try {
    state.value = 'processing'
    
    // Create FormData
    const formData = new FormData()
    formData.append('audio', audioBlob, 'recording.webm')
    
    // Optional: Add chat_id if continuing conversation
    // formData.append('chat_id', chatId.value)
    
    // Call voice API
    const response = await fetch('http://localhost:8000/api/voice/query', {
      method: 'POST',
      body: formData
    })
    
    if (!response.ok) {
      throw new Error(`Server error: ${response.statusText}`)
    }
    
    // Get response headers
    const headers = response.headers
    transcript.value = headers.get('X-Transcript') || ''
    answerText.value = headers.get('X-Answer') || ''
    const language = headers.get('X-Language') || ''
    
    // Get audio blob
    const responseBlob = await response.blob()
    audioResponse.value = URL.createObjectURL(responseBlob)
    
    state.value = 'playing'
    
    // Emit event
    emit('voice-query-complete', {
      transcript: transcript.value,
      answer: answerText.value,
      language
    })
    
  } catch (err) {
    console.error('Voice query failed:', err)
    state.value = 'error'
    error.value = `Failed to process voice query: ${err.message}`
  }
}

// Handle playback end
function handlePlaybackEnd() {
  state.value = 'idle'
  audioResponse.value = null
  transcript.value = ''
  answerText.value = ''
}

// Clear error
function clearError() {
  error.value = ''
  state.value = 'idle'
}

// Cleanup on unmount
onUnmounted(() => {
  if (durationInterval.value) {
    clearInterval(durationInterval.value)
  }
  if (audioResponse.value) {
    URL.revokeObjectURL(audioResponse.value)
  }
})
</script>

<style scoped>
.recording-container {
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

@keyframes ping {
  75%, 100% {
    transform: scale(1.5);
    opacity: 0;
  }
}

.animate-ping {
  animation: ping 1s cubic-bezier(0, 0, 0.2, 1) infinite;
}
</style>
