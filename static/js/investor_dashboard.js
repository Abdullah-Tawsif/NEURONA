src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"

  // Auto-hide flash messages
  setTimeout(function() {
    const alerts = document.querySelectorAll(".custom-alert");
    alerts.forEach(alert => {
      alert.classList.remove("show");
      alert.classList.add("fade");
    });
  }, 4000);

  // Profile dropdown toggle
  document.querySelector('.profile-dropdown').addEventListener('click', function() {
    this.classList.toggle('active');
  });

  // Close dropdown when clicking outside
  document.addEventListener('click', function(e) {
    if (!e.target.closest('.profile-dropdown')) {
      document.querySelector('.profile-dropdown').classList.remove('active');
    }
  });

  // View toggle functionality
  document.querySelectorAll('.view-toggle').forEach(btn => {
    btn.addEventListener('click', function() {
      document.querySelectorAll('.view-toggle').forEach(b => b.classList.remove('active'));
      this.classList.add('active');

      const view = this.dataset.view;
      const grid = document.getElementById('opportunitiesGrid');

      if (view === 'list') {
        grid.classList.add('list-view');
      } else {
        grid.classList.remove('list-view');
      }
    });
  });

  // Filter buttons
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
    });
  });

  // Bookmark functionality
  document.querySelectorAll('.bookmark-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      const icon = this.querySelector('i');
      if (icon.classList.contains('far')) {
        icon.classList.remove('far');
        icon.classList.add('fas');
        this.classList.add('bookmarked');
      } else {
        icon.classList.remove('fas');
        icon.classList.add('far');
        this.classList.remove('bookmarked');
      }
    });
  });

  // Filter functionality
  function applyFilters() {
    const category = document.getElementById('categoryFilter').value;
    const stage = document.getElementById('stageFilter').value;
    const search = document.querySelector('input[name="search"]').value;

    const url = new URL(window.location.href);
    url.searchParams.set('category', category);
    url.searchParams.set('stage', stage);
    url.searchParams.set('search', search);

    window.location.href = url.toString();
  }

  // Search form submission
  document.querySelector('.search-container form').addEventListener('submit', function(e) {
    e.preventDefault();
    applyFilters();
  });

  // Search functionality
  document.querySelector('.search-input').addEventListener('focus', function() {
    this.parentElement.classList.add('focused');
  });

  document.querySelector('.search-input').addEventListener('blur', function() {
    this.parentElement.classList.remove('focused');
  });

  // Search on Enter key
  document.querySelector('.search-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      applyFilters();
    }
  });
  
  // Set progress bar widths
  document.addEventListener('DOMContentLoaded', function() {
    const progressBars = document.querySelectorAll('.progress-fill');
    progressBars.forEach(function(bar) {
      const progress = bar.getAttribute('data-progress');
      bar.style.width = progress + '%';
    });
  });
