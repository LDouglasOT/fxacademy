// Theme toggle functionality
const themeToggle = document.getElementById('theme-toggle');
const html = document.documentElement;

// Check for saved theme preference or default to dark mode
const currentTheme = localStorage.getItem('theme') || 'dark';
html.classList.toggle('dark', currentTheme === 'dark');

// Update button icon and colors based on current theme
function updateThemeIcon() {
    const isDark = html.classList.contains('dark');
    themeToggle.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';

    // Update body background and text colors
    const body = document.body;
    if (isDark) {
        body.style.backgroundColor = '#005073';
        body.style.color = '#ffffff';
    } else {
        body.style.backgroundColor = '#ffffff';
        body.style.color = '#005073';
    }
}

updateThemeIcon();

// Toggle theme on button click
themeToggle.addEventListener('click', () => {
    html.classList.toggle('dark');
    const theme = html.classList.contains('dark') ? 'dark' : 'light';
    localStorage.setItem('theme', theme);
    updateThemeIcon();
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Animate elements on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-fade-in');
        }
    });
}, observerOptions);

// Observe elements for animation
document.querySelectorAll('.bg-primary, .bg-gray-900').forEach(el => {
    observer.observe(el);
});

// Add fade-in animation CSS
const style = document.createElement('style');
style.textContent = `
    .animate-fade-in {
        animation: fadeIn 0.6s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(style);