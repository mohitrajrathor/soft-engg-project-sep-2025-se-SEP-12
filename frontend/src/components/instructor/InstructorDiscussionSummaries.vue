<template>
  <div class="flex min-h-screen bg-[#f8fafc]">
    <div class="fixed left-0 top-0 h-screen z-10">
      <instructorSidebar />
    </div>
    
    <!-- Main Content -->
    <main class="flex-1 p-8 overflow-auto ml-48">
      <!-- Header -->
      <div class="mb-6">
        <h2 class="text-2xl font-semibold text-gray-800">Discussion Summaries</h2>
        <p class="text-gray-500">Overview of student discussions and feedback sentiment</p>
      </div>

      <!-- Overview Metrics -->
      <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div v-for="(metric, index) in overviewMetrics" :key="index" class="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
          <h3 class="text-gray-500 text-sm font-medium">{{ metric.title }}</h3>
          <p class="text-2xl font-semibold text-gray-800 mt-1">{{ metric.value }}</p>
          <small class="text-gray-400">{{ metric.subtitle }}</small>
        </div>
      </section>

      <!-- Charts Section -->
      <section class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div class="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
          <h3 class="text-gray-700 font-semibold mb-3">Sentiment Trend Over Time</h3>
          <canvas id="sentimentTrendChart" height="180"></canvas>
        </div>

        <div class="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
          <h3 class="text-gray-700 font-semibold mb-3">Key Sentiment Drivers</h3>
          <canvas id="sentimentDriverChart" height="180"></canvas>
        </div>
      </section>

      <!-- Discussion Topics -->
      <section class="mb-8">
        <h3 class="text-lg font-semibold text-gray-800 mb-3">Top Discussion Topics</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
          <div v-for="(topic, index) in discussionTopics" :key="index" class="bg-white p-5 rounded-xl shadow-sm border border-gray-100 flex flex-col justify-between">
            <div>
              <h4 class="font-semibold text-gray-800">{{ topic.title }}</h4>
              <p class="text-sm text-gray-600 mt-1">{{ topic.description }}</p>
              <div class="mt-2 text-sm">
                <strong>Participants:</strong>
                <span v-for="(p, i) in topic.participants" :key="i" class="ml-1 text-gray-700">{{ p }}</span>
              </div>

              <div class="flex justify-between mt-3 text-sm">
                <span class="text-green-600">🟢 {{ topic.sentiment.positive }}% Positive</span>
                <span class="text-yellow-600">🟡 {{ topic.sentiment.neutral }}% Neutral</span>
                <span class="text-red-600">🔴 {{ topic.sentiment.negative }}% Negative</span>
              </div>
            </div>

            <button class="mt-4 self-end text-blue-600 text-sm hover:underline">
              View Full Thread →
            </button>
          </div>
        </div>
      </section>

      <!-- Sentiment Insights Drawer -->
      <section class="bg-white rounded-xl shadow-md border border-gray-100 p-5 transition-all duration-300">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">Sentiment Insights</h3>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <!-- Positive Insights -->
          <div class="bg-green-50 p-4 rounded-lg border border-green-100">
            <h4 class="text-green-700 font-semibold mb-2">Positive Insights</h4>
            <ul class="text-sm text-gray-700 space-y-1">
              <li v-for="(item, index) in positiveInsights" :key="index">• {{ item }}</li>
            </ul>
            <button class="mt-3 text-green-700 text-sm font-medium hover:underline">
              View Full Thread →
            </button>
          </div>

          <!-- Neutral Insights -->
          <div class="bg-yellow-50 p-4 rounded-lg border border-yellow-100">
            <h4 class="text-yellow-700 font-semibold mb-2">Neutral Insights</h4>
            <ul class="text-sm text-gray-700 space-y-1">
              <li v-for="(item, index) in neutralInsights" :key="index">• {{ item }}</li>
            </ul>
            <button class="mt-3 text-yellow-700 text-sm font-medium hover:underline">
              View Full Thread →
            </button>
          </div>

          <!-- Negative Insights -->
          <div class="bg-red-50 p-4 rounded-lg border border-red-100">
            <h4 class="text-red-700 font-semibold mb-2">Negative Insights</h4>
            <ul class="text-sm text-gray-700 space-y-1">
              <li v-for="(item, index) in negativeInsights" :key="index">• {{ item }}</li>
            </ul>
            <button class="mt-3 text-red-700 text-sm font-medium hover:underline">
              View Full Thread →
            </button>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";
import instructorSidebar from '@/components/layout/instructorLayout/instructorSideBar.vue';

const overviewMetrics = ref([
  { title: "Total Discussions", value: "—", subtitle: "" },
  { title: "Active Threads", value: "—", subtitle: "" },
  { title: "Average Sentiment", value: "—", subtitle: "" },
  { title: "Unresolved Queries", value: "—", subtitle: "" },
]);

const discussionTopics = ref([]);
const positiveInsights = ref([]);
const neutralInsights = ref([]);
const negativeInsights = ref([]);

// Fetch API data (placeholder)
const fetchDiscussionData = async () => {
  try {
    const res = await fetch("/api/instructor/discussion-summaries");
    const data = await res.json();

    overviewMetrics.value = data.metrics;
    discussionTopics.value = data.topics;
    positiveInsights.value = data.insights.positive;
    neutralInsights.value = data.insights.neutral;
    negativeInsights.value = data.insights.negative;

    renderCharts(data.trends, data.drivers);
  } catch (err) {
    console.error("Error fetching discussion summaries:", err);

    // Fallback Mock Data
    discussionTopics.value = [
      {
        title: "Understanding Recursion",
        description: "Students discuss the conceptual depth of recursive algorithms.",
        participants: ["Alice", "Bob", "Priya"],
        sentiment: { positive: 60, neutral: 25, negative: 15 },
      },
      {
        title: "Data Structures – Linked List",
        description: "Common confusion around memory allocation and pointers.",
        participants: ["Rahul", "Neha", "Liam"],
        sentiment: { positive: 50, neutral: 30, negative: 20 },
      },
    ];

    positiveInsights.value = [
      "Students found the recursion examples engaging.",
      "Clear visualization improved understanding.",
    ];
    neutralInsights.value = [
      "Some students suggested slower pacing.",
      "Clarified syntax but still unsure of logic depth.",
    ];
    negativeInsights.value = [
      "Students struggled with base case logic.",
      "Need more practice problems for reinforcement.",
    ];

    renderCharts(
      {
        months: ["Jan", "Feb", "Mar", "Apr"],
        positive: [70, 65, 80, 75],
        neutral: [20, 25, 15, 20],
        negative: [10, 10, 5, 5],
      },
      {
        labels: ["Recursion", "Pointers", "Sorting", "Graphs"],
        positive: [50, 40, 70, 60],
        negative: [20, 35, 15, 25],
      }
    );
  }
};

// Render Charts
const renderCharts = (trendData, driverData) => {
  const ctx1 = document.getElementById("sentimentTrendChart");
  const ctx2 = document.getElementById("sentimentDriverChart");

  new Chart(ctx1, {
    type: "line",
    data: {
      labels: trendData.months,
      datasets: [
        { label: "Positive", data: trendData.positive, borderColor: "#22c55e", fill: false },
        { label: "Neutral", data: trendData.neutral, borderColor: "#eab308", fill: false },
        { label: "Negative", data: trendData.negative, borderColor: "#ef4444", fill: false },
      ],
    },
    options: { responsive: true, plugins: { legend: { display: true } } },
  });

  new Chart(ctx2, {
    type: "bar",
    data: {
      labels: driverData.labels,
      datasets: [
        { label: "Positive", data: driverData.positive, backgroundColor: "#22c55e" },
        { label: "Negative", data: driverData.negative, backgroundColor: "#ef4444" },
      ],
    },
    options: { responsive: true, plugins: { legend: { position: "bottom" } } },
  });
};

onMounted(fetchDiscussionData);
</script>

<style scoped>
/* Custom Scrollbar */
section::-webkit-scrollbar {
  height: 6px;
  width: 6px;
}
section::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 8px;
}
section::-webkit-scrollbar-thumb:hover {
  background-color: #94a3b8;
}
</style>