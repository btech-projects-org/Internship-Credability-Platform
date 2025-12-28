// ========================
// BUTTON CLICK STATE MANAGER
// ========================

document.addEventListener('DOMContentLoaded', function() {
  // Add click listeners to all buttons
  const buttons = document.querySelectorAll('.btn');

  buttons.forEach(btn => {
    btn.addEventListener('click', function(e) {
      // Remove clicked class from all other buttons
      buttons.forEach(b => b.classList.remove('clicked'));
      
      // Add clicked class to this button
      this.classList.add('clicked');
      
      // Keep the button focused to maintain the gray state
      this.focus();
    });
  });

  // Remove clicked class when clicking outside
  document.addEventListener('click', function(e) {
    if (!e.target.closest('.btn')) {
      buttons.forEach(b => b.classList.remove('clicked'));
      // Blur any focused button to remove focus state
      if (document.activeElement && document.activeElement.classList.contains('btn')) {
        document.activeElement.blur();
      }
    }
  });
});
