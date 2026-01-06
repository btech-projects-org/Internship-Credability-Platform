// ========================
// LOCAL STORAGE UTILITIES
// ========================

const Storage = {
  // Save data to localStorage
  save(key, data) {
    try {
      const jsonData = JSON.stringify(data);
      localStorage.setItem(key, jsonData);
      return true;
    } catch (error) {
      console.error('Error saving to localStorage:', error);
      return false;
    }
  },

  // Get data from localStorage
  get(key) {
    try {
      const jsonData = localStorage.getItem(key);
      return jsonData ? JSON.parse(jsonData) : null;
    } catch (error) {
      console.error('Error reading from localStorage:', error);
      return null;
    }
  },

  // Remove item from localStorage
  remove(key) {
    try {
      localStorage.removeItem(key);
      return true;
    } catch (error) {
      console.error('Error removing from localStorage:', error);
      return false;
    }
  },

  // Clear all localStorage
  clear() {
    try {
      localStorage.clear();
      return true;
    } catch (error) {
      console.error('Error clearing localStorage:', error);
      return false;
    }
  },

  // Check if key exists
  exists(key) {
    return localStorage.getItem(key) !== null;
  },

  // Get all keys
  getAllKeys() {
    return Object.keys(localStorage);
  },

  // Save internship data
  saveInternshipData(data) {
    return this.save('internship_data', data);
  },

  // Get internship data
  getInternshipData() {
    return this.get('internship_data');
  },

  // Save analysis results
  saveAnalysisResults(results) {
    return this.save('analysis_results', results);
  },

  // Get analysis results
  getAnalysisResults() {
    return this.get('analysis_results');
  },

  // Save user preferences
  savePreferences(preferences) {
    return this.save('user_preferences', preferences);
  },

  // Get user preferences
  getPreferences() {
    return this.get('user_preferences') || {
      theme: 'light',
      notifications: true
    };
  },

  // Save Hugging Face API key
  saveApiKey(key) {
    try {
      localStorage.setItem('hf_api_key', key);
      return true;
    } catch (error) {
      console.error('Error saving API key:', error);
      return false;
    }
  },

  // Get Hugging Face API key
  getApiKey() {
    try {
      return localStorage.getItem('hf_api_key') || '';
    } catch (error) {
      console.error('Error reading API key:', error);
      return '';
    }
  }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Storage;
}
