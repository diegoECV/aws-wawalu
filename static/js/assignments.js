// Dashboard Assignments - Submission modal
function openSubmissionModal(assignmentId, title) {
  const modal = document.getElementById('submissionModal');
  const form = document.getElementById('submissionForm');
  const titleEl = document.getElementById('modalTitle');
  
  form.action = `/dashboard/assignments/submit/${assignmentId}`;
  titleEl.textContent = `Entregar: ${title}`;
  
  modal.classList.remove('hidden');
  modal.classList.add('flex');
}

function closeSubmissionModal() {
  const modal = document.getElementById('submissionModal');
  modal.classList.add('hidden');
  modal.classList.remove('flex');
}

// Close on outside click
document.addEventListener('DOMContentLoaded', function() {
  const submissionModal = document.getElementById('submissionModal');
  if (submissionModal) {
    submissionModal.addEventListener('click', function(e) {
      if (e.target === this) closeSubmissionModal();
    });
  }
});
