<script setup>
import { ref, computed, nextTick, onMounted, onUnmounted, watch } from 'vue'
import instructorSidebar from '@/components/layout/instructorLayout/instructorSideBar.vue'
import { api } from '@/api'
import MarkdownIt from 'markdown-it'
import PptxGenJS from 'pptxgenjs'

// =======================================================================
// 1. SETUP & STATE
// =======================================================================
const md = new MarkdownIt({ html: true, linkify: true, typographer: true })

const loading = ref(false)
const selectedTemplate = ref('Modern Pro')
const isPreviewMode = ref(false) // False = Edit, True = View
const editorRef = ref(null)
const fileInput = ref(null)
const bgInput = ref(null)

// Editor Tools State
const currentFontSize = ref('16px')
const currentAlign = ref('text-left')
const currentFont = ref('font-sans')
const activeFormats = ref({ bold: false, italic: false, h1: false, h2: false, list: false })

// Slide Data & History
const slides = ref([
  { id: 1, title: "Welcome", htmlContent: "<h1>Welcome</h1><p>Click here to start editing.</p><ul><li>Add points</li><li>Add images</li></ul>", order: 1, bgImage: null },
])
const history = ref([])
const historyIndex = ref(-1)
const currentIndex = ref(0)

// Configuration
const config = ref({ courseId: null, title: '', description: '', numSlides: 5, includeGraphs: false })
const topicsInput = ref([''])

// Modals
const showImageModal = ref(false)
const tempImage = ref(null)
const imageConfig = ref({ width: 50, caption: '' })
const showExportModal = ref(false)
const exportConfig = ref({ type: 'pdf', ratio: '16:9', pageSize: 'A4', selection: [] })


// =======================================================================
// 2. THEME & STYLES
// =======================================================================
const currentSlide = computed(() => slides.value[currentIndex.value] || slides.value[0])

const themeClasses = computed(() => {
  // Base classes + Dynamic Font/Align
  const base = `${currentFont.value} ${currentAlign.value} h-full w-full p-16 overflow-y-auto custom-scrollbar relative transition-all duration-300 outline-none prose-headings:font-normal`
  
  switch (selectedTemplate.value) {
    case 'Classic Academic': return `${base} bg-[#fffdf7] text-slate-900 font-serif prose-headings:text-blue-900 border-t-8 border-blue-900`
    case 'Modern Pro': return `${base} bg-white text-slate-800 font-sans prose-headings:text-slate-900 border border-slate-200`
    case 'Minimalist Blue': return `${base} bg-blue-50/30 text-slate-700 font-sans prose-headings:text-indigo-600 border-l-8 border-indigo-500`
    case 'Vibrant Yellow': return `${base} bg-white text-black font-sans prose-headings:bg-yellow-300 prose-headings:inline-block prose-headings:px-2 border-b-8 border-yellow-400`
    default: return base
  }
})

const templates = [
  { name: 'Modern Pro', bg: 'bg-gray-100', border: 'border-slate-300', preview: 'bg-white' },
  { name: 'Classic Academic', bg: 'bg-[#f0e6d2]', border: 'border-blue-900', preview: 'bg-[#fffdf7]' },
  { name: 'Minimalist Blue', bg: 'bg-blue-50', border: 'border-indigo-500', preview: 'bg-slate-50' },
  { name: 'Vibrant Yellow', bg: 'bg-yellow-50', border: 'border-yellow-400', preview: 'bg-white' }
]

function getPrintThemeClasses() {
  const base = "w-screen h-screen p-16 flex flex-col justify-center bg-cover bg-center relative"
  switch (selectedTemplate.value) {
    case 'Classic Academic': return `${base} bg-[#fffdf7] text-slate-900 font-serif prose-headings:text-blue-900`
    case 'Modern Pro': return `${base} bg-white text-slate-800 font-sans`
    case 'Minimalist Blue': return `${base} bg-blue-50/20 text-slate-700 font-sans`
    case 'Vibrant Yellow': return `${base} bg-white text-black font-sans`
    default: return base
  }
}


// =======================================================================
// 3. NAVIGATION & HISTORY
// =======================================================================
function loadContentToEditor() {
    if (editorRef.value && currentSlide.value) {
        editorRef.value.innerHTML = currentSlide.value.htmlContent
        updateToolbarState()
    }
}

watch(currentIndex, () => { nextTick(loadContentToEditor) })
watch(isPreviewMode, (val) => { if(!val) nextTick(loadContentToEditor) })

function prevSlide() { if (currentIndex.value > 0) currentIndex.value-- }
function nextSlide() { if (currentIndex.value < slides.value.length - 1) currentIndex.value++ }
function jumpToSlide(index) { currentIndex.value = index }

watch(slides, (newVal) => {
    if(historyIndex.value === -1 || JSON.stringify(newVal) !== JSON.stringify(history.value[historyIndex.value])) {
        if (historyIndex.value < history.value.length - 1) history.value = history.value.slice(0, historyIndex.value + 1)
        history.value.push(JSON.parse(JSON.stringify(newVal)))
        historyIndex.value++
        if (history.value.length > 50) { history.value.shift(); historyIndex.value-- }
    }
}, { deep: true })

function undo() {
  if (historyIndex.value > 0) {
    historyIndex.value--
    slides.value = JSON.parse(JSON.stringify(history.value[historyIndex.value]))
    nextTick(loadContentToEditor)
  }
}

onMounted(() => {
    loadContentToEditor()
    window.addEventListener('keydown', (e) => { if ((e.ctrlKey || e.metaKey) && e.key === 'z') { e.preventDefault(); undo(); } })
    document.addEventListener('selectionchange', updateToolbarState)
})
onUnmounted(() => document.removeEventListener('selectionchange', updateToolbarState))


// =======================================================================
// 4. EDITOR ENGINE (COMMANDS)
// =======================================================================
function updateToolbarState() {
  if (!document || !editorRef.value) return
  
  const selection = window.getSelection()
  if (!selection.rangeCount) return
  if (!editorRef.value.contains(selection.anchorNode) && editorRef.value !== selection.anchorNode) return

  activeFormats.value = {
    bold: document.queryCommandState('bold'),
    italic: document.queryCommandState('italic'),
    h1: document.queryCommandValue('formatBlock') === 'h1',
    h2: document.queryCommandValue('formatBlock') === 'h2',
    list: document.queryCommandState('insertUnorderedList'),
  }
}

function execCmd(command, value = null) {
  // 1. Custom Font Size
  if (command === 'fontSize') {
    const selection = window.getSelection();
    if (selection.rangeCount > 0) {
      const range = selection.getRangeAt(0);
      if (!range.collapsed) {
        const span = document.createElement("span");
        span.style.fontSize = value;
        span.appendChild(range.extractContents());
        range.insertNode(span);
      }
    }
  }
  // 2. Toggle Heading
  else if (command === 'formatBlock') {
    const currentBlock = document.queryCommandValue('formatBlock')
    if (currentBlock === value.toLowerCase()) {
        document.execCommand('formatBlock', false, 'div')
    } else {
        document.execCommand(command, false, value)
    }
  }
  // 3. Standard
  else {
    document.execCommand(command, false, value)
  }

  editorRef.value.focus()
  saveState()
  updateToolbarState()
}

function saveState() {
  if (editorRef.value) currentSlide.value.htmlContent = editorRef.value.innerHTML
}


// =======================================================================
// 5. MEDIA HANDLING
// =======================================================================
function triggerUpload(type) { 
    if(type === 'bg') bgInput.value.click()
    else fileInput.value.click()
}

function handleUpload(e, type) {
    const file = e.target.files[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = (ev) => {
        if(type === 'bg') {
            currentSlide.value.bgImage = ev.target.result
            saveState()
        } else {
            tempImage.value = ev.target.result
            showImageModal.value = true
        }
    }
    reader.readAsDataURL(file)
    e.target.value = ''
}

function confirmInsertImage() {
    const html = `<img src="${tempImage.value}" style="width: ${imageConfig.value.width}%; border-radius: 8px; display: block; margin: 10px 0;" />`
    execCmd('insertHTML', html)
    showImageModal.value = false
    tempImage.value = null
}

function removeBackground() { 
    currentSlide.value.bgImage = null; 
    saveState() 
}


// =======================================================================
// 6. GENERATION & EXPORT
// =======================================================================
function addTopic() { topicsInput.value.push('') }
function removeTopic(i) { topicsInput.value.splice(i, 1) }

async function generateSlides() {
  if (!config.value.courseId || !config.value.title) return alert('Please enter Course ID and Title.')
  const topics = topicsInput.value.map(t => t.trim()).filter(Boolean)
  if (topics.length === 0) return alert('Please add at least one topic.')

  loading.value = true
  try {
    const payload = { 
        course_id: config.value.courseId,
        title: config.value.title,
        description: config.value.description,
        topics: topics,
        num_slides: config.value.numSlides
    }
    
    const res = await api.post('/slide-decks/', payload)
    const deck = res.data

    if (deck && Array.isArray(deck.slides)) {
      slides.value = deck.slides.map((s, idx) => ({ 
        id: s.id ?? idx, 
        title: s.title, 
        htmlContent: md.render(s.content || ''), 
        order: idx + 1, 
        bgImage: null 
      }))
      currentIndex.value = 0
      nextTick(() => {
          loadContentToEditor()
          document.getElementById('workspace')?.scrollIntoView({ behavior: 'smooth' })
      })
    }
  } catch (err) { 
      console.error(err)
      const msg = err.response?.data?.detail ? JSON.stringify(err.response.data.detail) : err.message
      alert(`Generation Failed: ${msg}`) 
  } finally { 
      loading.value = false 
  }
}

function openExportModal(type) {
    if(slides.value.length === 0) return alert("Generate slides first.")
    exportConfig.value.type = type
    exportConfig.value.selection = slides.value.map(s => s.id)
    showExportModal.value = true
}

function toggleSelectAll() {
    if(exportConfig.value.selection.length === slides.value.length) exportConfig.value.selection = []
    else exportConfig.value.selection = slides.value.map(s => s.id)
}

function confirmExport() {
    const count = exportConfig.value.selection.length
    if (count === 0) return alert("Select slides to download.")
    showExportModal.value = false
    
    if (exportConfig.value.type === 'pdf') {
        setTimeout(() => window.print(), 1000)
    } else {
        generatePPTX()
    }
}

function generatePPTX() {
    const pres = new PptxGenJS()
    let bgColor = 'FFFFFF'; let titleColor = '363636'; let bodyColor = '666666'
    
    if(selectedTemplate.value === 'Classic Academic') { bgColor = 'FFFDF7'; titleColor = '1E3A8A' } 
    else if (selectedTemplate.value === 'Minimalist Blue') { bgColor = 'F0F9FF'; titleColor = '4F46E5' }

    const slidesToExport = slides.value.filter(s => exportConfig.value.selection.includes(s.id))
    
    slidesToExport.forEach((slideData) => {
        const slide = pres.addSlide()
        slide.background = { color: bgColor }
        slide.addText(slideData.title, { x: 0.5, y: 0.5, w: '90%', fontSize: 24, bold: true, color: titleColor })
        const cleanText = slideData.htmlContent.replace(/<[^>]*>?/gm, '\n').replace(/\n\n+/g, '\n').trim()
        slide.addText(cleanText, { x: 0.5, y: 1.5, w: '90%', h: '70%', fontSize: 14, color: bodyColor, valign: 'top' })
    })
    pres.writeFile({ fileName: `${config.value.title || 'Presentation'}.pptx` })
}

async function shareLink() {
    await navigator.clipboard.writeText(window.location.href)
    alert("Link copied!")
}
</script>

<template>
  <div class="flex min-h-screen bg-[#f8fafc] font-sans text-slate-800">
    <instructorSidebar class="print:hidden"/>

    <main class="flex-1 p-6 lg:p-8 ml-64 print:ml-0 print:p-0">
      
      <section class="mb-8 max-w-[1600px] mx-auto print:hidden animate-fade-in">
          <div class="bg-white rounded-3xl shadow-sm border border-slate-200 p-0 overflow-hidden flex flex-col lg:flex-row min-h-[320px]">
            
            <div class="w-full lg:w-[65%] p-8 flex flex-col gap-6 relative">
               <div class="absolute top-0 left-0 w-1.5 h-full bg-blue-600"></div>
               <div>
                  <h1 class="font-extrabold text-3xl text-slate-900 tracking-tight">AI Deck Generator</h1>
                  <p class="text-slate-500 mt-1">Configure your topic and let AI structure the presentation.</p>
               </div>
               <div class="grid grid-cols-3 gap-6">
                  <div><label class="label-style">Course ID <span class="text-red-500">*</span></label><input v-model.number="config.courseId" type="number" min="1" placeholder="ID" class="input-style" /></div>
                  <div class="col-span-2"><label class="label-style">Deck Title <span class="text-red-500">*</span></label><input v-model="config.title" type="text" placeholder="Topic Title" class="input-style font-semibold" /></div>
               </div>
               <div><label class="label-style">Context</label><textarea v-model="config.description" rows="2" placeholder="Specific focus..." class="input-style resize-none"></textarea></div>
               <div class="flex items-center gap-2"><input type="checkbox" v-model="config.includeGraphs" class="w-4 h-4 text-blue-600 rounded"><label class="text-xs font-bold text-slate-600">Include AI Graphs</label></div>
            </div>

            <div class="w-full lg:w-[35%] bg-slate-50/50 border-l border-slate-100 p-6 flex flex-col justify-between">
                <div class="flex-1 flex flex-col">
                    <label class="label-style mb-2 flex justify-between"><span>Key Topics</span><span class="text-slate-400 text-[10px] cursor-pointer hover:text-blue-600" @click="topicsInput=['']">Clear</span></label>
                    <div class="flex-1 bg-white p-3 rounded-xl border border-slate-200 mb-3 overflow-y-auto max-h-[140px] custom-scrollbar shadow-sm">
                        <div v-for="(t, i) in topicsInput" :key="i" class="flex gap-2 mb-2 group">
                            <input v-model="topicsInput[i]" type="text" placeholder="Enter topic..." class="flex-1 px-3 py-1.5 bg-slate-50 border border-slate-100 rounded-lg outline-none text-sm focus:bg-white focus:border-blue-400 transition" />
                            <button @click="removeTopic(i)" class="text-slate-300 hover:text-red-500 px-1 font-bold">✕</button>
                        </div>
                        <button @click="addTopic" class="w-full py-1.5 border border-dashed border-blue-200 text-blue-600 text-[10px] font-bold rounded-lg hover:bg-blue-50 transition">+ ADD TOPIC</button>
                    </div>
                    <div class="flex items-center gap-3 mb-4">
                        <div class="w-20"><label class="label-style mb-1">Slides</label><input v-model.number="config.numSlides" type="number" class="input-style py-2 text-center" /></div>
                        <button @click.prevent="generateSlides" :disabled="loading" class="flex-1 h-[42px] mt-auto rounded-xl bg-slate-900 text-white font-bold text-sm shadow-lg hover:bg-blue-600 transition-all disabled:opacity-70 flex justify-center items-center gap-2">
                            <span v-if="loading" class="animate-spin">⟳</span> {{ loading ? 'Generating...' : 'Generate Deck' }}
                        </button>
                    </div>
                </div>
                <div class="pt-4 border-t border-slate-200">
                    <label class="label-style mb-2 text-slate-400 text-center">Quick Export</label>
                    <div class="flex gap-2">
                        <button @click="openExportModal('pdf')" class="mini-btn bg-white border border-slate-200 text-slate-600 hover:text-blue-600 hover:border-blue-200">📄 PDF</button>
                        <button @click="openExportModal('pptx')" class="mini-btn bg-white border border-slate-200 text-slate-600 hover:text-orange-600 hover:border-orange-200">📊 PPTX</button>
                        <button @click="shareLink" class="mini-btn bg-white border border-slate-200 text-slate-600 hover:text-green-600 hover:border-green-200">🔗 Share</button>
                    </div>
                </div>
            </div>
          </div>
      </section>

      <section id="workspace" class="max-w-[1600px] mx-auto flex flex-col xl:flex-row gap-6 items-start h-[calc(100vh-280px)] min-h-[600px]">
        
        <aside class="w-full xl:w-72 flex-shrink-0 flex flex-col gap-4 h-full print:hidden">
           <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-4">
              <h3 class="label-style mb-3">Visual Theme</h3>
              <div class="grid grid-cols-2 gap-2">
                <button v-for="temp in templates" :key="temp.name" @click="selectedTemplate = temp.name"
                  class="h-16 rounded-xl border-2 transition-all flex flex-col items-center justify-center p-1 group bg-white relative overflow-hidden"
                  :class="selectedTemplate === temp.name ? `border-blue-600 ring-1 ring-blue-100 bg-blue-50/20` : 'border-slate-100 hover:border-slate-300'">
                  <div :class="`absolute inset-0 opacity-30 ${temp.bg}`"></div>
                  <span class="relative z-10 text-[9px] font-bold text-slate-600">{{ temp.name }}</span>
                  <div v-if="selectedTemplate === temp.name" class="absolute top-1 right-1 w-3 h-3 bg-blue-600 rounded-full text-white flex items-center justify-center text-[7px] z-10">✓</div>
                </button>
              </div>
           </div>
           <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-0 flex-1 flex flex-col overflow-hidden">
              <div class="p-3 border-b border-slate-200 bg-slate-50/50 flex justify-between items-center">
                  <h3 class="label-style m-0">Outline</h3>
                  <span class="text-[9px] bg-white border border-slate-200 px-1.5 py-0.5 rounded text-slate-500 font-bold">{{ slides.length }}</span>
              </div>
              <div class="overflow-y-auto p-2 space-y-1 custom-scrollbar flex-1">
                <div v-for="(slide, idx) in slides" :key="slide.id" @click="jumpToSlide(idx)"
                  class="p-2 rounded-lg cursor-pointer text-xs font-semibold border-l-[3px] transition-all flex items-center gap-2 hover:bg-slate-50"
                  :class="currentIndex === idx ? 'bg-blue-50 border-blue-600 text-blue-700 shadow-sm' : 'border-transparent text-slate-500'">
                  <span class="w-5 h-5 flex-shrink-0 flex items-center justify-center rounded bg-white border border-slate-200 text-[9px]">{{ idx + 1 }}</span>
                  <span class="truncate flex-1">{{ slide.title || 'Untitled' }}</span>
                </div>
              </div>
           </div>
        </aside>

        <div class="flex-1 w-full bg-slate-200/50 rounded-3xl shadow-inner border border-slate-300/50 flex flex-col h-full overflow-hidden relative">
          
          <div class="absolute top-4 left-1/2 -translate-x-1/2 z-50 bg-white rounded-full shadow-xl border border-slate-200 px-3 py-2 flex items-center gap-3 print:hidden transition-all hover:scale-[1.01]">
             <div class="flex items-center gap-1 border-r border-slate-200 pr-3">
                <button @mousedown.prevent="execCmd('bold')" class="tool-btn font-bold" :class="{'bg-blue-50 text-blue-600': activeFormats.bold}">B</button>
                <button @mousedown.prevent="execCmd('italic')" class="tool-btn italic" :class="{'bg-blue-50 text-blue-600': activeFormats.italic}">I</button>
                <button @mousedown.prevent="execCmd('formatBlock', 'H1')" class="tool-btn text-xs font-black" :class="{'bg-blue-50 text-blue-600': activeFormats.h1}">H1</button>
                <button @mousedown.prevent="execCmd('formatBlock', 'H2')" class="tool-btn text-xs font-bold" :class="{'bg-blue-50 text-blue-600': activeFormats.h2}">H2</button>
             </div>
             <div class="flex items-center gap-2 border-r border-slate-200 pr-3">
                <div class="relative group">
                   <select @change="(e) => execCmd('fontSize', e.target.value)" class="text-xs border-none bg-transparent focus:ring-0 cursor-pointer w-12 font-mono text-slate-600 appearance-none text-center hover:text-blue-600">
                       <option value="" disabled selected>Sz</option>
                       <option value="12px">12</option><option value="14px">14</option><option value="16px">16</option>
                       <option value="18px">18</option><option value="24px">24</option><option value="30px">30</option>
                       <option value="36px">36</option><option value="48px">48</option>
                   </select>
                   <div class="absolute right-0 top-1/2 -translate-y-1/2 pointer-events-none text-slate-400"><svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg></div>
                </div>
                <select v-model="currentFont" class="text-xs border-none bg-transparent focus:ring-0 cursor-pointer w-16"><option value="font-sans">Sans</option><option value="font-serif">Serif</option><option value="font-mono">Mono</option></select>
                <select v-model="currentAlign" class="text-xs border-none bg-transparent focus:ring-0 cursor-pointer w-16"><option value="text-left">Left</option><option value="text-center">Center</option><option value="text-right">Right</option></select>
                <div class="relative w-6 h-6 rounded-full overflow-hidden border border-slate-300 cursor-pointer hover:scale-110 transition">
                    <input type="color" @change="(e) => execCmd('foreColor', e.target.value)" class="absolute inset-0 opacity-0 cursor-pointer w-full h-full" />
                    <div class="w-full h-full bg-gradient-to-br from-red-500 via-green-500 to-blue-500"></div>
                </div>
             </div>
             <div class="flex items-center gap-2">
                <button @mousedown.prevent="triggerUpload('img')" class="tool-btn text-blue-600 hover:bg-blue-50" title="Image"><svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg></button>
                <button @mousedown.prevent="triggerUpload('bg')" class="tool-btn text-blue-600 hover:bg-blue-50" title="Background"><svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg></button>
                <button v-if="currentSlide.bgImage" @mousedown.prevent="removeBackground" class="tool-btn text-red-500 bg-red-50" title="Remove BG">✕</button>
                <input type="file" ref="fileInput" @change="(e)=>handleUpload(e, 'img')" accept="image/*" class="hidden" />
                <input type="file" ref="bgInput" @change="(e)=>handleUpload(e, 'bg')" accept="image/*" class="hidden" />
                <div class="w-px h-4 bg-slate-200 mx-1"></div>
                <button @mousedown.prevent="execCmd('delete')" class="tool-btn text-red-500 hover:bg-red-50" title="Delete"><svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg></button>
                <button @mousedown.prevent="undo" class="tool-btn text-xs text-slate-400 hover:text-slate-600" title="Undo">↶</button>
                <button @mousedown.prevent="isPreviewMode = !isPreviewMode" class="px-3 py-1 rounded-lg text-xs font-bold transition-all ml-1" :class="isPreviewMode ? 'bg-blue-100 text-blue-700' : 'bg-slate-100 text-slate-600'">{{ isPreviewMode ? 'View' : 'Edit' }}</button>
             </div>
          </div>

          <div class="flex-1 flex items-center justify-center p-10 overflow-auto print:bg-white print:p-0" @click="updateToolbarState">
             <div id="printable-slide" 
                  ref="editorRef"
                  :contenteditable="!isPreviewMode"
                  @input="saveState"
                  @click="updateToolbarState"
                  @keyup="updateToolbarState"
                  class="aspect-video w-full max-w-5xl shadow-2xl rounded-lg p-16 outline-none transition-all duration-300 prose prose-lg max-w-none cursor-text relative bg-cover bg-center"
                  :class="themeClasses"
                  :style="currentSlide.bgImage ? `background-image: url(${currentSlide.bgImage})` : ''">
                  </div>
          </div>

          <div class="absolute bottom-6 left-1/2 -translate-x-1/2 bg-white/90 backdrop-blur border border-slate-200 shadow-lg rounded-full px-4 py-2 flex items-center gap-4 z-30 print:hidden">
             <button @click="prevSlide" :disabled="currentIndex === 0" class="w-8 h-8 rounded-full hover:bg-slate-100 flex items-center justify-center disabled:opacity-30 transition"><svg class="w-4 h-4 text-slate-700" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7" /></svg></button>
             <span class="text-xs font-bold text-slate-600 select-none">Slide {{ currentIndex + 1 }} / {{ slides.length }}</span>
             <button @click="nextSlide" :disabled="currentIndex === slides.length - 1" class="w-8 h-8 rounded-full hover:bg-slate-100 flex items-center justify-center disabled:opacity-30 transition"><svg class="w-4 h-4 text-slate-700" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M9 5l7 7-7 7" /></svg></button>
          </div>

        </div>
      </section>

      <div v-if="showImageModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-fade-in">
         <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm overflow-hidden">
            <div class="p-4 border-b flex justify-between items-center bg-slate-50"><h3 class="font-bold text-slate-800">Resize Image</h3><button @click="showImageModal=false" class="text-slate-400 hover:text-red-500">✕</button></div>
            <div class="p-6 bg-white flex flex-col gap-4"><div class="bg-slate-100 rounded-lg p-2 flex justify-center"><img :src="tempImage" class="max-h-[150px] object-contain" /></div><div><label class="label-style">Width: {{ imageConfig.width }}%</label><input type="range" v-model="imageConfig.width" min="20" max="100" class="w-full accent-blue-600" /></div></div>
            <div class="p-4 border-t bg-slate-50 flex justify-end gap-2"><button @click="showImageModal=false" class="px-3 py-2 text-xs font-bold text-slate-500 hover:bg-slate-200 rounded-lg">Cancel</button><button @click="confirmInsertImage" class="px-4 py-2 text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-lg">Insert</button></div>
         </div>
      </div>

      <div v-if="showExportModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-fade-in">
         <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm overflow-hidden">
            <div class="p-5 border-b border-slate-100 flex justify-between items-center bg-white"><h3 class="font-bold text-lg text-slate-800">Download Options</h3><button @click="showExportModal = false" class="text-slate-400 hover:text-red-500 text-lg">✕</button></div>
            <div class="p-6 space-y-6 bg-slate-50">
               <div class="grid grid-cols-2 gap-4"><div><label class="label-style">Size</label><select v-model="exportConfig.pageSize" class="input-style py-2 text-xs bg-white"><option value="A4">A4</option><option value="Letter">Letter</option></select></div><div><label class="label-style">Ratio</label><select v-model="exportConfig.ratio" class="input-style py-2 text-xs bg-white"><option value="16:9">16:9</option><option value="4:3">4:3</option></select></div></div>
               <div><label class="label-style">Pages</label><div class="flex gap-2"><button @click="toggleSelectAll" class="flex-1 py-2 bg-white border rounded text-xs font-bold hover:bg-slate-50">All</button><button @click="exportConfig.selection = [currentSlide.id]" class="flex-1 py-2 bg-white border rounded text-xs font-bold hover:bg-slate-50">Current</button></div><div class="mt-2 max-h-[100px] overflow-y-auto custom-scrollbar border rounded-lg p-2 bg-white"><label v-for="(slide, idx) in slides" :key="slide.id" class="flex items-center gap-2 p-1 hover:bg-slate-50 cursor-pointer"><input type="checkbox" v-model="exportConfig.selection" :value="slide.id" class="rounded text-blue-600"><span class="text-xs truncate text-slate-600">#{{idx+1}} - {{slide.title}}</span></label></div></div>
            </div>
            <div class="p-5 border-t bg-white"><button @click="confirmExport" class="w-full py-3 bg-slate-900 text-white rounded-xl font-bold shadow-lg hover:bg-black transition">Download</button></div>
         </div>
      </div>

      <div id="print-only-container" class="hidden print:block fixed left-[9999px] top-0 print:left-0 print:top-0">
        <div v-for="slide in slides" :key="slide.id">
          <div v-if="exportConfig.selection.includes(slide.id)" class="print-slide" :class="getPrintThemeClasses()" :style="slide.bgImage ? `background-image: url(${slide.bgImage})` : ''">
            <div class="prose prose-xl max-w-none w-full" v-html="slide.htmlContent"></div>
            <div class="fixed bottom-6 right-8 text-sm opacity-50 font-sans">Slide {{ slide.order }}</div>
          </div>
        </div>
      </div>

    </main>
  </div>
</template>

<style scoped>
.label-style { @apply block text-[9px] font-extrabold text-slate-400 mb-1.5 uppercase tracking-wider ml-1; }
.input-style { @apply w-full px-3 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition text-sm text-slate-800; }
.mini-btn { @apply w-full flex items-center justify-center gap-2 px-2 py-2 rounded-lg text-[10px] font-bold border transition-all active:scale-95 shadow-sm; }
.tool-btn { @apply p-2 rounded-lg text-slate-500 hover:bg-slate-100 hover:text-blue-600 transition flex items-center justify-center; }
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.animate-fade-in { animation: fadeIn 0.3s ease-out; }
@keyframes fadeIn { from { opacity: 0; transform: scale(0.98); } to { opacity: 1; transform: scale(1); } }
@media print { body * { visibility: hidden; } #print-only-container, #print-only-container * { visibility: visible; } #print-only-container { display: block !important; position: absolute; left: 0; top: 0; width: 100vw; height: auto; z-index: 9999; } .print-slide { width: 100vw; height: 100vh; page-break-after: always; display: flex; flex-direction: column; justify-content: center; padding: 4rem; background-color: white; -webkit-print-color-adjust: exact; } .bg-\[\#fffdf7\] { background-color: #fffdf7 !important; } .bg-blue-50\/20 { background-color: rgb(239 246 255 / 0.2) !important; } }
</style>