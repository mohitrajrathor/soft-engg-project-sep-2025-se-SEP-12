<template>
  <div class="flex min-h-screen bg-slate-50 text-slate-800">
    <!-- Role-based sidebar -->
    <component :is="role === 'ta' ? taSidebar : instructorSidebar" class="print:hidden" />

    <main class="flex-1 ml-64 p-6 lg:p-8 print:ml-0">
      <div class="max-w-[1600px] mx-auto flex flex-col gap-6">
        <!-- Config / Actions Bar -->
        <div class="bg-white border border-slate-200 rounded-3xl shadow-sm p-6 flex flex-col gap-4">
          <div class="flex items-start justify-between flex-wrap gap-4">
            <div class="flex-1 min-w-[280px]">
              <h1 class="font-extrabold text-3xl tracking-tight">Slide Deck Workspace</h1>
              <p class="text-slate-500 text-sm mt-1">Unified generation, editing & export environment.</p>
            </div>
            <div class="flex items-center gap-2 flex-wrap">
              <button @click="preview" :disabled="loading" class="btn-secondary">🔍 Preview</button>
              <button @click="generate" :disabled="loading" class="btn-primary">⚙️ {{ deckId ? 'Regenerate' : 'Generate' }}</button>
              <button @click="addSlide" :disabled="loading" class="btn-secondary">➕ Add Slide</button>
              <button @click="duplicateSlide(currentIndex)" :disabled="!currentSlide" class="btn-secondary">📄 Duplicate</button>
              <button @click="save" :disabled="!deckId || loading" class="btn-success">💾 Save</button>
              <button @click="openExport('pptx')" :disabled="slides.length===0" class="btn-secondary">📊 PPTX</button>
              <button @click="openExport('pdf')" :disabled="slides.length===0" class="btn-secondary">🖨️ PDF</button>
            </div>
          </div>

          <!-- Config Panel -->
          <details class="group" open>
            <summary class="cursor-pointer flex items-center justify-between py-2 font-bold text-xs text-slate-600 uppercase tracking-wide">
              <span>Configuration</span>
              <span class="text-[10px] text-slate-400 group-open:hidden">(expand)</span>
              <span class="text-[10px] text-slate-400 hidden group-open:inline">(collapse)</span>
            </summary>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-2">
              <div>
                <label class="form-label">Course ID *</label>
                <input v-model.number="config.courseId" type="number" class="form-input" />
              </div>
              <div class="md:col-span-2">
                <label class="form-label">Title *</label>
                <input v-model="config.title" type="text" class="form-input" />
              </div>
              <div class="md:col-span-3">
                <label class="form-label">Description</label>
                <textarea v-model="config.description" rows="2" class="form-input"></textarea>
              </div>
              <div>
                <label class="form-label">Format</label>
                <select v-model="config.format" class="form-input">
                  <option value="presentation">Presentation</option>
                  <option value="document">Document</option>
                </select>
              </div>
              <div>
                <label class="form-label">Slides</label>
                <input v-model.number="config.numSlides" type="number" min="1" max="20" class="form-input" />
              </div>
              <div>
                <label class="form-label">Include Graphs</label>
                <div class="flex items-center gap-2">
                  <input type="checkbox" v-model="config.includeGraphs" />
                  <span class="text-xs text-slate-600">Enable AI chart embedding</span>
                </div>
                <div v-if="config.includeGraphs" class="flex flex-wrap gap-2 mt-2">
                  <label v-for="g in graphOptions" :key="g" class="flex items-center gap-1 text-[10px] font-semibold text-slate-600">
                    <input type="checkbox" v-model="config.graphTypes" :value="g" /> {{ g }}
                  </label>
                </div>
              </div>
              <div class="md:col-span-3">
                <label class="form-label">Topics *</label>
                <div class="flex flex-wrap gap-2 mb-2">
                  <span v-for="(t,i) in config.topics" :key="i" class="px-2 py-1 rounded bg-slate-100 text-[11px] font-semibold flex items-center gap-1">
                    {{ t }} <button @click="config.topics.splice(i,1)" class="text-slate-400 hover:text-red-500">✕</button>
                  </span>
                </div>
                <div class="flex gap-2">
                  <input v-model="newTopic" @keyup.enter.prevent="addTopic" placeholder="Add topic & hit Enter" class="form-input flex-1" />
                  <button @click="addTopic" class="btn-secondary">Add</button>
                  <button @click="config.topics=[]" class="btn-danger" v-if="config.topics.length">Clear</button>
                </div>
              </div>
            </div>
          </details>

          <!-- Preview Outline -->
          <div v-if="previewOutline.length" class="mt-4 bg-slate-50 border border-slate-200 rounded-xl p-4">
            <div class="flex items-center justify-between mb-2">
              <h3 class="text-xs font-bold uppercase tracking-wide text-slate-600">Preview Outline</h3>
              <button @click="previewOutline=[]" class="text-[10px] text-slate-400 hover:text-red-500">Clear</button>
            </div>
            <ol class="list-decimal ml-4 space-y-1 text-xs text-slate-700">
              <li v-for="(item,i) in previewOutline" :key="i">{{ item }}</li>
            </ol>
          </div>
        </div>

        <!-- Workspace Body -->
        <div class="flex flex-col xl:flex-row gap-6 h-[calc(100vh-340px)]">
          <!-- Outline Sidebar -->
          <aside class="w-full xl:w-72 flex-shrink-0 bg-white rounded-2xl shadow-sm border border-slate-200 flex flex-col overflow-hidden">
            <div class="p-3 border-b border-slate-200 bg-slate-50/50 flex justify-between items-center">
              <h3 class="text-[10px] font-extrabold uppercase tracking-wider text-slate-500 m-0">Outline</h3>
              <span class="text-[10px] bg-white border border-slate-200 px-1.5 py-0.5 rounded text-slate-500 font-bold">{{ slides.length }}</span>
            </div>
            <div class="overflow-y-auto p-2 space-y-1 custom-scrollbar flex-1">
              <div v-for="(slide, idx) in slides" :key="slide.id" @click="currentIndex=idx"
                   class="p-2 rounded-lg cursor-pointer text-xs font-semibold border-l-[3px] transition-all flex items-center gap-2 hover:bg-slate-50"
                   :class="currentIndex === idx ? 'bg-blue-50 border-blue-600 text-blue-700 shadow-sm' : 'border-transparent text-slate-500'">
                <span class="w-5 h-5 flex-shrink-0 flex items-center justify-center rounded bg-white border border-slate-200 text-[9px]">{{ idx + 1 }}</span>
                <span class="truncate flex-1">{{ slide.title || 'Untitled' }}</span>
              </div>
            </div>
            <div class="p-2 border-t border-slate-200 flex gap-2">
              <button @click="moveSlide(-1)" class="btn-xxs flex-1" :disabled="currentIndex===0">↑</button>
              <button @click="moveSlide(1)" class="btn-xxs flex-1" :disabled="currentIndex===slides.length-1">↓</button>
              <button @click="removeSlide(currentIndex)" class="btn-xxs flex-1 btn-danger" :disabled="slides.length===0">✕</button>
            </div>
          </aside>

          <!-- Editor Canvas -->
          <div class="flex-1 w-full bg-slate-200/50 rounded-3xl shadow-inner border border-slate-300/50 flex flex-col h-full overflow-hidden relative">
            <!-- Formatting Toolbar -->
            <div class="absolute top-4 left-1/2 -translate-x-1/2 z-50 bg-white rounded-full shadow-xl border border-slate-200 px-3 py-2 flex items-center gap-3 print:hidden">
              <div class="flex items-center gap-1 border-r border-slate-200 pr-3">
                <button @click="applyHeading('h1')" class="tool-btn">H1</button>
                <button @click="applyHeading('h2')" class="tool-btn">H2</button>
                <button @click="toggleBold" class="tool-btn">B</button>
                <button @click="toggleItalic" class="tool-btn">I</button>
              </div>
              <div class="flex items-center gap-2 border-r border-slate-200 pr-3">
                <select v-model="editorFont" class="text-xs bg-transparent outline-none">
                  <option value="font-sans">Sans</option>
                  <option value="font-serif">Serif</option>
                  <option value="font-mono">Mono</option>
                </select>
                <select v-model="editorAlign" class="text-xs bg-transparent outline-none">
                  <option value="text-left">Left</option>
                  <option value="text-center">Center</option>
                  <option value="text-right">Right</option>
                </select>
                <button @click="undo" class="tool-btn text-slate-400">↶</button>
              </div>
              <div class="flex items-center gap-2">
                <button @click="duplicateSlide(currentIndex)" class="tool-btn">Copy</button>
                <button @click="addSlide" class="tool-btn">+</button>
              </div>
            </div>

            <!-- Editable Area -->
            <div class="flex-1 flex flex-col items-center justify-center p-10 overflow-auto" v-if="currentSlide">
              <input v-model="currentSlide.title" class="w-full max-w-5xl mb-4 px-4 py-2 rounded-lg bg-white border border-slate-300 text-lg font-bold outline-none" placeholder="Slide title" />
              <textarea v-model="currentSlide.rawMarkdown" @input="updateMarkdown(currentIndex, currentSlide.rawMarkdown)"
                        class="w-full max-w-5xl h-[340px] rounded-xl p-4 bg-white border border-slate-300 outline-none font-mono text-sm custom-scrollbar"
                        placeholder="Write markdown content..."></textarea>
              <div class="w-full max-w-5xl mt-4 bg-white border border-slate-200 rounded-xl p-4 prose max-w-none" v-html="currentSlide.htmlContent"></div>
              <div v-if="currentSlide.graphImage" class="mt-4">
                <img :src="currentSlide.graphImage" class="w-full max-w-xl rounded-lg border" />
              </div>
            </div>
            <div v-else class="flex-1 flex items-center justify-center text-slate-400">No slide selected</div>

            <!-- Navigation Footer -->
            <div class="absolute bottom-6 left-1/2 -translate-x-1/2 bg-white/90 backdrop-blur border border-slate-200 shadow-lg rounded-full px-4 py-2 flex items-center gap-4 z-30 print:hidden">
              <button @click="currentIndex--" :disabled="currentIndex===0" class="nav-btn">Prev</button>
              <span class="text-xs font-bold text-slate-600 select-none">Slide {{ currentIndex + 1 }} / {{ slides.length }}</span>
              <button @click="currentIndex++" :disabled="currentIndex===slides.length-1" class="nav-btn">Next</button>
            </div>
          </div>
        </div>

        <!-- Export Modal -->
        <div v-if="showExport" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4" @click.self="closeExport">
          <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm overflow-hidden">
            <div class="p-5 border-b border-slate-100 flex justify-between items-center bg-white"><h3 class="font-bold text-lg">Export {{ exportType.toUpperCase() }}</h3><button @click="closeExport" class="text-slate-400 hover:text-red-500 text-lg">✕</button></div>
            <div class="p-5 space-y-4 bg-slate-50">
              <div>
                <label class="form-label">Select Slides</label>
                <div class="max-h-[160px] overflow-y-auto border rounded-lg p-2 bg-white custom-scrollbar">
                  <label v-for="(slide,idx) in slides" :key="slide.id" class="flex items-center gap-2 p-1 text-xs">
                    <input type="checkbox" v-model="exportSelection" :value="slide.id" />
                    <span class="truncate">#{{ idx+1 }} - {{ slide.title }}</span>
                  </label>
                </div>
              </div>
              <div class="flex gap-2">
                <button @click="selectAll" class="btn-secondary flex-1">All</button>
                <button @click="exportSelection=[currentSlide?.id]" class="btn-secondary flex-1">Current</button>
                <button @click="exportSelection=[]" class="btn-danger flex-1">Clear</button>
              </div>
            </div>
            <div class="p-5 border-t bg-white"><button @click="confirmExport" class="btn-primary w-full">Download</button></div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import instructorSidebar from '@/components/layout/instructorLayout/instructorSideBar.vue'
import taSidebar from '@/components/layout/TaLayout/TASidebar.vue'
import PptxGenJS from 'pptxgenjs'
import { useSlideDeck } from './useSlideDeck'

const props = defineProps({ role: { type: String, default: 'instructor' } })
const route = useRoute()

const {
  config, slides, currentIndex, currentSlide, previewOutline, deckId,
  preview, generate, load, save, addSlide, removeSlide, updateMarkdown,
  duplicateSlide, undo, moveSlide
} = useSlideDeck()

// Simple editor style state
const editorFont = ref('font-sans')
const editorAlign = ref('text-left')
const newTopic = ref('')
const graphOptions = ['bar','line','pie','scatter']

// Export modal state
const showExport = ref(false)
const exportType = ref('pptx')
const exportSelection = ref([])

function addTopic(){ if(newTopic.value.trim()){ config.value.topics.push(newTopic.value.trim()); newTopic.value='' } }

function openExport(type){ exportType.value=type; exportSelection.value=slides.value.map(s=>s.id); showExport.value=true }
function closeExport(){ showExport.value=false }
function selectAll(){ exportSelection.value=slides.value.map(s=>s.id) }
function confirmExport(){ if(exportSelection.value.length===0) return alert('Select slides'); closeExport(); if(exportType.value==='pdf'){ setTimeout(()=>window.print(),500) } else { exportPptx() } }

function exportPptx(){
  const pres = new PptxGenJS(); pres.layout='LAYOUT_16x9';
  const chosen = slides.value.filter(s=>exportSelection.value.includes(s.id))
  chosen.forEach(s=>{
    const slide = pres.addSlide(); slide.background={ color:'FFFFFF'}
    slide.addText(s.title,{x:0.5,y:0.5,w:'90%',fontSize:24,bold:true,color:'363636'})
    const clean = s.htmlContent.replace(/<[^>]*>?/gm,'\n').replace(/\n\n+/g,'\n').trim()
    let textHeight='70%'; if(s.graphImage||s.graphData) textHeight='30%'
    slide.addText(clean,{x:0.5,y:1.5,w:'90%',h:textHeight,fontSize:14,color:'666666',valign:'top'})
    if(s.graphImage){ slide.addImage({ data:s.graphImage,x:0.5,y:3.3,w:'90%',h:2.5 }) }
  })
  pres.writeFile({ fileName: `${config.value.title||'Deck'}.pptx` })
}

function applyHeading(tag){ if(!currentSlide.value) return; const mk = currentSlide.value.rawMarkdown||''; if(mk.startsWith(`#`)){ currentSlide.value.rawMarkdown = mk.replace(/^#+\s*/, `${tag==='h1'? '#':'##'} `) } else { currentSlide.value.rawMarkdown = `${tag==='h1'? '#':'##'} ${mk}` } updateMarkdown(currentIndex.value, currentSlide.value.rawMarkdown) }
function toggleBold(){ if(!currentSlide.value) return; currentSlide.value.rawMarkdown = `**${currentSlide.value.rawMarkdown}**`; updateMarkdown(currentIndex.value, currentSlide.value.rawMarkdown) }
function toggleItalic(){ if(!currentSlide.value) return; currentSlide.value.rawMarkdown = `*${currentSlide.value.rawMarkdown}*`; updateMarkdown(currentIndex.value, currentSlide.value.rawMarkdown) }

onMounted(()=>{ if(route.query.deckId) load(route.query.deckId); if(route.params.id) load(route.params.id) })
watch(()=>route.params.id,(val)=>{ if(val) load(val) })
</script>

<style scoped>
.form-label { @apply block text-[9px] font-extrabold text-slate-400 mb-1.5 uppercase tracking-wider; }
.form-input { @apply w-full px-3 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition text-sm text-slate-800; }
.btn-primary { @apply px-4 py-2 rounded-lg bg-blue-600 text-white text-xs font-bold shadow hover:bg-blue-700 transition disabled:opacity-40; }
.btn-secondary { @apply px-4 py-2 rounded-lg bg-white border border-slate-300 text-slate-700 text-xs font-bold shadow-sm hover:bg-slate-50 transition disabled:opacity-40; }
.btn-success { @apply px-4 py-2 rounded-lg bg-green-600 text-white text-xs font-bold shadow hover:bg-green-700 transition disabled:opacity-40; }
.btn-danger { @apply px-4 py-2 rounded-lg bg-red-100 text-red-600 text-xs font-bold shadow-sm hover:bg-red-200 transition disabled:opacity-40; }
.btn-xxs { @apply px-2 py-1 rounded bg-white border border-slate-300 text-[10px] font-bold hover:bg-slate-50 disabled:opacity-30; }
.tool-btn { @apply p-2 rounded-lg text-slate-500 hover:bg-slate-100 hover:text-blue-600 transition text-[11px] font-bold; }
.nav-btn { @apply w-14 h-8 rounded-full bg-white border border-slate-300 text-[11px] font-bold hover:bg-slate-50 disabled:opacity-30; }
.custom-scrollbar::-webkit-scrollbar { width:4px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background:#cbd5e1; border-radius:10px; }
</style>
