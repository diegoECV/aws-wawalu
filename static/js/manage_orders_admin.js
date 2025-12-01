function updateOrderStatus(selectElement) {
  const orderId = selectElement.dataset.orderId;
  const newStatus = selectElement.value;
  
  if (!confirm('¿Está seguro de cambiar el estado de este pedido?')) {
    selectElement.value = selectElement.dataset.previousValue || 'pending';
    return;
  }
  
  fetch(`/orders/update_status/${orderId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ status: newStatus })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // Update select styling based on new status
      selectElement.className = selectElement.className.replace(/bg-\w+-100 text-\w+-800/g, '');
      const statusColors = {
        'pending': 'bg-yellow-100 text-yellow-800',
        'paid': 'bg-blue-100 text-blue-800',
        'shipped': 'bg-purple-100 text-purple-800',
        'completed': 'bg-green-100 text-green-800',
        'cancelled': 'bg-red-100 text-red-800'
      };
      selectElement.className += ' ' + statusColors[newStatus];
      selectElement.dataset.previousValue = newStatus;
      
      // Show success message
      const message = document.createElement('div');
      message.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50';
      message.textContent = 'Estado actualizado correctamente. Email enviado al cliente.';
      document.body.appendChild(message);
      setTimeout(() => message.remove(), 3000);
    } else {
      alert('Error al actualizar el estado: ' + data.message);
      selectElement.value = selectElement.dataset.previousValue || 'pending';
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Error al actualizar el estado');
    selectElement.value = selectElement.dataset.previousValue || 'pending';
  });
}

// Store initial values
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.status-select').forEach(select => {
    select.dataset.previousValue = select.value;
  });
});
