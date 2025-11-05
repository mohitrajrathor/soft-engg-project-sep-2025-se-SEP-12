<script setup>
import { useRouter } from 'vue-router'
import { RouterLink } from 'vue-router'

const router = useRouter()

// Navigation structure for student (you could make this role-based later)
const mainNav = [
  { name: 'Dashboard', path: '/ta/dashboard', icon: 'bi-speedometer2' },
  { name: 'Query Tracker', path: '/ta/query-tracker', icon: 'bi-robot' },
  { name: 'Doubt Summarizer', path: '/ta/doubt-summarizer', icon: 'bi-journal-text' },
  { name: 'Resource Hub', path: '/ta/resource', icon: 'bi-question-circle' },
  {name: 'Onboarding Mentor', path: '/ta/onboarding-mentor', icon: 'bi-people-fill' },
  {name: 'Assessment Generator', path: '/ta/assessment-generator', icon: 'bi-file-earmark-text' },
  {name: 'Slide Deck Creator', path: '/ta/slide-deck-creator', icon: 'bi-file-slides' },
  { name: 'Profile', path: '/ta/profile', icon: 'bi-gear' },
]

// const quickActions = [
//   { name: 'New Query', path: '/student/my-query', icon: 'bi-plus-circle' },
//   { name: 'Book Office Hour', path: '/student/office-hour', icon: 'bi-calendar-check' },
// ]

function signOut() {
  alert('Signed out successfully!')
  router.push('/login')
}
</script>

<template>
  <div class="d-flex flex-column flex-shrink-0 p-3 text-white vh-100" style="width: 250px; background-color: #0d1b2a; height: 100vh; position: fixed; top: 0; left: 0; z-index: 100;">
    <RouterLink to="/" class="d-flex align-items-center mb-3 text-white text-decoration-none">
      <span class="fs-4 fw-semibold">AURA</span>
    </RouterLink>
    <hr class="border-light opacity-25" />

    <!-- Main nav -->
    <ul class="nav nav-pills flex-column mb-auto">
      <li v-for="item in mainNav" :key="item.path">
        <RouterLink :to="item.path" class="nav-link text-white" active-class="active-link">
          <i :class="`${item.icon} me-2`"></i> {{ item.name }}
        </RouterLink>
      </li>
    </ul>

    <!-- <hr class="border-light opacity-25" /> -->

    <!-- Quick Actions -->
    <!-- <p class="text-secondary text-uppercase small mb-2">Quick Actions</p>
    <ul class="nav nav-pills flex-column mb-auto">
      <li v-for="action in quickActions" :key="action.path">
        <RouterLink :to="action.path" class="nav-link text-white" active-class="active-link">
          <i :class="`${action.icon} me-2`"></i> {{ action.name }}
        </RouterLink>
      </li>
    </ul> -->

    <!-- Sign Out -->
    <div class="mt-auto">
      <button @click="signOut" class="btn btn-outline-light w-100 mt-3">
        <i class="bi bi-box-arrow-right me-2"></i> Sign Out
      </button>
      <p class="small text-secondary text-center mt-2 mb-0">Logged in as TA</p>
    </div>
  </div>
</template>

<style scoped>
.nav-link:hover {
  background-color: #1b263b !important;
}
.active-link {
  background-color: #1b263b !important;
}
</style>
