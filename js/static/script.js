console.log("NRIIT LMS REST API script.js loaded");

// --- API Utility Function for GET, POST, PUT, DELETE ---
async function apiFetch(endpoint, method = 'GET', data = null) {
  const options = {
    method: method,
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    }
  };

  if (data && (method === 'POST' || method === 'PUT')) {
    options.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(endpoint, options);
    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || `HTTP error! Status: ${response.status}`);
    }
    return result;
  } catch (error) {
    console.error(`API Error [${method} ${endpoint}]:`, error);
    showNotification(`Error: ${error.message}`, 'error', method);
    throw error;
  }
}

// --- Notification Banner Helper ---
function showNotification(message, type = 'success', method = 'INFO') {
  let alertContainer = document.getElementById("apiNotification");
  if (!alertContainer) {
    alertContainer = document.createElement("div");
    alertContainer.id = "apiNotification";
    document.body.prepend(alertContainer);
  }

  const badgeClass = {
    'GET': 'badge-get',
    'POST': 'badge-post',
    'PUT': 'badge-put',
    'DELETE': 'badge-delete'
  }[method] || 'badge-get';

  const alertClass = type === 'error' ? 'api-alert-error' : (type === 'info' ? 'api-alert-info' : 'api-alert-success');

  alertContainer.innerHTML = `
    <div class="api-alert ${alertClass}">
      <span>${message}</span>
    </div>
  `;

  setTimeout(() => {
    if (alertContainer) alertContainer.innerHTML = '';
  }, 4000);
}

// --- Legacy Heading Buttons & Interactivity ---
function showWelcomeAlert() {
  alert("Welcome to Dr RVR NRI University");
}

function changeHeadingText() {
  let headingEl = document.getElementById("Welcome");
  if (!headingEl) return;
  headingEl.innerHTML = "Dr RVR NRI University";
}

function restoreHeadingText() {
  let headingEl = document.getElementById("Welcome");
  if (!headingEl) return;
  headingEl.innerHTML = "Welcome to NRIIT Learning Management System";
  alert("Welcome to NRIIT Learning Management System");
}

window.showWelcomeAlert = showWelcomeAlert;
window.changeHeadingText = changeHeadingText;
window.restoreHeadingText = restoreHeadingText;

// --- 1. HOMEPAGE MODULE (index.html) ---
async function initHomePage() {
  // Load Stats via GET
  const statsContainer = document.getElementById("statsContainer");
  if (statsContainer) {
    try {
      const res = await apiFetch('/api/stats', 'GET');
      if (res.success && res.stats) {
        statsContainer.innerHTML = `
          <div class="stat-card">
            <h4>${res.stats.students_enrolled}</h4>
            <p>Students Enrolled</p>
          </div>
          <div class="stat-card">
            <h4>${res.stats.courses_offered}</h4>
            <p>Courses Offered</p>
          </div>
          <div class="stat-card">
            <h4>${res.stats.expert_trainers}</h4>
            <p>Expert Trainers</p>
          </div>
          <div class="stat-card">
            <h4>${res.stats.active_inquiries}</h4>
            <p>Active Inquiries</p>
          </div>
        `;
      }
    } catch (e) {
      console.warn("Could not load stats", e);
    }
  }

  // Load Registered Users List via GET
  loadRegisteredUsersList();
}

async function loadRegisteredUsersList() {
  const usersContainer = document.getElementById("registeredUsersList");
  if (!usersContainer) return;

  try {
    const res = await apiFetch('/api/users', 'GET');
    if (res.success && res.users) {
      if (res.users.length === 0) {
        usersContainer.innerHTML = "<p>No users registered yet.</p>";
        return;
      }

      let html = `
        <table border="1" cellpadding="8">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Enrolled Course</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
      `;

      res.users.forEach(u => {
        html += `
          <tr>
            <td>${u.id}</td>
            <td><strong>${u.name}</strong></td>
            <td>${u.email}</td>
            <td>${u.course}</td>
            <td>
              <button class="btn btn-sm btn-put" onclick="editUserPrompt(${u.id}, '${u.name}', '${u.course}')">
                Edit
              </button>
              <button class="btn btn-sm btn-delete" onclick="deleteUser(${u.id}, '${u.name}')">
                Remove
              </button>
            </td>
          </tr>
        `;
      });

      html += `</tbody></table>`;
      usersContainer.innerHTML = html;
    }
  } catch (e) {
    usersContainer.innerHTML = "<p style='color:red;'>Failed to load user list from server.</p>";
  }
}

// User Edit via PUT /api/users/<id>
async function editUserPrompt(id, currentName, currentCourse) {
  const newName = prompt("Enter updated Name:", currentName);
  if (newName === null) return;
  const newCourse = prompt("Enter updated Course:", currentCourse);
  if (newCourse === null) return;

  try {
    const res = await apiFetch(`/api/users/${id}`, 'PUT', { name: newName, course: newCourse });
    if (res.success) {
      showNotification(res.message, 'success', 'PUT');
      loadRegisteredUsersList();
      initHomePage();
    }
  } catch (e) {
    showNotification(e.message, 'error', 'PUT');
  }
}

// User Delete via DELETE /api/users/<id>
async function deleteUser(id, name) {
  if (!confirm(`Are you sure you want to delete user '${name}'?`)) return;

  try {
    const res = await apiFetch(`/api/users/${id}`, 'DELETE');
    if (res.success) {
      showNotification(res.message, 'success', 'DELETE');
      loadRegisteredUsersList();
      initHomePage();
    }
  } catch (e) {
    showNotification(e.message, 'error', 'DELETE');
  }
}

window.editUserPrompt = editUserPrompt;
window.deleteUser = deleteUser;


// --- 2. COURSES MODULE (courses.html) ---
async function initCoursesPage() {
  loadCourses();

  const addForm = document.getElementById("addCourseForm");
  if (addForm) {
    addForm.addEventListener("submit", handleAddCourse);
  }
}

async function loadCourses() {
  const tableContainer = document.getElementById("coursesTableContainer");
  if (!tableContainer) return;

  try {
    const res = await apiFetch('/api/courses', 'GET');
    if (res.success && res.courses) {
      let html = `
        <table border="1" cellpadding="10">
          <thead>
            <tr>
              <th>ID</th>
              <th>Course Title</th>
              <th>Duration</th>
              <th>Mode</th>
              <th>Topics Covered</th>
              <th>Trainer</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
      `;

      res.courses.forEach(c => {
        html += `
          <tr>
            <td>${c.id}</td>
            <td><strong>${c.title}</strong></td>
            <td>${c.duration}</td>
            <td>${c.mode}</td>
            <td>${c.topics}</td>
            <td>${c.trainer}</td>
            <td>
              <button class="btn btn-sm btn-put" onclick="editCoursePrompt(${c.id}, '${c.title.replace(/'/g, "\\'")}', '${c.duration}', '${c.mode}')">
                Edit
              </button>
              <button class="btn btn-sm btn-delete" onclick="deleteCourse(${c.id}, '${c.title.replace(/'/g, "\\'")}')">
                Delete
              </button>
            </td>
          </tr>
        `;
      });

      html += `</tbody></table>`;
      tableContainer.innerHTML = html;
    }
  } catch (e) {
    tableContainer.innerHTML = "<p style='color:red;'>Failed to fetch courses from backend API.</p>";
  }
}

// Add Course via POST /api/courses
async function handleAddCourse(e) {
  if (e) e.preventDefault();

  const titleEl = document.getElementById("newCourseTitle");
  const durationEl = document.getElementById("newCourseDuration");
  const modeEl = document.getElementById("newCourseMode");
  const topicsEl = document.getElementById("newCourseTopics");
  const trainerEl = document.getElementById("newCourseTrainer");

  const newCourseData = {
    title: titleEl ? titleEl.value.trim() : '',
    duration: durationEl ? durationEl.value.trim() : '3 Months',
    mode: modeEl ? modeEl.value : 'Offline',
    topics: topicsEl ? topicsEl.value.trim() : 'Core Concepts',
    trainer: trainerEl ? trainerEl.value.trim() : 'Faculty'
  };

  if (!newCourseData.title) {
    alert("Please enter a course title!");
    return;
  }

  try {
    const res = await apiFetch('/api/courses', 'POST', newCourseData);
    if (res.success) {
      showNotification(res.message, 'success', 'POST');
      if (document.getElementById("addCourseForm")) document.getElementById("addCourseForm").reset();
      loadCourses();
    }
  } catch (err) {
    showNotification(err.message, 'error', 'POST');
  }
}

// Edit Course via PUT /api/courses/<id>
async function editCoursePrompt(id, currentTitle, currentDuration, currentMode) {
  const newTitle = prompt("Update Course Title:", currentTitle);
  if (newTitle === null) return;
  const newDuration = prompt("Update Duration:", currentDuration);
  if (newDuration === null) return;
  const newMode = prompt("Update Mode (Online / Offline / Hybrid):", currentMode);
  if (newMode === null) return;

  try {
    const res = await apiFetch(`/api/courses/${id}`, 'PUT', {
      title: newTitle,
      duration: newDuration,
      mode: newMode
    });
    if (res.success) {
      showNotification(res.message, 'success', 'PUT');
      loadCourses();
    }
  } catch (err) {
    showNotification(err.message, 'error', 'PUT');
  }
}

// Delete Course via DELETE /api/courses/<id>
async function deleteCourse(id, title) {
  if (!confirm(`Are you sure you want to delete course '${title}'?`)) return;

  try {
    const res = await apiFetch(`/api/courses/${id}`, 'DELETE');
    if (res.success) {
      showNotification(res.message, 'success', 'DELETE');
      loadCourses();
    }
  } catch (err) {
    showNotification(err.message, 'error', 'DELETE');
  }
}

window.editCoursePrompt = editCoursePrompt;
window.deleteCourse = deleteCourse;


// --- 3. TRAINERS MODULE (trainers.html) ---
async function initTrainersPage() {
  loadTrainers();

  const addTrainerForm = document.getElementById("addTrainerForm");
  if (addTrainerForm) {
    addTrainerForm.addEventListener("submit", handleAddTrainer);
  }
}

async function loadTrainers() {
  const trainersContainer = document.getElementById("trainersListContainer");
  if (!trainersContainer) return;

  try {
    const res = await apiFetch('/api/trainers', 'GET');
    if (res.success && res.trainers) {
      let html = '';
      res.trainers.forEach(t => {
        html += `
          <article style="margin-bottom: 1.5rem;">
            <img src="../image/static/logo.png" alt="${t.name}" width="120">
            <h3>${t.name}</h3>
            <p><strong>Role:</strong> ${t.role}</p>
            <p><strong>Experience:</strong> ${t.experience}</p>
            <p><strong>Specialization:</strong> ${t.specialization}</p>
            <div style="margin-top: 1rem;">
              <button class="btn btn-sm btn-put" onclick="editTrainerPrompt(${t.id}, '${t.name.replace(/'/g, "\\'")}', '${t.role.replace(/'/g, "\\'")}')">
                Edit Trainer
              </button>
              <button class="btn btn-sm btn-delete" onclick="deleteTrainer(${t.id}, '${t.name.replace(/'/g, "\\'")}')">
                Remove Trainer
              </button>
            </div>
          </article>
        `;
      });
      trainersContainer.innerHTML = html;
    }
  } catch (e) {
    trainersContainer.innerHTML = "<p style='color:red;'>Failed to load trainers from backend API.</p>";
  }
}

// Add Trainer via POST /api/trainers
async function handleAddTrainer(e) {
  if (e) e.preventDefault();

  const nameEl = document.getElementById("trainerName");
  const roleEl = document.getElementById("trainerRole");
  const expEl = document.getElementById("trainerExperience");
  const specEl = document.getElementById("trainerSpec");

  const trainerData = {
    name: nameEl ? nameEl.value.trim() : '',
    role: roleEl ? roleEl.value.trim() : 'Instructor',
    experience: expEl ? expEl.value.trim() : '2+ years',
    specialization: specEl ? specEl.value.trim() : 'FullStack'
  };

  if (!trainerData.name) {
    alert("Please enter trainer name!");
    return;
  }

  try {
    const res = await apiFetch('/api/trainers', 'POST', trainerData);
    if (res.success) {
      showNotification(res.message, 'success', 'POST');
      if (document.getElementById("addTrainerForm")) document.getElementById("addTrainerForm").reset();
      loadTrainers();
    }
  } catch (err) {
    showNotification(err.message, 'error', 'POST');
  }
}

// Edit Trainer via PUT /api/trainers/<id>
async function editTrainerPrompt(id, currentName, currentRole) {
  const newName = prompt("Update Trainer Name:", currentName);
  if (newName === null) return;
  const newRole = prompt("Update Role:", currentRole);
  if (newRole === null) return;

  try {
    const res = await apiFetch(`/api/trainers/${id}`, 'PUT', { name: newName, role: newRole });
    if (res.success) {
      showNotification(res.message, 'success', 'PUT');
      loadTrainers();
    }
  } catch (err) {
    showNotification(err.message, 'error', 'PUT');
  }
}

// Delete Trainer via DELETE /api/trainers/<id>
async function deleteTrainer(id, name) {
  if (!confirm(`Are you sure you want to remove trainer '${name}'?`)) return;

  try {
    const res = await apiFetch(`/api/trainers/${id}`, 'DELETE');
    if (res.success) {
      showNotification(res.message, 'success', 'DELETE');
      loadTrainers();
    }
  } catch (err) {
    showNotification(err.message, 'error', 'DELETE');
  }
}

window.editTrainerPrompt = editTrainerPrompt;
window.deleteTrainer = deleteTrainer;


// --- 4. AUTHENTICATION MODULE (register.html & login.html) ---
async function handleRegister(event) {
  if (event) event.preventDefault();

  let nameEl = document.getElementById("regName");
  let emailEl = document.getElementById("regEmail");
  let passwordEl = document.getElementById("regPassword");
  let dobEl = document.getElementById("regDob");
  let courseEl = document.getElementById("regCourse");
  let genderEl = document.querySelector('input[name="gender"]:checked');

  let nameVal = nameEl ? nameEl.value.trim() : "Student";
  let emailVal = emailEl ? emailEl.value.trim() : "";
  let passwordVal = passwordEl ? passwordEl.value : "";
  let dobVal = dobEl ? dobEl.value : "";
  let courseVal = courseEl ? courseEl.value : "Python FullStack";
  let genderVal = genderEl ? genderEl.value : "Male";

  if (!emailVal || !passwordVal) {
    alert("Please enter both Email and Password!");
    return false;
  }

  const payload = {
    name: nameVal,
    email: emailVal,
    password: passwordVal,
    dob: dobVal,
    course: courseVal,
    gender: genderVal
  };

  try {
    // POST request to backend
    const res = await apiFetch('/api/register', 'POST', payload);
    if (res.success) {
      localStorage.setItem("nriit_last_registered_email", emailVal);
      showNotification(res.message, 'success', 'POST');
      alert(`Registration Successful for ${nameVal}! Please login.`);
      window.location.href = "/login";
    }
  } catch (err) {
    alert(err.message || "Registration failed!");
    showNotification(err.message, 'error', 'POST');
  }

  return false;
}
window.handleRegister = handleRegister;

async function handleLogin(event) {
  if (event) event.preventDefault();

  let emailEl = document.getElementById("loginEmail");
  let passwordEl = document.getElementById("loginPassword");
  let emailVal = emailEl ? emailEl.value.trim() : "";
  let passwordVal = passwordEl ? passwordEl.value : "";

  if (!emailVal || !passwordVal) {
    alert("Please enter both Email and Password!");
    return false;
  }

  const payload = {
    email: emailVal,
    password: passwordVal
  };

  try {
    // POST request to backend
    const res = await apiFetch('/api/login', 'POST', payload);
    if (res.success && res.user) {
      localStorage.setItem("nriit_current_user", JSON.stringify(res.user));
      showNotification(res.message, 'success', 'POST');
      alert(`Welcome back, ${res.user.name}!`);
      window.location.href = "/";
    }
  } catch (err) {
    alert(err.message || "Login failed! Please check your credentials.");
    showNotification(err.message, 'error', 'POST');
  }

  return false;
}
window.handleLogin = handleLogin;


// --- 5. CONTACT & INQUIRIES MODULE (contact.html) ---
async function initContactPage() {
  loadContacts();

  const contactForm = document.getElementById("contactForm");
  if (contactForm) {
    contactForm.addEventListener("submit", handleContactSubmit);
  }
}

async function handleContactSubmit(e) {
  if (e) e.preventDefault();

  const nameEl = document.getElementById("contactName");
  const emailEl = document.getElementById("contactEmail");
  const msgEl = document.getElementById("contactMessage");

  const payload = {
    name: nameEl ? nameEl.value.trim() : '',
    email: emailEl ? emailEl.value.trim() : '',
    message: msgEl ? msgEl.value.trim() : ''
  };

  if (!payload.name || !payload.email || !payload.message) {
    alert("Please fill out Name, Email, and Message!");
    return;
  }

  try {
    const res = await apiFetch('/api/contacts', 'POST', payload);
    if (res.success) {
      showNotification(res.message, 'success', 'POST');
      if (document.getElementById("contactForm")) document.getElementById("contactForm").reset();
      loadContacts();
    }
  } catch (err) {
    showNotification(err.message, 'error', 'POST');
  }
}

async function loadContacts() {
  const container = document.getElementById("contactsListContainer");
  if (!container) return;

  try {
    const res = await apiFetch('/api/contacts', 'GET');
    if (res.success && res.contacts) {
      if (res.contacts.length === 0) {
        container.innerHTML = "<p>No active inquiries found.</p>";
        return;
      }

      let html = `
        <table border="1" cellpadding="8">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Message</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
      `;

      res.contacts.forEach(c => {
        const isResolved = c.status === 'Resolved';
        html += `
          <tr>
            <td>${c.id}</td>
            <td><strong>${c.name}</strong></td>
            <td>${c.email}</td>
            <td>${c.message}</td>
            <td><span class="badge ${isResolved ? 'badge-get' : 'badge-put'}">${c.status}</span></td>
            <td>
              <button class="btn btn-sm btn-put" onclick="toggleContactStatus(${c.id}, '${c.status}')">
                ${isResolved ? 'Mark Pending' : 'Mark Resolved'}
              </button>
              <button class="btn btn-sm btn-delete" onclick="deleteContact(${c.id})">
                Delete
              </button>
            </td>
          </tr>
        `;
      });

      html += `</tbody></table>`;
      container.innerHTML = html;
    }
  } catch (e) {
    container.innerHTML = "<p style='color:red;'>Failed to load contact inquiries.</p>";
  }
}

// Update Inquiry Status via PUT /api/contacts/<id>
async function toggleContactStatus(id, currentStatus) {
  const newStatus = currentStatus === 'Resolved' ? 'Pending' : 'Resolved';
  try {
    const res = await apiFetch(`/api/contacts/${id}`, 'PUT', { status: newStatus });
    if (res.success) {
      showNotification(res.message, 'success', 'PUT');
      loadContacts();
    }
  } catch (err) {
    showNotification(err.message, 'error', 'PUT');
  }
}

// Delete Inquiry via DELETE /api/contacts/<id>
async function deleteContact(id) {
  if (!confirm(`Are you sure you want to delete inquiry ID ${id}?`)) return;

  try {
    const res = await apiFetch(`/api/contacts/${id}`, 'DELETE');
    if (res.success) {
      showNotification(res.message, 'success', 'DELETE');
      loadContacts();
    }
  } catch (err) {
    showNotification(err.message, 'error', 'DELETE');
  }
}

window.toggleContactStatus = toggleContactStatus;
window.deleteContact = deleteContact;


// --- DOM INITIALIZATION ROUTER ---
document.addEventListener("DOMContentLoaded", () => {
  // Pre-fill email on login page if registered
  const loginEmailInput = document.getElementById("loginEmail");
  if (loginEmailInput && !loginEmailInput.value) {
    let lastEmail = localStorage.getItem("nriit_last_registered_email");
    if (lastEmail) loginEmailInput.value = lastEmail;
  }

  // Personalize welcome message if logged in
  const messageEl = document.getElementById("message");
  if (messageEl) {
    try {
      let currentUser = JSON.parse(localStorage.getItem("nriit_current_user"));
      if (currentUser && currentUser.name) {
        messageEl.innerHTML = `Learning never Stops, <strong>${currentUser.name}</strong>! (<a href="#" onclick="handleLogout(event)" style="font-size:0.9rem;">Logout</a>)`;
      }
    } catch (e) {}
  }

  // Page Specific Inits
  initHomePage();
  initCoursesPage();
  initTrainersPage();
  initContactPage();
});

function handleLogout(e) {
  if (e) e.preventDefault();
  localStorage.removeItem("nriit_current_user");
  alert("You have logged out.");
  window.location.reload();
}
window.handleLogout = handleLogout;

