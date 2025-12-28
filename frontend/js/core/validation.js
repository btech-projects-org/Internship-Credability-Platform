// ========================
// FORM VALIDATION UTILITIES
// ========================

const Validation = {
  // Email validation
  isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  },

  // URL validation
  isValidURL(url) {
    try {
      new URL(url);
      return true;
    } catch (error) {
      return false;
    }
  },

  // Phone number validation
  isValidPhone(phone) {
    const phoneRegex = /^[\d\s\-\+\(\)]+$/;
    return phoneRegex.test(phone) && phone.replace(/\D/g, '').length >= 10;
  },

  // Required field validation
  isRequired(value) {
    return value !== null && value !== undefined && value.trim() !== '';
  },

  // Minimum length validation
  minLength(value, min) {
    return value.length >= min;
  },

  // Maximum length validation
  maxLength(value, max) {
    return value.length <= max;
  },

  // Number validation
  isNumber(value) {
    return !isNaN(parseFloat(value)) && isFinite(value);
  },

  // Date validation
  isValidDate(dateString) {
    const date = new Date(dateString);
    return date instanceof Date && !isNaN(date);
  },

  // Show error message
  showError(inputElement, message) {
    inputElement.classList.add('error');
    const errorElement = inputElement.parentElement.querySelector('.form-error');
    if (errorElement) {
      errorElement.textContent = message;
      errorElement.classList.add('active');
    }
  },

  // Clear error message
  clearError(inputElement) {
    inputElement.classList.remove('error');
    const errorElement = inputElement.parentElement.querySelector('.form-error');
    if (errorElement) {
      errorElement.textContent = '';
      errorElement.classList.remove('active');
    }
  },

  // Validate form
  validateForm(formId, rules) {
    const form = document.getElementById(formId);
    if (!form) return false;

    let isValid = true;

    Object.keys(rules).forEach(fieldName => {
      const field = form.querySelector(`[name="${fieldName}"]`);
      if (!field) return;

      const fieldRules = rules[fieldName];
      const value = field.value;

      // Clear previous errors
      this.clearError(field);

      // Check required
      if (fieldRules.required && !this.isRequired(value)) {
        this.showError(field, fieldRules.requiredMessage || 'This field is required');
        isValid = false;
        return;
      }

      // Skip other validations if field is empty and not required
      if (!this.isRequired(value) && !fieldRules.required) {
        return;
      }

      // Check email
      if (fieldRules.email && !this.isValidEmail(value)) {
        this.showError(field, fieldRules.emailMessage || 'Please enter a valid email');
        isValid = false;
        return;
      }

      // Check URL
      if (fieldRules.url && !this.isValidURL(value)) {
        this.showError(field, fieldRules.urlMessage || 'Please enter a valid URL');
        isValid = false;
        return;
      }

      // Check phone
      if (fieldRules.phone && !this.isValidPhone(value)) {
        this.showError(field, fieldRules.phoneMessage || 'Please enter a valid phone number');
        isValid = false;
        return;
      }

      // Check min length
      if (fieldRules.minLength && !this.minLength(value, fieldRules.minLength)) {
        this.showError(field, fieldRules.minLengthMessage || `Minimum ${fieldRules.minLength} characters required`);
        isValid = false;
        return;
      }

      // Check max length
      if (fieldRules.maxLength && !this.maxLength(value, fieldRules.maxLength)) {
        this.showError(field, fieldRules.maxLengthMessage || `Maximum ${fieldRules.maxLength} characters allowed`);
        isValid = false;
        return;
      }

      // Custom validation
      if (fieldRules.custom && !fieldRules.custom(value)) {
        this.showError(field, fieldRules.customMessage || 'Invalid value');
        isValid = false;
        return;
      }
    });

    return isValid;
  }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Validation;
}
