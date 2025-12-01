// Dashboard Profile - Tab switching
function switchTab(tabId) {
  // Hide all sections
  document.querySelectorAll(".profile-section").forEach((el) => {
    el.classList.add("hidden");
  });

  // Remove active styles from all tabs
  document.querySelectorAll(".profile-tab-link").forEach((el) => {
    el.classList.remove("bg-blue-50", "border-blue-600", "text-blue-600");
    el.classList.add("text-gray-600", "border-transparent");
  });

  // Show selected section
  document.getElementById(tabId).classList.remove("hidden");

  // Add active styles to selected tab
  const activeTab = document.getElementById("tab-" + tabId);
  if (activeTab) {
    activeTab.classList.remove("text-gray-600", "border-transparent");
    activeTab.classList.add("bg-blue-50", "border-blue-600", "text-blue-600");
  }
}
