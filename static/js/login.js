window.setTimeout(function () {
  const flashes = document.querySelectorAll('.flash-message');
  flashes.forEach(function (flash) {
    flash.style.transition = 'opacity 0.5s ease-out';
    flash.style.opacity = '0';
    setTimeout(function () {
      flash.remove();
    }, 500);
  });
}, 4000);
