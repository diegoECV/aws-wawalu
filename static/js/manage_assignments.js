function openAddModal() {
  document.getElementById("addModal").classList.remove("hidden");
  document.getElementById("addModal").classList.add("flex");
}

function closeAddModal() {
  document.getElementById("addModal").classList.add("hidden");
  document.getElementById("addModal").classList.remove("flex");
}

document.getElementById("addModal").addEventListener("click", function (e) {
  if (e.target === this) {
    closeAddModal();
  }
});
