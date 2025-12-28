// ========================
// CONFIG: API Keys and Settings
// ========================

// API Configuration
const CONFIG = {
  API_BASE_URL: 'http://localhost:5000/api',
  HF_API_KEY: ''
};

// Provide your Hugging Face API key here. Keep private when deploying.
// Example: CONFIG.HF_API_KEY = 'hf_XXXXXXXXXXXXXXXXXXXXXXXX';
window.HF_API_KEY = CONFIG.HF_API_KEY;
window.CONFIG = CONFIG;
