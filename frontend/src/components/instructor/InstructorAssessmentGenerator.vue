<template>
  <div class="d-flex">
    <div class="fixed top-0 left-0 h-screen w-64">
      <InstructorSidebar />
    </div>

    <main class="flex-1 flex flex-col min-h-screen ml-64 bg-gray-50">
      <div class="p-8">
        <div class="max-w-3xl mx-auto bg-white rounded-xl shadow-sm border border-gray-200 p-8">
          <div class="mb-6 border-b pb-4">
            <h1 class="text-2xl font-bold text-[#0d1b2a]">Generate New Assessment</h1>
            <p class="text-gray-500 text-sm mt-1">Configure AI parameters to generate questions.</p>
          </div>

          <form @submit.prevent="generateAssessment" class="space-y-6">
            <div class="grid grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Course ID <span class="text-red-500">*</span></label>
                <input v-model.number="form.courseId" type="number" required class="w-full p-2.5 border rounded-lg text-sm focus:ring-2 focus:ring-[#0d1b2a] outline-none" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Quiz Title <span class="text-red-500">*</span></label>
                <input v-model="form.title" type="text" required placeholder="e.g. Mid-Term Logic" class="w-full p-2.5 border rounded-lg text-sm focus:ring-2 focus:ring-[#0d1b2a] outline-none" />
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Topics</label>
              <div class="flex flex-wrap gap-2 mb-2">
                <span v-for="(topic, idx) in form.topics" :key="idx" class="bg-blue-50 text-blue-700 px-2 py-1 rounded-md text-sm flex items-center gap-2">
                  {{ topic.name }}
                  <button type="button" @click="removeTopic(idx)" class="hover:text-red-500"><i class="bi bi-x"></i></button>
                </span>
              </div>
              <div class="flex gap-2">
                <input v-model="newTopicName" @keydown.enter.prevent="addTopic" type="text" placeholder="Add topic and press Enter" class="flex-1 p-2.5 border rounded-lg text-sm" />
                <button type="button" @click="addTopic" class="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm font-medium">Add</button>
              </div>
            </div>

            <div class="grid grid-cols-3 gap-6">
               <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Difficulty</label>
                <select v-model="form.difficulty" class="w-full p-2.5 border rounded-lg text-sm bg-white">
                  <option>Easy</option><option>Medium</option><option>Hard</option><option>Mixed</option>
                </select>
               </div>
               <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Marks/Q</label>
                <input v-model.number="form.marks" type="number" class="w-full p-2.5 border rounded-lg text-sm" />
               </div>
               <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Total Qs</label>
                <input v-model.number="form.count" type="number" max="20" class="w-full p-2.5 border rounded-lg text-sm" />
               </div>
            </div>

            <div class="grid grid-cols-2 gap-4 pt-4">
              <div class="flex items-center gap-3">
                <input type="checkbox" id="useLatex" v-model="form.useLatex" class="w-4 h-4" />
                <label for="useLatex" class="text-sm text-gray-700">Enable LaTeX rendering (preview)</label>
              </div>
              <div class="flex items-center gap-4">
                <div class="text-sm text-gray-700">Publish Mode:</div>
                <label class="flex items-center gap-2 text-sm">
                  <input type="radio" value="manual" v-model="form.publishMode" name="publishMode" /> Manual Review
                </label>
                <label class="flex items-center gap-2 text-sm">
                  <input type="radio" value="auto" v-model="form.publishMode" name="publishMode" /> Auto Publish
                </label>
              </div>
            </div>

            <div class="pt-4 flex justify-end gap-3">
               <button type="button" @click="resetForm" class="px-5 py-2.5 text-gray-600 hover:bg-gray-50 rounded-lg text-sm font-medium">Reset</button>
               <button type="submit" :disabled="generating" class="px-6 py-2.5 bg-[#0d1b2a] text-white rounded-lg text-sm font-medium hover:bg-[#1b263b] disabled:opacity-50 flex items-center gap-2">
                  <span v-if="generating" class="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full"></span>
                  {{ generating ? 'Generating...' : 'Generate Quiz' }}
               </button>
            </div>
          </form>

          <div v-if="successMessage" class="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg text-green-800 text-sm flex items-center justify-between">
            <span>✓ {{ successMessage }}</span>
            <router-link to="/instructor/quiz-list" class="font-semibold underline ml-4">View all quizzes →</router-link>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import InstructorSidebar from '@/components/layout/instructorLayout/instructorSidebar.vue';
import { api } from '@/api';

const router = useRouter();
const generating = ref(false);
const successMessage = ref('');

// --- Form State ---
const newTopicName = ref('');
const form = reactive({
  courseId: 1,
  title: '',
  topics: [],
  difficulty: 'Medium',
  marks: 5,
  count: 5,
  useLatex: false,
  publishMode: 'manual' // 'manual' | 'auto'
});

const generateAssessment = async () => {
  if(form.topics.length === 0) return alert("Please add at least one topic");
  
  generating.value = true;
  successMessage.value = '';
  try {
    const payload = {
      course_id: form.courseId,
      title: form.title,
      topics: form.topics.map(t => t.name),
      difficulty: form.difficulty,
      marks_per_question: form.marks,
      num_questions: form.count,
      use_latex: form.useLatex,
      publish_mode: form.publishMode
    };

    // Increased timeout for AI generation
    const response = await api.post('/quizzes/generate', payload, { timeout: 60000 });
    
    successMessage.value = `Quiz "${form.title}" generated successfully!`;
    resetForm();
  } catch (err) {
    alert(err.response?.data?.detail || "Generation failed");
  } finally {
    generating.value = false;
  }
};

const addTopic = () => {
  if (newTopicName.value.trim()) {
    form.topics.push({ name: newTopicName.value.trim() });
    newTopicName.value = '';
  }
};

const removeTopic = (index) => {
  form.topics.splice(index, 1);
};

const resetForm = () => {
  form.title = '';
  form.topics = [];
  form.difficulty = 'Medium';
  form.marks = 5;
  form.count = 5;
  form.useLatex = false;
  form.publishMode = 'manual';
};
</script>

<style scoped>
</style>
