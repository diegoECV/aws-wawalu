function openAddModal() {
  document.getElementById("addModal").classList.remove("hidden");
  document.getElementById("addModal").classList.add("flex");
}

function closeAddModal() {
  document.getElementById("addModal").classList.add("hidden");
  document.getElementById("addModal").classList.remove("flex");
}

function openEditModal(id, name, programId, description, teacher) {
  document.getElementById("editForm").action = `/courses/edit/${id}`;
  document.getElementById("editName").value = name;
  document.getElementById("editProgramId").value = programId;
  document.getElementById("editDescription").value = description;
  document.getElementById("editTeacher").value = teacher;

  document.getElementById("editModal").classList.remove("hidden");
  document.getElementById("editModal").classList.add("flex");
}

function closeEditModal() {
  document.getElementById("editModal").classList.add("hidden");
  document.getElementById("editModal").classList.remove("flex");
}

// Close modals on outside click
document.getElementById("addModal").addEventListener("click", function (e) {
  if (e.target === this) closeAddModal();
});

document.getElementById("editModal").addEventListener("click", function (e) {
  if (e.target === this) closeEditModal();
});
