// Order status update
function updateOrderStatus(orderId, newStatus) {
  if (!confirm("¿Confirmar que el pago ha sido verificado?")) return;

  fetch(`/orders/update_status/${orderId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status: newStatus }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        location.reload();
      } else {
        alert("Error: " + data.message);
      }
    });
}
