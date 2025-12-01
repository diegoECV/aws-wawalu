let currentStudents = [];

// Set today's date as default
document.getElementById("dateSelect").valueAsDate = new Date();

function loadAttendance() {
  const programId = document.getElementById("programSelect").value;
  const date = document.getElementById("dateSelect").value;

  if (!programId || !date) {
    alert("Por favor seleccione un programa y una fecha");
    return;
  }

  fetch(`/attendance/get/${programId}/${date}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        currentStudents = data.students;
        renderStudents();
        document.getElementById("attendanceTable").classList.remove("hidden");
      } else {
        alert("Error al cargar estudiantes");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Error al cargar estudiantes");
    });
}

function renderStudents() {
  const tbody = document.getElementById("studentsList");
  tbody.innerHTML = "";

  if (currentStudents.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="3" class="px-6 py-12 text-center text-gray-500">
          <span class="material-symbols-outlined text-4xl mb-2 text-gray-300">group</span>
          <p>No hay estudiantes activos en este programa.</p>
        </td>
      </tr>
    `;
    return;
  }

  currentStudents.forEach((student) => {
    const row = document.createElement("tr");
    row.className = "hover:bg-gray-50 transition-colors";
    row.dataset.enrollmentId = student.enrollment_id;

    row.innerHTML = `
      <td class="px-6 py-4">
        <div class="font-medium text-gray-800">${student.first_name} ${
      student.last_name
    }</div>
      </td>
      <td class="px-6 py-4">
        <select class="attendance-status px-3 py-1 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
          <option value="present" ${
            student.status === "present" ? "selected" : ""
          }>Presente</option>
          <option value="absent" ${
            student.status === "absent" ? "selected" : ""
          }>Ausente</option>
          <option value="late" ${
            student.status === "late" ? "selected" : ""
          }>Tarde</option>
          <option value="excused" ${
            student.status === "excused" ? "selected" : ""
          }>Justificado</option>
        </select>
      </td>
      <td class="px-6 py-4">
        <input 
          type="text" 
          class="attendance-remarks w-full px-3 py-1 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
          placeholder="Observaciones..."
          value="${student.remarks || ""}"
        >
      </td>
    `;

    tbody.appendChild(row);
  });
}

function saveAttendance() {
  const programId = document.getElementById("programSelect").value;
  const date = document.getElementById("dateSelect").value;
  const rows = document.querySelectorAll(
    "#studentsList tr[data-enrollment-id]"
  );

  const records = Array.from(rows).map((row) => ({
    enrollment_id: row.dataset.enrollmentId,
    status: row.querySelector(".attendance-status").value,
    remarks: row.querySelector(".attendance-remarks").value,
  }));

  fetch("/attendance/take", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      program_id: programId,
      date: date,
      records: records,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        const message = document.createElement("div");
        message.className =
          "fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50";
        message.textContent = "Asistencia guardada correctamente";
        document.body.appendChild(message);
        setTimeout(() => message.remove(), 3000);
      } else {
        alert("Error al guardar asistencia: " + data.message);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Error al guardar asistencia");
    });
}
