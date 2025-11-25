// --- FUNÇÕES GLOBAIS ---

// Definindo explicitamente na janela para garantir que o HTML encontre
window.toggleTheme = function() {
    console.log("Botão de tema clicado!"); // Debug para o console
    const html = document.documentElement;
    
    if (html.classList.contains('dark')) {
        html.classList.remove('dark');
        localStorage.setItem('theme', 'light');
    } else {
        html.classList.add('dark');
        localStorage.setItem('theme', 'dark');
    }
};

window.fecharModal = function(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
};

// Aplica o tema salvo IMEDIATAMENTE
(function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
})();

// ... (O resto do arquivo com document.addEventListener continua igual) ...

// --- INICIALIZAÇÃO ---
document.addEventListener("DOMContentLoaded", () => {
    console.log("Sistema iniciado.");

    if (typeof lucide !== "undefined") {
        lucide.createIcons();
    }

    // Dropdowns
    const dropdownToggles = document.querySelectorAll('[data-toggle="dropdown"]');
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', (event) => {
            event.stopPropagation();
            const targetId = toggle.getAttribute('data-target');
            const targetMenu = document.getElementById(targetId);
            
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                if (menu.id !== targetId) menu.classList.add('hidden');
            });

            if (targetMenu) targetMenu.classList.toggle('hidden');
        });
    });

    // Modals
    const modalToggles = document.querySelectorAll('[data-toggle="modal"]');
    modalToggles.forEach(toggle => {
        toggle.addEventListener('click', (event) => {
            event.preventDefault();
            document.querySelectorAll('.dropdown-menu').forEach(m => m.classList.add('hidden'));
            const targetId = toggle.getAttribute('data-target');
            const targetModal = document.getElementById(targetId);
            
            if (targetModal) {
                targetModal.classList.remove('hidden');
                targetModal.classList.add('flex');
            }
        });
    });

    // Fechar ao clicar fora
    window.addEventListener('click', (event) => {
        if (!event.target.closest('[data-toggle="dropdown"]') && !event.target.closest('.dropdown-menu')) {
            document.querySelectorAll('.dropdown-menu').forEach(menu => menu.classList.add('hidden'));
        }
        if (event.target.classList.contains('modal-overlay')) {
            event.target.classList.add('hidden');
            event.target.classList.remove('flex');
        }
    });
});