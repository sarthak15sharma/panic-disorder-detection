const navbarMenu = document.querySelector(".navbar .links");
const hamburgerBtn = document.querySelector(".hamburger-btn");
const hideMenuBtn = navbarMenu.querySelector(".close-btn");
const showPopupBtn = document.querySelector(".take-assessment"); // Updated selector
const formPopup = document.querySelector(".form-popup");
const hidePopupBtn = formPopup.querySelector(".close-btn");
const predictionForm = document.getElementById("prediction-form");
const predictionResult = document.getElementById("prediction-result");

// Show mobile menu
hamburgerBtn.addEventListener("click", () => {
  navbarMenu.classList.toggle("show-menu");
});

// Hide mobile menu
hideMenuBtn.addEventListener("click", () => hamburgerBtn.click());

// Show assessment popup
showPopupBtn.addEventListener("click", (event) => {
  event.preventDefault(); // Prevent default link behavior
  document.body.classList.toggle("show-popup");
});

// Hide assessment popup (optional)
hidePopupBtn.addEventListener("click", () => showPopupBtn.click());

// Handle prediction form submission using AJAX
predictionForm.addEventListener("submit", (event) => {
  event.preventDefault(); // Prevent default form submission

  const formData = new FormData(predictionForm);

  fetch("/predict", {
    method: "POST",
    body: formData
  })
  .then(response => response.text())
  .then(data => {
    predictionResult.textContent = data; // Update prediction result paragraph
  })
  .catch(error => {
    console.error("Error submitting prediction form:", error);
    predictionResult.textContent = "An error occurred. Please try again.";
  });
});
