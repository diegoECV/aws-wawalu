function openAddModal() {
  document.getElementById("addModal").classList.remove("hidden");
  document.getElementById("addModal").classList.add("flex");
}

function closeAddModal() {
  document.getElementById("addModal").classList.add("hidden");
  document.getElementById("addModal").classList.remove("flex");
}

// Close modal on outside click
document.getElementById("addModal").addEventListener("click", function (e) {
  if (e.target === this) closeAddModal();
});
