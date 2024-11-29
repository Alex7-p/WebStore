document.addEventListener("DOMContentLoaded", () => {
    const buttons = document.querySelectorAll(".product-card button");

    buttons.forEach((button) => {
        button.addEventListener("click", (event) => {
            // Verificar si el botón es para agregar o eliminar
            if (event.target.textContent.trim() === "Agregar al Carrito") {
                alert("Producto agregado al carrito.");
            }
        });
    });
});

function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    const mainContent = document.getElementById("main-content");

    sidebar.classList.toggle("active");
    mainContent.classList.toggle("active");
}
