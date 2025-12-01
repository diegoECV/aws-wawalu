// Gestión de comentarios - Filtrado
function filterComments(status) {
  const cards = document.querySelectorAll(".comment-card");
  const tabs = document.querySelectorAll(".filter-tab");

  // Update active tab
  tabs.forEach((tab) => {
    tab.classList.remove(
      "active",
      "border-blue-600",
      "text-blue-600",
      "border-green-600",
      "text-green-600",
      "border-yellow-600",
      "text-yellow-600"
    );
    if (tab.dataset.filter === status) {
      tab.classList.add("active");
      if (status === "all") {
        tab.classList.add("border-blue-600", "text-blue-600");
      } else if (status === "approved") {
        tab.classList.add("border-green-600", "text-green-600");
      } else if (status === "pending") {
        tab.classList.add("border-yellow-600", "text-yellow-600");
      }
    }
  });

  // Filter cards
  cards.forEach((card) => {
    if (status === "all") {
      card.style.display = "block";
    } else {
      const cardStatus = card.dataset.status;
      card.style.display = cardStatus === status ? "block" : "none";
    }
  });
}

// Initialize with 'all' filter
document.addEventListener("DOMContentLoaded", function () {
  filterComments("all");
});
