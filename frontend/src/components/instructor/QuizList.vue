<template>
  <div class="flex">
    <div class="fixed top-0 left-0 h-screen w-[250px]">
      <InstructorSidebar />
    </div>

    <main class="flex-1 flex flex-col min-h-screen ml-[250px] bg-gray-50 ml-64">
      <div class="p-8">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-3xl font-bold text-[#0d1b2a]">All Quizzes</h1>
          <button
            @click="router.push('/instructor/quizzes/generate')"
            class="bg-[#0d1b2a] text-white px-4 py-2 rounded hover:bg-[#1b263b] transition"
          >
            <i class="bi bi-plus-circle mr-2"></i>Create New Quiz
          </button>
        </div>

        <!-- Search and Filter -->
        <div class="flex space-x-4 mb-6">
          <input
            v-model="searchQuery"
            @input="fetchQuizzes"
            type="text"
            placeholder="Search quizzes..."
            class="flex-1 p-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-[#0d1b2a] focus:outline-none"
          />
          <input
            v-model.number="filterCourseId"
            @input="fetchQuizzes"
            type="number"
            placeholder="Filter by Course ID"
            class="w-48 p-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-[#0d1b2a] focus:outline-none"
          />
        </div>

        <!-- Loading -->
        <div v-if="loading" class="flex justify-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#0d1b2a]"></div>
        </div>

        <!-- Quiz List -->
        <div v-else-if="quizzes.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="quiz in quizzes"
            :key="quiz.id"
            class="bg-white rounded-lg shadow-md p-6 border border-gray-200 hover:shadow-lg transition"
          >
            <h3 class="text-xl font-semibold text-[#0d1b2a] mb-2">{{ quiz.title }}</h3>
            <p class="text-gray-600 text-sm mb-4">{{ quiz.description || 'No description' }}</p>
            
            <div class="text-sm text-gray-500 space-y-1 mb-4">
              <p><strong>Course ID:</strong> {{ quiz.course_id }}</p>
              <p><strong>Questions:</strong> {{ quiz.questions?.questions?.length || 0 }}</p>
              <p><strong>Created:</strong> {{ formatDate(quiz.created_at) }}</p>
            </div>

            <div class="flex space-x-2">
              <button
                @click="viewQuiz(quiz.id)"
                class="flex-1 bg-[#0d1b2a] text-white px-3 py-2 rounded text-sm hover:bg-[#1b263b] transition"
              >
                View
              </button>
              <button
                v-if="quiz.creator.id === currentUserId"
                @click="deleteQuiz(quiz.id)"
                class="bg-red-500 text-white px-3 py-2 rounded text-sm hover:bg-red-600 transition"
              >
                Delete
              </button>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-12">
          <p class="text-gray-500">No quizzes found.</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import InstructorSidebar from '@/components/layout/instructorLayout/instructorSidebar.vue';
import { api } from '@/api';

const router = useRouter();
const quizzes = ref([]);
const loading = ref(false);
const searchQuery = ref('');
const filterCourseId = ref(null);
const currentUserId = ref(null); // Set from auth state

onMounted(() => {
  fetchQuizzes();
  // Get current user ID from your auth store/composable
  // currentUserId.value = useAuthStore().user.id;
});

const fetchQuizzes = async () => {
  loading.value = true;
  try {
    const params = {};
    if (searchQuery.value) params.search = searchQuery.value;
    if (filterCourseId.value) params.course_id = filterCourseId.value;

    const response = await api.get('/quizzes/', { params });
    quizzes.value = response.data;
  } catch (err) {
    console.error('Fetch quizzes error:', err);
    alert('Failed to load quizzes');
  } finally {
    loading.value = false;
  }
};

const viewQuiz = (quizId) => {
  router.push(`/instructor/quizzes/${quizId}`);
};

const deleteQuiz = async (quizId) => {
  if (!confirm('Are you sure you want to delete this quiz?')) return;

  try {
    await api.delete(`/quizzes/${quizId}`);
    quizzes.value = quizzes.value.filter(q => q.id !== quizId);
    alert('Quiz deleted successfully');
  } catch (err) {
    console.error('Delete quiz error:', err);
    alert('Failed to delete quiz');
  }
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString();
};
</script>