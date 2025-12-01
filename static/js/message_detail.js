// Message detail - Reply modal
function replyToMessage() {
  const modal = document.getElementById("replyModal");
  modal.classList.remove("hidden");
  modal.classList.add("flex");
}

function closeReplyModal() {
  const modal = document.getElementById("replyModal");
  modal.classList.add("hidden");
  modal.classList.remove("flex");
}

// Close on outside click
document.addEventListener('DOMContentLoaded', function() {
  const replyModal = document.getElementById("replyModal");
  if (replyModal) {
    replyModal.addEventListener("click", function (e) {
      if (e.target === this) closeReplyModal();
    });
  }
});
