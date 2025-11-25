document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');

    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (validateForm()) {
                // Simulate form submission
                const submitBtn = this.querySelector('button[type="submit"]');
                const originalText = submitBtn.innerHTML;
                
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="material-symbols-outlined animate-spin mr-2">refresh</span> Enviando...';
                
                // Simulate network request
                setTimeout(() => {
                    alert('¡Mensaje enviado con éxito! Nos pondremos en contacto contigo pronto.');
                    contactForm.reset();
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 1500);
            }
        });
    }

    // Real-time validation
    const inputs = document.querySelectorAll('input, textarea');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            validateField(this);
        });
        
        input.addEventListener('blur', function() {
            validateField(this);
        });
    });
});

function validateForm() {
    let isValid = true;
    const inputs = document.querySelectorAll('#contactForm input, #contactForm textarea');
    
    inputs.forEach(input => {
        if (!validateField(input)) {
            isValid = false;
        }
    });
    
    return isValid;
}

function validateField(input) {
    const errorElement = input.parentElement.querySelector('.error-message');
    let isValid = true;
    let errorMessage = '';

    // Remove existing error styles
    input.classList.remove('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
    input.classList.add('border-gray-300', 'focus:border-blue-500', 'focus:ring-blue-500');
    
    if (errorElement) {
        errorElement.classList.add('hidden');
        errorElement.textContent = '';
    }

    // Required check
    if (input.hasAttribute('required') && !input.value.trim()) {
        isValid = false;
        errorMessage = 'Este campo es obligatorio';
    }
    
    // Email check
    if (isValid && input.type === 'email' && input.value.trim()) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(input.value.trim())) {
            isValid = false;
            errorMessage = 'Por favor ingresa un correo electrónico válido';
        }
    }

    if (!isValid) {
        // Add error styles
        input.classList.remove('border-gray-300', 'focus:border-blue-500', 'focus:ring-blue-500');
        input.classList.add('border-red-500', 'focus:border-red-500', 'focus:ring-red-500');
        
        // Add shake animation
        input.classList.add('animate-shake');
        setTimeout(() => input.classList.remove('animate-shake'), 500);

        if (errorElement) {
            errorElement.textContent = errorMessage;
            errorElement.classList.remove('hidden');
        }
    }

    return isValid;
}
