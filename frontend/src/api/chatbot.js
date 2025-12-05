/**
 * Chatbot API service
 * Handles all chatbot-related API calls
 */

import api from './axios'

/**
 * Send a message to the chatbot
 * @param {Object} params - Chat parameters
 * @param {string} params.message - User message
 * @param {string} params.mode - Chat mode (academic, doubt_clarification, study_help, general)
 * @param {string} params.conversation_id - Optional conversation ID
 * @returns {Promise} - API response with chatbot reply
 */
export const sendChatMessage = async ({ message, mode = 'academic', conversation_id = null }) => {
  try {
    const response = await api.post('/chatbot/chat', {
      message,
      mode,
      conversation_id
    })
    return response.data
  } catch (error) {
    console.error('Chat API error:', error)
    throw error
  }
}

/**
 * Get chatbot status
 * @returns {Promise} - Chatbot configuration status
 */
export const getChatbotStatus = async () => {
  try {
    const response = await api.get('/chatbot/status')
    return response.data
  } catch (error) {
    console.error('Chatbot status error:', error)
    throw error
  }
}

/**
 * Get conversation history
 * @param {string} conversationId - Conversation ID
 * @returns {Promise} - Conversation history
 */
export const getConversationHistory = async (conversationId) => {
  try {
    const response = await api.get(`/chatbot/conversation/${conversationId}/history`)
    return response.data
  } catch (error) {
    console.error('Get history error:', error)
    throw error
  }
}

/**
 * Clear conversation history
 * @param {string} conversationId - Conversation ID
 * @returns {Promise} - Success message
 */
export const clearConversation = async (conversationId) => {
  try {
    const response = await api.delete(`/chatbot/conversation/${conversationId}`)
    return response.data
  } catch (error) {
    console.error('Clear conversation error:', error)
    throw error
  }
}

/**
 * Send enhanced chat message with knowledge base integration
 * @param {Object} params - Chat parameters
 * @param {string} params.message - User message
 * @param {string} params.conversation_id - Optional conversation ID
 * @param {string} params.mode - Chat mode (default: academic)
 * @param {boolean} params.use_knowledge_base - Whether to use knowledge base (default: true)
 * @returns {Promise} - Enhanced chat response with sources
 */
export const sendEnhancedChatMessage = async ({
  message,
  conversation_id = null,
  mode = 'academic',
  use_knowledge_base = true
}) => {
  try {
    const response = await api.post('/chatbot/chat/enhanced', {
      message,
      conversation_id,
      mode,
      use_knowledge_base
    })
    return response.data
  } catch (error) {
    console.error('Enhanced chat API error:', error)
    throw error
  }
}

/**
 * Search knowledge base directly
 * @param {Object} params - Search parameters
 * @param {string} params.query - Search query
 * @param {string} params.category - Optional category filter
 * @param {number} params.limit - Maximum results (default: 5)
 * @returns {Promise} - Knowledge base search results
 */
export const searchKnowledge = async ({ query, category = null, limit = 5 }) => {
  try {
    const params = { query, limit }
    if (category) params.category = category

    const response = await api.get('/chatbot/search-knowledge', { params })
    return response.data
  } catch (error) {
    console.error('Knowledge search error:', error)
    throw error
  }
}

/**
 * Answer a specific query using AI and knowledge base
 * @param {number} queryId - Query ID to answer
 * @returns {Promise} - AI-generated answer with sources
 */
export const answerQuery = async (queryId) => {
  try {
    const response = await api.post(`/chatbot/answer-query/${queryId}`)
    return response.data
  } catch (error) {
    console.error('Answer query error:', error)
    throw error
  }
}

/**
 * Get user context for chatbot personalization
 * @returns {Promise} - User context data
 */
export const getUserContext = async () => {
  try {
    const response = await api.get('/chatbot/user-context')
    return response.data
  } catch (error) {
    console.error('Get user context error:', error)
    throw error
  }
}

/**
 * Get chatbot metrics (observability data)
 * @returns {Promise} - Chatbot metrics
 */
export const getChatbotMetrics = async () => {
  try {
    const response = await api.get('/chatbot/metrics')
    return response.data
  } catch (error) {
    console.error('Get metrics error:', error)
    throw error
  }
}

/**
 * Get conversation session state
 * @param {string} conversationId - Conversation ID
 * @returns {Promise} - Session state
 */
export const getConversationState = async (conversationId) => {
  try {
    const response = await api.get(`/chatbot/conversation/${conversationId}/state`)
    return response.data
  } catch (error) {
    console.error('Get conversation state error:', error)
    throw error
  }
}

export default {
  sendChatMessage,
  getChatbotStatus,
  getConversationHistory,
  clearConversation,
  // Enhanced endpoints
  sendEnhancedChatMessage,
  searchKnowledge,
  answerQuery,
  getUserContext,
  getChatbotMetrics,
  getConversationState
}
