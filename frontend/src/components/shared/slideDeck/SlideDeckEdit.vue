<template>
  <div class="flex min-h-screen bg-slate-50 text-slate-800">
    <component :is="role === 'ta' ? taSidebar : instructorSidebar" />
    <main class="flex-1 ml-64 p-6 lg:p-10" v-if="deck">
      <div class="max-w-5xl mx-auto">
        <div class="mb-8 flex items-center justify-between">
          <div>
            <h1 class="font-extrabold text-3xl text-slate-900 tracking-tight">Edit Deck: {{ deck.title }}</h1>
            <p class="text-slate-500 mt-1">Course #{{ deck.course_id }} • {{ formatDate(deck.created_at) }}</p>
          </div>
          <div class="flex gap-2">
            <RouterLink :to="`/${role}/slide-deck/${deck.id}`" class="px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold rounded-lg">← Back</RouterLink>
            <button @click="save" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg" :disabled="saving">💾 {{ saving? 'Saving...' : 'Save' }}</button>
          </div>
        </div>
        <div class="mb-6 bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <label class="text-xs font-bold uppercase text-slate-600 mb-1">Deck Title</label>
          <input v-model="deck.title" class="w-full px-3 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none mb-3" />
          <label class="text-xs font-bold uppercase text-slate-600 mb-1">Description</label>
          <textarea v-model="deck.description" rows="3" class="w-full px-3 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none"></textarea>
        </div>
        <div class="space-y-6">
          <div v-for="(slide, idx) in deck.slides" :key="idx" class="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
            <div class="flex items-center justify-between mb-3">
              <h3 class="text-lg font-bold text-slate-900">Slide {{ idx + 1 }}</h3>
              <button @click="removeSlide(idx)" class="text-xs px-2 py-1 bg-red-100 text-red-600 rounded hover:bg-red-200">✕ Remove</button>
            </div>
            <label class="text-xs font-bold uppercase text-slate-600 mb-1">Title</label>
            <input v-model="slide.title" class="w-full mb-3 px-3 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none" />
            <label class="text-xs font-bold uppercase text-slate-600 mb-1">Content (Markdown)</label>
            <textarea v-model="slide.content" rows="6" class="w-full px-3 py-2 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 outline-none font-mono text-sm"></textarea>
            <div v-if="slide.graph_image" class="mt-4">
              <p class="text-xs font-bold uppercase text-slate-600 mb-2">Graph Preview</p>
              <img :src="slide.graph_image" alt="Chart" class="w-full max-w-xl rounded-lg border" />
            </div>
          </div>
          <button @click="addSlide" class="w-full py-3 border-2 border-dashed border-slate-300 rounded-xl text-slate-600 hover:border-blue-400 hover:text-blue-600 font-bold text-sm">+ Add Slide</button>
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
import { useRoute, useRouter, RouterLink } from 'vue-router'

const props = defineProps({
  role: {
    type: String,
    default: 'instructor'
  }
})

const route = useRoute(); const router = useRouter()
const deck = ref(null); const saving = ref(false)
function formatDate(date){ return new Date(date).toLocaleDateString('en-US',{year:'numeric',month:'short',day:'numeric'}) }
async function load(){ try { const res = await api.get(`/slide-decks/${route.params.id}`); deck.value = res.data } catch(e){ console.error(e) } }
function addSlide(){ deck.value.slides.push({ title: 'New Slide', content: 'Describe content here...', graph_data: null, graph_image: null }) }
function removeSlide(i){ deck.value.slides.splice(i,1) }
async function save(){ saving.value = true; try { await api.put(`/slide-decks/${deck.value.id}`, { title: deck.value.title, description: deck.value.description, slides: deck.value.slides }); alert('Saved!'); router.push(`/${props.role}/slide-deck/${deck.value.id}`) } catch(e){ console.error(e); alert('Save failed: '+(e.response?.data?.detail||e.message)) } finally { saving.value=false } }
onMounted(load)
</script>
<style scoped></style>
