// Flash Messages Auto-dismiss
document.addEventListener('DOMContentLoaded', function() {
  const flashMessages = document.querySelectorAll('.flash-message');
  
  flashMessages.forEach(function(message) {
    // Auto-dismiss after 5 seconds
    setTimeout(function() {
      dismissFlash(message);
    }, 5000);
  });
});

function dismissFlash(element) {
  element.style.opacity = '0';
  element.style.transform = 'translateX(100%)';
  setTimeout(function() {
    element.remove();
  }, 300);
}

// Manual dismiss handler
document.addEventListener('click', function(e) {
  if (e.target.closest('.flash-dismiss')) {
    const flashMessage = e.target.closest('.flash-message');
    if (flashMessage) {
      dismissFlash(flashMessage);
    }
  }
});
