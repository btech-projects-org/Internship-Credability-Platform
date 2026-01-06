// ========================
// NAVIGATION UTILITIES
// ========================

const Navigation = {
  // Navigate to page with data
  navigateWithData(page, data) {
    if (data) {
      Storage.save('temp_navigation_data', data);
    }
    window.location.href = page;
  },

  // Get navigation data
  getNavigationData() {
    const data = Storage.get('temp_navigation_data');
    Storage.remove('temp_navigation_data');
    return data;
  },

  // Go to check page
  goToCheck() {
    window.location.href = 'check.html';
  },

  // Go to analysis page with data
  goToAnalysis(formData) {
    Storage.saveInternshipData(formData);
    window.location.href = 'analysis.html';
  },

  // Go to result page with analysis
  goToResults(analysisResults) {
    Storage.saveAnalysisResults(analysisResults);
    window.location.href = 'result.html';
  },

  // Go back to previous page
  goBack() {
    window.history.back();
  },

  // Go to home page
  goHome() {
    window.location.href = 'index.html';
  },

  // Confirm navigation if unsaved changes
  confirmNavigation(message = 'You have unsaved changes. Are you sure you want to leave?') {
    return confirm(message);
  }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Navigation;
}
