const API_BASE_URL = 'http://127.0.0.1:8000/api/quize';

class ApiService {
  joinUrl(base, path) {
    const cleanBase = base.replace(/\/+$/, '');
    const cleanPath = path.replace(/^\/+/, '/');
    return `${cleanBase}${cleanPath}`;
  }

  async request(url, options = {}) {
    const fullUrl = this.joinUrl(API_BASE_URL, url);
    const response = await fetch(fullUrl, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP error! status: ${response.status} - ${errorText || response.statusText}`);
    }
    return response.json();
  }

  async fetchCategories() {
    return this.request('/categories/');
  }

  async fetchCategoryData(categoryName) {
    const encoded = encodeURIComponent(categoryName);
    return this.request(`/categories/${encoded}/`);
  }

  // 🚩🚩 ADD THIS FUNCTION 🚩🚩
  async submitQuiz(quizData) {
    return this.request('/quiz/submit/', {
      method: 'POST',
      body: JSON.stringify(quizData),
    });
  }
}

export default new ApiService();