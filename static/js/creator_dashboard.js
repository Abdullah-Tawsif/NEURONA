src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"

    setTimeout(function() {
      const alert = document.querySelector(".alert");
      if (alert) {
        alert.classList.remove("show");
        alert.classList.add("fade");
      }
    }, 3000);
    
    // Set progress bar widths
    document.addEventListener('DOMContentLoaded', function() {
      const progressBars = document.querySelectorAll('.progress-bar');
      progressBars.forEach(function(bar) {
        const progress = bar.getAttribute('data-progress');
        bar.style.width = progress + '%';
      });
    });
