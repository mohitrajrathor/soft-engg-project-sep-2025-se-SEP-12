/**
 * Instructor Analytics API endpoints for Discussion Summaries Dashboard
 */

import api from './axios'

export const instructorAnalyticsAPI = {
  /**
   * Get discussion summaries with sentiment analysis
   * @param {Object} params - Query parameters
   * @param {number} [params.days] - Time period in days (default: 30)
   * @param {number} [params.limit] - Number of topics to return (default: 10)
   * @returns {Promise} Discussion summaries including metrics, topics, trends, and insights
   */
  async getDiscussionSummaries(params = { days: 30, limit: 10 }) {
    const response = await api.get('/instructor/discussion-summaries', { params })
    return response.data
  },

  /**
   * Get topic clustering analysis
   * @param {Object} params - Query parameters
   * @param {number} [params.days] - Time period in days (default: 30)
   * @returns {Promise} Topic clusters with keywords and sentiment scores
   */
  async getTopicClusters(params = { days: 30 }) {
    const response = await api.get('/instructor/topic-clusters', { params })
    return response.data
  },

  /**
   * Get real-time sentiment data for live charts
   * @param {Object} params - Query parameters
   * @param {number} [params.hours] - Hours of data to return (default: 24)
   * @returns {Promise} Time series sentiment data
   */
  async getRealtimeSentiment(params = { hours: 24 }) {
    const response = await api.get('/instructor/realtime-sentiment', { params })
    return response.data
  },

  /**
   * Get detailed discussion thread
   * @param {number} queryId - Query/Discussion ID
   * @returns {Promise} Full discussion details with all responses
   */
  async getDiscussionDetail(queryId) {
    const response = await api.get(`/instructor/discussion/${queryId}`)
    return response.data
  },

  /**
   * Get all instructor analytics data at once (for dashboard initialization)
   * @param {Object} options - Options for specific endpoints
   * @param {number} [options.days] - Time period in days
   * @param {number} [options.topicLimit] - Number of topics
   * @param {number} [options.realtimeHours] - Hours for realtime data
   * @returns {Promise} Combined analytics data
   */
  async getAllInstructorAnalytics(options = {}) {
    const { days = 30, topicLimit = 10, realtimeHours = 24 } = options

    const [summaries, clusters, realtime] = await Promise.all([
      this.getDiscussionSummaries({ days, limit: topicLimit }),
      this.getTopicClusters({ days }),
      this.getRealtimeSentiment({ hours: realtimeHours })
    ])

    return {
      summaries,
      clusters,
      realtime
    }
  }
}

export default instructorAnalyticsAPI
