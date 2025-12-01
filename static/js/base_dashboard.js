// Simple Mobile Sidebar Logic
document.addEventListener("DOMContentLoaded", () => {
  const sidebarBtn = document.getElementById("mobile-sidebar-btn");
  const closeBtn = document.getElementById("close-sidebar-btn");
  const sidebar = document.getElementById("mobile-sidebar");
  const overlay = document.getElementById("sidebar-overlay");

  function toggleSidebar() {
    const isClosed = sidebar.classList.contains("-translate-x-full");
    if (isClosed) {
      sidebar.classList.remove("-translate-x-full");
      overlay.classList.remove("hidden");
    } else {
      sidebar.classList.add("-translate-x-full");
      overlay.classList.add("hidden");
    }
  }

  if (sidebarBtn) sidebarBtn.addEventListener("click", toggleSidebar);
  if (closeBtn) closeBtn.addEventListener("click", toggleSidebar);
  if (overlay) overlay.addEventListener("click", toggleSidebar);
});
