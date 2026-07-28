// Main application JavaScript
console.log("script.js loaded");
alert("Welcome to NRIIT Learning Management System!");

document.addEventListener("DOMContentLoaded", () => {
  // 1. Highlight the active navigation link based on the current page
  const currentPage = window.location.pathname.split("/").pop() || "index.html";
  const navLinks = document.querySelectorAll("header nav a");

  navLinks.forEach((link) => {
    const linkPage = link.getAttribute("href");
    if (linkPage === currentPage) {
      link.style.backgroundColor = "rgba(255, 255, 255, 0.35)";
      link.style.fontWeight = "bold";
    }
  });

  // 2. Add interactive confirmation for form submissions (Login, Register, Contact)
  const forms = document.querySelectorAll("form");
  forms.forEach((form) => {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      alert("Form submitted successfully! Thank you for connecting with NRIIT.");
    });
  });

  // 3. Smooth fade-in animation for section elements
  const sections = document.querySelectorAll("main section");
  sections.forEach((section, index) => {
    section.style.opacity = "0";
    section.style.transition = "opacity 0.6s ease-in-out";
    setTimeout(() => {
      section.style.opacity = "1";
    }, index * 150);
  });
});
