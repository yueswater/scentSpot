document.addEventListener("DOMContentLoaded", () => {
  const alerts = document.querySelectorAll(".alert");

  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.classList.add("opacity-0", "transition-opacity", "duration-500");
      setTimeout(() => alert.remove(), 500);
    }, 3000);
  });
});
