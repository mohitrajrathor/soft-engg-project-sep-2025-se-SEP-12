<script setup>
import InstructorSidebar from '@/components/layout/instructorLayout/instructorSideBar.vue'

import {
  UserCircleIcon,
  EnvelopeIcon,
  KeyIcon,
  Cog6ToothIcon,
  TrashIcon,
  CheckCircleIcon,
  ArrowRightOnRectangleIcon,
  AcademicCapIcon,
} from "@heroicons/vue/24/outline"
</script>

<template>
  <div class="flex min-h-screen bg-gray-50">
    <!-- Sidebar -->
    <InstructorSidebar class="fixed top-0 left-0 h-screen w-[250px]" />

    <!-- Main -->
    <main class="flex-1 p-8 ml-[250px] overflow-y-auto">
      <HeaderBar searchPlaceholder="Search students, courses, or resources" />
      <h2 class="font-bold text-2xl mb-6">Instructor Settings</h2>

      <div class="grid grid-cols-12 gap-8">
        <!-- Left main content -->
        <div class="col-span-8 space-y-8">
          <!-- Profile Card -->
          <div class="bg-white rounded-2xl p-6 shadow flex flex-col sm:flex-row items-start gap-8 hover:shadow-xl transition group">
            <div class="flex flex-col items-center min-w-[120px]">
              <img
                src="https://randomuser.me/api/portraits/men/28.jpg"
                alt="Instructor avatar"
                class="w-20 h-20 rounded-full object-cover border-4 border-green-100 shadow mb-3 transition group-hover:scale-110"
              />
              <button class="px-4 py-1 bg-green-100 text-green-700 font-semibold rounded-lg text-xs hover:bg-green-200 active:scale-95 transition">
                Change avatar
              </button>
              <span class="mt-2 text-xs bg-green-100 text-green-800 rounded-full px-2 py-1 font-semibold">Instructor</span>
            </div>

            <form class="flex-1 w-full grid grid-cols-1 gap-3">
              <div class="grid md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-xs text-gray-700 mb-1">Full name</label>
                  <input type="text" class="w-full border rounded-lg p-2 mb-3 focus:ring focus:border-green-400 hover:border-green-400 transition" value="Dr. Emily Carter" />
                  <label class="block text-xs text-gray-700 mb-1">Institution email</label>
                  <input type="email" class="w-full border rounded-lg p-2 mb-3 focus:ring focus:border-green-400 hover:border-green-400 transition" value="emily.carter@iitm.ac.in" />
                  <label class="block text-xs text-gray-700 mb-1">Department</label>
                  <input type="text" class="w-full border rounded-lg p-2 mb-3 focus:ring focus:border-green-400 hover:border-green-400 transition" value="Data Science" />
                </div>
                <div class="flex flex-col items-start gap-3 justify-center">
                  <label class="hidden sm:block text-xs text-gray-700 mb-1">&nbsp;</label>
                  <button type="button" class="w-full py-2 bg-green-600 text-white font-semibold rounded-lg shadow hover:bg-green-700 active:scale-95 transition">
                    Upload
                  </button>
                  <button type="button" class="w-full py-2 flex items-center justify-center gap-2 bg-green-500 text-white font-semibold rounded-lg shadow hover:bg-green-600 active:scale-95 transition">
                    <CheckCircleIcon class="w-5 h-5" /> Save changes
                  </button>
                </div>
              </div>
            </form>
          </div>

          <!-- Teaching Preferences -->
          <div class="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition">
            <div class="font-bold mb-2">Teaching Preferences</div>
            <div class="flex flex-col gap-3">
              <label class="flex items-center cursor-pointer hover:bg-green-50 px-2 py-1 rounded transition">
                <input type="checkbox" checked class="mr-2 accent-green-600"> Enable AI grading assistant
              </label>
              <label class="flex items-center cursor-pointer hover:bg-green-50 px-2 py-1 rounded transition">
                <input type="checkbox" checked class="mr-2 accent-green-600"> Allow student message alerts
              </label>
              <label class="flex items-center cursor-pointer hover:bg-green-50 px-2 py-1 rounded transition">
                <input type="checkbox" class="mr-2 accent-green-600"> Auto-schedule office hours
              </label>
            </div>
          </div>

          <!-- Connected Platforms -->
          <div class="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition">
            <div class="font-bold mb-2">Connected Platforms</div>
            <div class="flex flex-wrap gap-6">
              <div><span class="font-semibold">Google Classroom</span><button class="text-green-600 underline ml-2 hover:text-green-800 active:scale-95 transition">Linked</button></div>
              <div><span class="font-semibold">GitHub</span><button class="text-green-600 underline ml-2 hover:text-green-800 active:scale-95 transition">Linked</button></div>
              <div><span class="font-semibold">Zoom</span><button class="text-green-600 underline ml-2 hover:text-green-800 active:scale-95 transition">Linked</button></div>
            </div>
          </div>

          <!-- Danger Zone -->
          <div class="bg-white rounded-2xl p-6 shadow flex items-center justify-between hover:shadow-lg transition">
            <div>
              <div class="font-bold text-red-600 mb-2">Danger zone</div>
              <div>Delete instructor account</div>
              <div class="text-xs text-gray-400">This action cannot be undone</div>
            </div>
            <button class="bg-red-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-red-700 active:scale-95 transition">
              <TrashIcon class="w-5 h-5" /> Delete
            </button>
          </div>
        </div>

        <!-- Right Sidebar -->
        <div class="col-span-4 space-y-6">
          <div class="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition">
            <div class="font-bold">Instructor Summary</div>
            <div class="text-xs text-gray-700 mt-1">Instructor ID: <span class="font-mono">I-40215</span></div>
            <div class="text-xs text-gray-700">Joined: Jan 2024</div>
            <div class="text-xs text-gray-700">Active Courses: 3</div>
          </div>

          <div class="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition">
            <div class="font-bold mb-2">Shortcuts</div>
            <div class="space-y-2">
              <button class="flex items-center gap-2 w-full text-left text-sm hover:text-green-700 hover:bg-green-50 rounded-lg px-2 py-2 transition">
                <Cog6ToothIcon class="w-4 h-4" /> Manage courses
              </button>
              <button class="flex items-center gap-2 w-full text-left text-sm hover:text-green-700 hover:bg-green-50 rounded-lg px-2 py-2 transition">
                <UserCircleIcon class="w-4 h-4" /> View enrolled students
              </button>
              <button class="flex items-center gap-2 w-full text-left text-sm hover:text-green-700 hover:bg-green-50 rounded-lg px-2 py-2 transition">
                <AcademicCapIcon class="w-4 h-4" /> Grade submissions
              </button>
            </div>
          </div>

          <div class="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition">
            <div class="font-bold mb-2">Session</div>
            <div class="text-xs text-gray-700">Current IP: <span class="font-mono">192.168.1.12</span></div>
            <div class="text-xs text-gray-700">Device: Windows + Chrome</div>
            <button class="mt-2 px-3 py-2 border border-green-600 bg-green-50 rounded-lg text-green-700 font-semibold w-full flex items-center justify-center gap-2 hover:bg-green-100 hover:border-green-800 active:scale-95 transition">
              <ArrowRightOnRectangleIcon class="w-5 h-5" /> Sign out of all
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
/* Instructor settings styling handled mostly via Tailwind */
</style>
