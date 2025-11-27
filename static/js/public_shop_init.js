document.addEventListener("DOMContentLoaded", () => {
  new PageFilters({
    containerId: "productsGrid",
    itemSelector: ".product-item",
    searchInputId: "shopSearch",
    categoryFilterId: "shopCategory",
    sortSelectId: "shopSort",
  });
});
