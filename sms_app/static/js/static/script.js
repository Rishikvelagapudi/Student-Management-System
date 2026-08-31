// ==========================================================================
// NRIIT Student Management System - Interactive Frontend Logic
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
  initStats();
  initStudents();
  initCourses();
  initTrainers();
  initAdmin();
  initAuth();
  initContact();
  initModals();
});

// Helper: Toast Notifications
function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${type === 'error' ? '❌' : type === 'success' ? '✅' : 'ℹ️'}</span> <div>${message}</div>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

// Helper: API Fetcher
async function apiFetch(url, method = 'GET', data = null) {
  const options = {
    method,
    headers: { 'Content-Type': 'application/json' }
  };
  if (data) {
    options.body = JSON.stringify(data);
  }
  try {
    const res = await fetch(url, options);
    const json = await res.json();
    return json;
  } catch (err) {
    console.error('API Error:', err);
    showToast('Network error or server unreachable', 'error');
    return { success: false, message: 'Server error' };
  }
}

// Counter Animation for Dashboard & Hero Stats
function animateCounter(elemId, target) {
  const elem = document.getElementById(elemId);
  if (!elem) return;
  let current = 0;
  const increment = Math.max(1, Math.ceil(target / 25));
  const timer = setInterval(() => {
    current += increment;
    if (current >= target) {
      current = target;
      clearInterval(timer);
    }
    elem.textContent = current;
  }, 40);
}

// 1. Stats Loader
async function initStats() {
  const res = await apiFetch('/api/stats');
  if (res.success && res.stats) {
    animateCounter('stat-students', res.stats.students_enrolled);
    animateCounter('stat-courses', res.stats.courses_offered);
    animateCounter('stat-trainers', res.stats.expert_trainers);
    animateCounter('stat-inquiries', res.stats.active_inquiries);

    animateCounter('admin-stat-students', res.stats.students_enrolled);
    animateCounter('admin-stat-courses', res.stats.courses_offered);
    animateCounter('admin-stat-trainers', res.stats.expert_trainers);
}

// 2. Students Directory Logic
async function initStudents() {
  const container = document.getElementById('students-grid');
  if (!container) return;

  const res = await apiFetch('/api/students');
  if (res.success && res.users) {
    window.allStudents = res.users;
    renderStudents(window.allStudents);

    const searchInput = document.getElementById('studentSearchInput');
    const filterSelect = document.getElementById('courseFilterSelect');

    const filterHandler = () => {
      const q = (searchInput ? searchInput.value : '').toLowerCase();
      const course = filterSelect ? filterSelect.value : 'ALL';

      const filtered = window.allStudents.filter(s => {
        const matchesQuery = (s.name || '').toLowerCase().includes(q) ||
                             (s.email || '').toLowerCase().includes(q) ||
                             (s.course || '').toLowerCase().includes(q);
        const matchesCourse = (course === 'ALL') || ((s.course || '').toLowerCase() === course.toLowerCase());
        return matchesQuery && matchesCourse;
      });
      renderStudents(filtered);
    };

    if (searchInput) searchInput.addEventListener('input', filterHandler);
    if (filterSelect) filterSelect.addEventListener('change', filterHandler);
  }
}

function renderStudents(students) {
  const container = document.getElementById('students-grid');
  if (!container) return;

  if (!students || students.length === 0) {
    container.innerHTML = `<div class="glass-panel" style="grid-column: 1 / -1; text-align: center; color: var(--text-muted);">No registered students found matching your criteria.</div>`;
    return;
  }

  container.innerHTML = students.map(s => `
    <div class="card">
      <div class="card-header">
        <div style="display: flex; align-items: center; gap: 0.85rem;">
          <div class="avatar" style="width: 48px; height: 48px; font-size: 1.25rem;">${(s.name || 'S').charAt(0)}</div>
          <div>
            <h3 class="card-title">${s.name}</h3>
            <p style="font-size: 0.84rem; color: var(--text-secondary);">${s.email}</p>
          </div>
        </div>
      </div>
      <div class="card-body">
        <p class="card-text" style="margin-bottom: 0.5rem;">
          <strong>Enrolled Track:</strong>
          <span class="badge badge-mode" style="margin-left: 0.25rem;">${s.course || 'Python FullStack'}</span>
        </p>
        <div class="card-topics" style="margin-top: 0.65rem;">
          <div><strong>DOB:</strong> ${s.dob || 'N/A'} | <strong>Gender:</strong> ${s.gender || 'N/A'}</div>
          ${s.created_at ? `<div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 0.25rem;">Registered: ${s.created_at.substring(0, 10)}</div>` : ''}
        </div>
      </div>
      <div class="card-footer" style="justify-content: space-between;">
        <span style="font-size: 0.82rem; font-weight: 600; color: var(--accent-cyan);">Status: Active</span>
        <button onclick="window.location.href='/courses'" class="btn btn-outline btn-sm">View Track →</button>
      </div>
    </div>
  `).join('');
}

// 3. Courses Logic
async function initCourses() {
  const container = document.getElementById('courses-grid');
  if (!container) return;

  const res = await apiFetch('/api/courses');
  if (res.success && res.courses) {
    container.innerHTML = res.courses.map(c => `
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">${c.title}</h3>
          <span class="badge badge-duration">${c.duration || '3 Months'}</span>
        </div>
        <div class="card-body">
          <p class="card-text"><strong>Mode:</strong> <span class="badge badge-mode">${c.mode || 'Online'}</span></p>
          <div class="card-topics">
            <strong>Topics:</strong> ${c.topics || 'N/A'}
          </div>
        </div>
        <div class="card-footer">
          <div class="trainer-info">
            <div class="avatar">${(c.trainer || 'Faculty').charAt(0)}</div>
            <span style="font-size: 0.88rem; font-weight: 600;">${c.trainer || 'Faculty'}</span>
          </div>
          <div style="display: flex; gap: 0.5rem;">
            <button onclick="editCourse(${c.id}, '${escapeHtml(c.title)}', '${escapeHtml(c.duration)}', '${escapeHtml(c.mode)}', '${escapeHtml(c.topics)}', '${escapeHtml(c.trainer)}')" class="btn btn-outline btn-sm">Edit</button>
            <button onclick="deleteCourse(${c.id})" class="btn btn-danger btn-sm">Delete</button>
          </div>
        </div>
      </div>
    `).join('');
  }

  const courseForm = document.getElementById('courseForm');
  if (courseForm) {
    courseForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const id = document.getElementById('courseId').value;
      const payload = {
        title: document.getElementById('courseTitle').value,
        duration: document.getElementById('courseDuration').value,
        mode: document.getElementById('courseMode').value,
        topics: document.getElementById('courseTopics').value,
        trainer: document.getElementById('courseTrainer').value
      };

      const url = id ? `/api/courses/${id}` : '/api/courses';
      const method = id ? 'PUT' : 'POST';
      const res = await apiFetch(url, method, payload);

      if (res.success) {
        showToast(res.message, 'success');
        document.getElementById('courseModal').classList.remove('active');
        initCourses();
        initStats();
      } else {
        showToast(res.message || 'Action failed', 'error');
      }
    });
  }
}

function escapeHtml(str) {
  return (str || '').replace(/'/g, "\\'").replace(/"/g, '&quot;');
}

window.editCourse = function(id, title, duration, mode, topics, trainer) {
  document.getElementById('courseId').value = id;
  document.getElementById('courseTitle').value = title;
  document.getElementById('courseDuration').value = duration;
  document.getElementById('courseMode').value = mode;
  document.getElementById('courseTopics').value = topics;
  document.getElementById('courseTrainer').value = trainer;
  document.getElementById('modalCourseTitle').textContent = 'Edit Course';
  document.getElementById('courseModal').classList.add('active');
};

window.deleteCourse = async function(id) {
  if (confirm('Are you sure you want to delete this course?')) {
    const res = await apiFetch(`/api/courses/${id}`, 'DELETE');
    if (res.success) {
      showToast(res.message, 'success');
      initCourses();
      initStats();
    } else {
      showToast(res.message, 'error');
    }
  }
};

// 3. Trainers Logic
async function initTrainers() {
  const container = document.getElementById('trainers-grid');
  if (!container) return;

  const res = await apiFetch('/api/trainers');
  if (res.success && res.trainers) {
    container.innerHTML = res.trainers.map(t => `
      <div class="card">
        <div class="card-header">
          <div style="display: flex; align-items: center; gap: 0.85rem;">
            <div class="avatar" style="width: 48px; height: 48px; font-size: 1.25rem;">${(t.name || 'T').charAt(0)}</div>
            <div>
              <h3 class="card-title">${t.name}</h3>
              <p style="font-size: 0.82rem; color: var(--accent-cyan); font-weight: 600;">${t.role || 'Instructor'}</p>
            </div>
          </div>
          <span class="badge badge-mode">${t.experience || '3+ yrs'}</span>
        </div>
        <div class="card-body">
          <div class="card-topics" style="margin-top: 0.5rem;">
            <strong>Specialization:</strong> ${t.specialization || 'FullStack Tech'}
          </div>
        </div>
        <div class="card-footer" style="justify-content: flex-end; gap: 0.5rem;">
          <button onclick="editTrainer(${t.id}, '${escapeHtml(t.name)}', '${escapeHtml(t.role)}', '${escapeHtml(t.experience)}', '${escapeHtml(t.specialization)}')" class="btn btn-outline btn-sm">Edit</button>
          <button onclick="deleteTrainer(${t.id})" class="btn btn-danger btn-sm">Remove</button>
        </div>
      </div>
    `).join('');
  }

  const trainerForm = document.getElementById('trainerForm');
  if (trainerForm) {
    trainerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const id = document.getElementById('trainerId').value;
      const payload = {
        name: document.getElementById('trainerName').value,
        role: document.getElementById('trainerRole').value,
        experience: document.getElementById('trainerExperience').value,
        specialization: document.getElementById('trainerSpecialization').value
      };

      const url = id ? `/api/trainers/${id}` : '/api/trainers';
      const method = id ? 'PUT' : 'POST';
      const res = await apiFetch(url, method, payload);

      if (res.success) {
        showToast(res.message, 'success');
        document.getElementById('trainerModal').classList.remove('active');
        initTrainers();
        initStats();
      } else {
        showToast(res.message || 'Action failed', 'error');
      }
    });
  }
}

window.editTrainer = function(id, name, role, exp, spec) {
  document.getElementById('trainerId').value = id;
  document.getElementById('trainerName').value = name;
  document.getElementById('trainerRole').value = role;
  document.getElementById('trainerExperience').value = exp;
  document.getElementById('trainerSpecialization').value = spec;
  document.getElementById('modalTrainerTitle').textContent = 'Edit Trainer Profile';
  document.getElementById('trainerModal').classList.add('active');
};

window.deleteTrainer = async function(id) {
  if (confirm('Are you sure you want to remove this trainer profile?')) {
    const res = await apiFetch(`/api/trainers/${id}`, 'DELETE');
    if (res.success) {
      showToast(res.message, 'success');
      initTrainers();
      initStats();
    } else {
      showToast(res.message, 'error');
    }
  }
};

// 4. Admin Dashboard Logic
async function initAdmin() {
  const usersTbody = document.getElementById('admin-users-tbody');
  const contactsTbody = document.getElementById('admin-contacts-tbody');
  if (!usersTbody && !contactsTbody) return;

  if (usersTbody) {
    const res = await apiFetch('/api/users');
    if (res.success && res.users) {
      usersTbody.innerHTML = res.users.map(u => `
        <tr>
          <td>#${u.id}</td>
          <td style="font-weight: 600;">${u.name}</td>
          <td>${u.email}</td>
          <td><span class="badge badge-mode">${u.course || 'Python FullStack'}</span></td>
          <td>${u.dob || '-'}</td>
          <td>${u.gender || '-'}</td>
          <td>
            <div style="display: flex; gap: 0.4rem;">
              <button onclick="editUser(${u.id}, '${escapeHtml(u.name)}', '${escapeHtml(u.course)}')" class="btn btn-outline btn-sm">Edit</button>
              <button onclick="deleteUser(${u.id})" class="btn btn-danger btn-sm">Delete</button>
            </div>
          </td>
        </tr>
      `).join('');
    }
  }

  if (contactsTbody) {
    const res = await apiFetch('/api/contacts');
    if (res.success && res.contacts) {
      contactsTbody.innerHTML = res.contacts.map(c => `
        <tr>
          <td>#${c.id}</td>
          <td style="font-weight: 600;">${c.name}</td>
          <td>${c.email}</td>
          <td>${c.message}</td>
          <td><span class="badge ${c.status === 'Resolved' ? 'badge-mode' : 'badge-duration'}">${c.status || 'Pending'}</span></td>
          <td>
            <div style="display: flex; gap: 0.4rem;">
              <button onclick="toggleInquiryStatus(${c.id}, '${c.status === 'Pending' ? 'Resolved' : 'Pending'}')" class="btn btn-secondary btn-sm">${c.status === 'Pending' ? 'Mark Resolved' : 'Mark Pending'}</button>
              <button onclick="deleteInquiry(${c.id})" class="btn btn-danger btn-sm">Delete</button>
            </div>
          </td>
        </tr>
      `).join('');
    }
  }

  const editUserForm = document.getElementById('editUserForm');
  if (editUserForm) {
    editUserForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const id = document.getElementById('editUserId').value;
      const payload = {
        name: document.getElementById('editUserName').value,
        course: document.getElementById('editUserCourse').value
      };
      const res = await apiFetch(`/api/users/${id}`, 'PUT', payload);
      if (res.success) {
        showToast(res.message, 'success');
        document.getElementById('editUserModal').classList.remove('active');
        initAdmin();
        initStats();
      } else {
        showToast(res.message, 'error');
      }
    });
  }
}

window.editUser = function(id, name, course) {
  document.getElementById('editUserId').value = id;
  document.getElementById('editUserName').value = name;
  document.getElementById('editUserCourse').value = course;
  document.getElementById('editUserModal').classList.add('active');
};

window.deleteUser = async function(id) {
  if (confirm('Are you sure you want to delete this student account?')) {
    const res = await apiFetch(`/api/users/${id}`, 'DELETE');
    if (res.success) {
      showToast(res.message, 'success');
      initAdmin();
      initStats();
    } else {
      showToast(res.message, 'error');
    }
  }
};

window.toggleInquiryStatus = async function(id, newStatus) {
  const res = await apiFetch(`/api/contacts/${id}`, 'PUT', { status: newStatus });
  if (res.success) {
    showToast(res.message, 'success');
    initAdmin();
    initStats();
  } else {
    showToast(res.message, 'error');
  }
};

window.deleteInquiry = async function(id) {
  if (confirm('Are you sure you want to delete this inquiry?')) {
    const res = await apiFetch(`/api/contacts/${id}`, 'DELETE');
    if (res.success) {
      showToast(res.message, 'success');
      initAdmin();
      initStats();
    } else {
      showToast(res.message, 'error');
    }
  }
};

// 5. Auth & Navigation Logic
function initAuth() {
  const currentUser = JSON.parse(localStorage.getItem('sms_user') || 'null');
  const isLoggedIn = localStorage.getItem('sms_logged_in') === 'true';

  const currentPath = window.location.pathname.toLowerCase();

  // Auth Guard: If not logged in and accessing internal app pages, redirect to login
  const isPublicPage = currentPath === '/' || currentPath === '/login' || currentPath === '/login.html' || currentPath === '/register' || currentPath === '/register.html';

  if (!isLoggedIn && !isPublicPage) {
    showToast('Please sign in to access the Student Management System portal.', 'info');
    setTimeout(() => { window.location.href = '/login'; }, 800);
    return;
  }

  // If already logged in and visiting login/root page, enter the app directly!
  if (isLoggedIn && (currentPath === '/' || currentPath === '/login' || currentPath === '/login.html')) {
    window.location.href = (currentUser && currentUser.role === 'admin') ? '/admin' : '/home';
    return;
  }

  // Update Dynamic Navigation UI
  updateNavAuthUI(currentUser, isLoggedIn);

  // Handle Login Form
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('loginEmail').value.trim();
      const password = document.getElementById('loginPassword').value;

      if (!email || !password) {
        showToast('Please enter both email and password.', 'error');
        return;
      }

      const payload = { email, password };
      const res = await apiFetch('/api/login', 'POST', payload);
      if (res.success && res.user) {
        localStorage.setItem('sms_user', JSON.stringify(res.user));
        localStorage.setItem('sms_logged_in', 'true');
        showToast(res.message || `Welcome back, ${res.user.name}! Entering app...`, 'success');
        setTimeout(() => {
          if (res.user.role === 'admin') {
            window.location.href = '/admin';
          } else {
            window.location.href = '/home';
          }
        }, 1000);
      } else {
        showToast(res.message || 'Invalid email or password. Please try again.', 'error');
      }
    });
  }

  // Handle Registration Form
  const registerForm = document.getElementById('registerForm');
  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const name = document.getElementById('regName').value.trim();
      const email = document.getElementById('regEmail').value.trim();
      const password = document.getElementById('regPassword').value;
      const course = document.getElementById('regCourse').value;
      const dob = document.getElementById('regDob').value;
      const gender = document.getElementById('regGender').value;

      if (!name || !email || !password) {
        showToast('Name, Email, and Password are required fields.', 'error');
        return;
      }

      const payload = { name, email, password, course, dob, gender };
      const res = await apiFetch('/api/register', 'POST', payload);
      if (res.success) {
        showToast(res.message || 'Registration successful! You can now log in.', 'success');
        setTimeout(() => { window.location.href = '/login'; }, 1200);
      } else {
        showToast(res.message || 'Registration failed.', 'error');
      }
    });
  }
}

function updateNavAuthUI(user, isLoggedIn) {
  const navActions = document.querySelector('.nav-actions');
  if (!navActions) return;

  if (isLoggedIn && user) {
    navActions.innerHTML = `
      <div style="display: flex; align-items: center; gap: 0.75rem;">
        <span style="font-size: 0.88rem; font-weight: 600; color: var(--text-main);">👋 ${escapeHtml(user.name)}</span>
        <button onclick="logoutUser()" class="btn btn-secondary btn-sm">Logout</button>
      </div>
    `;
  } else {
    navActions.innerHTML = `
      <a href="/login" class="btn btn-secondary btn-sm">Login</a>
      <a href="/register" class="btn btn-primary btn-sm">Get Started</a>
    `;
  }
}

window.logoutUser = function() {
  localStorage.removeItem('sms_user');
  localStorage.removeItem('sms_logged_in');
  showToast('Logged out successfully.', 'info');
  setTimeout(() => { window.location.href = '/login'; }, 800);
};

// 6. Contact Form Logic
function initContact() {
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const payload = {
        name: document.getElementById('contactName').value,
        email: document.getElementById('contactEmail').value,
        message: document.getElementById('contactMessage').value
      };
      const res = await apiFetch('/api/contacts', 'POST', payload);
      if (res.success) {
        showToast(res.message, 'success');
        contactForm.reset();
        initStats();
      } else {
        showToast(res.message, 'error');
      }
    });
  }
}

// 7. Modal Handlers
function initModals() {
  const openAddCourse = document.getElementById('openAddCourseModal');
  const courseModal = document.getElementById('courseModal');
  const closeCourse = document.getElementById('closeCourseModal');

  if (openAddCourse && courseModal) {
    openAddCourse.addEventListener('click', () => {
      document.getElementById('courseForm').reset();
      document.getElementById('courseId').value = '';
      document.getElementById('modalCourseTitle').textContent = 'Add New Course';
      courseModal.classList.add('active');
    });
  }

  if (closeCourse && courseModal) {
    closeCourse.addEventListener('click', () => courseModal.classList.remove('active'));
  }

  const openAddTrainer = document.getElementById('openAddTrainerModal');
  const trainerModal = document.getElementById('trainerModal');
  const closeTrainer = document.getElementById('closeTrainerModal');

  if (openAddTrainer && trainerModal) {
    openAddTrainer.addEventListener('click', () => {
      document.getElementById('trainerForm').reset();
      document.getElementById('trainerId').value = '';
      document.getElementById('modalTrainerTitle').textContent = 'Add New Trainer';
      trainerModal.classList.add('active');
    });
  }

  if (closeTrainer && trainerModal) {
    closeTrainer.addEventListener('click', () => trainerModal.classList.remove('active'));
  }

  const closeEditUser = document.getElementById('closeEditUserModal');
  const editUserModal = document.getElementById('editUserModal');
  if (closeEditUser && editUserModal) {
    closeEditUser.addEventListener('click', () => editUserModal.classList.remove('active'));
  }
}
