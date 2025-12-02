<template>
  <div class="graph-renderer-container w-full h-auto my-4">
    <div v-if="!graphData" class="text-slate-400 text-sm italic">No graph data</div>
    
    <div v-else class="graph-wrapper">
      <h4 class="text-sm font-semibold text-slate-700 mb-3">{{ graphData.title }}</h4>
      
      <!-- Chart.js Canvas -->
      <canvas 
        ref="chartCanvas" 
        class="max-w-full h-auto"
        :width="300"
        :height="200"
      ></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'

// Try to import Chart.js
let Chart
try {
  Chart = (await import('chart.js')).default
} catch (e) {
  console.warn('Chart.js not available. Install with: npm install chart.js')
}

const props = defineProps({
  graphData: {
    type: Object,
    default: null
  }
})

const chartCanvas = ref(null)
let chartInstance = null

const chartConfig = {
  bar: (graphData) => ({
    type: 'bar',
    data: {
      labels: graphData.labels,
      datasets: graphData.datasets
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { display: true }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  }),
  line: (graphData) => ({
    type: 'line',
    data: {
      labels: graphData.labels,
      datasets: graphData.datasets
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { display: true }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  }),
  pie: (graphData) => ({
    type: 'pie',
    data: {
      labels: graphData.labels,
      datasets: graphData.datasets
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { display: true }
      }
    }
  }),
  scatter: (graphData) => ({
    type: 'scatter',
    data: {
      datasets: graphData.datasets
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { display: true }
      },
      scales: {
        x: { type: 'linear' },
        y: { type: 'linear' }
      }
    }
  })
}

function renderChart() {
  if (!Chart || !chartCanvas.value || !props.graphData) return

  // Destroy previous chart instance
  if (chartInstance) {
    chartInstance.destroy()
    chartInstance = null
  }

  const type = props.graphData.type.toLowerCase()
  const config = chartConfig[type]

  if (!config) {
    console.warn(`Unsupported graph type: ${type}`)
    return
  }

  try {
    const ctx = chartCanvas.value.getContext('2d')
    chartInstance = new Chart(ctx, config(props.graphData))
  } catch (error) {
    console.error('Failed to render chart:', error)
  }
}

watch(() => props.graphData, () => {
  nextTick(() => renderChart())
}, { deep: true })

onMounted(() => {
  nextTick(() => renderChart())
})
</script>

<style scoped>
.graph-renderer-container {
  @apply bg-white/50 p-4 rounded-lg border border-slate-200;
}

.graph-wrapper {
  @apply flex flex-col items-center;
}
</style>
