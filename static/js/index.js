window.addEventListener('scroll', function () {
  var navbar = document.querySelector('.navbar');
  if (window.scrollY > 50) {
    navbar.classList.add('scrolled', 'dark');
    navbar.classList.remove('light');
  } else {
    navbar.classList.remove('scrolled', 'dark');
    navbar.classList.add('light');
  }
});

function animateCounter(element) {
  var target = parseFloat(element.getAttribute('data-target'));
  var suffix = element.getAttribute('data-suffix') || '';
  var duration = 2000;
  var increment = target / (duration / 16);
  var current = 0;

  var timer = setInterval(function () {
    current += increment;
    if (current >= target) {
      current = target;
      clearInterval(timer);
    }
    if (suffix === 'M') {
      element.textContent = current.toFixed(1) + suffix;
    } else {
      element.textContent = Math.floor(current).toLocaleString() + suffix;
    }
  }, 16);
}

var observerOptions = {
  threshold: 0.3,
  rootMargin: '0px 0px -50px 0px',
};

var observer = new IntersectionObserver(function (entries) {
  entries.forEach(function (entry) {
    if (entry.isIntersecting) {
      var aboutContent = entry.target.closest('.about-section').querySelector('.about-content');
      var statsGrid = entry.target.closest('.about-section').querySelector('.stats-grid');
      aboutContent.classList.add('animate');
      statsGrid.classList.add('animate');

      var counters = entry.target.querySelectorAll('.stat-number');
      setTimeout(function () {
        counters.forEach(function (counter) { animateCounter(counter); });
      }, 400);

      observer.unobserve(entry.target);
    }
  });
}, observerOptions);

document.addEventListener('DOMContentLoaded', function () {
  var statsSection = document.querySelector('.stats-grid');
  if (statsSection) {
    observer.observe(statsSection);
  }
});

var currentSlide = 0;
var slides = document.querySelectorAll('.slide');
var navDots = document.querySelectorAll('.nav-dot');
var totalSlides = slides.length;

function showSlide(index) {
  slides.forEach(function (slide) { slide.classList.remove('active', 'prev'); });
  navDots.forEach(function (dot) { dot.classList.remove('active'); });

  slides[index].classList.add('active');
  navDots[index].classList.add('active');

  var prevIndex = currentSlide;
  if (prevIndex !== index) {
    slides[prevIndex].classList.add('prev');
  }
  currentSlide = index;
}

function nextSlide() {
  var next = (currentSlide + 1) % totalSlides;
  showSlide(next);
}

var slideInterval = setInterval(nextSlide, 5000);

navDots.forEach(function (dot, index) {
  dot.addEventListener('click', function () {
    clearInterval(slideInterval);
    showSlide(index);
    slideInterval = setInterval(nextSlide, 5000);
  });
});

var slideshowContainer = document.querySelector('.slideshow-container');
if (slideshowContainer) {
  slideshowContainer.addEventListener('mouseenter', function () {
    clearInterval(slideInterval);
  });
  slideshowContainer.addEventListener('mouseleave', function () {
    slideInterval = setInterval(nextSlide, 5000);
  });
}

document.addEventListener('DOMContentLoaded', function () {
  if (slides.length > 0) {
    showSlide(0);
  }
});
