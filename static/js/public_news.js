// Public news filtering
document.addEventListener("DOMContentLoaded", () => {
  const newsGrid = document.getElementById("newsGrid");
  const searchInput = document.getElementById("newsSearch");
  const sortSelect = document.getElementById("newsSort");
  
  if (newsGrid && typeof PageFilters !== 'undefined') {
    new PageFilters({
      containerId: "newsGrid",
      itemSelector: ".news-item",
      searchInputId: "newsSearch",
      sortSelectId: "newsSort",
    });
  }
});
