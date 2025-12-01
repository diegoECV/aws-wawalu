// Dashboard Shop - Product modals and cart functions
function openAddProductModal() {
  const modal = document.getElementById("addProductModal");
  modal.classList.remove("hidden");
  modal.classList.add("flex");
}

function closeAddProductModal() {
  const modal = document.getElementById("addProductModal");
  modal.classList.add("hidden");
  modal.classList.remove("flex");
}

function openProductModal(product) {
  const modal = document.getElementById("productModal");
  const modalImage = document.getElementById("modalImage");
  const modalTitle = document.getElementById("modalTitle");
  const modalPrice = document.getElementById("modalPrice");
  const modalDescription = document.getElementById("modalDescription");
  const modalCategory = document.getElementById("modalCategory");
  const modalMaterial = document.getElementById("modalMaterial");
  const modalUsage = document.getElementById("modalUsage");
  const modalDimensions = document.getElementById("modalDimensions");
  const modalSizes = document.getElementById("modalSizes");
  const modalForm = document.getElementById("modalForm");

  // Populate data - Use serve_image route
  const serveImageUrl = modalForm.getAttribute('data-serve-image-base');
  modalImage.src = serveImageUrl.replace("/0", "/" + product.id);

  modalImage.onerror = function () {
    this.src = modalForm.getAttribute('data-default-image');
  };

  modalTitle.textContent = product.name;
  modalPrice.textContent = "S/ " + parseFloat(product.price).toFixed(2);
  modalDescription.textContent = product.description || "Sin descripción";
  modalCategory.textContent = product.category;
  modalMaterial.textContent = product.material || "N/A";
  modalUsage.textContent = product.usage_info || "N/A";
  modalDimensions.textContent = product.dimensions || "N/A";

  // Sizes
  modalSizes.innerHTML = "";
  if (product.sizes) {
    const sizes = product.sizes.split(",");
    sizes.forEach((size) => {
      const span = document.createElement("span");
      span.className = "px-3 py-1 border border-gray-200 rounded-lg text-sm text-gray-600";
      span.textContent = size.trim();
      modalSizes.appendChild(span);
    });
  } else {
    modalSizes.textContent = "Estándar";
  }

  // Form action
  const addToCartUrl = modalForm.getAttribute('data-add-to-cart-base');
  modalForm.action = addToCartUrl.replace("0", product.id);

  modal.classList.remove("hidden");
  modal.classList.add("flex");
}

function closeProductModal() {
  const modal = document.getElementById("productModal");
  modal.classList.add("hidden");
  modal.classList.remove("flex");
}

function incrementQty(btn) {
  const input = btn.previousElementSibling;
  input.value = parseInt(input.value) + 1;
}

function decrementQty(btn) {
  const input = btn.nextElementSibling;
  if (parseInt(input.value) > 1) {
    input.value = parseInt(input.value) - 1;
  }
}
