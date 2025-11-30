// Manejo de errores de imágenes en el carrito
document.addEventListener('DOMContentLoaded', function() {
    const cartImages = document.querySelectorAll('.cart-item-image');
    
    cartImages.forEach(img => {
        img.addEventListener('error', function() {
            const fallbackUrl = this.getAttribute('data-fallback');
            if (fallbackUrl && this.src !== fallbackUrl) {
                this.src = fallbackUrl;
            } else {
                // Si el fallback también falla, mostrar icono por defecto
                this.style.display = 'none';
                const parent = this.parentElement;
                parent.innerHTML = '<span class="material-symbols-outlined text-gray-300">shopping_bag</span>';
            }
        });
    });
});