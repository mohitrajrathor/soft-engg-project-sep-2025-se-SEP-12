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

export default {
  sendChatMessage,
  getChatbotStatus,
  getConversationHistory,
  clearConversation
}
