// ========================
// UI UTILITIES
// ========================

const UI = {
  // Show alert message
  showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alert-container');
    if (!alertContainer) {
      console.log(`Alert: ${message}`);
      return;
    }

    const alert = document.createElement('div');
    alert.className = `alert alert-${type} fade-in`;
    alert.textContent = message;

    alertContainer.appendChild(alert);

    // Auto remove after 5 seconds
    setTimeout(() => {
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 300);
    }, 5000);
  },

  // Show loading spinner
  showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;

    element.innerHTML = '<div class="spinner"></div><p class="text-center">Processing...</p>';
  },

  // Hide loading spinner
  hideLoading(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;

    element.innerHTML = '';
  },

  // Toggle mobile menu
  toggleMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    if (navMenu) {
      navMenu.classList.toggle('active');
    }
  },

  // Close mobile menu
  closeMobileMenu() {
    const navMenu = document.querySelector('.nav-menu');
    if (navMenu) {
      navMenu.classList.remove('active');
    }
  },

  // Set active navigation link
  setActiveNav() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === currentPage) {
        link.classList.add('active');
      }
    });
  },

  // Smooth scroll to element
  smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  },

  // Animate elements on scroll
  animateOnScroll() {
    const elements = document.querySelectorAll('.fade-in-up, .fade-in-left, .fade-in-right');

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0) translateX(0)';
        }
      });
    }, { threshold: 0.1 });

    elements.forEach(el => {
      el.style.opacity = '0';
      observer.observe(el);
    });
  },

  // Format date
  formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  },

  // Copy text to clipboard
  copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
      this.showAlert('Copied to clipboard!', 'success');
    }).catch(() => {
      this.showAlert('Failed to copy', 'error');
    });
  },

  // Initialize tooltips
  initTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');

    tooltips.forEach(element => {
      element.addEventListener('mouseenter', function() {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = this.getAttribute('data-tooltip');
        document.body.appendChild(tooltip);

        const rect = this.getBoundingClientRect();
        tooltip.style.top = `${rect.top - tooltip.offsetHeight - 10}px`;
        tooltip.style.left = `${rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2)}px`;
      });

      element.addEventListener('mouseleave', function() {
        const tooltip = document.querySelector('.tooltip');
        if (tooltip) tooltip.remove();
      });
    });
  }
};

// Initialize UI on page load
document.addEventListener('DOMContentLoaded', () => {
  UI.setActiveNav();
  UI.animateOnScroll();

  // Mobile menu toggle
  const navToggle = document.querySelector('.nav-toggle');
  if (navToggle) {
    navToggle.addEventListener('click', () => UI.toggleMobileMenu());
  }

  // Close mobile menu when clicking nav links
  const navLinks = document.querySelectorAll('.nav-link');
  navLinks.forEach(link => {
    link.addEventListener('click', () => UI.closeMobileMenu());
  });
});

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = UI;
}
