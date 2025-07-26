// frontend/src/services/ChatService.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

class ChatService {
  /**
   * Get API status and information
   */
  static async getApiStatus() {
    try {
      const response = await api.get('/chat/');
      return response.data;
    } catch (error) {
      console.error('API Status Error:', error);
      throw new Error('Failed to connect to chatbot API');
    }
  }

  /**
   * Send message to chatbot
   */
  static async sendMessage(question, sessionId = null) {
    try {
      const payload = {
        question: question.trim(),
        session_id: sessionId
      };

      console.log('Sending message:', payload);
      
      const response = await api.post('/chat/', payload);
      
      console.log('Received response:', response.data);
      
      return response.data;
    } catch (error) {
      console.error('Send Message Error:', error);
      
      if (error.response) {
        // Server responded with error status
        const errorMessage = error.response.data?.error || 'Server error occurred';
        throw new Error(`Server Error (${error.response.status}): ${errorMessage}`);
      } else if (error.request) {
        // Request made but no response
        throw new Error('No response from server. Please check if the backend is running.');
      } else {
        // Something else happened
        throw new Error(`Request Error: ${error.message}`);
      }
    }
  }

  /**
   * Test similarity search (for debugging)
   */
  static async testSimilarity(query, k = 4) {
    try {
      const response = await api.post('/test-similarity/', {
        query: query,
        k: k
      });
      return response.data;
    } catch (error) {
      console.error('Similarity Test Error:', error);
      throw new Error('Failed to test similarity search');
    }
  }
}

export default ChatService;