function updateStatus(id, status) {
  if (!confirm("¿Estás seguro de cambiar el estado de esta matrícula?"))
    return;

  fetch(`/enrollments/update_status/${id}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status: status }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        location.reload();
      } else {
        alert("Error al actualizar: " + data.message);
      }
    })
    .catch((error) => console.error("Error:", error));
}
