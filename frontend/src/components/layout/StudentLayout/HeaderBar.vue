<template>
  <header class="sticky top-0 z-30 bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/80 py-2 px-8 shadow-sm border-b border-[#e6eaff] flex items-center justify-between">
    <!-- Left: Brand or logo (optional) -->
    <!-- <span class="text-xl font-extrabold tracking-tight text-blue-700">AURA</span> -->
    
    <!-- Search -->
    <div class="flex items-center w-full max-w-[430px] bg-[#f3f6fa] rounded-full pl-3 pr-2 py-1 border border-gray-200 focus-within:ring-2 focus-within:ring-blue-100">
      <i class="bi bi-search text-gray-400 text-base mr-2"></i>
      <input
        type="text"
        placeholder="Search courses, threads, or resources"
        class="bg-transparent border-none outline-none flex-1 text-gray-700 text-sm placeholder-gray-400 py-2"
        autocomplete="off"
      />
    </div>

    <!-- Right: Actions -->
    <div class="flex items-center gap-4 ml-7">
      <!-- Ask AI Button -->
      <button class="inline-flex items-center gap-2 px-4 py-2 rounded-full border-2 border-blue-600 text-blue-600 bg-white font-bold shadow-sm hover:bg-blue-600/95 hover:text-white transition duration-150">
        <i class="bi bi-stars text-base"></i>
        Ask AI
      </button>
      <!-- Notifications (with animated badge) -->
      <div class="relative">
        <button class="relative w-11 h-11 flex items-center justify-center rounded-full bg-white shadow hover:bg-blue-50 border border-gray-200 focus:ring-2 focus:ring-blue-200 transition">
          <i class="bi bi-bell-fill text-lg text-gray-700"></i>
          <span class="absolute -top-0.5 -right-0.5 flex items-center justify-center bg-red-500 text-white rounded-full border-2 border-white shadow text-xs font-bold w-5 h-5 animate-pulse">
            3
          </span>
        </button>

        <!-- Profile dropdown -->
        <div class="dropdown">
          <a href="#" class="d-flex align-items-center text-decoration-none dropdown-toggle" data-bs-toggle="dropdown">
            <img :src="profileImage" alt="Profile" class="rounded-circle me-2" width="36" height="36" />
            <span class="fw-semibold text-dark">Student</span>
          </a>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import profileImage from '@/assets/profile.jpg'
</script>
