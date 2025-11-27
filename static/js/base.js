document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const closeMenuBtn = document.getElementById('close-menu-btn');
    const overlay = document.getElementById('mobile-menu-overlay');

    // Dropdown "Más"
    const moreMenuBtn = document.getElementById('more-menu-btn');
    const moreMenuContent = document.getElementById('more-menu-content');

    function toggleMenu() {
        const isClosed = mobileMenu.classList.contains('translate-x-full');
        if (isClosed) {
            mobileMenu.classList.remove('translate-x-full');
            overlay.classList.remove('hidden');
            setTimeout(() => overlay.classList.remove('opacity-0'), 10); // Fade in
        } else {
            mobileMenu.classList.add('translate-x-full');
            overlay.classList.add('opacity-0');
            setTimeout(() => overlay.classList.add('hidden'), 300); // Wait for fade out
        }
    }

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', toggleMenu);
    }

    if (closeMenuBtn) {
        closeMenuBtn.addEventListener('click', toggleMenu);
    }

    if (overlay) {
        overlay.addEventListener('click', toggleMenu);
    }

    // Toggle Dropdown "Más"
    if (moreMenuBtn && moreMenuContent) {
        moreMenuBtn.addEventListener('click', function(e) {
            e.stopPropagation(); // Prevent event bubbling
            moreMenuContent.classList.toggle('hidden');
            // Close user menu if open
            if (userMenuContent && !userMenuContent.classList.contains('hidden')) {
                userMenuContent.classList.add('hidden');
            }
        });
    }

    // User Menu Dropdown
    const userMenuBtn = document.getElementById('user-menu-btn');
    const userMenuContent = document.getElementById('user-menu-content');

    if (userMenuBtn && userMenuContent) {
        userMenuBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            userMenuContent.classList.toggle('hidden');
            // Close more menu if open
            if (moreMenuContent && !moreMenuContent.classList.contains('hidden')) {
                moreMenuContent.classList.add('hidden');
            }
        });
    }

    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (moreMenuBtn && moreMenuContent && !moreMenuBtn.contains(e.target) && !moreMenuContent.contains(e.target)) {
            moreMenuContent.classList.add('hidden');
        }
        if (userMenuBtn && userMenuContent && !userMenuBtn.contains(e.target) && !userMenuContent.contains(e.target)) {
            userMenuContent.classList.add('hidden');
        }
    });

    // Close menu when resizing to desktop
    window.addEventListener('resize', () => {
        if (window.innerWidth >= 1024) { // lg breakpoint
            if (!mobileMenu.classList.contains('translate-x-full')) {
                toggleMenu();
            }
        }
    });
});
