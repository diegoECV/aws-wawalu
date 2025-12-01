// Filtrar reclamos por estado
function filterComplaints(status) {
  const rows = document.querySelectorAll('.complaint-row');
  const buttons = document.querySelectorAll('.filter-btn');
  
  // Actualizar estilos de botones
  buttons.forEach(btn => {
    if (btn.dataset.status === status) {
      btn.classList.remove('bg-white', 'text-gray-700', 'border-gray-200');
      btn.classList.add('bg-blue-600', 'text-white', 'border-blue-600');
    } else {
      btn.classList.remove('bg-blue-600', 'text-white', 'border-blue-600');
      btn.classList.add('bg-white', 'text-gray-700', 'border-gray-200');
    }
  });
  
  // Filtrar filas
  rows.forEach(row => {
    if (status === 'all' || row.dataset.status === status) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  });
  
  // Actualizar contador visible
  const visibleCount = Array.from(rows).filter(row => row.style.display !== 'none').length;
  updateEmptyState(visibleCount);
}

// Actualizar mensaje cuando no hay resultados
function updateEmptyState(count) {
  let emptyState = document.getElementById('empty-state');
  
  if (count === 0) {
    if (!emptyState) {
      emptyState = document.createElement('tr');
      emptyState.id = 'empty-state';
      emptyState.innerHTML = `
        <td colspan="7" class="px-6 py-12 text-center">
          <div class="flex flex-col items-center gap-3 text-gray-400">
            <span class="material-symbols-outlined text-5xl">folder_open</span>
            <p class="text-lg font-medium">No hay reclamos con este filtro</p>
          </div>
        </td>
      `;
      document.querySelector('tbody').appendChild(emptyState);
    }
    emptyState.style.display = '';
  } else {
    if (emptyState) {
      emptyState.style.display = 'none';
    }
  }
}

// Actualizar estado de reclamo
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
      
      // Actualizar badge si existe en la misma fila
      const row = selectElement.closest('tr');
      if (row) {
        const badge = row.querySelector('.status-badge');
        if (badge) {
          badge.classList.remove('bg-yellow-100', 'text-yellow-800');
          badge.classList.remove('bg-blue-100', 'text-blue-800');
          badge.classList.remove('bg-green-100', 'text-green-800');
          
          if (newStatus === 'pending') {
            badge.classList.add('bg-yellow-100', 'text-yellow-800');
            badge.textContent = '⏱️ Pendiente';
          } else if (newStatus === 'in_process') {
            badge.classList.add('bg-blue-100', 'text-blue-800');
            badge.textContent = '🔄 En Proceso';
          } else if (newStatus === 'resolved') {
            badge.classList.add('bg-green-100', 'text-green-800');
            badge.textContent = '✅ Resuelto';
          }
        }
        
        // Actualizar data-status de la fila
        row.dataset.status = newStatus;
      }
      
      // Mostrar mensaje de éxito
      showNotification('Estado actualizado correctamente', 'success');
      
      // Actualizar contadores de estadísticas
      updateStatistics();
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

// Actualizar estadísticas en tiempo real
function updateStatistics() {
  const rows = document.querySelectorAll('.complaint-row');
  const pending = Array.from(rows).filter(row => row.dataset.status === 'pending').length;
  const inProcess = Array.from(rows).filter(row => row.dataset.status === 'in_process').length;
  const resolved = Array.from(rows).filter(row => row.dataset.status === 'resolved').length;
  
  // Actualizar contadores en las tarjetas de estadísticas
  const pendingCounter = document.querySelector('[data-stat="pending"]');
  const inProcessCounter = document.querySelector('[data-stat="in_process"]');
  const resolvedCounter = document.querySelector('[data-stat="resolved"]');
  
  if (pendingCounter) pendingCounter.textContent = pending;
  if (inProcessCounter) inProcessCounter.textContent = inProcess;
  if (resolvedCounter) resolvedCounter.textContent = resolved;
  
  // Actualizar badges en los botones de filtro
  const allBadge = document.querySelector('[data-filter-badge="all"]');
  const pendingBadge = document.querySelector('[data-filter-badge="pending"]');
  const inProcessBadge = document.querySelector('[data-filter-badge="in_process"]');
  const resolvedBadge = document.querySelector('[data-filter-badge="resolved"]');
  
  if (allBadge) allBadge.textContent = rows.length;
  if (pendingBadge) pendingBadge.textContent = pending;
  if (inProcessBadge) inProcessBadge.textContent = inProcess;
  if (resolvedBadge) resolvedBadge.textContent = resolved;
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

// Buscar reclamos en tiempo real
function searchComplaints(searchTerm) {
  const rows = document.querySelectorAll('.complaint-row');
  searchTerm = searchTerm.toLowerCase().trim();
  
  rows.forEach(row => {
    const text = row.textContent.toLowerCase();
    if (text.includes(searchTerm)) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  });
  
  const visibleCount = Array.from(rows).filter(row => row.style.display !== 'none').length;
  updateEmptyState(visibleCount);
}

// Inicializar al cargar la página
document.addEventListener('DOMContentLoaded', function() {
  // Guardar el estado original de todos los selects
  document.querySelectorAll('.status-select').forEach(select => {
    select.dataset.originalStatus = select.value;
  });
  
  // Configurar búsqueda si existe el input
  const searchInput = document.getElementById('complaint-search');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchComplaints(e.target.value);
    });
  }
});
