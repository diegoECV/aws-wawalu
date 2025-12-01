function updateGrade(input) {
  const submissionId = input.dataset.submissionId;
  const grade = input.value;

  if (!grade || grade < 0 || grade > 20) {
    alert("La nota debe estar entre 0 y 20");
    return;
  }

  const formData = new FormData();
  formData.append("grade", grade);

  fetch(`/submissions/grade/${submissionId}`, {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Show success message
        const message = document.createElement("div");
        message.className =
          "fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50";
        message.textContent = "Nota guardada correctamente";
        document.body.appendChild(message);
        setTimeout(() => message.remove(), 3000);

        // Update row styling
        const row = input.closest("tr");
        const statusBadge = row.querySelector("td:nth-child(3) span");
        if (statusBadge) {
          statusBadge.className =
            "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800";
          statusBadge.textContent = "Calificado";
        }
      } else {
        alert("Error al guardar la nota: " + data.message);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Error al guardar la nota");
    });
}
