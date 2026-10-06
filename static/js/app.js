// Expense Tracker - Frontend helpers

document.addEventListener("DOMContentLoaded", () => {
    // Auto-hide flash messages
    setTimeout(() => {
        document.querySelectorAll(".flash").forEach((el) => {
            el.style.opacity = "0";
            el.style.transition = "opacity .4s";

            setTimeout(() => el.remove(), 400);
        });
    }, 3200);

    // Prevent accidental double submission
    const transactionForm = document.querySelector(".transaction-form");

    if (transactionForm) {
        transactionForm.addEventListener("submit", (event) => {
            const submitButton = transactionForm.querySelector(
                'button[type="submit"], button:not([type])'
            );

            if (transactionForm.dataset.submitting === "true") {
                event.preventDefault();
                return;
            }

            transactionForm.dataset.submitting = "true";

            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = "Adding...";
            }
        });
    }
});