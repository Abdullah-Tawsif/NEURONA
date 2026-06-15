setTimeout(function () {
  var alerts = document.querySelectorAll('.custom-alert');
  alerts.forEach(function (alert) {
    alert.classList.remove('show');
    alert.classList.add('fade');
  });
}, 4000);

document.querySelector('.profile-dropdown').addEventListener('click', function () {
  this.classList.toggle('active');
});

document.addEventListener('click', function (e) {
  if (!e.target.closest('.profile-dropdown')) {
    document.querySelector('.profile-dropdown').classList.remove('active');
  }
});

document.querySelectorAll('.view-toggle').forEach(function (btn) {
  btn.addEventListener('click', function () {
    document.querySelectorAll('.view-toggle').forEach(function (b) { b.classList.remove('active'); });
    this.classList.add('active');
    var view = this.dataset.view;
    var grid = document.getElementById('opportunitiesGrid');
    if (view === 'list') {
      grid.classList.add('list-view');
    } else {
      grid.classList.remove('list-view');
    }
  });
});

document.querySelectorAll('.filter-btn').forEach(function (btn) {
  btn.addEventListener('click', function () {
    document.querySelectorAll('.filter-btn').forEach(function (b) { b.classList.remove('active'); });
    this.classList.add('active');
  });
});

document.querySelectorAll('.bookmark-btn').forEach(function (btn) {
  btn.addEventListener('click', function (e) {
    e.stopPropagation();
    var icon = this.querySelector('i');
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

function applyFilters() {
  var category = document.getElementById('categoryFilter').value;
  var stage = document.getElementById('stageFilter').value;
  var search = document.querySelector('input[name="search"]').value;
  var url = new URL(window.location.href);
  url.searchParams.set('category', category);
  url.searchParams.set('stage', stage);
  url.searchParams.set('search', search);
  window.location.href = url.toString();
}

var searchContainer = document.querySelector('.search-container form');
if (searchContainer) {
  searchContainer.addEventListener('submit', function (e) {
    e.preventDefault();
    applyFilters();
  });
}

document.querySelector('.search-input').addEventListener('focus', function () {
  this.parentElement.classList.add('focused');
});

document.querySelector('.search-input').addEventListener('blur', function () {
  this.parentElement.classList.remove('focused');
});

document.querySelector('.search-input').addEventListener('keypress', function (e) {
  if (e.key === 'Enter') {
    e.preventDefault();
    applyFilters();
  }
});

document.addEventListener('DOMContentLoaded', function () {
  var progressBars = document.querySelectorAll('.progress-fill');
  progressBars.forEach(function (bar) {
    var progress = bar.getAttribute('data-progress');
    bar.style.width = progress + '%';
  });
});
