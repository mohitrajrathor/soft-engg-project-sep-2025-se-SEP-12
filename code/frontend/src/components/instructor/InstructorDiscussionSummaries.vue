<template>
  <div class="flex min-h-screen bg-[#f8fafc]">
    <div class="fixed left-0 top-0 h-screen z-10">
      <instructorSidebar />
    </div>

    <!-- Main Content -->
    <main class="flex-1 p-8 overflow-auto ml-64">
      <!-- Header -->
      <div class="flex justify-between items-center mb-6">
        <div>
          <h2 class="text-2xl font-semibold text-gray-800">Discussion Summaries</h2>
          <p class="text-gray-500">Overview of student discussions and feedback sentiment</p>
        </div>

        <!-- Controls -->
        <div class="flex items-center gap-4">
          <!-- Time Period Filter -->
          <select
            v-model="timePeriod"
            @change="fetchDiscussionData"
            class="px-4 py-2 border border-gray-200 rounded-lg bg-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option :value="7">Last 7 days</option>
            <option :value="30">Last 30 days</option>
            <option :value="90">Last 90 days</option>
            <option :value="365">Last year</option>
          </select>

          <!-- Refresh Button -->
          <button
            @click="fetchDiscussionData"
            :disabled="loading"
            class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
          >
            <svg :class="{'animate-spin': loading}" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {{ loading ? 'Loading...' : 'Refresh' }}
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading && !hasData" class="flex items-center justify-center py-20">
        <div class="text-center">
          <svg class="animate-spin h-12 w-12 text-blue-600 mx-auto mb-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p class="text-gray-500">Loading discussion data...</p>
        </div>
      </div>

      <!-- Error State -->
      <div v-if="error" class="bg-red-50 border border-red-200 rounded-xl p-4 mb-6">
        <div class="flex items-center gap-2 text-red-700">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>{{ error }}</span>
        </div>
      </div>

      <!-- Overview Metrics -->
      <section v-if="hasData" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div
          v-for="(metric, index) in overviewMetrics"
          :key="index"
          class="bg-white rounded-xl p-4 shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
        >
          <h3 class="text-gray-500 text-sm font-medium">{{ metric.title }}</h3>
          <p class="text-2xl font-semibold text-gray-800 mt-1">{{ metric.value }}</p>
          <small class="text-gray-400">{{ metric.subtitle }}</small>
        </div>
      </section>

      <!-- Trend Indicator -->
      <section v-if="trendDirection && hasData" class="mb-6">
        <div
          :class="[
            'inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium',
            trendDirection === 'improving' ? 'bg-green-100 text-green-700' :
            trendDirection === 'declining' ? 'bg-red-100 text-red-700' :
            'bg-gray-100 text-gray-700'
          ]"
        >
          <span v-if="trendDirection === 'improving'">Sentiment Improving</span>
          <span v-else-if="trendDirection === 'declining'">Sentiment Declining</span>
          <span v-else>Sentiment Stable</span>
        </div>
      </section>

      <!-- Charts Section -->
      <section v-if="hasData" class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div class="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
          <h3 class="text-gray-700 font-semibold mb-3">Sentiment Trend Over Time</h3>
          <canvas ref="sentimentTrendChart" height="180"></canvas>
        </div>

        <div class="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
          <h3 class="text-gray-700 font-semibold mb-3">Key Sentiment Drivers</h3>
          <canvas ref="sentimentDriverChart" height="180"></canvas>
        </div>
      </section>

      <!-- Real-time Activity (if available) -->
      <section v-if="realtimeData && realtimeData.data_points && realtimeData.data_points.length > 0" class="mb-8">
        <div class="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
          <div class="flex justify-between items-center mb-3">
            <h3 class="text-gray-700 font-semibold">Real-time Activity (Last 24 Hours)</h3>
            <div class="flex items-center gap-2">
              <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
              <span class="text-xs text-gray-500">Live</span>
            </div>
          </div>
          <canvas ref="realtimeChart" height="120"></canvas>
        </div>
      </section>

      <!-- Discussion Topics -->
      <section v-if="hasData" class="mb-8">
        <h3 class="text-lg font-semibold text-gray-800 mb-3">Top Discussion Topics</h3>
        <div v-if="discussionTopics.length === 0" class="bg-white p-8 rounded-xl shadow-sm border border-gray-100 text-center">
          <p class="text-gray-500">No discussions found in the selected time period.</p>
        </div>
        <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
          <div
            v-for="(topic, index) in discussionTopics"
            :key="index"
            class="bg-white p-5 rounded-xl shadow-sm border border-gray-100 flex flex-col justify-between hover:shadow-md transition-shadow"
          >
            <div>
              <div class="flex items-start justify-between">
                <h4 class="font-semibold text-gray-800 flex-1">{{ topic.title }}</h4>
                <span
                  :class="[
                    'ml-2 px-2 py-0.5 text-xs rounded-full',
                    topic.status === 'resolved' ? 'bg-green-100 text-green-700' :
                    topic.status === 'in_progress' ? 'bg-yellow-100 text-yellow-700' :
                    'bg-gray-100 text-gray-700'
                  ]"
                >
                  {{ topic.status }}
                </span>
              </div>
              <p class="text-sm text-gray-600 mt-1 line-clamp-2">{{ topic.description }}</p>

              <div class="mt-2 text-sm">
                <strong class="text-gray-500">Participants:</strong>
                <span v-for="(p, i) in topic.participants" :key="i" class="ml-1 text-gray-700">
                  {{ p }}{{ i < topic.participants.length - 1 ? ',' : '' }}
                </span>
              </div>

              <div class="flex items-center gap-2 mt-2 text-xs text-gray-500">
                <span>{{ topic.thread_count }} responses</span>
                <span v-if="topic.category" class="px-2 py-0.5 bg-blue-50 text-blue-600 rounded">
                  {{ topic.category }}
                </span>
              </div>

              <div class="flex justify-between mt-3 text-sm">
                <span class="text-green-600">{{ topic.sentiment.positive }}% Positive</span>
                <span class="text-yellow-600">{{ topic.sentiment.neutral }}% Neutral</span>
                <span class="text-red-600">{{ topic.sentiment.negative }}% Negative</span>
              </div>
            </div>

            <button
              @click="viewThread(topic.id)"
              class="mt-4 self-end text-blue-600 text-sm hover:underline flex items-center gap-1"
            >
              View Full Thread
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>
      </section>

      <!-- Sentiment Insights Drawer -->
      <section v-if="hasData" class="bg-white rounded-xl shadow-md border border-gray-100 p-5 transition-all duration-300">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">Sentiment Insights</h3>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <!-- Positive Insights -->
          <div class="bg-green-50 p-4 rounded-lg border border-green-100">
            <h4 class="text-green-700 font-semibold mb-2 flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Positive Insights
            </h4>
            <ul class="text-sm text-gray-700 space-y-1">
              <li v-for="(item, index) in positiveInsights" :key="index" class="flex items-start gap-2">
                <span class="text-green-500 mt-0.5">+</span>
                {{ item }}
              </li>
            </ul>
          </div>

          <!-- Neutral Insights -->
          <div class="bg-yellow-50 p-4 rounded-lg border border-yellow-100">
            <h4 class="text-yellow-700 font-semibold mb-2 flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Neutral Insights
            </h4>
            <ul class="text-sm text-gray-700 space-y-1">
              <li v-for="(item, index) in neutralInsights" :key="index" class="flex items-start gap-2">
                <span class="text-yellow-500 mt-0.5">~</span>
                {{ item }}
              </li>
            </ul>
          </div>

          <!-- Negative Insights -->
          <div class="bg-red-50 p-4 rounded-lg border border-red-100">
            <h4 class="text-red-700 font-semibold mb-2 flex items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Needs Attention
            </h4>
            <ul class="text-sm text-gray-700 space-y-1">
              <li v-for="(item, index) in negativeInsights" :key="index" class="flex items-start gap-2">
                <span class="text-red-500 mt-0.5">!</span>
                {{ item }}
              </li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Topic Clusters (Optional Section) -->
      <section v-if="topicClusters && topicClusters.length > 0" class="mt-8">
        <h3 class="text-lg font-semibold text-gray-800 mb-3">Topic Clusters</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="cluster in topicClusters"
            :key="cluster.cluster_name"
            class="bg-white p-4 rounded-xl shadow-sm border border-gray-100"
          >
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-semibold text-gray-800">{{ cluster.cluster_name }}</h4>
              <span class="text-sm text-gray-500">{{ cluster.query_count }} queries</span>
            </div>
            <div class="flex flex-wrap gap-1 mb-2">
              <span
                v-for="keyword in cluster.keywords"
                :key="keyword"
                class="px-2 py-0.5 bg-blue-50 text-blue-600 text-xs rounded"
              >
                {{ keyword }}
              </span>
            </div>
            <div class="flex items-center gap-2">
              <div class="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
                <div
                  class="h-full bg-green-500 rounded-full"
                  :style="{ width: `${cluster.sentiment_score * 100}%` }"
                ></div>
              </div>
              <span class="text-xs text-gray-500">{{ Math.round(cluster.sentiment_score * 100) }}%</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Last Updated -->
      <div v-if="lastUpdated" class="mt-6 text-center text-sm text-gray-400">
        Last updated: {{ formatDate(lastUpdated) }}
      </div>
    </main>

    <!-- Thread Detail Modal -->
    <div v-if="selectedThread" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl max-w-2xl w-full max-h-[80vh] overflow-hidden">
        <div class="p-4 border-b border-gray-200 flex justify-between items-center">
          <h3 class="font-semibold text-gray-800">{{ selectedThread.title }}</h3>
          <button @click="selectedThread = null" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="p-4 overflow-y-auto max-h-[60vh]">
          <p class="text-gray-600 mb-4">{{ selectedThread.description }}</p>
          <div class="space-y-3">
            <div
              v-for="response in selectedThread.responses"
              :key="response.id"
              :class="[
                'p-3 rounded-lg',
                response.is_solution ? 'bg-green-50 border border-green-200' : 'bg-gray-50'
              ]"
            >
              <div class="flex justify-between items-start mb-1">
                <span class="font-medium text-gray-700">{{ response.author }}</span>
                <span class="text-xs text-gray-400">{{ response.author_role }}</span>
              </div>
              <p class="text-sm text-gray-600">{{ response.content }}</p>
              <div v-if="response.is_solution" class="mt-2 text-xs text-green-600 font-medium">
                Marked as Solution
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, nextTick } from "vue";
import Chart from "chart.js/auto";
import instructorSidebar from '@/components/layout/instructorLayout/instructorSideBar.vue';
import { instructorAnalyticsAPI } from '@/api/instructorAnalytics';

// Refs for data
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
const topicClusters = ref([]);
const realtimeData = ref(null);
const trendDirection = ref('');
const lastUpdated = ref(null);
const selectedThread = ref(null);

// UI State
const loading = ref(false);
const error = ref(null);
const timePeriod = ref(30);

// Chart instances
let trendChartInstance = null;
let driverChartInstance = null;
let realtimeChartInstance = null;

// Chart refs
const sentimentTrendChart = ref(null);
const sentimentDriverChart = ref(null);
const realtimeChart = ref(null);

// Auto-refresh interval
let refreshInterval = null;

// Computed
const hasData = computed(() => {
  return discussionTopics.value.length > 0 || overviewMetrics.value[0].value !== "—";
});

// Format date helper
const formatDate = (date) => {
  if (!date) return '';
  return new Date(date).toLocaleString();
};

// Fetch API data
const fetchDiscussionData = async () => {
  loading.value = true;
  error.value = null;

  try {
    // Fetch main discussion summaries
    const data = await instructorAnalyticsAPI.getDiscussionSummaries({
      days: timePeriod.value,
      limit: 12
    });

    // Update metrics
    if (data.metrics) {
      overviewMetrics.value = data.metrics;
    }

    // Update topics
    if (data.topics) {
      discussionTopics.value = data.topics;
    }

    // Update insights
    if (data.insights) {
      positiveInsights.value = data.insights.positive || [];
      neutralInsights.value = data.insights.neutral || [];
      negativeInsights.value = data.insights.negative || [];
    }

    // Update last updated time
    lastUpdated.value = data.generated_at || new Date().toISOString();

    // Render charts after data is loaded
    await nextTick();
    if (data.trends && data.drivers) {
      renderCharts(data.trends, data.drivers);
    }

    // Fetch additional data
    try {
      const [clustersData, realtimeResponse] = await Promise.all([
        instructorAnalyticsAPI.getTopicClusters({ days: timePeriod.value }),
        instructorAnalyticsAPI.getRealtimeSentiment({ hours: 24 })
      ]);

      if (clustersData?.clusters) {
        topicClusters.value = clustersData.clusters;
      }

      if (realtimeResponse) {
        realtimeData.value = realtimeResponse;
        trendDirection.value = realtimeResponse.trend_direction || 'stable';
        await nextTick();
        renderRealtimeChart(realtimeResponse);
      }
    } catch (additionalErr) {
      console.warn("Could not fetch additional analytics:", additionalErr);
    }

  } catch (err) {
    console.error("Error fetching discussion summaries:", err);
    error.value = "Failed to load discussion data. Please try again.";

    // Use fallback mock data
    useFallbackData();
  } finally {
    loading.value = false;
  }
};

// Fallback mock data
const useFallbackData = () => {
  discussionTopics.value = [
    {
      id: 1,
      title: "Understanding Recursion",
      description: "Students discuss the conceptual depth of recursive algorithms.",
      participants: ["Alice", "Bob", "Priya"],
      sentiment: { positive: 60, neutral: 25, negative: 15 },
      thread_count: 5,
      category: "technical",
      status: "resolved"
    },
    {
      id: 2,
      title: "Data Structures – Linked List",
      description: "Common confusion around memory allocation and pointers.",
      participants: ["Rahul", "Neha", "Liam"],
      sentiment: { positive: 50, neutral: 30, negative: 20 },
      thread_count: 3,
      category: "technical",
      status: "in_progress"
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

  overviewMetrics.value = [
    { title: "Total Discussions", value: "24", subtitle: "Sample data" },
    { title: "Active Threads", value: "8", subtitle: "Sample data" },
    { title: "Average Sentiment", value: "65%", subtitle: "Positive" },
    { title: "Unresolved Queries", value: "5", subtitle: "Needs attention" },
  ];

  nextTick(() => {
    renderCharts(
      {
        months: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        positive: [70, 65, 80, 75, 72, 78],
        neutral: [20, 25, 15, 20, 22, 18],
        negative: [10, 10, 5, 5, 6, 4],
      },
      {
        labels: ["Recursion", "Pointers", "Sorting", "Graphs", "SQL"],
        positive: [50, 40, 70, 60, 55],
        negative: [20, 35, 15, 25, 20],
      }
    );
  });
};

// View thread detail
const viewThread = async (queryId) => {
  try {
    const threadData = await instructorAnalyticsAPI.getDiscussionDetail(queryId);
    selectedThread.value = threadData;
  } catch (err) {
    console.error("Error fetching thread details:", err);
    // Show a simple version from local data
    const topic = discussionTopics.value.find(t => t.id === queryId);
    if (topic) {
      selectedThread.value = {
        ...topic,
        responses: []
      };
    }
  }
};

// Render Charts
const renderCharts = (trendData, driverData) => {
  // Destroy existing charts
  if (trendChartInstance) {
    trendChartInstance.destroy();
    trendChartInstance = null;
  }
  if (driverChartInstance) {
    driverChartInstance.destroy();
    driverChartInstance = null;
  }

  // Trend Chart
  if (sentimentTrendChart.value) {
    const ctx1 = sentimentTrendChart.value.getContext('2d');
    trendChartInstance = new Chart(ctx1, {
      type: "line",
      data: {
        labels: trendData.months,
        datasets: [
          {
            label: "Positive",
            data: trendData.positive,
            borderColor: "#22c55e",
            backgroundColor: "rgba(34, 197, 94, 0.1)",
            fill: true,
            tension: 0.4
          },
          {
            label: "Neutral",
            data: trendData.neutral,
            borderColor: "#eab308",
            backgroundColor: "rgba(234, 179, 8, 0.1)",
            fill: true,
            tension: 0.4
          },
          {
            label: "Negative",
            data: trendData.negative,
            borderColor: "#ef4444",
            backgroundColor: "rgba(239, 68, 68, 0.1)",
            fill: true,
            tension: 0.4
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: true, position: 'bottom' }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 100
          }
        }
      },
    });
  }

  // Driver Chart
  if (sentimentDriverChart.value) {
    const ctx2 = sentimentDriverChart.value.getContext('2d');
    driverChartInstance = new Chart(ctx2, {
      type: "bar",
      data: {
        labels: driverData.labels,
        datasets: [
          {
            label: "Positive",
            data: driverData.positive,
            backgroundColor: "#22c55e",
            borderRadius: 4
          },
          {
            label: "Negative",
            data: driverData.negative,
            backgroundColor: "#ef4444",
            borderRadius: 4
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: "bottom" }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      },
    });
  }
};

// Render realtime chart
const renderRealtimeChart = (data) => {
  if (realtimeChartInstance) {
    realtimeChartInstance.destroy();
    realtimeChartInstance = null;
  }

  if (!realtimeChart.value || !data.data_points || data.data_points.length === 0) {
    return;
  }

  const ctx = realtimeChart.value.getContext('2d');
  const labels = data.data_points.map(dp => {
    const date = new Date(dp.timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  });

  realtimeChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Activity',
          data: data.data_points.map(dp => dp.total),
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          fill: true,
          tension: 0.4,
          pointRadius: 2
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          beginAtZero: true
        },
        x: {
          ticks: {
            maxTicksLimit: 8
          }
        }
      }
    }
  });
};

// Setup auto-refresh (every 5 minutes)
const setupAutoRefresh = () => {
  refreshInterval = setInterval(() => {
    fetchDiscussionData();
  }, 5 * 60 * 1000); // 5 minutes
};

onMounted(() => {
  fetchDiscussionData();
  setupAutoRefresh();
});

onUnmounted(() => {
  // Cleanup
  if (refreshInterval) {
    clearInterval(refreshInterval);
  }
  if (trendChartInstance) {
    trendChartInstance.destroy();
  }
  if (driverChartInstance) {
    driverChartInstance.destroy();
  }
  if (realtimeChartInstance) {
    realtimeChartInstance.destroy();
  }
});
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

/* Line clamp for descriptions */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
