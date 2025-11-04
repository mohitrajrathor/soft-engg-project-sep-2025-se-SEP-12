<script setup>
import TASidebar from '@/components/layout/TaLayout/TASideBar.vue'
import TaHeaderBar from '@/components/layout/TaLayout/TaHeaderBar.vue';

import { PlusCircleIcon, ArrowRightOnRectangleIcon, ClipboardDocumentListIcon, ChatBubbleLeftRightIcon } from "@heroicons/vue/24/outline";
</script>


<template>
  <div class="flex min-h-screen bg-[#f8fafc]">
    <TASidebar />
    <main class="flex-1 p-0">
      <TaHeaderBar searchPlaceholder="Search dashboard, queries, resources" />
      <div class="px-8 pt-6 flex flex-col lg:flex-row gap-8">
        <!-- MAIN DASHBOARD SECTION -->
        <div class="flex-1 flex flex-col gap-8">
          <!-- Dashboard Headline -->
          <div class="flex items-center justify-between mb-2">
            <h1 class="font-black text-3xl text-black tracking-tight">TA Dashboard</h1>
          </div>
          <!-- Metric Cards Row -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div class="bg-white rounded-2xl shadow-2xl p-6 flex flex-col items-start">
              <span class="text-sm font-medium text-gray-500 mb-1">Pending Queries</span>
              <span class="text-2xl font-bold mb-2 text-black">28 <span class="text-xs text-gray-500 ml-1">this week</span></span>
              <div class="flex-1 w-full flex items-end justify-between">
                <div class="w-14 h-8 bg-blue-50 rounded-lg"></div>
              </div>
              <button class="text-xs font-semibold mt-3 text-blue-700 hover:text-blue-900 hover:underline transition-colors">View Details</button>
            </div>
            <div class="bg-white rounded-2xl shadow-2xl p-6 flex flex-col items-start">
              <span class="text-sm font-medium text-gray-500 mb-1">Resolved This Week</span>
              <span class="text-2xl font-bold mb-2 text-black">64 <span class="text-xs text-gray-500 ml-1">total</span></span>
              <div class="flex-1 w-full flex items-end justify-between">
                <div class="w-14 h-8 bg-blue-50 rounded-lg"></div>
              </div>
              <button class="text-xs font-semibold mt-3 text-blue-700 hover:text-blue-900 hover:underline transition-colors">View Details</button>
            </div>
            <div class="bg-white rounded-2xl shadow-2xl p-6 flex flex-col items-start">
              <span class="text-sm font-medium text-gray-500 mb-1">New Resources</span>
              <span class="text-2xl font-bold mb-2 text-black">12 <span class="text-xs text-gray-500 ml-1">added</span></span>
              <div class="flex-1 w-full flex items-end justify-between">
                <div class="w-14 h-8 bg-blue-50 rounded-lg"></div>
              </div>
              <button class="text-xs font-semibold mt-3 text-blue-700 hover:text-blue-900 hover:underline transition-colors">Explore Resources</button>
            </div>
            <div class="bg-white rounded-2xl shadow-2xl p-6 flex flex-col items-start">
              <span class="text-sm font-medium text-gray-500 mb-1">Avg. Response Time</span>
              <span class="text-2xl font-bold mb-2 text-black">3.5 <span class="text-xs text-gray-500 ml-1">hours</span></span>
              <div class="flex-1 w-full flex items-end justify-between">
                <div class="w-14 h-8 bg-blue-50 rounded-lg"></div>
              </div>
            </div>
          </div>
          <!-- Trends and Analytics -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-2">
            <div class="bg-white rounded-2xl shadow-2xl p-6">
              <div class="font-semibold text-lg mb-2 text-black">Doubt Trends by Topic</div>
              <div class="text-xs text-gray-400 mb-4">Overview of student queries across various academic topics.</div>
              <div class="h-48 flex items-center justify-center">
                <div class="w-full h-full bg-blue-50 rounded-xl flex items-center justify-center text-gray-400">[Bar Chart]</div>
              </div>
            </div>
            <div class="bg-white rounded-2xl shadow-2xl p-6">
              <div class="font-semibold text-lg mb-2 text-black">Resource Access Over Time</div>
              <div class="text-xs text-gray-400 mb-4">Monthly views and downloads of academic resources.</div>
              <div class="h-48 flex items-center justify-center">
                <div class="w-full h-full bg-blue-50 rounded-xl flex items-center justify-center text-gray-400">[Line Chart]</div>
              </div>
            </div>
          </div>
        </div>
        <!-- SIDE PANEL SECTION (RIGHT) -->
        <aside class="w-full lg:w-80 flex flex-col gap-6">
          <!-- Quick Actions -->
          <div class="bg-white rounded-2xl shadow-2xl p-5">
            <div class="font-bold mb-4 text-lg text-black">Quick Actions</div>
            <button class="flex items-center gap-2 w-full px-4 py-3 mb-2 rounded-lg text-blue-700 bg-blue-50 hover:bg-blue-100 shadow-sm font-semibold transition-colors">
              <PlusCircleIcon class="w-5 h-5" /> Add New Resource
            </button>
            <button class="flex items-center gap-2 w-full px-4 py-3 mb-2 rounded-lg text-blue-700 bg-blue-50 hover:bg-blue-100 shadow-sm font-semibold transition-colors">
              <ClipboardDocumentListIcon class="w-5 h-5" /> Summarize Doubts
            </button>
            <button class="flex items-center gap-2 w-full px-4 py-3 mb-2 rounded-lg text-blue-700 bg-blue-50 hover:bg-blue-100 shadow-sm font-semibold transition-colors">
              <ChatBubbleLeftRightIcon class="w-5 h-5" /> View All Queries
            </button>
            <button class="flex items-center gap-2 w-full px-4 py-3 rounded-lg text-blue-700 bg-blue-50 hover:bg-blue-100 shadow-sm font-semibold transition-colors">
              <ArrowRightOnRectangleIcon class="w-5 h-5" /> Start Onboarding Session
            </button>
          </div>
          <!-- Announcements -->
          <div class="bg-white rounded-2xl shadow-2xl p-5">
            <div class="font-bold mb-3 text-lg text-black">Recent Announcements</div>
            <div class="mb-2">
              <div class="font-semibold text-blue-800">New Feature: AI Summarizer</div>
              <div class="text-xs text-gray-500">The new doubt summarizer is now live! Explore its capabilities.</div>
            </div>
            <div class="mb-2">
              <div class="font-semibold text-blue-800">System Maintenance</div>
              <div class="text-xs text-gray-500">Scheduled maintenance on 15th May, 10 PM - 12 AM IST.</div>
            </div>
            <div>
              <div class="font-semibold text-blue-800">Resource HUB Updates</div>
              <div class="text-xs text-gray-500">Latest academic papers for 'Advanced AI' course added.</div>
            </div>
          </div>
        </aside>
      </div>
    </main>
  </div>
</template>

