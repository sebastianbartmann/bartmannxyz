document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
        const html = document.documentElement;
        const isDark = html.classList.toggle("dark");
        localStorage.theme = isDark ? "dark" : "light";
    });
});

// Small screens: the navigation opens below the header row.
document.querySelectorAll("[data-menu-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
        const isOpen = button.closest(".site-header").classList.toggle("site-header--menu-open");
        button.setAttribute("aria-expanded", String(isOpen));
    });
});
