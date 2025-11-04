<template>
  <div class="min-h-screen bg-white">
    <!-- ==================== HEADER ==================== -->
    <header class="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <!-- Logo -->
          <div class="flex items-center">
            <div
              class="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center"
            >
              <span class="text-white font-bold text-xl">A</span>
            </div>
            <span class="ml-3 text-2xl font-bold text-gray-900">Aura</span>
          </div>

          <!-- Desktop Nav -->
          <nav class="flex space-x-8">
            <a href="#home" class="text-gray-700 hover:text-blue-600 font-medium">Home</a>
            <a href="#features" class="text-gray-700 hover:text-blue-600 font-medium">Features</a>
            <a href="#about" class="text-gray-700 hover:text-blue-600 font-medium">About</a>
            <a href="#contact" class="text-gray-700 hover:text-blue-600 font-medium">Contact</a>
          </nav>

          <!-- Buttons -->
          <div class="flex items-center space-x-4">
            <button 
            @click="goToLogin"
            class="px-4 py-2 text-blue-600 font-medium hover:text-blue-700">
              Sign In
            </button>
            <button
              @click="goToRegister"
              class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition duration-200"
            >
              Get Started
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- ==================== HERO ==================== -->
    <section id="home" class="py-20 bg-gradient-to-b from-blue-50 to-white text-center">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 class="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
          Welcome to <span class="text-blue-600">Aura</span>
        </h1>
        <p class="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          Your AI-Powered Academic Support System for IITM Students, TAs, Instructors, and Administrators
        </p>
        <p class="text-lg text-gray-500 mb-10 max-w-2xl mx-auto">
          Revolutionizing academic support through intelligent assistance, personalized learning, and seamless communication
        </p>
        <button
          class="px-8 py-4 bg-blue-600 text-white rounded-lg text-lg font-medium hover:bg-blue-700 shadow-lg"
        >
          Explore Aura
        </button>
      </div>
    </section>

    <!-- ==================== FEATURES ==================== -->
    <section id="features" class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl font-bold text-gray-900 mb-4">Key Features</h2>
          <p class="text-xl text-gray-600">Empowering academic excellence through AI innovation</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <FeatureCard
            v-for="(feature, index) in features"
            :key="index"
            :icon="feature.icon"
            :title="feature.title"
            :color="feature.color"
            :description="feature.description"
          />
        </div>
      </div>
    </section>

    <!-- ==================== ABOUT ==================== -->
    <section id="about" class="py-20 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold text-gray-900 mb-4">About Aura</h2>
          <p class="text-xl text-gray-600 max-w-3xl mx-auto">
            Aura is an innovative AI-powered academic support system designed specifically for the IITM BS Degree Program community.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          <!-- Mission -->
          <div>
            <h3 class="text-2xl font-bold text-gray-900 mb-4">Our Mission</h3>
            <p class="text-gray-600 mb-6">
              To revolutionize the academic experience at IITM by leveraging cutting-edge Generative AI technologies…
            </p>

            <h3 class="text-2xl font-bold text-gray-900 mb-4">Who We Serve</h3>
            <ul class="space-y-3">
              <li v-for="(item, index) in serveList" :key="index" class="flex items-start">
                <div
                  class="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center mr-3 mt-0.5"
                >
                  <span class="text-blue-600 text-sm font-bold">✓</span>
                </div>
                <span class="text-gray-600" v-html="item"></span>
              </li>
            </ul>
          </div>

          <!-- Technologies -->
          <div class="bg-white rounded-xl shadow-lg p-8 border border-gray-200">
            <h3 class="text-2xl font-bold text-gray-900 mb-6">Key Technologies</h3>
            <div class="space-y-4">
              <div
                v-for="(tech, i) in technologies"
                :key="i"
                class="flex items-center"
              >
                <div
                  :class="['w-10 h-10 rounded-lg flex items-center justify-center mr-4', tech.bg]"
                >
                  <i :data-lucide="tech.icon" class="lucide text-white"></i>
                </div>
                <div>
                  <h4 class="font-bold text-gray-900">{{ tech.title }}</h4>
                  <p class="text-sm text-gray-600">{{ tech.desc }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== CONTACT ==================== -->
    <section id="contact" class="py-20 bg-white text-center">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">Get in Touch</h2>
        <p class="text-xl text-gray-600 mb-8">
          Have questions about Aura? We'd love to hear from you.
        </p>
        <div class="bg-gray-50 rounded-xl p-8 border border-gray-200">
          <p class="text-gray-700 mb-6">
            For inquiries, feedback, or support, please contact us at:
          </p>
          <a
            href="mailto:aura@iitm.ac.in"
            class="text-blue-600 font-bold text-lg hover:text-blue-700"
          >
            aura@iitm.ac.in
          </a>
        </div>
      </div>
    </section>

    <!-- ==================== FOOTER ==================== -->
    <footer class="bg-gray-900 text-white py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <div class="flex items-center mb-4">
              <div
                class="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center"
              >
                <span class="text-white font-bold text-xl">A</span>
              </div>
              <span class="ml-3 text-2xl font-bold">Aura</span>
            </div>
            <p class="text-gray-400">AI-Powered Academic Support System for IITM</p>
          </div>

          <div>
            <h4 class="font-bold text-lg mb-4">Quick Links</h4>
            <ul class="space-y-2">
              <li><a href="#home" class="text-gray-400 hover:text-white">Home</a></li>
              <li><a href="#features" class="text-gray-400 hover:text-white">Features</a></li>
              <li><a href="#about" class="text-gray-400 hover:text-white">About</a></li>
              <li><a href="#contact" class="text-gray-400 hover:text-white">Contact</a></li>
            </ul>
          </div>

          <div>
            <h4 class="font-bold text-lg mb-4">Connect</h4>
            <p class="text-gray-400 mb-2">Indian Institute of Technology Madras</p>
            <p class="text-gray-400">Chennai, Tamil Nadu 600036</p>
          </div>
        </div>

        <div class="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>© 2024 Aura. All rights reserved. | IITM BS Degree Program</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const goToRegister = () => {
  router.push('/register')
} 
const goToLogin = () => {
  router.push('/login')
}

// =================== DATA ===================
const features = [
  { icon: 'message-circle', color: 'bg-blue-100 text-blue-600', title: 'RAG-based Multilingual AI Assistant', description: 'Get instant answers to academic and administrative questions…' },
  { icon: 'calendar', color: 'bg-purple-100 text-purple-600', title: 'Smart Study Assistant', description: 'Receive weekly summaries of lectures and tasks…' },
  { icon: 'book-open', color: 'bg-green-100 text-green-600', title: 'AI Content Recommender', description: 'Get personalized content recommendations…' },
  { icon: 'file-text', color: 'bg-orange-100 text-orange-600', title: 'TA Doubt Summarizer', description: 'Automatically summarize student queries…' },
  { icon: 'bell', color: 'bg-red-100 text-red-600', title: 'AI Query Escalation System', description: 'Automatically route queries to the right person…' },
  { icon: 'trending-up', color: 'bg-indigo-100 text-indigo-600', title: 'Admin Analytics Dashboard', description: 'Visualize system-wide metrics…' },
  { icon: 'users', color: 'bg-pink-100 text-pink-600', title: 'AI Discourse Integration', description: 'Quickly find if your question has been asked before…' },
  { icon: 'brain', color: 'bg-cyan-100 text-cyan-600', title: 'AI Onboarding Mentor', description: 'Personalized onboarding guide for new TAs…' },
  { icon: 'file-text', color: 'bg-yellow-100 text-yellow-600', title: 'Automated Assessment Generator', description: 'Dynamically create question sets…' }
]

const serveList = [
  '<strong>Students:</strong> Get instant answers…',
  '<strong>TAs:</strong> Manage workload efficiently…',
  '<strong>Instructors:</strong> Track student engagement…',
  '<strong>Administrators:</strong> Gain insights…'
]

const technologies = [
  { bg: 'bg-gradient-to-br from-blue-500 to-blue-600', icon: 'brain', title: 'RAG (Retrieval Augmented Generation)', desc: 'For accurate, context-aware responses' },
  { bg: 'bg-gradient-to-br from-purple-500 to-purple-600', icon: 'message-circle', title: 'Conversational AI', desc: 'Natural language interaction' },
  { bg: 'bg-gradient-to-br from-green-500 to-green-600', icon: 'trending-up', title: 'AI Agents & Workflow Automation', desc: 'Intelligent task management' },
  { bg: 'bg-gradient-to-br from-orange-500 to-orange-600', icon: 'file-text', title: 'LLM-based Summarization', desc: 'Concise information extraction' }
]

// =================== ICONS ===================
onMounted(() => {
  const script = document.createElement('script')
  script.src = 'https://unpkg.com/lucide@latest/dist/umd/lucide.js'
  script.onload = () => window.lucide?.createIcons()
  document.head.appendChild(script)
})

// =================== COMPONENT ===================
const FeatureCard = {
  props: ['icon', 'title', 'description', 'color'],
  template: `
    <div class="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-lg transition-shadow">
      <div :class="['w-12 h-12 rounded-lg flex items-center justify-center mb-4', color]">
        <i :data-lucide="icon" class="lucide"></i>
      </div>
      <h3 class="text-xl font-bold text-gray-900 mb-3">{{ title }}</h3>
      <p class="text-gray-600">{{ description }}</p>
    </div>
  `
}
</script>

<style scoped>
.lucide {
  width: 1.5rem;
  height: 1.5rem;
}
</style>
