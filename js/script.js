console.log("script.js loaded");

let heading = document.getElementById("Welcome");
if (heading) {
  console.log("Heading element:", heading);
}

// 1. "click me" button alert functionality
function showWelcomeAlert() {
  alert("Welcome to Dr RVR NRI University");
}
window.showWelcomeAlert = showWelcomeAlert;

// 2. "changeheading" button functionality
function changeHeadingText() {
  let headingEl = document.getElementById("Welcome");
  if (!headingEl) return;
  headingEl.innerHTML = "Dr RVR NRI University";
  console.log("Heading changed to:", headingEl.innerHTML);
}
window.changeHeadingText = changeHeadingText;

// 3. "back" button functionality
function restoreHeadingText() {
  let headingEl = document.getElementById("Welcome");
  if (!headingEl) return;
  headingEl.innerHTML = "Welcome to NRIIT Learning Management System";
  console.log("Heading restored to:", headingEl.innerHTML);
  alert("Welcome to NRIIT Learning Management System");
}
window.restoreHeadingText = restoreHeadingText;

function connectButtons() {
  let imageBtn = document.getElementById("imageBtn");
  if (imageBtn && !imageBtn.getAttribute("onclick")) {
    imageBtn.removeEventListener("click", showWelcomeAlert);
    imageBtn.addEventListener("click", showWelcomeAlert);
  }

  let changeHeadingBtn = document.getElementById("changeHeadingBtn");
  if (changeHeadingBtn && !changeHeadingBtn.getAttribute("onclick")) {
    changeHeadingBtn.removeEventListener("click", changeHeadingText);
    changeHeadingBtn.addEventListener("click", changeHeadingText);
  }

  let backBtn = document.getElementById("backBtn");
  if (backBtn && !backBtn.getAttribute("onclick")) {
    backBtn.removeEventListener("click", restoreHeadingText);
    backBtn.addEventListener("click", restoreHeadingText);
  }
}

connectButtons();
document.addEventListener("DOMContentLoaded", connectButtons);

// Optional image click functionality (toggles image source)
let logoImage = document.getElementById("logoImage");
function toggleBannerImage() {
  if (!logoImage) return;
  let currentSrc = logoImage.getAttribute("src");
  if (currentSrc === "image/logo.png") {
    logoImage.setAttribute("src", "image/banner.jpg");
    logoImage.setAttribute("alt", "NRIIT Banner");
    console.log("Image changed to banner.jpg");
  } else {
    logoImage.setAttribute("src", "image/logo.png");
    logoImage.setAttribute("alt", "NRIIT Logo");
    console.log("Image changed to logo.png");
  }
}

if (logoImage) {
  logoImage.style.cursor = "pointer";
  logoImage.addEventListener("click", toggleBannerImage);
}

// Register form submission handler with localStorage storage
function handleRegister(event) {
  if (event) event.preventDefault();

  let nameEl = document.getElementById("regName");
  let emailEl = document.getElementById("regEmail");
  let passwordEl = document.getElementById("regPassword");
  let dobEl = document.getElementById("regDob");
  let courseEl = document.getElementById("regCourse");

  let nameVal = nameEl ? nameEl.value.trim() : "Student";
  let emailVal = emailEl ? emailEl.value.trim() : "";
  let passwordVal = passwordEl ? passwordEl.value : "";
  let dobVal = dobEl ? dobEl.value : "";
  let courseVal = courseEl ? courseEl.value : "";

  if (!emailVal || !passwordVal) {
    alert("Please enter both Email and Password!");
    return false;
  }

  let users = [];
  try {
    users = JSON.parse(localStorage.getItem("nriit_users")) || [];
  } catch (e) {
    users = [];
  }

  // Check if email already registered
  let existingIndex = users.findIndex(u => u.email.toLowerCase() === emailVal.toLowerCase());
  let userObj = {
    name: nameVal,
    email: emailVal,
    password: passwordVal,
    dob: dobVal,
    course: courseVal
  };

  if (existingIndex >= 0) {
    users[existingIndex] = userObj;
  } else {
    users.push(userObj);
  }

  localStorage.setItem("nriit_users", JSON.stringify(users));
  localStorage.setItem("nriit_last_registered_email", emailVal);

  alert("Registration Successful! Account stored for " + nameVal + " (" + emailVal + "). Welcome to Dr RVR NRI University!");
  console.log("Registered users stored:", users);

  let form = document.getElementById("registerForm");
  if (form) form.reset();

  window.location.href = "login.html";
  return false;
}
window.handleRegister = handleRegister;

// Login / Sign-in form submission handler
function handleLogin(event) {
  if (event) event.preventDefault();

  let emailEl = document.getElementById("loginEmail");
  let passwordEl = document.getElementById("loginPassword");
  let emailVal = emailEl ? emailEl.value.trim() : "";
  let passwordVal = passwordEl ? passwordEl.value : "";

  if (!emailVal || !passwordVal) {
    alert("Please enter both Email and Password!");
    return false;
  }

  let users = [];
  try {
    users = JSON.parse(localStorage.getItem("nriit_users")) || [];
  } catch (e) {
    users = [];
  }

  let foundUser = users.find(u => u.email.toLowerCase() === emailVal.toLowerCase());

  if (!foundUser) {
    alert("Account not found with email: " + emailVal + ". Please Register first!");
    return false;
  }

  if (foundUser.password !== passwordVal) {
    alert("Incorrect password for " + emailVal + "! Please check your credentials.");
    return false;
  }

  localStorage.setItem("nriit_current_user", JSON.stringify(foundUser));
  alert("Login Successful! Welcome back " + foundUser.name + " to Dr RVR NRI University.");
  console.log("Logged in user:", foundUser);

  window.location.href = "index.html";
  return false;
}
window.handleLogin = handleLogin;

function connectAuthForms() {
  let registerForm = document.getElementById("registerForm");
  if (registerForm && !registerForm.getAttribute("onsubmit")) {
    registerForm.addEventListener("submit", handleRegister);
  }

  let loginForm = document.getElementById("loginForm");
  if (loginForm && !loginForm.getAttribute("onsubmit")) {
    loginForm.addEventListener("submit", handleLogin);
  }

  // Pre-fill email on login page if just registered
  let loginEmailInput = document.getElementById("loginEmail");
  if (loginEmailInput && !loginEmailInput.value) {
    let lastEmail = localStorage.getItem("nriit_last_registered_email");
    if (lastEmail) {
      loginEmailInput.value = lastEmail;
    }
  }

  // Personalize homepage message if logged in
  let messageEl = document.getElementById("message");
  if (messageEl) {
    try {
      let currentUser = JSON.parse(localStorage.getItem("nriit_current_user"));
      if (currentUser && currentUser.name) {
        messageEl.innerHTML = "Learning never Stops, <strong>" + currentUser.name + "</strong>!";
      }
    } catch (e) {}
  }
}

connectAuthForms();
document.addEventListener("DOMContentLoaded", connectAuthForms);
