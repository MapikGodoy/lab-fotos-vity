// ==========================================
// DESKTOPIA LAB - UTILIDADES GLOBALES
// ==========================================

function mostrarToast(mensaje, tipo = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    const colores = {
        success: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
        error: 'bg-red-500/20 text-red-400 border-red-500/30',
        info: 'bg-indigo-500/20 text-indigo-400 border-indigo-500/30'
    };
    
    toast.className = `toast-enter flex items-center gap-3 px-5 py-3 rounded-xl font-medium shadow-2xl border backdrop-blur-md text-sm ${colores[tipo] || colores.info}`;
    toast.innerHTML = `<span>${mensaje}</span>`;
    container.appendChild(toast);
    
    setTimeout(() => { 
        toast.classList.replace('toast-enter', 'toast-exit'); 
        setTimeout(() => toast.remove(), 300); 
    }, 4000);
}
