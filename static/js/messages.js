// Dashboard Messages - Tab switching and modal management
function switchTab(tab) {
  // Hide all content
  document.getElementById("content-inbox").classList.add("hidden");
  document.getElementById("content-sent").classList.add("hidden");

  // Reset tabs
  document
    .getElementById("tab-inbox")
    .classList.remove("bg-blue-100", "text-blue-700");
  document
    .getElementById("tab-inbox")
    .classList.add("text-gray-600", "hover:bg-gray-100");
  document
    .getElementById("tab-sent")
    .classList.remove("bg-blue-100", "text-blue-700");
  document
    .getElementById("tab-sent")
    .classList.add("text-gray-600", "hover:bg-gray-100");

  // Activate selected
  document.getElementById("content-" + tab).classList.remove("hidden");
  document
    .getElementById("tab-" + tab)
    .classList.add("bg-blue-100", "text-blue-700");
  document
    .getElementById("tab-" + tab)
    .classList.remove("text-gray-600", "hover:bg-gray-100");
}

function openComposeModal() {
  const modal = document.getElementById("composeModal");
  modal.classList.remove("hidden");
  modal.classList.add("flex");
}

function closeComposeModal() {
  const modal = document.getElementById("composeModal");
  modal.classList.add("hidden");
  modal.classList.remove("flex");
}

// Close on outside click
document.addEventListener("DOMContentLoaded", function() {
  const composeModal = document.getElementById("composeModal");
  if (composeModal) {
    composeModal.addEventListener("click", function (e) {
      if (e.target === this) closeComposeModal();
    });
  }
});

function viewMessage(id) {
  // Redirect to message detail page
  window.location.href = `/dashboard/messages/view/${id}`;
}
