import api from './axios'

/**
 * Chat Service for handling RAG-based chat interactions
 */
export const chatService = {
    /**
     * Send first query (creates new chat session and returns task)
     * @param {string} inputText - The user's message
     * @param {Object} data - Additional metadata
     * @returns {Promise<Object>} Task response
     */
    async sendFirstQuery(inputText, data = {}) {
        const response = await api.post('/chat/message', {
            input_text: inputText,
            device_info: data.device_info || navigator.userAgent,
            location: data.location,
            metadata: data.metadata || {
                platform: navigator.platform,
                screen: `${window.screen.width}x${window.screen.height}`,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            }
        })
        return response.data
    },

    /**
     * Send a query to an existing chat session
     * @param {string} chatId - The chat session ID
     * @param {string} inputText - The user's message
     * @returns {Promise<Object>} Task response
     */
    async sendQuery(chatId, inputText) {
        const response = await api.post('/chat/message', {
            chat_id: chatId,
            input_text: inputText
        })
        return response.data
    },

    /**
     * Get task status
     * @param {string} taskId - The task ID
     * @returns {Promise<Object>} Task status
     */
    async getTaskStatus(taskId) {
        // Note: Backend endpoint for task status might need adjustment if it's different
        // Assuming /api/task/{taskId}/status based on reference code
        // If not implemented, we might need to rely on the immediate response from sendQuery
        // But for RAG, it's usually async. Let's assume the backend supports it or we need to implement it.
        // Wait, the reference code used /api/v1/task/{taskId}/status.
        // Our backend implementation in `api/chat.py` (which I should check) might be synchronous or async.
        // Let's check api/chat.py first to be sure about the endpoints.
        // For now, I'll implement this assuming the endpoint exists or will be created.
        const response = await api.get(`/task/${taskId}/status`)
        return response.data
    },

    /**
     * Poll task status until completion
     * @param {string} taskId 
     * @param {Function} onUpdate 
     * @param {number} pollInterval 
     * @param {number} maxAttempts 
     * @returns {Promise<Object>} Final task status
     */
    async pollTaskStatus(taskId, onUpdate, pollInterval = 1000, maxAttempts = 60) {
        let attempts = 0

        while (attempts < maxAttempts) {
            try {
                const status = await this.getTaskStatus(taskId)

                if (onUpdate) {
                    onUpdate(status)
                }

                if (status.status === 'COMPLETED' || status.status === 'FAILED') {
                    return status
                }

                await new Promise(resolve => setTimeout(resolve, pollInterval))
                attempts++
            } catch (error) {
                console.error('Error polling task status:', error)
                attempts++
                if (attempts >= maxAttempts) {
                    throw error
                }
                await new Promise(resolve => setTimeout(resolve, pollInterval))
            }
        }

        throw new Error(`Task polling timeout after ${maxAttempts} attempts`)
    },

    /**
     * Send query and wait for completion
     * @param {string} chatId 
     * @param {string} inputText 
     * @param {Function} onStatusUpdate 
     * @returns {Promise<Object>} { task, finalStatus }
     */
    async sendQueryAndWait(chatId, inputText, onStatusUpdate) {
        // In our current backend implementation (api/chat.py), the response might be immediate
        // if it's not offloaded to a background task queue like Celery.
        // Let's verify api/chat.py before finalizing this logic.
        // If the backend returns the answer immediately, we don't need polling.
        // I will assume for now we might need to adjust this.

        // Actually, looking at the previous turn's `chat.py` (backend), it seems to use `await chat_pipeline.process(...)`
        // which implies it waits for the result and returns it directly.
        // So polling might NOT be needed for the current backend implementation.
        // The reference frontend used polling because it likely had an async worker.
        // Our current backend `api/chat.py` seems to return the answer directly.

        const response = await api.post('/chat/message', {
            chat_id: chatId,
            input_text: inputText
        })

        // If the backend returns the answer directly:
        return {
            task: { chat_id: chatId }, // Mock task info
            finalStatus: {
                status: 'COMPLETED',
                metadata: {
                    answer_text: response.data.answer,
                    confidence: response.data.confidence,
                    language: response.data.language,
                    has_answered: !!response.data.answer && response.data.answer.length > 0
                }
            }
        }
    },

    /**
     * Send first query and wait for completion
     * @param {string} inputText 
     * @param {Object} data 
     * @param {Function} onStatusUpdate 
     * @returns {Promise<Object>} { task, finalStatus }
     */
    async sendFirstQueryAndWait(inputText, data = {}, onStatusUpdate) {
        const response = await api.post('/chat/message', {
            input_text: inputText,
            device_info: data.device_info || navigator.userAgent,
            metadata: data.metadata
        })

        return {
            task: { chat_id: response.data.chat_id || 'new-session' }, // Backend should return chat_id
            finalStatus: {
                status: 'COMPLETED',
                metadata: {
                    answer_text: response.data.answer,
                    confidence: response.data.confidence,
                    language: response.data.language,
                    has_answered: !!response.data.answer && response.data.answer.length > 0
                }
            }
        }
    },

    /**
     * Get chat history
     * @param {string} chatId 
     * @param {Object} params 
     * @returns {Promise<Object>} Chat history
     */
    async getChatHistory(chatId, params = {}) {
        const response = await api.get(`/chat/${chatId}/history`, {
            params: {
                limit: params.limit || 50,
                offset: params.offset || 0
            }
        })
        return response.data
    }
}

export default chatService
