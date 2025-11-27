function openGaleryModal(src, title) {
  const modal = document.getElementById("galeryModal");
  const img = document.getElementById("modalImage");
  const titleEl = document.getElementById("modalTitle");

  img.src = src;
  titleEl.textContent = title;
  modal.classList.remove("hidden");
  document.body.style.overflow = "hidden";
}

function closeGaleryModal() {
  const modal = document.getElementById("galeryModal");
  modal.classList.add("hidden");
  document.body.style.overflow = "auto";
}

// Close on Escape key
document.addEventListener("keydown", function (event) {
  if (event.key === "Escape") {
    closeGaleryModal();
  }
});

document.addEventListener("DOMContentLoaded", () => {
  new PageFilters({
    containerId: "galleryGrid",
    itemSelector: ".gallery-item",
    searchInputId: "gallerySearch",
    categoryFilterId: "galleryCategories",
  });
});
