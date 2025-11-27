// Validación de archivos
function validateFile(input) {
  const file = input.files[0];
  if (!file) return;

  const maxSize = 5 * 1024 * 1024; // 5MB
  const allowedTypes = [
    "image/jpeg",
    "image/jpg",
    "image/png",
    "application/pdf",
  ];

  // Validar tamaño
  if (file.size > maxSize) {
    alert("El archivo es demasiado grande. El tamaño máximo es 5MB.");
    input.value = "";
    input.classList.add("border-red-500");
    return false;
  }

  // Validar tipo
  if (!allowedTypes.includes(file.type)) {
    alert("Formato de archivo no permitido. Use JPG, PNG o PDF.");
    input.value = "";
    input.classList.add("border-red-500");
    return false;
  }

  // Si pasa las validaciones, remover borde rojo
  input.classList.remove("border-red-500");
  input.classList.add("border-green-500");
  return true;
}

function switchTab(tabName) {
  // Ocultar todos los contenidos
  document.querySelectorAll(".tab-content").forEach((content) => {
    content.classList.add("hidden");
  });

  // Remover clase active de todos los botones
  document.querySelectorAll(".tab-button").forEach((button) => {
    button.classList.remove("active", "border-blue-600", "text-blue-600");
    button.classList.add("border-transparent", "text-gray-500");
  });

  // Mostrar contenido seleccionado
  document.getElementById("content-" + tabName).classList.remove("hidden");

  // Activar botón seleccionado
  const activeButton = document.getElementById("tab-" + tabName);
  activeButton.classList.add("active", "border-blue-600", "text-blue-600");
  activeButton.classList.remove("border-transparent", "text-gray-500");
}

// Validación del formulario
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("matriculaForm");
    if (form) {
        form.addEventListener("submit", function (e) {
            const requiredFields = this.querySelectorAll("[required]");
            let isValid = true;

            requiredFields.forEach((field) => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add("border-red-500");
                } else {
                    field.classList.remove("border-red-500");
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert("Por favor complete todos los campos obligatorios (*)");
            }
        });
    }
});
