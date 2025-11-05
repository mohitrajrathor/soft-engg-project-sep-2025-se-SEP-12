<script setup>
import Sidebar from '@/components/layout/TaLayout/TASideBar.vue'
import HeaderBar from '@/components/layout/TaLayout/TaHeaderBar.vue'

import {
  CheckCircleIcon,
  TrashIcon,
  EnvelopeIcon,
  Cog6ToothIcon,
  ClipboardDocumentListIcon,
  AcademicCapIcon,
  ChatBubbleLeftRightIcon,
  ClockIcon,
  ArrowRightOnRectangleIcon,
} from "@heroicons/vue/24/outline"
</script>

<template>
  <div class="flex min-h-screen bg-gray-50">
    <Sidebar class="fixed top-0 left-0 h-screen w-[250px]" />

    <main class="flex-1 p-8 ml-[250px] overflow-y-auto">
      <HeaderBar searchPlaceholder="Search students, courses, or threads" />

      <h2 class="font-bold text-2xl mb-6">TA Settings</h2>

      <div class="grid grid-cols-12 gap-8">
        <!-- Left main content -->
        <div class="col-span-8 space-y-8">
          <!-- Profile Card -->
          <div
            class="bg-white rounded-2xl p-6 shadow cursor-pointer flex flex-col sm:flex-row items-start gap-8 hover:shadow-xl transition group"
          >
            <div class="flex flex-col items-center min-w-[120px]">
              <img
                src="https://randomuser.me/api/portraits/women/45.jpg"
                alt="Profile avatar"
                class="w-20 h-20 rounded-full object-cover border-4 border-blue-100 shadow mb-3 transition group-hover:scale-110"
              />
              <button
                class="px-4 py-1 bg-blue-100 text-blue-700 font-semibold rounded-lg text-xs hover:bg-blue-200 active:scale-95 transition"
              >Change avatar</button>
              <span
                class="mt-2 text-xs bg-green-100 text-green-800 rounded-full px-2 py-1 font-semibold"
              >Teaching Assistant</span>
            </div>

            <form class="flex-1 w-full grid grid-cols-1 gap-3">
              <div class="grid md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-xs text-gray-700 mb-1">Full name</label>
                  <input
                    type="text"
                    class="w-full border rounded-lg p-2 mb-3 focus:ring focus:border-blue-400 hover:border-blue-400 transition"
                    value="Taniya Chouhan"
                  />
                  <label class="block text-xs text-gray-700 mb-1">Institute email</label>
                  <input
                    type="email"
                    class="w-full border rounded-lg p-2 mb-3 focus:ring focus:border-blue-400 hover:border-blue-400 transition"
                    value="taniya.chouhan@ds.iitm.ac.in"
                  />
                  <label class="block text-xs text-gray-700 mb-1">Department</label>
                  <input
                    type="text"
                    class="w-full border rounded-lg p-2 mb-3 focus:ring focus:border-blue-400 hover:border-blue-400 transition"
                    value="Data Science"
                  />
                </div>
                <div class="flex flex-col items-start gap-3 justify-center">
                  <label class="hidden sm:block text-xs text-gray-700 mb-1">&nbsp;</label>
                  <button
                    type="button"
                    class="w-full py-2 bg-blue-600 text-white font-semibold rounded-lg shadow hover:bg-blue-700 active:scale-95 transition"
                  >Upload</button>
                  <button
                    type="button"
                    class="w-full py-2 flex items-center justify-center gap-2 bg-blue-500 text-white font-semibold rounded-lg shadow hover:bg-blue-600 active:scale-95 transition"
                  >
                    <CheckCircleIcon class="w-5 h-5" />Save changes
                  </button>
                </div>
              </div>
            </form>
          </div>

          <!-- Responsibilities -->
          <div class="bg-white rounded-2xl p-6 shadow space-y-2 hover:shadow-lg transition">
            <div class="font-bold mb-2">Responsibilities</div>
            <ul class="text-sm text-gray-700 space-y-2">
              <li class="flex items-center gap-2">
                <ClipboardDocumentListIcon class="w-4 h-4 text-blue-600" /> Grading and assignment
                review
              </li>
              <li class="flex items-center gap-2">
                <ChatBubbleLeftRightIcon class="w-4 h-4 text-blue-600" /> Student query resolution
              </li>
              <li class="flex items-center gap-2">
                <ClockIcon class="w-4 h-4 text-blue-600" /> Office hours and support sessions
              </li>
              <li class="flex items-center gap-2">
                <AcademicCapIcon class="w-4 h-4 text-blue-600" /> Assisting instructors with
                course materials
              </li>
            </ul>
          </div>

          <!-- Connected Services -->
          <div class="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition">
            <div class="font-bold mb-2">Connected Services</div>
            <div class="flex flex-wrap gap-6">
              <div>
                <span class="font-semibold">GitHub</span>
                <button
                  class="text-blue-600 underline ml-2 hover:text-blue-800 active:scale-95 transition"
                >Linked</button>
              </div>
              <div>
                <span class="font-semibold">LinkedIn</span>
                <button
                  class="text-blue-600 underline ml-2 hover:text-blue-800 active:scale-95 transition"
                >Linked</button>
              </div>
              <div>
                <span class="font-semibold">Google Drive</span>
                <button
                  class="text-blue-600 underline ml-2 hover:text-blue-800 active:scale-95 transition"
                >Linked</button>
              </div>
            </div>
          </div>

          <!-- Danger Zone -->
          <div
            class="bg-white rounded-2xl p-6 shadow flex items-center justify-between hover:shadow-lg transition"
          >
            <div>
              <div class="font-bold text-red-600 mb-2">Danger zone</div>
              <div>Deactivate TA access</div>
              <div class="text-xs text-gray-400">This will remove access to TA dashboard</div>
            </div>
            <button
              class="bg-red-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-red-700 active:scale-95 transition"
            >
              <TrashIcon class="w-5 h-5" />Deactivate
            </button>
          </div>
        </div>

        <!-- Sidebar (Right) -->
        <div class="col-span-4 space-y-6">
          <div class="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition">
            <div class="font-bold">TA Summary</div>
            <div class="text-xs text-gray-700 mt-1">TA ID: <span class="font-mono">TA-1023</span></div>
            <div class="text-xs text-gray-700">Course: System Commands</div>
            <div class="text-xs text-gray-700">Students: 85</div>
            <div class="text-xs text-gray-700">Joined: Jan 2025</div>
          </div>

          <div class="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition">
            <div class="font-bold mb-2">Shortcuts</div>
            <div class="space-y-2">
              <button
                class="flex items-center gap-2 w-full text-left text-sm hover:text-blue-700 hover:bg-blue-50 rounded-lg px-2 py-2 transition"
              >
                <Cog6ToothIcon class="w-4 h-4" />Manage Course Materials
              </button>
              <button
                class="flex items-center gap-2 w-full text-left text-sm hover:text-blue-700 hover:bg-blue-50 rounded-lg px-2 py-2 transition"
              >
                <EnvelopeIcon class="w-4 h-4" />Student Communication
              </button>
              <button
                class="flex items-center gap-2 w-full text-left text-sm hover:text-blue-700 hover:bg-blue-50 rounded-lg px-2 py-2 transition"
              >
                <CheckCircleIcon class="w-4 h-4" />Report Submission Status
              </button>
            </div>
          </div>

          <div class="bg-white rounded-2xl p-6 shadow hover:shadow-lg transition">
            <div class="font-bold mb-2">Session</div>
            <div class="text-xs text-gray-700">Current IP: <span class="font-mono">192.168.3.10</span></div>
            <div class="text-xs text-gray-700">Device: Windows + Chrome</div>
            <button
              class="mt-2 px-3 py-2 border border-blue-600 bg-blue-50 rounded-lg text-blue-700 font-semibold w-full flex items-center justify-center gap-2 hover:bg-blue-100 hover:border-blue-800 active:scale-95 transition"
            >
              <ArrowRightOnRectangleIcon class="w-5 h-5" />Sign out of all
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
/* All hover and focus effects are included via Tailwind classes */
</style>
