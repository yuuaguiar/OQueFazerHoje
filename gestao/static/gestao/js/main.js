/* Este script encontra todos os ícones <i data-lucide="..."></i> 
  no HTML e os substitui por SVGs da biblioteca Lucide.
*/
document.addEventListener("DOMContentLoaded", () => {
  if (typeof lucide !== "undefined") {
    lucide.createIcons();
  }
});