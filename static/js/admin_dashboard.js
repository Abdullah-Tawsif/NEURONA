src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"

    document.getElementById('sidebarCollapse').addEventListener('click', function () {
      document.getElementById('sidebar').classList.toggle('active');
      document.getElementById('content').classList.toggle('active');
    });

    // Add smooth transitions and interactions
    document.addEventListener('DOMContentLoaded', function() {
      // Animate stats cards on load
      const statsCards = document.querySelectorAll('.stats-card');
      statsCards.forEach((card, index) => {
        setTimeout(() => {
          card.style.opacity = '1';
          card.style.transform = 'translateY(0)';
        }, index * 100);
      });
    });
