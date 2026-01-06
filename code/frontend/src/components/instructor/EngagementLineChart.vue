<script setup>
import { Line } from 'vue-chartjs'
import {
  Chart, Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale,
} from 'chart.js'

Chart.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale)

// Dummy data for student engagement
const chartData = {
  labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
  datasets: [
    {
      label: 'Active Students',
      backgroundColor: 'rgba(79, 70, 229, 0.1)',
      borderColor: '#6366f1',
      data: [15, 19, 13, 22, 17],
      fill: true,
      tension: 0.4,
      pointBackgroundColor: '#6366f1',
      pointRadius: 4,
      pointHoverRadius: 6
    },
  ],
}

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: false,
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: { color: '#E5E7EB' },
      ticks: { color: '#64748b' }
    },
    x: {
      grid: { display: false },
      ticks: { color: '#64748b' }
    }
  }
}
</script>

<template>
  <Line :data="chartData" :options="chartOptions" class="!bg-blue-50/70 rounded-xl !p-4" />
</template>
