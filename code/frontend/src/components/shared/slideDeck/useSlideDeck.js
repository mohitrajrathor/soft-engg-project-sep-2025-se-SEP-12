import { ref, computed, nextTick } from 'vue'
import MarkdownIt from 'markdown-it'
import { api } from '@/api'

// Unified composable for slide deck generation / editing / export
export function useSlideDeck() {
  const md = new MarkdownIt({ html: true, linkify: true, typographer: true })

  // Config state
  const config = ref({
    courseId: null,
    title: '',
    description: '',
    format: 'presentation',
    numSlides: 5,
    includeGraphs: false,
    graphTypes: [],
    topics: []
  })

  // Deck state
  const deckId = ref(null)
  const slides = ref([])
  const currentIndex = ref(0)
  const loading = ref(false)
  const previewOutline = ref([])

  // History (undo)
  const history = ref([])
  const historyIndex = ref(-1)

  const currentSlide = computed(() => slides.value[currentIndex.value] || null)

  function pushHistory() {
    const snapshot = JSON.parse(JSON.stringify(slides.value))
    if (historyIndex.value < history.value.length - 1) {
      history.value = history.value.slice(0, historyIndex.value + 1)
    }
    history.value.push(snapshot)
    historyIndex.value++
    if (history.value.length > 50) {
      history.value.shift(); historyIndex.value--
    }
  }

  function undo() {
    if (historyIndex.value > 0) {
      historyIndex.value--
      slides.value = JSON.parse(JSON.stringify(history.value[historyIndex.value]))
    }
  }

  function setTopics(raw) { config.value.topics = raw.map(t => t.trim()).filter(Boolean) }

  async function preview() {
    if (!config.value.courseId || !config.value.title) return alert('Provide course & title')
    setTopics(config.value.topics)
    if (config.value.topics.length === 0) return alert('Add at least one topic')
    loading.value = true
    try {
      const payload = {
        course_id: config.value.courseId,
        title: config.value.title,
        description: config.value.description,
        topics: config.value.topics,
        num_slides: config.value.numSlides,
        format: config.value.format,
        include_graphs: config.value.includeGraphs,
        graph_types: config.value.graphTypes
      }
      const res = await api.post('/slide-decks/preview', payload)
      previewOutline.value = res.data.outline || []
    } catch (e) { console.error(e); alert('Preview failed: ' + (e.response?.data?.detail || e.message)) } finally { loading.value = false }
  }

  async function generate() {
    if (!config.value.courseId || !config.value.title) return alert('Provide course & title')
    setTopics(config.value.topics)
    if (config.value.topics.length === 0) return alert('Add at least one topic')
    loading.value = true
    try {
      const payload = {
        course_id: config.value.courseId,
        title: config.value.title,
        description: config.value.description,
        topics: config.value.topics,
        num_slides: config.value.numSlides,
        format: config.value.format,
        include_graphs: config.value.includeGraphs,
        graph_types: config.value.graphTypes
      }
      const res = await api.post('/slide-decks/', payload)
      deckId.value = res.data.id
      mapSlides(res.data.slides)
      currentIndex.value = 0
      pushHistory()
    } catch (e) { console.error(e); alert('Generation failed: ' + (e.response?.data?.detail || e.message)) } finally { loading.value = false }
  }

  async function load(id) {
    loading.value = true
    try {
      const res = await api.get(`/slide-decks/${id}`)
      deckId.value = res.data.id
      config.value.title = res.data.title
      config.value.description = res.data.description || ''
      config.value.courseId = res.data.course_id
      mapSlides(res.data.slides)
      currentIndex.value = 0
      pushHistory()
    } catch (e) { console.error(e); alert('Load failed: ' + (e.response?.data?.detail || e.message)) } finally { loading.value = false }
  }

  async function save() {
    if (!deckId.value) return alert('Nothing to save yet')
    loading.value = true
    try {
      const payload = {
        title: config.value.title,
        description: config.value.description,
        slides: slides.value.map(s => ({
          title: s.title,
          content: s.rawMarkdown || s.originalMarkdown || '',
          graph_data: s.graphData || null,
          graph_image: s.graphImage || null
        }))
      }
      await api.put(`/slide-decks/${deckId.value}`, payload)
      alert('Saved ✓')
    } catch (e) { console.error(e); alert('Save failed: ' + (e.response?.data?.detail || e.message)) } finally { loading.value = false }
  }

  function mapSlides(rawSlides) {
    slides.value = (rawSlides || []).map((s, idx) => ({
      id: s.id ?? idx,
      title: s.title,
      rawMarkdown: s.content || '',
      htmlContent: md.render(s.content || ''),
      graphData: s.graph_data,
      graphImage: s.graph_image,
      bgImage: null,
      order: idx + 1
    }))
  }

  function addSlide() {
    slides.value.push({ id: Date.now(), title: 'New Slide', rawMarkdown: 'Content...', htmlContent: md.render('Content...'), order: slides.value.length + 1, bgImage: null })
    pushHistory()
  }

  function removeSlide(idx) {
    slides.value.splice(idx, 1)
    slides.value.forEach((s, i) => s.order = i + 1)
    if (currentIndex.value >= slides.value.length) currentIndex.value = slides.value.length - 1
    pushHistory()
  }

  function updateMarkdown(idx, markdown) {
    const slide = slides.value[idx]
    slide.rawMarkdown = markdown
    slide.htmlContent = md.render(markdown)
    pushHistory()
  }

  function duplicateSlide(idx) {
    const s = slides.value[idx]
    const copy = { ...JSON.parse(JSON.stringify(s)), id: Date.now(), title: s.title + ' (Copy)', order: s.order + 1 }
    slides.value.splice(idx + 1, 0, copy)
    slides.value.forEach((sl, i) => sl.order = i + 1)
    pushHistory()
  }

  function moveSlide(delta) {
    const newIndex = currentIndex.value + delta
    if (newIndex < 0 || newIndex >= slides.value.length) return
    const temp = slides.value[currentIndex.value]
    slides.value[currentIndex.value] = slides.value[newIndex]
    slides.value[newIndex] = temp
    slides.value.forEach((s, i) => s.order = i + 1)
    currentIndex.value = newIndex
    pushHistory()
  }

  return {
    config,
    slides,
    currentIndex,
    currentSlide,
    loading,
    previewOutline,
    deckId,
    preview,
    generate,
    load,
    save,
    addSlide,
    removeSlide,
    updateMarkdown,
    duplicateSlide,
    undo,
    moveSlide
  }
}
