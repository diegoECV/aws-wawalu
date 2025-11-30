// Search Functionality
document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("searchInput");
    if (searchInput) {
        searchInput.addEventListener("keyup", function () {
            const searchValue = this.value.toLowerCase();
            const rows = document.querySelectorAll("#enrollmentsTableBody tr");

            rows.forEach((row) => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchValue) ? "" : "none";
            });
        });
    }
});

// Update Status
function updateStatus(id, status) {
  if (
    !confirm(
      "¿Estás seguro de cambiar el estado a " +
        (status === "active" ? "Activa" : "Rechazada") +
        "?"
    )
  )
    return;

  fetch(`/enrollments/update_status/${id}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
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

// Delete Enrollment
function deleteEnrollment(id) {
  if (
    !confirm(
      "¿Estás seguro de eliminar esta matrícula? Esta acción no se puede deshacer."
    )
  )
    return;

  fetch(`/enrollments/delete/${id}`, {
    method: "POST",
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        location.reload();
      } else {
        alert("Error al eliminar: " + data.message);
      }
    })
    .catch((error) => console.error("Error:", error));
}

// View Enrollment Details
function viewEnrollment(id) {
  window.location.href = `/enrollments/view/${id}`;
}
