// Auto-hide flash messages
  window.setTimeout(function() {

    const flashes = document.querySelectorAll('.flash-message');

    flashes.forEach(flash => {

      flash.style.transition = 'opacity 0.5s ease-out';
      flash.style.opacity = '0';

      setTimeout(() => {
        flash.remove();
      }, 500);

    });

  }, 4000);


src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"