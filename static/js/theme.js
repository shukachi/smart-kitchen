// Инициализация темы при загрузке
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = savedTheme === 'auto' ? (systemPrefersDark ? 'dark' : 'light') : savedTheme;
    
    document.documentElement.setAttribute('data-theme', theme);
    
    // Обновляем переключатель
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.checked = theme === 'dark';
    }
    
    // Обновляем meta theme-color
    updateMetaThemeColor(theme);
});

// Функция для переключения темы
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Обновляем переключатель
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.checked = newTheme === 'dark';
    }
    
    // Обновляем meta theme-color
    updateMetaThemeColor(newTheme);
}

// Функция для обновления meta theme-color
function updateMetaThemeColor(theme) {
    let metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (!metaThemeColor) {
        metaThemeColor = document.createElement('meta');
        metaThemeColor.name = 'theme-color';
        document.head.appendChild(metaThemeColor);
    }
    metaThemeColor.content = theme === 'dark' ? '#0f172a' : '#ffffff';
}

