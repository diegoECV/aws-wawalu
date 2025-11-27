function nextStep(stepNumber) {
    // Hide all steps
    document.querySelectorAll('.checkout-step-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.step').forEach(el => el.classList.remove('active'));

    // Show target step
    document.getElementById(`step-${stepNumber}-content`).classList.add('active');
    
    // Update progress bar
    for (let i = 1; i <= stepNumber; i++) {
        document.querySelector(`.step[data-step="${i}"]`).classList.add('active');
    }
}

function togglePaymentDetails() {
    // Hide all details
    document.querySelectorAll('.payment-details').forEach(el => el.style.display = 'none');
    
    // Get selected method
    const selectedMethod = document.querySelector('input[name="payment_method"]:checked').value;
    
    // Show selected details
    const detailsElement = document.getElementById(`${selectedMethod}-details`);
    if (detailsElement) {
        detailsElement.style.display = 'block';
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    togglePaymentDetails();
});
