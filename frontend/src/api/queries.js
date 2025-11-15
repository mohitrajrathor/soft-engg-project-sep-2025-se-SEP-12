/**
 * Queries API Service
 *
 * Provides methods for query/doubt management:
 * - List queries with filtering
 * - Get query details with responses
 * - Create new queries
 * - Add responses to queries
 * - Update query status
 * - Get query statistics
 */

import api from './axios'

export const queriesAPI = {
  /**
   * Get list of queries with optional filters
   * @param {Object} params - Filter parameters
   * @param {string} params.status - Filter by status (OPEN, IN_PROGRESS, RESOLVED)
   * @param {string} params.category - Filter by category
   * @param {string} params.priority - Filter by priority
   * @param {number} params.limit - Max results (default: 50)
   * @param {number} params.offset - Skip results (default: 0)
   * @returns {Promise} List of queries
   */
  async getQueries(params = {}) {
    const response = await api.get('/queries/', { params })
    return response.data
  },

  /**
   * Get specific query with all responses
   * @param {number} queryId - Query ID
   * @returns {Promise} Query details with responses
   */
  async getQuery(queryId) {
    const response = await api.get(`/queries/${queryId}`)
    return response.data
  },

  /**
   * Create a new query
   * @param {Object} data - Query data
   * @param {string} data.title - Query title (5-200 chars)
   * @param {string} data.description - Query description (min 10 chars)
   * @param {string} data.category - Query category
   * @param {string} data.priority - Priority (LOW, MEDIUM, HIGH, URGENT)
   * @param {Array<string>} data.tags - Optional tags
   * @returns {Promise} Created query
   */
  async createQuery(data) {
    const response = await api.post('/queries/', data)
    return response.data
  },

  /**
   * Add a response to a query
   * @param {number} queryId - Query ID
   * @param {Object} data - Response data
   * @param {string} data.content - Response content
   * @param {boolean} data.is_solution - Whether this is the solution
   * @returns {Promise} Created response
   */
  async addResponse(queryId, data) {
    const response = await api.post(`/queries/${queryId}/response`, data)
    return response.data
  },

  /**
   * Update query status (TA/Instructor/Admin only)
   * @param {number} queryId - Query ID
   * @param {Object} data - Status update data
   * @param {string} data.status - New status (OPEN, IN_PROGRESS, RESOLVED)
   * @param {string} data.resolution_notes - Optional resolution notes
   * @returns {Promise} Updated query
   */
  async updateStatus(queryId, data) {
    const response = await api.put(`/queries/${queryId}/status`, data)
    return response.data
  },

  /**
   * Get query statistics
   * @returns {Promise} Query statistics
   */
  async getStatistics() {
    const response = await api.get('/queries/statistics/summary')
    return response.data
  },

  /**
   * Get queries by status (convenience method)
   * @param {string} status - Status filter (OPEN, IN_PROGRESS, RESOLVED)
   * @param {number} limit - Max results
   * @returns {Promise} Filtered queries
   */
  async getQueriesByStatus(status, limit = 50) {
    return this.getQueries({ status, limit })
  },

  /**
   * Get open queries (convenience method)
   * @param {number} limit - Max results
   * @returns {Promise} Open queries
   */
  async getOpenQueries(limit = 50) {
    return this.getQueriesByStatus('OPEN', limit)
  },

  /**
   * Get resolved queries (convenience method)
   * @param {number} limit - Max results
   * @returns {Promise} Resolved queries
   */
  async getResolvedQueries(limit = 50) {
    return this.getQueriesByStatus('RESOLVED', limit)
  },

  /**
   * Get in-progress queries (convenience method)
   * @param {number} limit - Max results
   * @returns {Promise} In-progress queries
   */
  async getInProgressQueries(limit = 50) {
    return this.getQueriesByStatus('IN_PROGRESS', limit)
  }
}

export default queriesAPI
