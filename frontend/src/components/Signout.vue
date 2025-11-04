<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function signOut() {
  if (confirm("Are you sure you want to sign out?")) {
    localStorage.removeItem('aura_user')
    localStorage.removeItem('aura_role')
    router.push('/login')
  }
}
</script>

<template>
  <button
    @click="signOut"
    class="w-full flex items-center justify-center gap-3 px-5 py-3 mt-5 font-bold text-white bg-blue-600 hover:bg-blue-700 transition rounded-xl shadow-sm text-lg"
  >
    <span>
      <i class="bi bi-box-arrow-right text-xl"></i>
    </span>
    Sign Out
  </button>
</template>
