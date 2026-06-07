// Light/Dark theme toggle
(function() {
    const html = document.documentElement;
    const btn = document.getElementById("themeToggle");
    const icon = document.getElementById("themeIcon");
    const saved = localStorage.getItem("theme") || "light";

    html.setAttribute("data-bs-theme", saved);
    updateIcon(saved);

    btn?.addEventListener("click", () => {
        const current = html.getAttribute("data-bs-theme");
        const next = current === "dark" ? "light" : "dark";
        html.setAttribute("data-bs-theme", next);
        localStorage.setItem("theme", next);
        updateIcon(next);
    });

    function updateIcon(theme) {
        if (icon) {
            icon.className = theme === "dark" ? "bi bi-sun-fill" : "bi bi-moon-fill";
        }
    }
})();
