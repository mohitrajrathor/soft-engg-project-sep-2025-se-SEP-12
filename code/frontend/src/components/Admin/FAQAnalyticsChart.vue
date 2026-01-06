<template>
  <div>
    <Bar :data="data" :options="options" />
  </div>
</template>
<script setup>
import { Bar } from 'vue-chartjs'
import { ref } from 'vue'
const data = ref({
  labels: ['Admissions', 'Fees', 'Exams'],
  datasets: [{
    label: 'FAQ Frequency',
    backgroundColor: '#6366f1',
    data: [30, 8, 5]
  }]
})
const options = ref({ responsive: true })
</script>
