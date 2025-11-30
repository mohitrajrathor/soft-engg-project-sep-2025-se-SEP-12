<template>
  <div class="flex min-h-screen bg-slate-50 text-slate-800">
    <component :is="role === 'ta' ? taSidebar : instructorSidebar" />
    <main class="flex-1 ml-64 p-6 lg:p-10" v-if="deck">
      <div class="max-w-5xl mx-auto">
        <div class="mb-8 flex items-center justify-between">
          <div>
            <h1 class="font-extrabold text-3xl text-slate-900 tracking-tight">{{ deck.title }}</h1>
            <p class="text-slate-500 mt-1">Course #{{ deck.course_id }} • {{ formatDate(deck.created_at) }}</p>
          </div>
          <div class="flex gap-2">
            <RouterLink :to="`/${role}/slide-deck/${deck.id}/edit`" class="px-4 py-2 bg-amber-600 hover:bg-amber-700 text-white font-bold rounded-lg">✏️ Edit</RouterLink>
            <RouterLink :to="`/${role}/slide-decks`" class="px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold rounded-lg">← Back</RouterLink>
          </div>
        </div>
        <div v-if="deck.description" class="mb-6 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <h2 class="text-sm font-bold uppercase text-slate-600 mb-2">Description</h2>
          <p class="text-slate-700">{{ deck.description }}</p>
        </div>
        <div class="space-y-6">
          <div v-for="(slide, idx) in deck.slides" :key="idx" class="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
            <div class="flex items-center justify-between mb-3">
              <h3 class="text-lg font-bold text-slate-900">Slide {{ idx + 1 }}: {{ slide.title }}</h3>
            </div>
            <div class="prose max-w-none" v-html="renderMarkdown(slide.content)"></div>
            <div v-if="slide.graph_image" class="mt-4">
              <img :src="slide.graph_image" alt="Chart" class="w-full max-w-xl rounded-lg border" />
            </div>
          </div>
        </div>
      </div>
    </main>
    <main v-else class="flex-1 ml-64 p-10 flex items-center justify-center">
      <p class="text-slate-500">Loading deck...</p>
    </main>
  </div>
</template>
<script setup>
import instructorSidebar from '@/components/layout/instructorLayout/instructorSideBar.vue'
import taSidebar from '@/components/layout/TaLayout/TASidebar.vue'
import { api } from '@/api'
import { ref, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import MarkdownIt from 'markdown-it'

const props = defineProps({
  role: {
    type: String,
    default: 'instructor'
  }
})

const md = new MarkdownIt()
const route = useRoute()
const deck = ref(null)
function renderMarkdown(content){ return md.render(content || '') }
function formatDate(date){ return new Date(date).toLocaleDateString('en-US',{year:'numeric',month:'short',day:'numeric'}) }
async function load(){
  try { const res = await api.get(`/slide-decks/${route.params.id}`); deck.value = res.data } catch(e){ console.error(e) }
}
onMounted(load)
</script>
<style scoped>
.prose :where(h1,h2,h3){margin-top:0}
</style>
