<template>
  <div class="flex h-screen" :style="{ color: $themeStore?.currentTheme === 'dark' ? 'white' : 'black' }">
    <!-- Sidebar -->
    <Sidebar />

    <!-- Main Section -->
    <div class="flex flex-col flex-grow main-theme ml-[250px]" :style="{ color: $themeStore?.currentTheme === 'dark' ? 'white' : 'black' }">
      <HeaderBar v-if="!isOnBreak" />

      <!-- Main Body -->
      <div class="flex flex-grow overflow-hidden main-theme" :style="{ color: $themeStore?.currentTheme === 'dark' ? 'white' : 'black' }">
        <!-- Course Section -->
        <div class="p-6 flex-grow overflow-y-auto section-theme" :style="{ color: $themeStore?.currentTheme === 'dark' ? 'white' : 'black' }">
          <div class="flex flex-wrap justify-between items-center mb-6 gap-3">
              <div class="flex flex-wrap items-center gap-2 section-text" :style="{ color: $themeStore?.currentTheme === 'dark' ? 'white' : 'black' }">
              <i class="bi bi-journal-bookmark text-blue-600 text-lg"></i>
              <span class="font-semibold" :style="{ color: $themeStore?.currentTheme === 'dark' ? 'white' : 'black' }">4 Active Courses</span>
              <span class="section-subtext" :style="{ color: $themeStore?.currentTheme === 'dark' ? 'white' : 'black' }">| 3 Deadlines This Week</span>
            </div>            <!-- Buttons -->
            <div class="flex flex-wrap gap-3 justify-end">
              <!-- Filter Buttons -->
              <div class="flex flex-wrap gap-2">
          <button
            v-for="option in filterOptions"
            :key="option"
            @click="setFilter(option)"
            class="px-3 py-1.5 border rounded-full text-sm font-medium transition filter-btn"
            :class="currentFilter === option ? 'filter-btn-active' : 'filter-btn-inactive'"
            :style="{ color: $themeStore?.currentTheme === 'dark' ? 'white' : 'black' }"
          >
            {{ option }}
          </button>
              </div>

              <!-- Add Resource -->
                <button
              @click="showAddResource = true"
              class="px-3 py-1.5 border rounded-full text-sm font-medium transition add-resource-btn"
              :style="{ color: $themeStore?.currentTheme === 'dark' ? 'white' : 'black' }"
                >
              <i class="bi bi-collection me-1"></i> Add Resources
                </button>

                <!-- Study Break -->
                <button
                @click="showStudyBreak = true"
                class="px-3 py-1.5 border rounded-full text-sm font-medium transition study-break-btn"
                :style="{ color: $themeStore?.currentTheme === 'dark' ? 'white' : 'black' }"
                >
                <i class="bi bi-cup-hot me-1"></i>
                {{ isOnBreak ? `Break: ${formattedTime}` : 'Study Break' }}
                </button>
                </div>
                </div>

          <!-- Course Cards -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div
              v-for="(course, index) in filteredCourses"
              :key="index"
              class="rounded-3xl shadow hover:shadow-lg overflow-hidden transition card-theme"
              :style="{ color: $themeStore?.currentTheme === 'dark' ? 'white' : 'black' }"
            >
              <img :src="course.image" class="w-full h-40 object-cover" />
              <div class="p-4 flex flex-col justify-between h-48" :style="{ color: $themeStore?.currentTheme === 'dark' ? 'white' : 'black' }">
          <div>
            <h3 class="font-semibold card-title" :style="{ color: $themeStore?.currentTheme === 'dark' ? 'white' : 'black' }">{{ course.title }}</h3>
            <p class="text-sm card-subtext" :style="{ color: $themeStore?.currentTheme === 'dark' ? 'white' : 'black' }"><i class="bi bi-calendar me-1"></i>{{ course.schedule }}</p>
            <p class="text-sm card-subtext" :style="{ color: $themeStore?.currentTheme === 'dark' ? 'white' : 'black' }"><i class="bi bi-person-badge me-1"></i>{{ course.instructor }}</p>
          </div>
          <div class="flex justify-between items-center mt-auto gap-2" :style="{ color: $themeStore?.currentTheme === 'dark' ? 'white' : 'black' }">
            <button class="px-3 py-1 border rounded-full text-sm transition card-btn-blue" :style="{ color: $themeStore?.currentTheme === 'dark' ? 'white' : 'black' }">
              <i class="bi bi-play-circle me-1"></i> Open
            </button>
            <button class="px-3 py-1 border rounded-full text-sm transition card-btn-green" :style="{ color: $themeStore?.currentTheme === 'dark' ? 'white' : 'black' }">
              <i class="bi bi-robot me-1"></i> Ask AI
            </button>
            <span class="text-xs px-2 py-1 rounded-full card-status" :style="{ color: $themeStore?.currentTheme === 'dark' ? 'white' : 'black' }">
              <i class="bi bi-check-circle me-1"></i>{{ course.status }}
            </span>
          </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Panel -->
        <div class="w-[320px] border-l" :style="{ background: 'var(--color-bg-card)' }">
          <RightPanel />
        </div>
      </div>
    </div>

    <!-- Add Resource Modal -->
    <div
      v-if="showAddResource"
      class="fixed inset-0 flex items-center justify-center bg-black/40 z-50"
    >
      <div class="rounded-3xl shadow-lg w-full max-w-md p-6 relative modal-theme">
        <h3 class="text-xl font-semibold modal-title mb-4 flex items-center">
          <i class="bi bi-folder-plus me-2"></i> Add Resource
        </h3>

        <div class="space-y-4">
          <div>
            <label class="font-semibold block mb-1">Upload Document</label>
            <input type="file" accept=".pdf,.doc,.docx" class="w-full border rounded-lg p-2" />
          </div>
          <div>
            <label class="font-semibold block mb-1">Upload Image</label>
            <input type="file" accept="image/*" class="w-full border rounded-lg p-2" />
          </div>
          <div>
            <label class="font-semibold block mb-1">Add Link</label>
            <input type="url" placeholder="https://example.com" class="w-full border rounded-lg p-2" />
          </div>
        </div>

        <div class="mt-6 flex justify-end gap-2">
          <button @click="showAddResource = false" class="px-4 py-2 rounded-full border hover:bg-gray-100" :style="{ color: themeStore.currentTheme === 'dark' ? 'white' : 'black' }">
            Cancel
          </button>
          <button @click="saveResource" class="px-4 py-2 rounded-full bg-blue-600 text-white hover:bg-blue-700">
            Save
          </button>
        </div>
      </div>
    </div>

    <!-- Study Break Modal -->

    <div
      v-if="showStudyBreak"
      class="fixed inset-0 flex items-center justify-center bg-black/40 z-50"
    >
      <div class="rounded-3xl shadow-lg w-full max-w-md p-6 modal-theme">
      <h3 class="text-xl font-semibold mb-4 flex items-center" style="color: var(--color-btn-yellow-text)">
        <i class="bi bi-cup-hot me-2"></i> Take a Break
      </h3>

      <p class="font-semibold mb-3 text-center" style="color: var(--color-text-primary)">Select your break duration:</p>
      <div class="grid grid-cols-2 gap-2 mb-3">
        <button v-for="mins in [5,10,15,30]" :key="mins"
        @click="startBreak(mins)"
        class="py-2 border rounded-lg transition"
        style="border-color: var(--color-btn-yellow-border); color: var(--color-btn-yellow-text); background: var(--color-btn-bg);"
        :style="{ borderColor: 'var(--color-btn-yellow-border)', color: 'var(--color-btn-yellow-text)' }">
        {{ mins }} min
        </button>
      </div>

      <div class="flex gap-2 items-center">
        <input
        v-model="customBreak"
        type="number"
        min="1"
        placeholder="Custom (min)"
        class="border rounded-lg p-2 flex-grow"
        style="border-color: var(--color-btn-border); background: var(--color-btn-bg); color: var(--color-text-primary);"
        />
        <button @click="startCustomBreak" class="px-4 py-2 rounded-lg transition"
        style="background: var(--color-btn-active-bg); color: var(--color-btn-active-text); border: 1px solid var(--color-btn-active-border);">
        Start
        </button>
      </div>

      <div class="mt-5 text-right">
        <button @click="showStudyBreak = false" class="transition" style="color: var(--color-text-secondary);">Close</button>
      </div>
      </div>
    </div>

    <!-- Full-Screen Break Overlay -->
    <div
      v-if="isOnBreak"
      class="fixed inset-0 bg-gradient-to-br from-yellow-400 via-orange-400 to-pink-400 flex flex-col items-center justify-center z-50 text-white transition"
    >
      <h1 class="text-5xl font-bold mb-3 animate-pulse">☕ Break Started</h1>
      <h2 class="text-2xl mb-6">Time Left: {{ formattedTime }}</h2>
      <button
        @click="endBreak"
        class="px-6 py-3 bg-red-600 rounded-full text-lg font-semibold hover:bg-red-700 transition"
      >
        End Break
      </button>
    </div>
  </div>
</template>

<script>
import { useThemeStore } from '@/stores/theme';
import Sidebar from '@/components/layout/StudentLayout/SideBar.vue'
import HeaderBar from '@/components/layout/StudentLayout/HeaderBar.vue'
import RightPanel from '@/components/layout/StudentLayout/RightPanel.vue'

import algorithms from '@/assets/algorithms.jpg'
import systems from '@/assets/systems.jpg'
import linearAlgebra from '@/assets/linear-algebra.jpg'
import worldHistory from '@/assets/world-history.jpg'

export default {
  components: { Sidebar, HeaderBar, RightPanel },
  setup() {
    const $themeStore = useThemeStore();
    return { $themeStore };
  },
  data() {
    return {
      showAddResource: false,
      showStudyBreak: false,
      isOnBreak: false,
      currentFilter: 'All',
      filterOptions: ['All', 'Enrolled', 'Archived'],
      courses: [
        { title: 'CS 301: Algorithms', status: 'Enrolled', schedule: 'Mon/Wed • 10:00–11:15', instructor: 'Prof. Nguyen', image: algorithms },
        { title: 'CS 210: Systems', status: 'Archived', schedule: 'Tue/Thu • 9:00–10:15', instructor: 'Prof. Clarke', image: systems },
        { title: 'MATH 241: Linear Algebra', status: 'Enrolled', schedule: 'Tue/Thu • 1:00–2:15', instructor: 'Dr. Patel', image: linearAlgebra },
        { title: 'HIST 110: World History', status: 'Archived', schedule: 'Fri • 11:00–12:30', instructor: 'Dr. Tanaka', image: worldHistory },
      ],
      breakTime: 0,
      breakTimer: null,
      customBreak: '',
    }
  },
  computed: {
    filteredCourses() {
      return this.currentFilter === 'All'
        ? this.courses
        : this.courses.filter((c) => c.status === this.currentFilter)
    },
    formattedTime() {
      const m = Math.floor(this.breakTime / 60)
      const s = this.breakTime % 60
      return `${m}:${s.toString().padStart(2, '0')}`
    },
  },
  methods: {
    setFilter(opt) {
      this.currentFilter = opt
    },
    saveResource() {
      alert('Resource saved successfully!')
      this.showAddResource = false
    },
    startBreak(mins) {
      this.showStudyBreak = false
      this.isOnBreak = true
      this.breakTime = mins * 60
      this.breakTimer = setInterval(() => {
        if (this.breakTime > 0) this.breakTime--
        else {
          this.endBreak()
          alert('Break over! Time to study again!')
        }
      }, 1000)
    },
    startCustomBreak() {
      const mins = parseInt(this.customBreak)
      if (!mins || mins <= 0) return alert('Enter a valid number!')
      this.startBreak(mins)
      this.customBreak = ''
    },
    endBreak() {
      clearInterval(this.breakTimer)
      this.isOnBreak = false
      this.breakTime = 0
    },
  },
}
</script>

<style>
.main-theme {
  background: var(--page-bg);
  color: var(--color-text-primary);
  transition: background 0.3s, color 0.3s;
}
.section-theme {
  background: var(--color-bg-section);
  color: var(--color-text-primary);
  transition: background 0.3s, color 0.3s;
}
.section-text {
  color: var(--color-text-primary);
}
.section-subtext {
  color: var(--color-text-secondary);
}
.filter-btn {
  border-color: var(--color-btn-border);
  background: var(--color-btn-bg);
  color: var(--color-btn-text);
}
.filter-btn-active {
  background: var(--color-btn-active-bg);
  color: var(--color-btn-active-text);
  border-color: var(--color-btn-active-border);
}
.filter-btn-inactive {
  background: var(--color-btn-bg);
  color: var(--color-btn-text);
  border-color: var(--color-btn-border);
}
.add-resource-btn {
  border-color: var(--color-btn-green-border);
  color: var(--color-btn-green-text);
  background: var(--color-btn-bg);
}
.study-break-btn {
  border-color: var(--color-btn-yellow-border);
  color: var(--color-btn-yellow-text);
  background: var(--color-btn-bg);
}
.card-theme {
  background: var(--color-bg-card);
  color: var(--color-text-primary);
  transition: background 0.3s, color 0.3s;
}
.card-content-theme {
  background: var(--color-bg-card);
  color: var(--color-text-primary);
}
.card-title {
  color: var(--color-text-primary);
}
.card-subtext {
  color: var(--color-text-secondary);
}
.card-btn-blue {
  border-color: var(--color-btn-blue-border);
  color: var(--color-btn-blue-text);
  background: var(--color-btn-bg);
}
.card-btn-green {
  border-color: var(--color-btn-green-border);
  color: var(--color-btn-green-text);
  background: var(--color-btn-bg);
}
.card-status {
  color: var(--color-status-text);
  background: var(--color-status-bg);
}
.right-panel-theme {
  background: var(--color-bg-card);
  color: var(--color-text-primary);
  border-color: var(--color-border);
}
.modal-theme {
  background: var(--color-bg-card);
  color: var(--color-text-primary);
}
</style>
