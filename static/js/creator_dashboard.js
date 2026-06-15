setTimeout(function () {
  const alert = document.querySelector('.alert');
  if (alert) {
    alert.classList.remove('show');
    alert.classList.add('fade');
  }
}, 3000);

document.addEventListener('DOMContentLoaded', function () {
  const progressBars = document.querySelectorAll('.progress-bar');
  progressBars.forEach(function (bar) {
    const progress = bar.getAttribute('data-progress');
    bar.style.width = progress + '%';
  });
});
