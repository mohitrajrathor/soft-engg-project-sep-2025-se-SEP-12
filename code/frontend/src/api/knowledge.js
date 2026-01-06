/**
 * Knowledge Base API endpoints
 */

import api from './axios'

export const knowledgeAPI = {
  /**
   * Get all knowledge sources with optional filtering
   * @param {Object} params - Query parameters
   * @param {string} [params.category] - Filter by category
   * @param {string} [params.source_type] - Filter by source type
   * @param {string} [params.search] - Search in title/description/content
   * @param {number} [params.skip] - Pagination offset
   * @param {number} [params.limit] - Pagination limit
   * @returns {Promise} List of knowledge sources
   */
  async getSources(params = {}) {
    const response = await api.get('/knowledge/sources', { params })
    return response.data
  },

  /**
   * Get a specific knowledge source by ID
   * @param {number} id - Source ID
   * @returns {Promise} Knowledge source data
   */
  async getSource(id) {
    const response = await api.get(`/knowledge/sources/${id}`)
    return response.data
  },

  /**
   * Create a new knowledge source
   * @param {Object} data - Knowledge source data
   * @param {string} data.title - Source title
   * @param {string} [data.description] - Source description
   * @param {string} data.content - Source content
   * @param {string} data.category - Category (courses, assignments, quizzes, etc.)
   * @param {string} [data.source_type] - Source type (document, video, quiz, etc.)
   * @param {Object} [data.metadata] - Additional metadata
   * @returns {Promise} Created knowledge source
   */
  async createSource(data) {
    const response = await api.post('/knowledge/sources', data)
    return response.data
  },

  /**
   * Update a knowledge source
   * @param {number} id - Source ID
   * @param {Object} data - Updated data
   * @returns {Promise} Updated knowledge source
   */
  async updateSource(id, data) {
    const response = await api.put(`/knowledge/sources/${id}`, data)
    return response.data
  },

  /**
   * Delete a knowledge source
   * @param {number} id - Source ID
   * @returns {Promise} Deletion confirmation
   */
  async deleteSource(id) {
    const response = await api.delete(`/knowledge/sources/${id}`)
    return response.data
  },

  /**
   * Get text chunks for a knowledge source
   * @param {number} id - Source ID
   * @param {Object} params - Query parameters
   * @param {number} [params.limit] - Maximum number of chunks
   * @returns {Promise} List of text chunks
   */
  async getChunks(id, params = {}) {
    const response = await api.get(`/knowledge/sources/${id}/chunks`, { params })
    return response.data
  },

  /**
   * Search knowledge base using semantic search
   * @param {Object} data - Search parameters
   * @param {string} data.query - Search query
   * @param {number} [data.top_k] - Number of results (default: 5)
   * @param {string} [data.category] - Filter by category
   * @returns {Promise} Search results with relevance scores
   */
  async semanticSearch(data) {
    const response = await api.post('/knowledge/search', data)
    return response.data
  },

  /**
   * Get available knowledge categories
   * @returns {Promise} List of categories
   */
  async getCategories() {
    const response = await api.get('/knowledge/categories')
    return response.data
  },

  /**
   * Get knowledge base statistics
   * @returns {Promise} Statistics data
   */
  async getStats() {
    const response = await api.get('/knowledge/stats')
    return response.data
  }
}
