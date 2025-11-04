<template>
  <div class="flex">
    <!-- Sidebar -->
    <div class="fixed top-0 left-0 h-screen w-[250px]">
      <InstructorSidebar />
    </div>

    <!-- Main content area -->
    <main class="flex-1 flex flex-col min-h-screen ml-[250px] bg-gray-50">
      <!-- Page Content -->
      <div class="flex justify-center items-start p-8 overflow-auto flex-1">
        <div
          class="w-full max-w-4xl bg-white shadow-md rounded-xl p-8 border border-gray-200"
        >
          <!-- Title -->
          <h1
            class="text-2xl font-semibold text-[#0d1b2a] mb-2 text-center tracking-wide"
          >
            Automated Assessment Generator
          </h1>
          <p class="text-gray-500 text-center mb-8 text-sm">
            Configure your question paper by topics, difficulty, and marks distribution.
          </p>

          <!-- Input Form -->
          <div class="space-y-6">
            <!-- Course Name -->
            <div>
              <label class="block text-gray-700 font-medium mb-2">Course Name</label>
              <input
                v-model="courseName"
                type="text"
                placeholder="Enter course name (e.g., Data Structures)"
                class="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-[#0d1b2a] focus:outline-none"
              />
            </div>

            <!-- Topics (Dynamic Multiple) -->
            <div>
              <label class="block text-gray-700 font-medium mb-2">Topics</label>
              <div class="space-y-3">
                <div
                  v-for="(topic, index) in topics"
                  :key="index"
                  class="flex items-center space-x-3"
                >
                  <input
                    v-model="topic.name"
                    type="text"
                    placeholder="Enter topic name (e.g., Arrays, Trees)"
                    class="flex-1 p-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-[#0d1b2a] focus:outline-none"
                  />
                  <button
                    @click="removeTopic(index)"
                    class="text-red-500 hover:text-red-600"
                    title="Remove Topic"
                  >
                    <i class="bi bi-trash3"></i>
                  </button>
                </div>
                <button
                  @click="addTopic"
                  class="flex items-center text-[#0d1b2a] font-medium hover:underline"
                >
                  <i class="bi bi-plus-circle mr-2"></i> Add Another Topic
                </button>
              </div>
            </div>

            <!-- Difficulty Level -->
            <div>
              <label class="block text-gray-700 font-medium mb-2"
                >Difficulty Level</label
              >
              <select
                v-model="difficulty"
                class="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-[#0d1b2a] focus:outline-none bg-white"
              >
                <option value="Easy">Easy</option>
                <option value="Medium">Medium</option>
                <option value="Hard">Hard</option>
                <option value="Mixed">Mixed (Auto-distributed)</option>
              </select>
            </div>

            <!-- Marks Allocation -->
            <div>
              <label class="block text-gray-700 font-medium mb-2"
                >Marks per Question</label
              >
              <input
                v-model.number="marksPerQuestion"
                type="number"
                min="1"
                placeholder="Enter marks per question"
                class="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-[#0d1b2a] focus:outline-none"
              />
            </div>

            <!-- Number of Questions -->
            <div>
              <label class="block text-gray-700 font-medium mb-2"
                >Total Questions</label
              >
              <input
                v-model.number="numQuestions"
                type="number"
                min="1"
                placeholder="e.g., 10"
                class="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-[#0d1b2a] focus:outline-none"
              />
            </div>

            <!-- Review Mode -->
            <div>
              <label class="block text-gray-700 font-medium mb-2"
                >Review Mode</label
              >
              <div class="flex items-center space-x-6">
                <label class="flex items-center space-x-2">
                  <input
                    type="radio"
                    value="manual"
                    v-model="reviewMode"
                    class="text-[#0d1b2a]"
                  />
                  <span>Manual Review (Instructor/TA verifies)</span>
                </label>
                <label class="flex items-center space-x-2">
                  <input
                    type="radio"
                    value="auto"
                    v-model="reviewMode"
                    class="text-[#0d1b2a]"
                  />
                  <span>Auto Generate (Publish instantly)</span>
                </label>
              </div>
            </div>

            <!-- Generate Button -->
            <div class="flex justify-center mt-6">
              <button
                @click="generateAssessment"
                class="bg-[#0d1b2a] text-white px-6 py-3 rounded-lg font-medium hover:bg-[#1b263b] transition flex items-center space-x-2"
              >
                <i class="bi bi-cpu"></i>
                <span>Generate Question Paper</span>
              </button>
            </div>

            <!-- Generated Summary -->
            <div
              v-if="generatedSummary"
              class="mt-8 bg-gray-50 border border-gray-200 p-5 rounded-lg shadow-sm"
            >
              <h2 class="text-lg font-semibold text-[#0d1b2a] mb-3">
                Assessment Summary
              </h2>
              <p class="text-gray-700 text-sm leading-relaxed">
                <strong>Course:</strong> {{ courseName }} <br />
                <strong>Topics:</strong> {{ topics.map((t) => t.name).join(", ") }}<br />
                <strong>Difficulty:</strong> {{ difficulty }} <br />
                <strong>Marks/Question:</strong> {{ marksPerQuestion }} <br />
                <strong>Total Questions:</strong> {{ numQuestions }} <br />
                <strong>Review Mode:</strong>
                {{ reviewMode === "manual" ? "Manual Review" : "Auto Generate" }}
              </p>
              <div class="flex justify-end mt-4">
                <button
                  class="bg-[#0d1b2a] text-white px-4 py-2 rounded hover:bg-[#1b263b] transition"
                >
                  View Generated Paper
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from "vue";
import InstructorSidebar from '@/components/layout/instructorLayout/instructorSidebar.vue';

const courseName = ref("");
const topics = ref([{ name: "" }]);
const difficulty = ref("Easy");
const marksPerQuestion = ref(1);
const numQuestions = ref(10);
const reviewMode = ref("manual");
const generatedSummary = ref(false);

const addTopic = () => {
  topics.value.push({ name: "" });
};

const removeTopic = (index) => {
  topics.value.splice(index, 1);
};

const generateAssessment = () => {
  if (!courseName.value || topics.value.length === 0 || numQuestions.value <= 0) {
    alert("Please fill all required fields.");
    return;
  }
  generatedSummary.value = true;
};
</script>