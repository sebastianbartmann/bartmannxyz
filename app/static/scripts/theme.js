document.querySelectorAll("[data-theme-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
        const html = document.documentElement;
        const isDark = html.classList.toggle("dark");
        localStorage.theme = isDark ? "dark" : "light";
    });
});
