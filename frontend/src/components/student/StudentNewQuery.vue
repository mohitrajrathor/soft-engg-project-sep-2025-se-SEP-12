<template>
  <div class="d-flex vh-100">
    <!-- Sidebar -->
    <Sidebar />

    <!-- Main Content -->
    <div class="flex-grow-1 d-flex flex-column bg-light">
      <HeaderBar />

  <div class="flex justify-center items-start bg-gray-100 min-h-screen py-8 relative">
    <div class="bg-white w-11/12 max-w-6xl rounded-2xl shadow-lg p-8">
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-semibold text-gray-800">New Query</h2>
        <button class="text-gray-500 hover:text-gray-700">
          <i class="bi bi-x-lg"></i>
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Left Section -->
        <div class="space-y-4">
          <!-- Course -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Course</label>
            <select
              v-model="course"
              class="w-full border border-gray-300 rounded-lg p-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">Select course</option>
              <option>CS 201 - Data Structures</option>
              <option>CS 301 - Algorithms</option>
              <option>CS 101 - Programming Fundamentals</option>
            </select>
          </div>

          <!-- Title -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Title</label>
            <input
              type="text"
              v-model="title"
              placeholder="Segmentation fault when using linked list iterator"
              class="w-full border border-gray-300 rounded-lg p-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <!-- Details -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Details</label>
            <textarea
              v-model="details"
              rows="4"
              placeholder="Describe the issue, expected behavior, steps to reproduce..."
              class="w-full border border-gray-300 rounded-lg p-2 focus:ring-blue-500 focus:border-blue-500"
            ></textarea>
          </div>

          <!-- Attachments -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Attachments</label>
            <div
              class="flex items-center justify-between border border-gray-300 rounded-lg p-2 text-gray-500 hover:bg-gray-50 cursor-pointer"
            >
              <span><i class="bi bi-paperclip"></i> Upload files</span>
              <i class="bi bi-upload"></i>
            </div>
            <div class="flex gap-2 mt-2">
              <span class="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded-full">C++</span>
              <span class="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded-full">pointers</span>
              <span class="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded-full">linked-list</span>
            </div>
          </div>
        </div>

        <!-- Right Section -->
        <div class="space-y-4">
          <!-- Visibility -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Visibility</label>
            <select
              v-model="visibility"
              class="w-full border border-gray-300 rounded-lg p-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option>Visible to course</option>
              <option>Visible to instructors only</option>
            </select>
          </div>

          <!-- Category -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
            <select
              v-model="category"
              class="w-full border border-gray-300 rounded-lg p-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option>Programming Help</option>
              <option>Assignment Doubt</option>
              <option>Conceptual Clarification</option>
            </select>
          </div>

          <!-- Priority -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Priority</label>
            <select
              v-model="priority"
              class="w-full border border-gray-300 rounded-lg p-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option>Normal</option>
              <option>High</option>
            </select>
          </div>

          <!-- Generate Prompt -->
          <div>
            <button
              @click="togglePrompt"
              class="w-full px-4 py-2 mt-2 bg-blue-50 border border-blue-300 rounded-lg text-blue-700 hover:bg-blue-100 transition flex justify-between items-center"
            >
              <span>Generate Prompt</span>
              <i :class="showPrompt ? 'bi bi-chevron-up' : 'bi bi-chevron-down'"></i>
            </button>

            <transition name="slide">
              <div
                v-if="showPrompt"
                class="mt-3 border border-gray-300 rounded-lg bg-gray-50 p-3 overflow-hidden"
              >
                <textarea
                  v-model="generatedPrompt"
                  rows="5"
                  class="w-full p-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
                ></textarea>
              </div>
            </transition>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="flex justify-end items-center gap-3 mt-8">
        <button
          class="px-4 py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-100 transition"
        >
          Save Draft
        </button>
        <button
          @click="handleAskAI"
          class="px-5 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition"
        >
          Ask AI
        </button>
      </div>
    </div>

    <!-- AI Response Overlay -->
    <transition name="fade">
      <div
        v-if="showAIOverlay"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      >
        <div class="bg-white w-11/12 max-w-4xl p-8 rounded-2xl shadow-2xl relative">
          <button
            @click="showAIOverlay = false"
            class="absolute top-4 right-4 text-gray-500 hover:text-gray-700"
          >
            <i class="bi bi-x-lg"></i>
          </button>
          <h2 class="text-2xl font-semibold text-gray-800 mb-4">AI Response</h2>

          <div
            class="bg-gray-50 border border-gray-200 rounded-lg p-4 text-gray-700 max-h-[60vh] overflow-y-auto"
          >
            <p class="whitespace-pre-line">{{ aiResponse }}</p>
          </div>

          <div class="text-right mt-6">
            <button
              @click="sendToInstructor"
              class="px-5 py-2 rounded-lg bg-blue-100 text-blue-700 hover:bg-blue-200 transition"
            >
              Not satisfied? Ask TA/Instructor →
            </button>
          </div>
        </div>
      </div>
      
    </transition>
  </div>
    </div>
  </div>
</template>

<script setup>
import Sidebar from '@/components/layout/StudentLayout/SideBar.vue'
import HeaderBar from '@/components/layout/StudentLayout/HeaderBar.vue'

import { ref } from "vue";

const title = ref("");
const details = ref("");
const category = ref("");
const priority = ref("");
const visibility = ref("");
const course = ref("");
const aiResponse = ref("");
const showAIOverlay = ref(false);
const showPrompt = ref(false);
const generatedPrompt = ref("");

// Build prompt text
const buildPrompt = () => {
  return `
You are an academic assistant.
Course: ${course.value}
Category: ${category.value}
Title: ${title.value}
Details: ${details.value}
Priority: ${priority.value}
Visibility: ${visibility.value}
Generate a summarized answer for the student's question with clear reasoning.
  `.trim();
};

// Toggle prompt visibility and populate
const togglePrompt = () => {
  if (!showPrompt.value) {
    generatedPrompt.value = buildPrompt();
  }
  showPrompt.value = !showPrompt.value;
};

// Simulate AI response
const handleAskAI = () => {
  const prompt = generatedPrompt.value || buildPrompt();
  console.log("Prompt sent to AI:", prompt);
  aiResponse.value =
    "It seems your segmentation fault is likely caused by dereferencing a null or invalid iterator in your linked list traversal. Make sure to check if your iterator has reached the end before accessing its value.";
  showAIOverlay.value = true;
};

const sendToInstructor = () => {
  alert("Your query has been sent to the instructor.");
  showAIOverlay.value = false;
};
</script>

<style scoped>
/* Smooth slide transition */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.35s ease;
  max-height: 500px;
}
.slide-enter-from,
.slide-leave-to {
  max-height: 0;
  opacity: 0;
}

/* Fade overlay */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>