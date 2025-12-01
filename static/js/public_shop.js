// JS específico para la tienda pública
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
  document.getElementById("modalTitle").textContent = product.name;
  document.getElementById("modalCategory").textContent = product.category;
  document.getElementById("modalPrice").textContent = "S/ " + parseFloat(product.price).toFixed(2);
  document.getElementById("modalDescription").textContent = product.description || "Sin descripción";
  document.getElementById("modalMaterial").textContent = product.material || "N/A";
  document.getElementById("modalUsage").textContent = product.usage_info || "N/A";
  const img = document.getElementById("modalImage");
  if (product.has_image) {
    img.src = "/serve_image/products/" + product.id;
  } else if (product.image_url) {
    // Fallback for legacy images if needed, or just use serve_image if it handles legacy
    img.src = "/serve_image/products/" + product.id;
  } else {
    img.src = "/static/image/default_product.png";
  }
  const dimContainer = document.getElementById("modalDimensionsContainer");
  const sizeContainer = document.getElementById("modalSizesContainer");
  if (product.sizes) {
    dimContainer.classList.add("hidden");
    sizeContainer.classList.remove("hidden");
    const sizes = product.sizes.split(",");
    const sizeHtml = sizes.map((s) => `<span class="px-3 py-1 border border-gray-200 rounded-lg text-sm text-gray-600">${s}</span>`).join("");
    document.getElementById("modalSizes").innerHTML = sizeHtml;
  } else {
    sizeContainer.classList.add("hidden");
    dimContainer.classList.remove("hidden");
    document.getElementById("modalDimensions").textContent = product.dimensions || "N/A";
  }
  const form = document.getElementById("modalForm");
  form.action = "/cart/add/" + product.id;
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
