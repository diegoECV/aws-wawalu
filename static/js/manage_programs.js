// Toggle program active status
async function toggleProgramStatus(toggleElement) {
  const programId = toggleElement.dataset.programId;
  const newStatus = toggleElement.checked;
  
  try {
    // Deshabilitar el toggle mientras se procesa
    toggleElement.disabled = true;
    
    const response = await fetch(`/admin/programs/toggle/${programId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    
    const data = await response.json();
    
    if (data.success) {
      // Actualizar el estado del toggle
      toggleElement.checked = data.is_active;
      
      // Mostrar notificación de éxito
      showNotification(
        data.is_active ? 'Programa activado correctamente' : 'Programa desactivado correctamente', 
        'success'
      );
    } else {
      throw new Error(data.message || 'Error al actualizar el estado');
    }
  } catch (error) {
    console.error('Error:', error);
    showNotification('Error al actualizar el estado: ' + error.message, 'error');
    
    // Revertir el estado del toggle
    toggleElement.checked = !newStatus;
  } finally {
    toggleElement.disabled = false;
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

// Confirmar eliminación de programa
function confirmDelete(programId, programName) {
  return confirm(`¿Está seguro de eliminar el programa "${programName}"?\n\nEsta acción no se puede deshacer.`);
}

// Filtrar programas por estado
function filterPrograms(status) {
  const rows = document.querySelectorAll('.program-row');
  
  rows.forEach(row => {
    const toggle = row.querySelector('.status-toggle');
    const isActive = toggle ? toggle.checked : true;
    
    if (status === 'all') {
      row.style.display = '';
    } else if (status === 'active' && isActive) {
      row.style.display = '';
    } else if (status === 'inactive' && !isActive) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  });
}

// Buscar programas
function searchPrograms(searchTerm) {
  const rows = document.querySelectorAll('.program-row');
  searchTerm = searchTerm.toLowerCase().trim();
  
  rows.forEach(row => {
    const text = row.textContent.toLowerCase();
    if (text.includes(searchTerm)) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  });
}

// Inicializar al cargar la página
document.addEventListener('DOMContentLoaded', function() {
  // Configurar búsqueda si existe el input
  const searchInput = document.getElementById('program-search');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchPrograms(e.target.value);
    });
  }
});
