document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.dot');
    const prevBtn = document.querySelector('.prev');
    const nextBtn = document.querySelector('.next');
    
    if (slides.length === 0) return; // Exit if no slider

    let currentSlide = 0;
    const slideInterval = 7000; // 7 seconds
    let slideTimer;

    // Function to show a specific slide
    function showSlide(n) {
        // Reset all slides and dots
        slides.forEach(slide => slide.classList.remove('active'));
        dots.forEach(dot => dot.classList.remove('active'));

        // Handle wrapping
        if (n >= slides.length) currentSlide = 0;
        else if (n < 0) currentSlide = slides.length - 1;
        else currentSlide = n;

        // Activate new slide and dot
        slides[currentSlide].classList.add('active');
        if (dots[currentSlide]) {
            dots[currentSlide].classList.add('active');
        }
    }

    // Next Slide
    function nextSlide() {
        showSlide(currentSlide + 1);
    }

    // Previous Slide
    function prevSlide() {
        showSlide(currentSlide - 1);
    }

    // Start Auto Play
    function startSlideShow() {
        slideTimer = setInterval(nextSlide, slideInterval);
    }

    // Stop Auto Play (on interaction)
    function stopSlideShow() {
        clearInterval(slideTimer);
    }

    // Event Listeners
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            stopSlideShow();
            prevSlide();
            startSlideShow();
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            stopSlideShow();
            nextSlide();
            startSlideShow();
        });
    }

    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            stopSlideShow();
            showSlide(index);
            startSlideShow();
        });
    });

    // Initialize
    showSlide(0);
    startSlideShow();
});
