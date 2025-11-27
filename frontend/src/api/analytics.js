/**
 * Analytics API endpoints for Admin Dashboard
 */

import api from './axios'

export const analyticsAPI = {
  /**
   * Get overall system metrics
   * @returns {Promise} Overview metrics including users, queries, responses
   */
  async getOverview() {
    const response = await api.get('/analytics/overview')
    return response.data
  },

  /**
   * Get frequently asked questions
   * @param {Object} params - Query parameters
   * @param {number} [params.limit] - Number of FAQs to return (default: 20)
   * @param {number} [params.days] - Time period in days (default: 30)
   * @returns {Promise} FAQ data with counts and metadata
   */
  async getFAQs(params = { limit: 20, days: 30 }) {
    const response = await api.get('/analytics/faqs', { params })
    return response.data
  },

  /**
   * Get performance metrics
   * @returns {Promise} Response time and resolution rate metrics
   */
  async getPerformance() {
    const response = await api.get('/analytics/performance')
    return response.data
  },

  /**
   * Get sentiment analysis
   * @returns {Promise} Aggregate feedback sentiment data
   */
  async getSentiment() {
    const response = await api.get('/analytics/sentiment')
    return response.data
  },

  /**
   * Get usage statistics
   * @returns {Promise} Active users, API calls, session stats with breakdowns
   */
  async getUsage() {
    const response = await api.get('/analytics/usage')
    return response.data
  },

  /**
   * Get all analytics data at once (for dashboard initialization)
   * @param {Object} options - Options for specific endpoints
   * @param {number} [options.faqLimit] - Number of FAQs
   * @param {number} [options.faqDays] - FAQ time period
   * @returns {Promise} Combined analytics data
   */
  async getAllAnalytics(options = {}) {
    const { faqLimit = 10, faqDays = 30 } = options

    const [overview, faqs, performance, sentiment, usage] = await Promise.all([
      this.getOverview(),
      this.getFAQs({ limit: faqLimit, days: faqDays }),
      this.getPerformance(),
      this.getSentiment(),
      this.getUsage()
    ])

    return {
      overview,
      faqs,
      performance,
      sentiment,
      usage
    }
  }
}
