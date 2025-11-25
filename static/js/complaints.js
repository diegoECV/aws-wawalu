document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('complaintsForm');
    const clearBtn = document.getElementById('clearBtn');

    // Clear Form Functionality
    clearBtn.addEventListener('click', function() {
        if (confirm('¿Estás seguro de que deseas limpiar todo el formulario?')) {
            form.reset();
            // Reset any error states
            document.querySelectorAll('.error-message').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.border-red-500').forEach(el => el.classList.remove('border-red-500'));
        }
    });

    // Form Submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (validateForm()) {
            // Simulate submission
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="material-symbols-outlined animate-spin mr-2">refresh</span> Enviando...';

            setTimeout(() => {
                alert('Su reclamo ha sido registrado exitosamente. Se ha enviado una copia a su correo electrónico.');
                form.reset();
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }, 2000);
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
                if (input.name === 'document_number' && input.value.length < 8) {
                    showError(input, 'Ingrese un número de documento válido');
                    isValid = false;
                }
            }
        });

        // Validate Radio Buttons (Type of Claim)
        const claimType = form.querySelector('input[name="claim_type"]:checked');
        const claimTypeContainer = document.getElementById('claimTypeContainer');
        if (!claimType) {
            showError(claimTypeContainer, 'Debe seleccionar un tipo');
            isValid = false;
        } else {
            clearError(claimTypeContainer);
        }
        
        // Validate Checkbox
        const privacyCheck = document.getElementById('privacy_check');
        if (!privacyCheck.checked) {
            alert('Debe aceptar la política de protección de datos personales');
            isValid = false;
        }

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
