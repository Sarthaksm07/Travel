// AugyTravel — small progressive enhancements (no framework).
document.addEventListener("DOMContentLoaded", function () {
    // Mobile nav toggle
    const btn = document.querySelector("[data-nav-toggle]");
    const menu = document.querySelector("[data-mobile-menu]");
    if (btn && menu) {
        btn.addEventListener("click", () => menu.classList.toggle("hidden"));
    }

    // Turn text date inputs into date pickers on focus
    document.querySelectorAll('input[data-date]').forEach((el) => {
        el.addEventListener("focus", () => (el.type = "date"));
        el.addEventListener("blur", () => { if (!el.value) el.type = "text"; });
    });
});
