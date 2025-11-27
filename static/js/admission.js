document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('admissionForm');

    form.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
        } else {
            // Show loading state
            const submitBtn = form.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="material-symbols-outlined animate-spin">refresh</span> Enviando...';
        }
    });

    function validateForm() {
        let isValid = true;
        const requiredInputs = form.querySelectorAll('input[required], select[required], textarea[required]');

        requiredInputs.forEach(input => {
            if (!input.value.trim()) {
                showError(input, 'Este campo es obligatorio');
                isValid = false;
            } else {
                clearError(input);
                
                // Specific validations
                if (input.type === 'email' && !isValidEmail(input.value)) {
                    showError(input, 'Por favor ingrese un correo válido');
                    isValid = false;
                }
                if (input.name === 'phone' && input.value.length < 9) {
                    showError(input, 'Ingrese un número de teléfono válido');
                    isValid = false;
                }
            }
        });

        return isValid;
    }

    function showError(input, message) {
        const formGroup = input.closest('.form-group') || input.parentElement;
        let errorDisplay = formGroup.querySelector('.error-message');
        
        if (!errorDisplay) {
            errorDisplay = document.createElement('p');
            errorDisplay.className = 'error-message text-red-500 text-xs mt-1';
            formGroup.appendChild(errorDisplay);
        }
        
        errorDisplay.textContent = message;
        errorDisplay.classList.remove('hidden');
        if(input.classList) input.classList.add('border-red-500');
    }

    function clearError(input) {
        const formGroup = input.closest('.form-group') || input.parentElement;
        const errorDisplay = formGroup.querySelector('.error-message');
        if (errorDisplay) {
            errorDisplay.classList.add('hidden');
        }
        if(input.classList) input.classList.remove('border-red-500');
    }

    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
});
