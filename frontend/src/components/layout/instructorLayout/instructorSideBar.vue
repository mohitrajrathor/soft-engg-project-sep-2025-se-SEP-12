<script setup>
import { useRouter, useRoute, RouterLink } from 'vue-router'
const router = useRouter()
const route = useRoute()

const mainNav = [
  { name: 'Dashboard', path: '/instructor/dashboard', icon: 'bi-speedometer2' },
  { name: 'Discussion Summaries', path: '/instructor/discussion-summaries', icon: 'bi-robot' },
  { name: 'Slide Generator', path: '/instructor/slide-generator', icon: 'bi-journal-text' },
  { name: 'Question Paper Generator', path: '/instructor/assessment-generator', icon: 'bi-question-circle' },
  { name: 'Profile', path: '/instructor/profile', icon: 'bi-gear' }
]

function signOut() {
  alert('Signed out successfully!')
  router.push('/login')
}
</script>

<template>
  <aside class="fixed top-0 left-0 h-screen w-64 bg-[#0d1b2a] text-white flex flex-col justify-between z-40 shadow-lg">
    <div class="flex flex-col flex-1">
      <RouterLink to="/" class="flex items-center pl-3 pt-9 pb-5 mb-1 text-3xl font-extrabold tracking-tight">
        AURA
      </RouterLink>
      <hr class="border-t border-[#233554] mx-7 my-2 opacity-40" />

      <nav class="flex-1">
        <ul class="flex flex-col gap-2 mt-2 px-2">
          <li v-for="item in mainNav" :key="item.path">
            <RouterLink :to="item.path"
              class="flex items-center gap-3 px-2 py-2 rounded-lg font-medium text-base transition group"
              :class="{
                'bg-[#1b263b] font-semibold shadow-sm': route.path === item.path,
                'hover:bg-[#16213a]': route.path !== item.path
              }"
            >
              <i :class="`${item.icon} text-lg`"></i>
              <span class="leading-tight">{{ item.name }}</span>
            </RouterLink>
          </li>
        </ul>
      </nav>
    </div>
    <div class="px-2 pb-2 mt-auto">
      <button
        @click="signOut"
        class="w-full flex items-center justify-center gap-2 px-2 py-2 border border-blue-100 rounded-lg font-semibold text-blue-100 shadow transition hover:bg-white hover:text-[#0d1b2a] duration-150"
      >
        <i class="bi bi-box-arrow-right"></i>
        Sign Out
      </button>
      <p class="text-xs text-gray-400 text-center mt-3">Logged in as Instructor</p>
    </div>
  </aside>
</template>

<style scoped>
a,
.router-link-active,
.router-link-exact-active {
  text-decoration: none !important;
  color: inherit;
}
</style>
