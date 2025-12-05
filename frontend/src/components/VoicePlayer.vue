<template>
  <div class="voice-player p-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg max-w-md w-full">
    <h3 class="text-lg font-semibold mb-4 dark:text-gray-200">Response</h3>
    
    <!-- Transcript Display -->
    <div v-if="transcript" class="mb-4 p-3 bg-gray-50 dark:bg-gray-700 rounded">
      <p class="text-sm text-gray-700 dark:text-gray-300">
        {{ transcript }}
      </p>
    </div>

    <!-- Audio Player -->
    <div class="audio-controls">
      <audio
        ref="audioElement"
        :src="audioUrl"
        @loadedmetadata="onLoadedMetadata"
        @timeupdate="onTimeUpdate"
        @ended="onEnded"
        @play="isPlaying = true"
        @pause="isPlaying = false"
        autoplay
      ></audio>

      <!-- Play/Pause Button -->
      <div class="flex items-center space-x-4">
        <button
          @click="togglePlay"
          class="w-12 h-12 rounded-full bg-indigo-600 hover:bg-indigo-700 text-white flex items-center justify-center transition-colors"
        >
          <Play v-if="!isPlaying" :size="24" />
          <Pause v-else :size="24" />
        </button>

        <!-- Progress Bar -->
        <div class="flex-1">
          <input
            type="range"
            min="0"
            :max="duration"
            v-model="currentTime"
            @input="seek"
            class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer"
          />
          <div class="flex justify-between text-xs text-gray-600 dark:text-gray-400 mt-1">
            <span>{{ formattedCurrentTime }}</span>
            <span>{{ formattedDuration }}</span>
          </div>
        </div>

        <!-- Volume Control -->
        <div class="flex items-center space-x-2">
          <button @click="toggleMute" class="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200">
            <Volume2 v-if="!isMuted && volume > 0.5" :size="20" />
            <Volume1 v-else-if="!isMuted && volume > 0" :size="20" />
            <VolumeX v-else :size="20" />
          </button>
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            v-model="volume"
            @input="updateVolume"
            class="w-20 h-2 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer"
          />
        </div>

        <!-- Replay Button -->
        <button
          @click="replay"
          class="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200"
          title="Replay"
        >
          <RotateCcw :size="20" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Play, Pause, Volume2, Volume1, VolumeX, RotateCcw } from 'lucide-vue-next'

const props = defineProps({
  audioUrl: {
    type: String,
    required: true
  },
  transcript: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['playback-end'])

// Audio element ref
const audioElement = ref(null)

// Playback state
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const volume = ref(1)
const isMuted = ref(false)

// Format time (MM:SS)
function formatTime(seconds) {
  if (isNaN(seconds)) return '0:00'
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

const formattedCurrentTime = computed(() => formatTime(currentTime.value))
const formattedDuration = computed(() => formatTime(duration.value))

// Event handlers
function onLoadedMetadata() {
  if (audioElement.value) {
    duration.value = audioElement.value.duration
  }
}

function onTimeUpdate() {
  if (audioElement.value) {
    currentTime.value = audioElement.value.currentTime
  }
}

function onEnded() {
  isPlaying.value = false
  emit('playback-end')
}

// Playback controls
function togglePlay() {
  if (!audioElement.value) return
  
  if (isPlaying.value) {
    audioElement.value.pause()
  } else {
    audioElement.value.play()
  }
}

function seek() {
  if (audioElement.value) {
    audioElement.value.currentTime = currentTime.value
  }
}

function toggleMute() {
  if (audioElement.value) {
    audioElement.value.muted = !audioElement.value.muted
    isMuted.value = audioElement.value.muted
  }
}

function updateVolume() {
  if (audioElement.value) {
    audioElement.value.volume = volume.value
    if (volume.value > 0) {
      isMuted.value = false
      audioElement.value.muted = false
    }
  }
}

function replay() {
  if (audioElement.value) {
    audioElement.value.currentTime = 0
    audioElement.value.play()
  }
}

// Initialize
onMounted(() => {
  if (audioElement.value) {
    audioElement.value.volume = volume.value
  }
})

// Cleanup
onUnmounted(() => {
  if (audioElement.value) {
    audioElement.value.pause()
  }
})
</script>

<style scoped>
/* Custom slider styles */
input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #4f46e5;
  cursor: pointer;
}

input[type="range"]::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #4f46e5;
  cursor: pointer;
  border: none;
}

input[type="range"]::-webkit-slider-runnable-track {
  height: 8px;
  border-radius: 4px;
}

input[type="range"]::-moz-range-track {
  height: 8px;
  border-radius: 4px;
}
</style>
