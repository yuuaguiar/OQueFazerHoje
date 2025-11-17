document.addEventListener("DOMContentLoaded", () => {
    
    // --- Lógica para Dropdowns ---
    // Encontra todos os botões que abrem um dropdown
    const dropdownToggles = document.querySelectorAll('[data-toggle="dropdown"]');
    
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', (event) => {
            event.stopPropagation(); // Impede que o clique feche o menu imediatamente
            const targetMenu = document.getElementById(toggle.getAttribute('data-target'));
            if (targetMenu) {
                // Esconde todos os outros menus
                document.querySelectorAll('.dropdown-menu').forEach(menu => {
                    if (menu.id !== targetMenu.id) {
                        menu.classList.add('hidden');
                    }
                });
                // Mostra ou esconde o menu clicado
                targetMenu.classList.toggle('hidden');
            }
        });
    });

    // --- Lógica para Modals ---
    // Encontra todos os botões que abrem um modal
    const modalToggles = document.querySelectorAll('[data-toggle="modal"]');
    modalToggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            const targetModal = document.getElementById(toggle.getAttribute('data-target'));
            if (targetModal) {
                targetModal.classList.remove('hidden');
                targetModal.classList.add('flex');
            }
            // Fecha dropdowns ao abrir um modal
            document.querySelectorAll('.dropdown-menu').forEach(menu => menu.classList.add('hidden'));
        });
    });

    // Encontra todos os botões de fechar modal (ex: Cancelar ou o 'X')
    const modalCloses = document.querySelectorAll('[data-dismiss="modal"]');
    modalCloses.forEach(close => {
        close.addEventListener('click', () => {
            const modal = close.closest('.modal-overlay');
            if (modal) {
                modal.classList.add('hidden');
                modal.classList.remove('flex');
            }
        });
    });

    // Fecha dropdowns e modals se clicar fora deles
    window.addEventListener('click', (event) => {
        // Fecha dropdowns
        if (!event.target.closest('[data-toggle="dropdown"]')) {
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.classList.add('hidden');
            });
        }
        // Fecha modal se clicar no overlay (fundo)
        if (event.target.classList.contains('modal-overlay')) {
            event.target.classList.add('hidden');
            event.target.classList.remove('flex');
        }
    });

    // Ativa os ícones do Lucide (código que já tínhamos)
    if (typeof lucide !== "undefined") {
        lucide.createIcons();
    }
});
