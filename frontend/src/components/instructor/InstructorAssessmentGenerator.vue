<template>
  <div class="flex h-screen w-full bg-gray-50 overflow-hidden">
    
    <div class="w-[250px] flex-shrink-0 h-full border-r bg-white z-20">
      <InstructorSidebar />
    </div>

    <main class="flex-1 flex flex-col h-full overflow-hidden bg-[#f8fafc] relative">
      
      <div class="flex-1 overflow-y-auto p-8 custom-scrollbar">
        
        <div v-if="viewMode === 'create'" class="max-w-3xl mx-auto bg-white rounded-xl shadow-sm border border-gray-200 p-8">
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

            <div class="pt-4 flex justify-end gap-3">
               <button type="button" @click="resetForm" class="px-5 py-2.5 text-gray-600 hover:bg-gray-50 rounded-lg text-sm font-medium">Reset</button>
               <button type="submit" :disabled="generating" class="px-6 py-2.5 bg-[#0d1b2a] text-white rounded-lg text-sm font-medium hover:bg-[#1b263b] disabled:opacity-50 flex items-center gap-2">
                  <span v-if="generating" class="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full"></span>
                  {{ generating ? 'Generating...' : 'Generate Quiz' }}
               </button>
            </div>
          </form>
        </div>

        <div v-else-if="viewMode === 'view' && selectedQuiz" class="max-w-4xl mx-auto">
          <div class="flex justify-between items-start mb-8">
            <div>
              <h1 class="text-3xl font-bold text-[#0d1b2a]">{{ selectedQuiz.title }}</h1>
              <p class="text-gray-500 mt-1">{{ selectedQuiz.description || 'No description provided.' }}</p>
              <div class="flex gap-4 mt-4 text-sm text-gray-600">
                <span class="bg-blue-50 text-blue-800 px-2 py-1 rounded">ID: {{ selectedQuiz.id }}</span>
                <span class="bg-green-50 text-green-800 px-2 py-1 rounded">{{ selectedQuiz.questions?.questions?.length || 0 }} Questions</span>
              </div>
            </div>
            <div class="flex gap-2">
              <button @click="deleteQuiz(selectedQuiz.id)" class="px-4 py-2 text-red-600 bg-red-50 hover:bg-red-100 rounded-lg text-sm font-medium transition-colors">
                <i class="bi bi-trash3 mr-1"></i> Delete
              </button>
              <button class="px-4 py-2 text-white bg-[#0d1b2a] hover:bg-[#1b263b] rounded-lg text-sm font-medium transition-colors">
                <i class="bi bi-pencil mr-1"></i> Edit
              </button>
            </div>
          </div>

          <div class="space-y-6">
             <div v-for="(q, index) in selectedQuiz.questions.questions" :key="index" class="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <div class="flex justify-between items-start mb-4">
                   <h3 class="font-semibold text-lg text-[#0d1b2a]">Q{{ index + 1 }}: {{ q.question_text }}</h3>
                   <span class="text-xs font-bold bg-gray-100 px-2 py-1 rounded">{{ q.marks }} Marks</span>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4">
                   <div v-for="(opt, oIdx) in q.options" :key="oIdx" 
                        class="p-3 rounded-lg border text-sm"
                        :class="isCorrect(q, opt) ? 'bg-green-50 border-green-200 text-green-800' : 'bg-gray-50 border-gray-100'">
                      <span class="font-bold mr-2">{{ String.fromCharCode(65 + oIdx) }}.</span> {{ opt }}
                      <i v-if="isCorrect(q, opt)" class="bi bi-check-circle-fill float-right"></i>
                   </div>
                </div>
                <div v-if="q.explanation" class="bg-blue-50/50 p-3 rounded-lg text-sm text-blue-800">
                   <strong><i class="bi bi-info-circle mr-1"></i> Explanation:</strong> {{ q.explanation }}
                </div>
             </div>
          </div>
        </div>

        <div v-else class="h-full flex flex-col items-center justify-center text-gray-400">
          <i class="bi bi-ui-checks text-6xl mb-4 opacity-20"></i>
          <p class="text-lg">Select a quiz to view details or create a new one.</p>
        </div>

      </div>
    </main>

    <aside class="w-96 flex flex-col border-l border-gray-200 bg-white h-full shadow-[-5px_0_15px_rgba(0,0,0,0.05)] z-30">
      
      <div class="p-5 border-b border-gray-100 bg-white z-10">
        <h2 class="text-xl font-bold text-[#0d1b2a] mb-3">Assessments</h2>
        <button 
          @click="switchToCreateMode"
          class="w-full flex items-center justify-center gap-2 bg-[#0d1b2a] text-white py-2.5 px-4 rounded-lg hover:bg-[#1b263b] transition-all shadow-sm text-sm font-medium"
        >
          <i class="bi bi-plus-lg"></i> New Quiz
        </button>
      </div>

      <div class="px-5 py-3 bg-gray-50 border-b border-gray-100">
        <div class="relative">
          <i class="bi bi-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm"></i>
          <input 
            v-model="searchQuery" 
            @input="fetchQuizzes"
            type="text" 
            placeholder="Search quizzes..." 
            class="w-full pl-9 pr-3 py-2 text-sm border border-gray-200 rounded-md focus:ring-2 focus:ring-[#0d1b2a]/10 focus:border-[#0d1b2a] outline-none transition-all bg-white"
          >
        </div>
      </div>

      <div class="flex-1 overflow-y-auto custom-scrollbar bg-white">
        <div v-if="loadingList" class="p-6 text-center">
          <div class="animate-spin inline-block w-5 h-5 border-2 border-[#0d1b2a] border-t-transparent rounded-full"></div>
        </div>

        <div v-else-if="quizzes.length === 0" class="p-6 text-center text-gray-500 text-sm">
          No quizzes found.
        </div>

        <ul v-else class="divide-y divide-gray-50">
          <li v-for="quiz in quizzes" :key="quiz.id">
            <button 
              @click="selectQuiz(quiz)"
              class="w-full text-left p-5 hover:bg-blue-50/30 transition-colors border-l-4 relative group"
              :class="selectedQuiz?.id === quiz.id ? 'bg-blue-50 border-[#0d1b2a]' : 'border-transparent'"
            >
              <div class="font-semibold text-[#0d1b2a] text-sm mb-1 pr-2">{{ quiz.title }}</div>
              <div class="text-xs text-gray-500 flex justify-between items-center mt-2">
                <span class="flex items-center"><i class="bi bi-list-ol mr-1"></i> {{ quiz.questions?.questions?.length || 0 }} Qs</span>
                <span>{{ formatDate(quiz.created_at) }}</span>
              </div>
              
              <div class="mt-3 flex flex-wrap gap-1">
                 <span v-for="topic in (quiz.topics || ['General']).slice(0,3)" :key="topic" class="text-[10px] px-2 py-0.5 bg-gray-100 rounded-full text-gray-600 border border-gray-200">
                    {{ typeof topic === 'string' ? topic : topic.name }}
                 </span>
              </div>
            </button>
          </li>
        </ul>
      </div>
    </aside>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import InstructorSidebar from '@/components/layout/instructorLayout/instructorSidebar.vue';
import { api } from '@/api';

// --- State ---
const quizzes = ref([]);
const loadingList = ref(false);
const searchQuery = ref('');
const viewMode = ref('create'); // 'create' | 'view' | 'empty'
const selectedQuiz = ref(null);
const generating = ref(false);

// --- Form State ---
const newTopicName = ref('');
const form = reactive({
  courseId: 1,
  title: '',
  topics: [],
  difficulty: 'Medium',
  marks: 5,
  count: 5
});

// --- Initial Load ---
onMounted(() => {
  fetchQuizzes();
});

// --- API Actions ---
const fetchQuizzes = async () => {
  loadingList.value = true;
  try {
    const params = searchQuery.value ? { search: searchQuery.value } : {};
    const response = await api.get('/quizzes/', { params });
    quizzes.value = response.data;
  } catch (err) {
    console.error("Fetch failed", err);
  } finally {
    loadingList.value = false;
  }
};

const generateAssessment = async () => {
  if(form.topics.length === 0) return alert("Please add at least one topic");
  
  generating.value = true;
  try {
    const payload = {
      course_id: form.courseId,
      title: form.title,
      topics: form.topics.map(t => t.name),
      difficulty: form.difficulty,
      marks_per_question: form.marks,
      num_questions: form.count
    };

    // Increased timeout for AI generation
    const response = await api.post('/quizzes/generate', payload, { timeout: 60000 });
    
    // Refresh list and select the new quiz
    await fetchQuizzes(); 
    const newQuiz = quizzes.value.find(q => q.id === response.data.id);
    if(newQuiz) selectQuiz(newQuiz);
    
    resetForm();
  } catch (err) {
    alert(err.response?.data?.detail || "Generation failed");
  } finally {
    generating.value = false;
  }
};

const deleteQuiz = async (id) => {
  if(!confirm("Delete this quiz?")) return;
  try {
    await api.delete(`/quizzes/${id}`);
    quizzes.value = quizzes.value.filter(q => q.id !== id);
    viewMode.value = 'create'; // Go back to create or empty
    selectedQuiz.value = null;
  } catch(err) {
    alert("Delete failed");
  }
};

// --- Interaction Logic ---
const switchToCreateMode = () => {
  viewMode.value = 'create';
  selectedQuiz.value = null;
};

const selectQuiz = (quiz) => {
  selectedQuiz.value = quiz;
  viewMode.value = 'view';
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
};

// --- Helpers ---
const formatDate = (d) => new Date(d).toLocaleDateString();

const isCorrect = (question, optionText) => {
  // Helper to check if an option is in the correct answers list
  return question.correct_answers.includes(optionText);
};
</script>

<style scoped>
/* Custom Scrollbar for the list */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>