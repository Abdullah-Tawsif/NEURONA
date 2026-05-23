
  window.addEventListener('scroll', () => {
  const navbar = document.querySelector('.navbar');
  const logo = document.querySelector('.navbar-logo');

  if (window.scrollY > 50) {
    navbar.classList.add('scrolled', 'dark');
    navbar.classList.remove('light');
  } else {
    navbar.classList.remove('scrolled', 'dark');
    navbar.classList.add('light');
  }
});


    // Animated counter
    function animateCounter(element) {
      const target = parseFloat(element.getAttribute('data-target'));
      const suffix = element.getAttribute('data-suffix') || '';
      const duration = 2000;
      const increment = target / (duration / 16);
      let current = 0;

      const timer = setInterval(() => {
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

    const observerOptions = {
      threshold: 0.3,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const aboutContent = entry.target.closest('.about-section').querySelector('.about-content');
          const statsGrid = entry.target.closest('.about-section').querySelector('.stats-grid');

          aboutContent.classList.add('animate');
          statsGrid.classList.add('animate');

          const counters = entry.target.querySelectorAll('.stat-number');
          setTimeout(() => {
            counters.forEach(counter => animateCounter(counter));
          }, 400);

          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    document.addEventListener('DOMContentLoaded', () => {
      const statsSection = document.querySelector('.stats-grid');
      if (statsSection) {
        observer.observe(statsSection);
      }
    });

    // Slideshow functionality
    let currentSlide = 0;
    const slides = document.querySelectorAll('.slide');
    const navDots = document.querySelectorAll('.nav-dot');
    const totalSlides = slides.length;

    function showSlide(index) {
      // Remove active class from all slides and dots
      slides.forEach(slide => {
        slide.classList.remove('active', 'prev');
      });
      navDots.forEach(dot => dot.classList.remove('active'));

      // Add active class to current slide and dot
      slides[index].classList.add('active');
      navDots[index].classList.add('active');

      // Add prev class to previous slide for animation
      const prevIndex = currentSlide;
      if (prevIndex !== index) {
        slides[prevIndex].classList.add('prev');
      }

      currentSlide = index;
    }

    function nextSlide() {
      const next = (currentSlide + 1) % totalSlides;
      showSlide(next);
    }

    // Auto-advance slideshow
    let slideInterval = setInterval(nextSlide, 5000);

    // Navigation dot click handlers
    navDots.forEach((dot, index) => {
      dot.addEventListener('click', () => {
        clearInterval(slideInterval);
        showSlide(index);
        slideInterval = setInterval(nextSlide, 5000);
      });
    });

    // Pause slideshow on hover
    const slideshowContainer = document.querySelector('.slideshow-container');
    if (slideshowContainer) {
      slideshowContainer.addEventListener('mouseenter', () => {
        clearInterval(slideInterval);
      });

      slideshowContainer.addEventListener('mouseleave', () => {
        slideInterval = setInterval(nextSlide, 5000);
      });
    }

    // Initialize slideshow
    document.addEventListener('DOMContentLoaded', () => {
      if (slides.length > 0) {
        showSlide(0);
      }
    });
