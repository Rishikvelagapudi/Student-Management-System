import os
from flask import Flask, render_template, send_from_directory, request, jsonify

# Configure Flask app to locate templates and static assets
base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=templates_dir, static_folder=base_dir)

# --- Web Page Routes ---

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/about')
@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/courses')
@app.route('/courses.html')
def courses():
    return render_template('courses.html')

@app.route('/trainers')
@app.route('/trainers.html')
def trainers():
    return render_template('trainers.html')

@app.route('/register')
@app.route('/register.html')
def register():
    return render_template('register.html')

@app.route('/login')
@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/contact')
@app.route('/contact.html')
def contact():
    return render_template('contact.html')

# --- Static Resource Handlers ---

@app.route('/css/static/<path:filename>')
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(base_dir, 'css', 'static'), filename)

@app.route('/js/static/<path:filename>')
@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(base_dir, 'js', 'static'), filename)

@app.route('/image/static/<path:filename>')
@app.route('/image/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(base_dir, 'image', 'static'), filename)

@app.route('/images/static/<path:filename>')
@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(os.path.join(base_dir, 'images', 'static'), filename)

@app.route('/audio/static/<path:filename>')
@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory(os.path.join(base_dir, 'audio', 'static'), filename)

@app.route('/video/static/<path:filename>')
@app.route('/video/<path:filename>')
def serve_video(filename):
    return send_from_directory(os.path.join(base_dir, 'video', 'static'), filename)

# --- REST API In-Memory Data Stores ---

users_db = [
    {
        "id": 1,
        "name": "Rishik Velagapudi",
        "email": "rishik@nriit.edu",
        "password": "123",
        "course": "Python FullStack",
        "dob": "2002-05-15",
        "gender": "Male"
    }
]

courses_db = [
    {
        "id": 1,
        "title": "Python FullStack Development",
        "duration": "6 Months",
        "mode": "Offline & Online",
        "topics": "HTML5, CSS3, JavaScript, Flask, SQL, Git",
        "trainer": "Mr. Sriram"
    },
    {
        "id": 2,
        "title": "Java FullStack Development",
        "duration": "6 Months",
        "mode": "Offline & Online",
        "topics": "Core Java, Spring Boot, REST API, React, PostgreSQL",
        "trainer": "Dr. Ramesh"
    },
    {
        "id": 3,
        "title": "Data Science & AI",
        "duration": "4 Months",
        "mode": "Online",
        "topics": "Python, Pandas, NumPy, Scikit-Learn, Machine Learning",
        "trainer": "Ms. Priya"
    }
]

trainers_db = [
    {
        "id": 1,
        "name": "Mr. Sriram",
        "role": "Python Full Stack Trainer",
        "experience": "4+ years",
        "specialization": "Flask, Django, React, SQL"
    },
    {
        "id": 2,
        "name": "Dr. Ramesh",
        "role": "Java Full Stack Lead",
        "experience": "8+ years",
        "specialization": "Spring Boot, Microservices, System Design"
    },
    {
        "id": 3,
        "name": "Ms. Priya",
        "role": "Data Science Specialist",
        "experience": "5+ years",
        "specialization": "Machine Learning, Analytics, Python"
    }
]

contacts_db = [
    {
        "id": 1,
        "name": "Anil Kumar",
        "email": "anil@gmail.com",
        "message": "Inquiry regarding Python FullStack batch timings.",
        "status": "Pending"
    }
]

# --- REST API Endpoints (GET, POST, PUT, DELETE) ---

# ==============================================================================
# 1. COURSES ENDPOINTS (GET, POST, PUT, DELETE)
# ==============================================================================

# GET Method: Retrieve all courses
@app.route('/api/courses', methods=['GET'])
def get_courses():
    return jsonify({"success": True, "method": "GET", "courses": courses_db})

# POST Method: Add a new course
@app.route('/api/courses', methods=['POST'])
def add_course():
    data = request.get_json(silent=True) or request.form.to_dict()
    title = data.get('title')
    duration = data.get('duration', '3 Months')
    mode = data.get('mode', 'Offline')
    topics = data.get('topics', 'Basics & Advanced')
    trainer = data.get('trainer', 'Faculty')

    if not title:
        return jsonify({"success": False, "message": "Course title is required!"}), 400

    new_id = max([c['id'] for c in courses_db], default=0) + 1
    new_course = {
        "id": new_id,
        "title": title,
        "duration": duration,
        "mode": mode,
        "topics": topics,
        "trainer": trainer
    }
    courses_db.append(new_course)
    return jsonify({"success": True, "method": "POST", "message": f"Course '{title}' added successfully!", "course": new_course}), 201

# PUT Method: Update an existing course
@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    data = request.get_json(silent=True) or request.form.to_dict()
    course = next((c for c in courses_db if c['id'] == course_id), None)
    if not course:
        return jsonify({"success": False, "message": "Course not found!"}), 404

    if 'title' in data and data['title']:
        course['title'] = data['title']
    if 'duration' in data and data['duration']:
        course['duration'] = data['duration']
    if 'mode' in data and data['mode']:
        course['mode'] = data['mode']
    if 'topics' in data and data['topics']:
        course['topics'] = data['topics']
    if 'trainer' in data and data['trainer']:
        course['trainer'] = data['trainer']

    return jsonify({"success": True, "method": "PUT", "message": f"Course '{course['title']}' updated successfully!", "course": course})

# DELETE Method: Delete a course
@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    global courses_db
    course = next((c for c in courses_db if c['id'] == course_id), None)
    if not course:
        return jsonify({"success": False, "message": "Course not found!"}), 404

    courses_db = [c for c in courses_db if c['id'] != course_id]
    return jsonify({"success": True, "method": "DELETE", "message": f"Course ID {course_id} deleted successfully!"})


# ==============================================================================
# 2. TRAINERS ENDPOINTS (GET, POST, PUT, DELETE)
# ==============================================================================

# GET Method: Retrieve all trainers
@app.route('/api/trainers', methods=['GET'])
def get_trainers():
    return jsonify({"success": True, "method": "GET", "trainers": trainers_db})

# POST Method: Add a new trainer
@app.route('/api/trainers', methods=['POST'])
def add_trainer():
    data = request.get_json(silent=True) or request.form.to_dict()
    name = data.get('name')
    role = data.get('role', 'Instructor')
    experience = data.get('experience', '3+ years')
    specialization = data.get('specialization', 'FullStack')

    if not name:
        return jsonify({"success": False, "message": "Trainer name is required!"}), 400

    new_id = max([t['id'] for t in trainers_db], default=0) + 1
    new_trainer = {
        "id": new_id,
        "name": name,
        "role": role,
        "experience": experience,
        "specialization": specialization
    }
    trainers_db.append(new_trainer)
    return jsonify({"success": True, "method": "POST", "message": f"Trainer '{name}' added successfully!", "trainer": new_trainer}), 201

# PUT Method: Update a trainer profile
@app.route('/api/trainers/<int:trainer_id>', methods=['PUT'])
def update_trainer(trainer_id):
    data = request.get_json(silent=True) or request.form.to_dict()
    trainer = next((t for t in trainers_db if t['id'] == trainer_id), None)
    if not trainer:
        return jsonify({"success": False, "message": "Trainer not found!"}), 404

    if 'name' in data and data['name']:
        trainer['name'] = data['name']
    if 'role' in data and data['role']:
        trainer['role'] = data['role']
    if 'experience' in data and data['experience']:
        trainer['experience'] = data['experience']
    if 'specialization' in data and data['specialization']:
        trainer['specialization'] = data['specialization']

    return jsonify({"success": True, "method": "PUT", "message": f"Trainer '{trainer['name']}' updated successfully!", "trainer": trainer})

# DELETE Method: Remove a trainer
@app.route('/api/trainers/<int:trainer_id>', methods=['DELETE'])
def delete_trainer(trainer_id):
    global trainers_db
    trainer = next((t for t in trainers_db if t['id'] == trainer_id), None)
    if not trainer:
        return jsonify({"success": False, "message": "Trainer not found!"}), 404

    trainers_db = [t for t in trainers_db if t['id'] != trainer_id]
    return jsonify({"success": True, "method": "DELETE", "message": f"Trainer '{trainer['name']}' removed successfully!"})


# ==============================================================================
# 3. USER MANAGEMENT & AUTH ENDPOINTS (GET, POST, PUT, DELETE)
# ==============================================================================

# GET Method: Retrieve all registered users from users_db
@app.route('/api/users', methods=['GET'])
def get_users():
    clean_users = [{"id": u["id"], "name": u["name"], "email": u["email"], "course": u["course"], "dob": u.get("dob", ""), "gender": u.get("gender", "")} for u in users_db]
    return jsonify({"success": True, "method": "GET", "users": clean_users})

# POST Method: api_register - Register a new user into users_db
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json(silent=True) or request.form.to_dict()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    course = data.get('course')
    dob = data.get('dob', '')
    gender = data.get('gender', 'Male')

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required!"}), 400

    existing = next((u for u in users_db if u['email'].lower() == email.lower()), None)
    if existing:
        return jsonify({"success": False, "message": "Email already registered!"}), 400

    new_id = max([u['id'] for u in users_db], default=0) + 1
    user = {
        "id": new_id,
        "name": name or "Student",
        "email": email,
        "password": password,
        "course": course or "Python FullStack",
        "dob": dob,
        "gender": gender
    }
    users_db.append(user)
    return jsonify({"success": True, "method": "POST", "message": f"Registration successful for {user['name']}!", "user": {"id": user["id"], "name": user['name'], "email": user['email'], "course": user['course']}}), 201

# POST Method: api_login - Authenticate user credentials against users_db
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json(silent=True) or request.form.to_dict()
    email = data.get('email')
    password = data.get('password')

    user = next((u for u in users_db if u['email'].lower() == (email or '').lower()), None)
    if not user:
        return jsonify({"success": False, "message": "User not found! Please register first."}), 404

    if user['password'] != password:
        return jsonify({"success": False, "message": "Invalid password!"}), 401

    return jsonify({
        "success": True,
        "method": "POST",
        "message": f"Welcome back, {user['name']}!",
        "user": {
            "id": user['id'],
            "name": user['name'],
            "email": user['email'],
            "course": user['course'],
            "dob": user.get('dob', ''),
            "gender": user.get('gender', '')
        }
    })

# PUT Method: Update existing user in users_db
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json(silent=True) or request.form.to_dict()
    user = next((u for u in users_db if u['id'] == user_id), None)
    if not user:
        return jsonify({"success": False, "message": "User not found!"}), 404

    if 'name' in data and data['name']:
        user['name'] = data['name']
    if 'course' in data and data['course']:
        user['course'] = data['course']
    if 'password' in data and data['password']:
        user['password'] = data['password']
    if 'dob' in data:
        user['dob'] = data['dob']

    return jsonify({
        "success": True,
        "method": "PUT",
        "message": f"Profile updated for {user['name']}!",
        "user": {"id": user["id"], "name": user['name'], "email": user['email'], "course": user['course'], "dob": user.get("dob", "")}
    })

# DELETE Method: Delete user account from users_db
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users_db
    user = next((u for u in users_db if u['id'] == user_id), None)
    if not user:
        return jsonify({"success": False, "message": "User not found!"}), 404

    users_db = [u for u in users_db if u['id'] != user_id]
    return jsonify({"success": True, "method": "DELETE", "message": f"User account for '{user['name']}' deleted successfully!"})


# ==============================================================================
# 4. CONTACT & INQUIRIES ENDPOINTS (GET, POST, PUT, DELETE)
# ==============================================================================

# GET Method: Retrieve all inquiries
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    return jsonify({"success": True, "method": "GET", "contacts": contacts_db})

# POST Method: Submit a new inquiry
@app.route('/api/contacts', methods=['POST'])
def add_contact():
    data = request.get_json(silent=True) or request.form.to_dict()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not name or not email or not message:
        return jsonify({"success": False, "message": "Name, Email, and Message are required!"}), 400

    new_id = max([c['id'] for c in contacts_db], default=0) + 1
    new_contact = {
        "id": new_id,
        "name": name,
        "email": email,
        "message": message,
        "status": "Pending"
    }
    contacts_db.append(new_contact)
    return jsonify({"success": True, "method": "POST", "message": "Inquiry submitted successfully!", "contact": new_contact}), 201

# PUT Method: Update inquiry status
@app.route('/api/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    data = request.get_json(silent=True) or request.form.to_dict()
    contact = next((c for c in contacts_db if c['id'] == contact_id), None)
    if not contact:
        return jsonify({"success": False, "message": "Inquiry not found!"}), 404

    if 'status' in data:
        contact['status'] = data['status']
    if 'message' in data and data['message']:
        contact['message'] = data['message']

    return jsonify({"success": True, "method": "PUT", "message": f"Inquiry ID {contact_id} updated!", "contact": contact})

# DELETE Method: Delete an inquiry
@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    global contacts_db
    contact = next((c for c in contacts_db if c['id'] == contact_id), None)
    if not contact:
        return jsonify({"success": False, "message": "Inquiry not found!"}), 404

    contacts_db = [c for c in contacts_db if c['id'] != contact_id]
    return jsonify({"success": True, "method": "DELETE", "message": f"Inquiry ID {contact_id} deleted successfully!"})


# ==============================================================================
# 5. GENERAL SYSTEM STATS ENDPOINT (GET)
# ==============================================================================

# GET Method: System dashboard statistics
@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({
        "success": True,
        "method": "GET",
        "stats": {
            "students_enrolled": len(users_db),
            "courses_offered": len(courses_db),
            "expert_trainers": len(trainers_db),
            "active_inquiries": len(contacts_db)
        }
    })

if __name__ == '__main__':
    print("Starting NRIIT Learning Management Flask Server...")
    app.run(debug=True, port=5000)

