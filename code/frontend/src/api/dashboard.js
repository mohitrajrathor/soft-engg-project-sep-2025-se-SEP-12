/**
 * Dashboard and Analytics API endpoints
 */

import api from './axios'

export const dashboardAPI = {
  /**
   * Get overall system statistics
   * @returns {Promise} Dashboard statistics
   */
  async getStatistics() {
    const response = await api.get('/dashboard/statistics')
    return response.data
  },

  /**
   * Get activity timeline (queries, resources, announcements over time)
   * @param {Object} params - Query parameters
   * @param {number} [params.days] - Number of days to include (default: 7)
   * @returns {Promise} Activity timeline data
   */
  async getActivityTimeline(params = {}) {
    const response = await api.get('/dashboard/activity-timeline', { params })
    return response.data
  },

  /**
   * Get top knowledge sources by views/usage
   * @param {Object} params - Query parameters
   * @param {number} [params.limit] - Number of top sources (default: 10)
   * @returns {Promise} Top knowledge sources
   */
  async getTopSources(params = {}) {
    const response = await api.get('/dashboard/top-sources', { params })
    return response.data
  },

  /**
   * Get user-specific dashboard data (combination of multiple endpoints)
   * @returns {Promise} Combined dashboard data
   */
  async getDashboardData() {
    const [statistics, timeline, topSources] = await Promise.all([
      this.getStatistics(),
      this.getActivityTimeline(),
      this.getTopSources()
    ])

    return {
      statistics,
      timeline,
      topSources
    }
  }
}
