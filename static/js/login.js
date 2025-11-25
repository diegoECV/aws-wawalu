document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const togglePassword = document.getElementById('togglePassword');

    // Toggle Password Visibility
    togglePassword.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        const icon = this.querySelector('span');
        icon.textContent = type === 'password' ? 'visibility' : 'visibility_off';
    });

    // Real-time validation
    const inputs = [emailInput, passwordInput];
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.value.trim() !== '') {
                clearError(this);
            }
        });
        
        input.addEventListener('blur', function() {
            validateField(this);
        });
    });

    // Form Submission
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        let isValid = true;
        
        inputs.forEach(input => {
            if (!validateField(input)) {
                isValid = false;
            }
        });

        if (isValid) {
            // Simulate loading state
            const button = this.querySelector('button[type="submit"]');
            const originalText = button.innerHTML;
            button.disabled = true;
            button.innerHTML = '<span class="material-symbols-outlined animate-spin mr-2">refresh</span> Iniciando...';
            
            // Here you would typically send the data to the server
            // For now, we'll just simulate a delay
            setTimeout(() => {
                // alert('Login exitoso (Simulado)');
                // button.innerHTML = originalText;
                // button.disabled = false;
                this.submit(); // Actually submit the form to the backend
            }, 1000);
        }
    });

    function validateField(input) {
        const value = input.value.trim();
        let isValid = true;
        let errorMessage = '';

        if (value === '') {
            isValid = false;
            errorMessage = 'Este campo es obligatorio';
        } else if (input.type === 'email') {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                errorMessage = 'Ingresa un correo válido';
            }
        }

        if (!isValid) {
            showError(input, errorMessage);
        } else {
            clearError(input);
        }

        return isValid;
    }

    function showError(input, message) {
        const formGroup = input.closest('.form-group');
        const errorText = formGroup.querySelector('.error-message');
        
        input.classList.add('input-error');
        input.classList.add('shake');
        
        errorText.textContent = message;
        errorText.classList.remove('hidden');

        // Remove shake animation after it plays
        setTimeout(() => {
            input.classList.remove('shake');
        }, 500);
    }

    function clearError(input) {
        const formGroup = input.closest('.form-group');
        const errorText = formGroup.querySelector('.error-message');
        
        input.classList.remove('input-error');
        errorText.classList.add('hidden');
    }
});
