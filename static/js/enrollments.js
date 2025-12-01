// Enrollment form validation and animation
document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('enrollmentForm');
  const errorMsg = document.getElementById('formError');
  
  if (form) {
    form.addEventListener('submit', function(e) {
      let valid = true;
      errorMsg.classList.add('hidden');
      
      // Basic validation
      ['student_id','program_id','academic_year','status','enrollment_date','monthly_fee'].forEach(id => {
        const el = document.getElementById(id);
        if (!el.value) {
          valid = false;
          el.classList.add('border-red-500');
        } else {
          el.classList.remove('border-red-500');
        }
      });
      
      if (!valid) {
        e.preventDefault();
        errorMsg.textContent = 'Por favor completa todos los campos obligatorios.';
        errorMsg.classList.remove('hidden');
        form.classList.add('animate-shake');
        setTimeout(() => form.classList.remove('animate-shake'), 500);
      }
    });
  }
});
