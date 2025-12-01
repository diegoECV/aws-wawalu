document.getElementById("image").addEventListener("change", function (e) {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      // Create or update preview container
      let previewContainer = document.getElementById(
        "image-preview-container"
      );
      if (!previewContainer) {
        previewContainer = document.createElement("div");
        previewContainer.id = "image-preview-container";
        previewContainer.className = "mb-4 text-center";

        const uploadArea = document
          .querySelector('label[for="image"]')
          .closest(".border-dashed").parentElement;
        uploadArea.insertBefore(previewContainer, uploadArea.firstChild);
      }

      previewContainer.innerHTML = `
        <p class="text-xs text-gray-500 mb-2">Vista previa:</p>
        <img src="${e.target.result}" class="h-48 w-auto object-cover rounded-lg border border-gray-200 mx-auto shadow-sm" />
        <p class="text-xs text-blue-600 mt-2 font-medium">${file.name}</p>
      `;
    };
    reader.readAsDataURL(file);
  }
});
