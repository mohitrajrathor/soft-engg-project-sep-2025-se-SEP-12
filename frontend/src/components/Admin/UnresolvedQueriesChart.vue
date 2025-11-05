<template>
  <div>
    <Pie :data="data" :options="options" />
  </div>
</template>
<script setup>
import { Pie } from 'vue-chartjs'
import { ref } from 'vue'
const data = ref({
  labels: ['Academic', 'Technical', 'Exam'],
  datasets: [{
    label: 'Unresolved',
    backgroundColor: ['#fbbf24', '#34d399', '#60a5fa'],
    data: [9, 4, 2, 3]
  }]
})
const options = ref({ responsive: true })
</script>
