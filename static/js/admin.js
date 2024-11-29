// Script para manejar la eliminación y edición de productos
document.addEventListener("DOMContentLoaded", () => {
    const deleteButtons = document.querySelectorAll("button[data-action='delete']");
    const editButtons = document.querySelectorAll("button[data-action='edit']");

    deleteButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const productId = button.dataset.id;
            if (confirm(`¿Estás seguro de eliminar el producto con ID ${productId}?`)) {
                // Lógica para eliminar el producto (puedes usar fetch o AJAX aquí).
                console.log(`Producto ${productId} eliminado.`);
            }
        });
    });

    editButtons.forEach((button) => {
        button.addEventListener("click", () => {
            const productId = button.dataset.id;
            // Redirige a la página de edición
            window.location.href = `/admin/edit-product/${productId}`;
        });
    });
});
