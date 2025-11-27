<template>
  <div class="d-flex">
    <div class="fixed top-0 left-0 h-screen w-64">
      <InstructorSidebar />
    </div>

    <main class="flex-1 flex flex-col min-h-screen ml-64 bg-gray-50">
      <div class="p-8">
        <router-link to="/instructor/quiz-list"
          class="mb-4 text-[#0d1b2a] hover:underline flex items-center gap-2"
        >
          ← Back to Quizzes
        </router-link>

        <div v-if="loading" class="flex justify-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#0d1b2a]"></div>
        </div>

        <div v-else-if="quiz" class="bg-white rounded-lg shadow-md p-8 max-w-5xl">
          <div class="flex justify-between items-start mb-6">
            <div class="flex-1">
              <h1 class="text-3xl font-bold text-[#0d1b2a] mb-2">{{ quiz.title }}</h1>
              <p class="text-gray-600">{{ quiz.description }}</p>
            </div>
            <div class="flex gap-2">
              <button
                @click="showUpdateModal = true"
                class="bg-[#0d1b2a] text-white px-4 py-2 rounded hover:bg-[#1b263b] transition"
              >
                Update Quiz
              </button>
            </div>
          </div>

          <div class="mb-6 text-sm text-gray-600 bg-gray-50 p-4 rounded-lg">
            <p><strong>Course ID:</strong> {{ quiz.course_id }}</p>
            <p><strong>Created by:</strong> {{ quiz.creator.name || quiz.creator.email }}</p>
            <p><strong>Created at:</strong> {{ formatDate(quiz.created_at) }}</p>
            <p><strong>Publish Mode:</strong> {{ quiz.publish_mode === 'auto' ? 'Auto Publish' : 'Manual Review' }}</p>
            <p><strong>Status:</strong> <span :class="quiz.is_published ? 'text-green-600 font-semibold' : 'text-yellow-600 font-semibold'">{{ quiz.is_published ? 'Published' : 'Draft' }}</span></p>
          </div>

          <!-- Questions -->
          <div class="space-y-6">
            <h2 class="text-2xl font-semibold text-[#0d1b2a] mb-4">Questions</h2>
            <div
              v-for="(question, index) in quiz.questions.questions"
              :key="index"
              class="border border-gray-200 rounded-lg p-6 bg-gray-50"
            >
              <div class="flex justify-between items-start mb-3">
                <h3 class="text-lg font-semibold text-gray-800">
                  {{ index + 1 }}. {{ question.question_text }}
                </h3>
                <span class="bg-blue-100 text-blue-800 px-3 py-1 rounded text-sm">
                  {{ question.marks }} marks
                </span>
              </div>

              <p class="text-sm text-gray-500 mb-3">
                Type: <strong>{{ question.question_type.toUpperCase() }}</strong>
              </p>

              <div class="space-y-2 mb-4">
                <p class="font-medium text-gray-700">Options:</p>
                <ul class="list-disc list-inside space-y-1">
                  <li
                    v-for="(option, optIdx) in question.options"
                    :key="optIdx"
                    :class="{
                      'text-green-600 font-semibold': question.correct_answers.includes(option)
                    }"
                  >
                    {{ option }}
                    <span v-if="question.correct_answers.includes(option)" class="text-green-600">
                      ✓ (Correct)
                    </span>
                  </li>
                </ul>
              </div>

              <div v-if="question.explanation" class="bg-blue-50 border-l-4 border-blue-500 p-3 text-sm">
                <strong>Explanation:</strong> {{ question.explanation }}
              </div>
            </div>
          </div>
        </div>

        <!-- Update Modal -->
        <div
          v-if="showUpdateModal"
          class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
          @click.self="showUpdateModal = false"
        >
          <div class="bg-white rounded-lg p-8 max-w-2xl w-full mx-4">
            <h2 class="text-2xl font-bold text-[#0d1b2a] mb-4">Update Quiz</h2>
            <textarea
              v-model="updateFeedback"
              placeholder="Describe the changes you want (e.g., 'Make question 3 harder', 'Add a question about loops')"
              rows="6"
              class="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-[#0d1b2a] focus:outline-none mb-4"
            ></textarea>
            
            <div v-if="updateError" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
              {{ updateError }}
            </div>

            <div class="flex justify-end space-x-3">
              <button
                @click="showUpdateModal = false"
                class="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50 transition"
              >
                Cancel
              </button>
              <button
                @click="updateQuiz"
                :disabled="updatingQuiz || !updateFeedback.trim()"
                class="bg-[#0d1b2a] text-white px-4 py-2 rounded hover:bg-[#1b263b] transition disabled:opacity-50"
              >
                {{ updatingQuiz ? 'Updating...' : 'Update Quiz' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import InstructorSidebar from '@/components/layout/instructorLayout/instructorSidebar.vue';
import { api } from '@/api';

const route = useRoute();
const router = useRouter();

const quiz = ref(null);
const loading = ref(false);
const currentUserId = ref(null); // Set from auth

const showUpdateModal = ref(false);
const updateFeedback = ref('');
const updatingQuiz = ref(false);
const updateError = ref('');

onMounted(() => {
  fetchQuiz();
  // currentUserId.value = useAuthStore().user.id;
});

const fetchQuiz = async () => {
  loading.value = true;
  try {
    const response = await api.get(`/quizzes/${route.params.id}`);
    quiz.value = response.data;
  } catch (err) {
    console.error('Fetch quiz error:', err);
    alert('Failed to load quiz');
  } finally {
    loading.value = false;
  }
};

const updateQuiz = async () => {
  if (!updateFeedback.value.trim()) {
    updateError.value = 'Please provide feedback for the update.';
    return;
  }

  updatingQuiz.value = true;
  updateError.value = '';

  try {
    const response = await api.put(`/quizzes/${quiz.value.id}`, {
      feedback: updateFeedback.value.trim()
    });
    quiz.value = response.data;
    showUpdateModal.value = false;
    updateFeedback.value = '';
    alert('Quiz updated successfully!');
  } catch (err) {
    console.error('Update quiz error:', err);
    updateError.value = err.response?.data?.detail || 'Failed to update quiz';
  } finally {
    updatingQuiz.value = false;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleString();
};
</script>