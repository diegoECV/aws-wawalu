document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    const inputs = registerForm.querySelectorAll('input, select');
    const togglePassword = document.getElementById('togglePassword');
    const toggleConfirmPassword = document.getElementById('toggleConfirmPassword');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');

    // Toggle Password Visibility
    togglePassword.addEventListener('click', function() {
        toggleInputType(passwordInput, this);
    });

    toggleConfirmPassword.addEventListener('click', function() {
        toggleInputType(confirmPasswordInput, this);
    });

    function toggleInputType(input, toggler) {
        const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
        input.setAttribute('type', type);
        const icon = toggler.querySelector('span');
        icon.textContent = type === 'password' ? 'visibility' : 'visibility_off';
    }

    // Real-time validation
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.type === 'checkbox') {
                if (this.checked) clearError(this);
            } else {
                if (this.value.trim() !== '') clearError(this);
            }
            
            // Special case for password confirmation
            if (this.id === 'confirm_password' || this.id === 'password') {
                if (confirmPasswordInput.value !== '' && passwordInput.value !== '') {
                    validatePasswordMatch();
                }
            }
        });

        input.addEventListener('blur', function() {
            validateField(this);
        });
    });

    // Form Submission
    registerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        let isValid = true;
        
        inputs.forEach(input => {
            if (!validateField(input)) {
                isValid = false;
            }
        });

        if (isValid) {
            const button = this.querySelector('button[type="submit"]');
            button.disabled = true;
            button.innerHTML = '<span class="material-symbols-outlined animate-spin mr-2">refresh</span> Creando cuenta...';
            
            setTimeout(() => {
                this.submit();
            }, 1000);
        }
    });

    function validateField(input) {
        const value = input.value.trim();
        let isValid = true;
        let errorMessage = '';

        // Checkbox validation (Terms)
        if (input.type === 'checkbox') {
            if (!input.checked) {
                isValid = false;
                // For checkbox, we might handle error display differently or just shake the container
                // Here we'll just shake the parent div
                input.parentElement.classList.add('shake');
                setTimeout(() => input.parentElement.classList.remove('shake'), 500);
                return false; 
            }
            return true;
        }

        // Required check
        if (value === '' && input.hasAttribute('required')) {
            isValid = false;
            errorMessage = 'Este campo es obligatorio';
        } 
        // Email check
        else if (input.type === 'email') {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                errorMessage = 'Ingresa un correo válido';
            }
        }
        // Password Match check
        else if (input.id === 'confirm_password') {
            if (value !== passwordInput.value) {
                isValid = false;
                errorMessage = 'Las contraseñas no coinciden';
            }
        }

        if (!isValid) {
            showError(input, errorMessage);
        } else {
            clearError(input);
        }

        return isValid;
    }

    function validatePasswordMatch() {
        if (confirmPasswordInput.value !== passwordInput.value) {
            showError(confirmPasswordInput, 'Las contraseñas no coinciden');
            return false;
        } else {
            clearError(confirmPasswordInput);
            return true;
        }
    }

    function showError(input, message) {
        const formGroup = input.closest('.form-group');
        const errorText = formGroup.querySelector('.error-message');
        
        input.classList.add('input-error');
        input.classList.add('shake');
        
        if (errorText) {
            errorText.textContent = message;
            errorText.classList.remove('hidden');
        }

        setTimeout(() => {
            input.classList.remove('shake');
        }, 500);
    }

    function clearError(input) {
        const formGroup = input.closest('.form-group');
        const errorText = formGroup.querySelector('.error-message');
        
        input.classList.remove('input-error');
        if (errorText) {
            errorText.classList.add('hidden');
        }
    }
});
