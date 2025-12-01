// Actualizar estado de reclamo en la página de detalle
async function updateComplaintStatus(selectElement) {
  const complaintId = selectElement.dataset.complaintId;
  const newStatus = selectElement.value;
  const originalValue = selectElement.dataset.originalStatus || selectElement.value;
  
  // Actualizar estilos del select inmediatamente
  selectElement.classList.remove('bg-yellow-50', 'text-yellow-800', 'border-yellow-300');
  selectElement.classList.remove('bg-blue-50', 'text-blue-800', 'border-blue-300');
  selectElement.classList.remove('bg-green-50', 'text-green-800', 'border-green-300');
  
  if (newStatus === 'pending') {
    selectElement.classList.add('bg-yellow-50', 'text-yellow-800', 'border-yellow-300');
  } else if (newStatus === 'in_process') {
    selectElement.classList.add('bg-blue-50', 'text-blue-800', 'border-blue-300');
  } else if (newStatus === 'resolved') {
    selectElement.classList.add('bg-green-50', 'text-green-800', 'border-green-300');
  }
  
  try {
    // Deshabilitar el select mientras se procesa
    selectElement.disabled = true;
    
    const response = await fetch(`/admin/complaints/update_status/${complaintId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ status: newStatus })
    });
    
    const data = await response.json();
    
    if (data.success) {
      // Actualizar el estado original
      selectElement.dataset.originalStatus = newStatus;
      
      // Mostrar notificación de éxito
      showNotification('Estado actualizado correctamente', 'success');
    } else {
      throw new Error(data.message || 'Error al actualizar el estado');
    }
  } catch (error) {
    console.error('Error:', error);
    showNotification('Error al actualizar el estado: ' + error.message, 'error');
    
    // Revertir al estado original
    selectElement.value = originalValue;
    selectElement.classList.remove('bg-yellow-50', 'text-yellow-800', 'border-yellow-300');
    selectElement.classList.remove('bg-blue-50', 'text-blue-800', 'border-blue-300');
    selectElement.classList.remove('bg-green-50', 'text-green-800', 'border-green-300');
    
    if (originalValue === 'pending') {
      selectElement.classList.add('bg-yellow-50', 'text-yellow-800', 'border-yellow-300');
    } else if (originalValue === 'in_process') {
      selectElement.classList.add('bg-blue-50', 'text-blue-800', 'border-blue-300');
    } else if (originalValue === 'resolved') {
      selectElement.classList.add('bg-green-50', 'text-green-800', 'border-green-300');
    }
  } finally {
    selectElement.disabled = false;
  }
}

// Mostrar notificaciones
function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.className = `fixed top-24 right-4 z-50 px-6 py-4 rounded-lg shadow-lg transition-all transform translate-x-0 ${
    type === 'success' ? 'bg-green-500 text-white' :
    type === 'error' ? 'bg-red-500 text-white' :
    'bg-blue-500 text-white'
  }`;
  notification.innerHTML = `
    <div class="flex items-center gap-3">
      <span class="material-symbols-outlined">
        ${type === 'success' ? 'check_circle' : type === 'error' ? 'error' : 'info'}
      </span>
      <span>${message}</span>
    </div>
  `;
  
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.style.transform = 'translateX(400px)';
    notification.style.opacity = '0';
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

// Inicializar al cargar la página
document.addEventListener('DOMContentLoaded', function() {
  // Guardar el estado original del select
  const statusSelect = document.querySelector('.status-select-large');
  if (statusSelect) {
    statusSelect.dataset.originalStatus = statusSelect.value;
  }
});
