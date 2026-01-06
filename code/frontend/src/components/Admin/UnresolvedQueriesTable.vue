<template>
  <div class="overflow-x-auto">
    <table class="min-w-full bg-white rounded-lg">
      <thead class="bg-indigo-100">
        <tr>
          <th class="py-2 px-4">ID</th>
          <th class="py-2 px-4">Topic</th>
          <th class="py-2 px-4">Submitted By</th>
          <th class="py-2 px-4">Date</th>
          <th class="py-2 px-4">Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="q in rows" :key="q.id">
          <td class="py-2 px-4">{{ q.id }}</td>
          <td class="py-2 px-4">{{ q.topic }}</td>
          <td class="py-2 px-4">{{ q.by }}</td>
          <td class="py-2 px-4">{{ q.date }}</td>
          <td class="py-2 px-4">
            <span class="inline-block px-2 py-1 rounded-full bg-yellow-200 text-yellow-800 text-sm">{{ q.status }}</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script setup>
const rows = [
  { id: 1, topic: 'Hostel Allotment', by: 'Student', date: '2025-11-01', status: 'Pending' },
  { id: 2, topic: 'Exam Timetable', by: 'TA', date: '2025-11-02', status: 'Pending' },
  { id: 3, topic: 'Course Add/Drop', by: 'Student', date: '2025-11-03', status: 'Pending' }
]
</script>
