function incrementQty(btn, max) {
  const input = btn.previousElementSibling;
  let val = parseInt(input.value);
  if (max && val >= max) return;
  input.value = val + 1;
}

function decrementQty(btn) {
  const input = btn.nextElementSibling;
  let val = parseInt(input.value);
  if (val > 1) {
    input.value = val - 1;
  }
}

function openProductModal(product) {
  const modal = document.getElementById("productModal");

  // Populate data
  document.getElementById("modalTitle").textContent = product.name;
  document.getElementById("modalCategory").textContent = product.category;
  document.getElementById("modalPrice").textContent =
    "S/ " + parseFloat(product.price).toFixed(2);
  document.getElementById("modalDescription").textContent =
    product.description || "Sin descripción";
  document.getElementById("modalMaterial").textContent =
    product.material || "N/A";
  document.getElementById("modalUsage").textContent =
    product.usage_info || "N/A";

  // Image logic
  const img = document.getElementById("modalImage");
  const config = document.getElementById("shop-config").dataset;
  
  // Use config from DOM for paths
  if (product.image_url && product.image_url.startsWith("product_")) {
    img.src = config.uploadsUrl + product.image_url;
  } else {
    img.src = config.productsUrl + product.image_url;
  }

  // Dimensions vs Sizes
  const dimContainer = document.getElementById("modalDimensionsContainer");
  const sizeContainer = document.getElementById("modalSizesContainer");

  if (product.sizes) {
    dimContainer.classList.add("hidden");
    sizeContainer.classList.remove("hidden");
    const sizes = product.sizes.split(",");
    const sizeHtml = sizes
      .map(
        (s) =>
          `<span class="px-3 py-1 border border-gray-200 rounded-lg text-sm text-gray-600">${s}</span>`
      )
      .join("");
    document.getElementById("modalSizes").innerHTML = sizeHtml;
  } else {
    sizeContainer.classList.add("hidden");
    dimContainer.classList.remove("hidden");
    document.getElementById("modalDimensions").textContent =
      product.dimensions || "N/A";
  }

  // Form Action
  const form = document.getElementById("modalForm");
  form.action = "/cart/add/" + product.id;

  // Reset Qty
  document.getElementById("modalQty").value = 1;
  const incBtn = document.getElementById("modalIncBtn");
  incBtn.onclick = function () {
    incrementQty(this, product.stock);
  };

  modal.classList.remove("hidden");
  modal.classList.add("flex");
}

function closeProductModal() {
  const modal = document.getElementById("productModal");
  modal.classList.add("hidden");
  modal.classList.remove("flex");
}
