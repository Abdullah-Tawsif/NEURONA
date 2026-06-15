document.getElementById('sidebarCollapse').addEventListener('click', function () {
  document.getElementById('sidebar').classList.toggle('active');
  document.getElementById('content').classList.toggle('active');
});

document.addEventListener('DOMContentLoaded', function () {
  const statsCards = document.querySelectorAll('.stats-card');
  statsCards.forEach(function (card, index) {
    setTimeout(function () {
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, index * 100);
  });
});
