<template>
  <div class="flex h-screen">
    <!-- Sidebar -->
    <Sidebar />

    <!-- Main Section -->
    <div class="flex flex-col flex-grow bg-gray-50 ml-[250px]">
      <HeaderBar v-if="!isOnBreak" />

      <!-- Main Body -->
      <div class="flex flex-grow overflow-hidden ">
        <!-- Course Section -->
        <div class="p-6 flex-grow overflow-y-auto">
          <div class="flex flex-wrap justify-between items-center mb-6 gap-3">
            <div class="flex flex-wrap items-center gap-2 text-gray-700">
              <i class="bi bi-journal-bookmark text-blue-600 text-lg"></i>
              <span class="font-semibold">4 Active Courses</span>
              <span class="text-gray-400">| 3 Deadlines This Week</span>
            </div>

            <!-- Buttons -->
            <div class="flex flex-wrap gap-3 justify-end">
              <!-- Filter Buttons -->
              <div class="flex flex-wrap gap-2">
                <button
                  v-for="option in filterOptions"
                  :key="option"
                  @click="setFilter(option)"
                  class="px-3 py-1.5 border border-blue-500 rounded-full text-sm font-medium transition"
                  :class="currentFilter === option ? 'bg-blue-500 text-white' : 'text-blue-500 hover:bg-blue-100'"
                >
                  {{ option }}
                </button>
              </div>

              <!-- Add Resource -->
              <button
                @click="showAddResource = true"
                class="px-3 py-1.5 border border-green-500 rounded-full text-sm font-medium text-green-600 hover:bg-green-100 transition"
              >
                <i class="bi bi-collection me-1"></i> Add Resources
              </button>

              <!-- Study Break -->
              <button
                @click="showStudyBreak = true"
                class="px-3 py-1.5 border border-yellow-500 rounded-full text-sm font-medium text-yellow-600 hover:bg-yellow-100 transition"
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
              class="bg-white rounded-3xl shadow hover:shadow-lg overflow-hidden transition"
            >
              <img :src="course.image" class="w-full h-40 object-cover" />
              <div class="p-4 flex flex-col justify-between h-48">
                <div>
                  <h5 class="font-semibold text-gray-800 mb-1">
                    <i class="bi bi-journal-text text-blue-600 me-2"></i>{{ course.title }}
                  </h5>
                  <p class="text-sm text-gray-500"><i class="bi bi-calendar-event me-1"></i>{{ course.schedule }}</p>
                  <p class="text-sm text-gray-500"><i class="bi bi-person-badge me-1"></i>{{ course.instructor }}</p>
                </div>
                <div class="flex justify-between items-center mt-auto">
                  <button class="px-3 py-1 border border-blue-500 rounded-full text-sm text-blue-600 hover:bg-blue-100">
                    <i class="bi bi-play-circle me-1"></i> Open
                  </button>
                  <button class="px-3 py-1 border border-green-500 rounded-full text-sm text-green-600 hover:bg-green-100">
                    <i class="bi bi-robot me-1"></i> Ask AI
                  </button>
                  <span class="text-xs text-blue-600 bg-blue-100 px-2 py-1 rounded-full">
                    <i class="bi bi-check-circle me-1"></i>{{ course.status }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Resources Section -->
          <div class="mt-8">
            <h3 class="font-semibold text-gray-800 mb-3">My Resources</h3>
            <div v-if="resources.length === 0" class="text-gray-400">No resources added yet.</div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div v-for="(res, i) in resources" :key="i" class="bg-white p-4 rounded-2xl shadow">
                <!-- Document -->
                <div v-if="res.document" class="text-sm text-gray-700 mb-1">
                  📄
                  <a :href="res.document.url" target="_blank" class="underline hover:text-blue-600">{{ res.document.name }}</a>
                </div>

                <!-- Image -->
                <div v-if="res.image" class="mb-2">
                  <img :src="res.image" class="w-full h-32 object-cover rounded-lg" />
                </div>

                <!-- Link -->
                <div v-if="res.link" class="text-blue-600 text-sm">
                  🔗 <a :href="res.link" target="_blank" class="underline hover:text-blue-800">{{ res.link }}</a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Panel -->
        <div class="w-[320px] border-l bg-white">
          <RightPanel />
        </div>
      </div>
    </div>

    <!-- Add Resource Modal -->
    <div
      v-if="showAddResource"
      class="fixed inset-0 flex items-center justify-center bg-black/40 z-50"
    >
      <div class="bg-white rounded-3xl shadow-lg w-full max-w-md p-6 relative">
        <h3 class="text-xl font-semibold text-blue-600 mb-4 flex items-center">
          <i class="bi bi-folder-plus me-2"></i> Add Resource
        </h3>

        <div class="space-y-4">
          <div>
            <label class="font-semibold block mb-1">Upload Document</label>
            <input type="file" accept=".pdf,.doc,.docx" class="w-full border rounded-lg p-2" ref="docInput" />
          </div>
          <div>
            <label class="font-semibold block mb-1">Upload Image</label>
            <input type="file" accept="image/*" class="w-full border rounded-lg p-2" ref="imgInput" />
          </div>
          <div>
            <label class="font-semibold block mb-1">Add Link</label>
            <input type="url" placeholder="https://example.com" class="w-full border rounded-lg p-2" ref="linkInput" />
          </div>
        </div>

        <div class="mt-6 flex justify-end gap-2">
          <button @click="showAddResource = false" class="px-4 py-2 rounded-full border text-gray-600 hover:bg-gray-100">
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
      <div class="bg-white rounded-3xl shadow-lg w-full max-w-md p-6">
        <h3 class="text-xl font-semibold text-yellow-600 mb-4 flex items-center">
          <i class="bi bi-cup-hot me-2"></i> Take a Break
        </h3>

        <p class="font-semibold mb-3 text-center">Select your break duration:</p>
        <div class="grid grid-cols-2 gap-2 mb-3">
          <button v-for="mins in [5,10,15,30]" :key="mins"
            @click="startBreak(mins)"
            class="py-2 border border-yellow-500 text-yellow-600 rounded-lg hover:bg-yellow-100">
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
          />
          <button @click="startCustomBreak" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            Start
          </button>
        </div>

        <div class="mt-5 text-right">
          <button @click="showStudyBreak = false" class="text-gray-500 hover:text-gray-700">Close</button>
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
import Sidebar from '@/components/layout/StudentLayout/SideBar.vue'
import HeaderBar from '@/components/layout/StudentLayout/HeaderBar.vue'
import RightPanel from '@/components/layout/StudentLayout/RightPanel.vue'

import algorithms from '@/assets/algorithms.jpg'
import systems from '@/assets/systems.jpg'
import linearAlgebra from '@/assets/linear-algebra.jpg'
import worldHistory from '@/assets/world-history.jpg'

export default {
  components: { Sidebar, HeaderBar, RightPanel },
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
      resources: [], // store resources
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
      const docInput = this.$refs.docInput?.files[0];
      const imgInput = this.$refs.imgInput?.files[0];
      const linkInput = this.$refs.linkInput?.value;

      const newResource = {
        document: docInput ? { name: docInput.name, url: URL.createObjectURL(docInput) } : null,
        image: imgInput ? URL.createObjectURL(imgInput) : null,
        link: linkInput || null,
      };

      this.resources.push(newResource);
      this.showAddResource = false;

      // reset inputs
      if (docInput) this.$refs.docInput.value = '';
      if (imgInput) this.$refs.imgInput.value = '';
      if (linkInput) this.$refs.linkInput.value = '';
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
