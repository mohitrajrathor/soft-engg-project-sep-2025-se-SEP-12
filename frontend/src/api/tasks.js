/**
 * Background Tasks API endpoints
 */

import api from './axios'

export const tasksAPI = {
  /**
   * Get all background tasks with optional filtering
   * @param {Object} params - Query parameters
   * @param {string} [params.task_type] - Filter by task type
   * @param {string} [params.status] - Filter by status (pending, in_progress, completed, failed)
   * @param {number} [params.skip] - Pagination offset
   * @param {number} [params.limit] - Pagination limit
   * @returns {Promise} List of tasks
   */
  async getTasks(params = {}) {
    const response = await api.get('/tasks/', { params })
    return response.data
  },

  /**
   * Get a specific task by ID
   * @param {string} id - Task ID
   * @returns {Promise} Task details
   */
  async getTask(id) {
    const response = await api.get(`/tasks/${id}`)
    return response.data
  },

  /**
   * Delete a task
   * @param {string} id - Task ID
   * @returns {Promise} Deletion confirmation
   */
  async deleteTask(id) {
    const response = await api.delete(`/tasks/${id}`)
    return response.data
  },

  /**
   * Get task statistics summary
   * @returns {Promise} Task statistics
   */
  async getStatistics() {
    const response = await api.get('/tasks/statistics/summary')
    return response.data
  },

  /**
   * Get tasks by status
   * @param {string} status - Task status (pending, in_progress, completed, failed)
   * @returns {Promise} List of tasks with given status
   */
  async getTasksByStatus(status) {
    return this.getTasks({ status })
  },

  /**
   * Get completed tasks
   * @returns {Promise} List of completed tasks
   */
  async getCompletedTasks() {
    return this.getTasksByStatus('completed')
  },

  /**
   * Get failed tasks
   * @returns {Promise} List of failed tasks
   */
  async getFailedTasks() {
    return this.getTasksByStatus('failed')
  },

  /**
   * Get tasks in progress
   * @returns {Promise} List of tasks in progress
   */
  async getInProgressTasks() {
    return this.getTasksByStatus('in_progress')
  }
}
