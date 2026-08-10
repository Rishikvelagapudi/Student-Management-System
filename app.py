import os
import sqlite3
from flask import Flask, render_template, send_from_directory, request, jsonify

# Configure Flask app to locate templates and static assets
base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, 'templates')
DB_PATH = os.path.join(base_dir, 'database.db')

app = Flask(__name__, template_folder=templates_dir, static_folder=base_dir)

# --- SQLite Database Helper & Initialization ---

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            course TEXT,
            dob TEXT,
            gender TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Courses Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            duration TEXT,
            mode TEXT,
            topics TEXT,
            trainer TEXT
        )
    ''')

    # 3. Trainers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trainers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT,
            experience TEXT,
            specialization TEXT
        )
    ''')

    # 4. Contacts Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    ''')

    # Seed default user if users table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO users (name, email, password, course, dob, gender)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ("Rishik Velagapudi", "rishik@nriit.edu", "123", "Python FullStack", "2002-05-15", "Male"))

    # Seed Admin User (admin@11 / 12345678)
    cursor.execute("SELECT id FROM users WHERE LOWER(email) = 'admin@11'")
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO users (name, email, password, course, dob, gender)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ("System Administrator", "admin@11", "12345678", "Admin", "2000-01-01", "Admin"))

    # Seed default courses if empty
    cursor.execute("SELECT COUNT(*) FROM courses")
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO courses (title, duration, mode, topics, trainer)
            VALUES (?, ?, ?, ?, ?)
        ''', [
            ("Python FullStack Development", "6 Months", "Offline & Online", "HTML5, CSS3, JavaScript, Flask, SQL, Git", "Mr. Sriram"),
            ("Java FullStack Development", "6 Months", "Offline & Online", "Core Java, Spring Boot, REST API, React, PostgreSQL", "Dr. Ramesh"),
            ("Data Science & AI", "4 Months", "Online", "Python, Pandas, NumPy, Scikit-Learn, Machine Learning", "Ms. Priya")
        ])

    # Seed default trainers if empty
    cursor.execute("SELECT COUNT(*) FROM trainers")
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO trainers (name, role, experience, specialization)
            VALUES (?, ?, ?, ?)
        ''', [
            ("Mr. Sriram", "Python Full Stack Trainer", "4+ years", "Flask, Django, React, SQL"),
            ("Dr. Ramesh", "Java Full Stack Lead", "8+ years", "Spring Boot, Microservices, System Design"),
            ("Ms. Priya", "Data Science Specialist", "5+ years", "Machine Learning, Analytics, Python")
        ])

    # Seed default contacts if empty
    cursor.execute("SELECT COUNT(*) FROM contacts")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO contacts (name, email, message, status)
            VALUES (?, ?, ?, ?)
        ''', ("Anil Kumar", "anil@gmail.com", "Inquiry regarding Python FullStack batch timings.", "Pending"))

    conn.commit()
    conn.close()

# Initialize DB on server start
init_db()

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

@app.route('/admin')
@app.route('/admin.html')
def admin():
    return render_template('admin.html')

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

# --- REST API Endpoints (GET, POST, PUT, DELETE) ---

# ==============================================================================
# 1. COURSES ENDPOINTS
# ==============================================================================

@app.route('/api/courses', methods=['GET'])
def get_courses():
    conn = get_db_connection()
    courses = conn.execute("SELECT * FROM courses").fetchall()
    conn.close()
    return jsonify({"success": True, "method": "GET", "courses": [dict(c) for c in courses]})

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

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO courses (title, duration, mode, topics, trainer)
        VALUES (?, ?, ?, ?, ?)
    ''', (title, duration, mode, topics, trainer))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    new_course = {"id": new_id, "title": title, "duration": duration, "mode": mode, "topics": topics, "trainer": trainer}
    return jsonify({"success": True, "method": "POST", "message": f"Course '{title}' added successfully!", "course": new_course}), 201

@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    data = request.get_json(silent=True) or request.form.to_dict()
    conn = get_db_connection()
    course = conn.execute("SELECT * FROM courses WHERE id = ?", (course_id,)).fetchone()
    if not course:
        conn.close()
        return jsonify({"success": False, "message": "Course not found!"}), 404

    title = data.get('title', course['title'])
    duration = data.get('duration', course['duration'])
    mode = data.get('mode', course['mode'])
    topics = data.get('topics', course['topics'])
    trainer = data.get('trainer', course['trainer'])

    conn.execute('''
        UPDATE courses SET title = ?, duration = ?, mode = ?, topics = ?, trainer = ?
        WHERE id = ?
    ''', (title, duration, mode, topics, trainer, course_id))
    conn.commit()
    conn.close()

    updated = {"id": course_id, "title": title, "duration": duration, "mode": mode, "topics": topics, "trainer": trainer}
    return jsonify({"success": True, "method": "PUT", "message": f"Course '{title}' updated successfully!", "course": updated})

@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    conn = get_db_connection()
    course = conn.execute("SELECT * FROM courses WHERE id = ?", (course_id,)).fetchone()
    if not course:
        conn.close()
        return jsonify({"success": False, "message": "Course not found!"}), 404

    conn.execute("DELETE FROM courses WHERE id = ?", (course_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "method": "DELETE", "message": f"Course ID {course_id} deleted successfully!"})


# ==============================================================================
# 2. TRAINERS ENDPOINTS
# ==============================================================================

@app.route('/api/trainers', methods=['GET'])
def get_trainers():
    conn = get_db_connection()
    trainers = conn.execute("SELECT * FROM trainers").fetchall()
    conn.close()
    return jsonify({"success": True, "method": "GET", "trainers": [dict(t) for t in trainers]})

@app.route('/api/trainers', methods=['POST'])
def add_trainer():
    data = request.get_json(silent=True) or request.form.to_dict()
    name = data.get('name')
    role = data.get('role', 'Instructor')
    experience = data.get('experience', '3+ years')
    specialization = data.get('specialization', 'FullStack')

    if not name:
        return jsonify({"success": False, "message": "Trainer name is required!"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO trainers (name, role, experience, specialization)
        VALUES (?, ?, ?, ?)
    ''', (name, role, experience, specialization))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    new_trainer = {"id": new_id, "name": name, "role": role, "experience": experience, "specialization": specialization}
    return jsonify({"success": True, "method": "POST", "message": f"Trainer '{name}' added successfully!", "trainer": new_trainer}), 201

@app.route('/api/trainers/<int:trainer_id>', methods=['PUT'])
def update_trainer(trainer_id):
    data = request.get_json(silent=True) or request.form.to_dict()
    conn = get_db_connection()
    trainer = conn.execute("SELECT * FROM trainers WHERE id = ?", (trainer_id,)).fetchone()
    if not trainer:
        conn.close()
        return jsonify({"success": False, "message": "Trainer not found!"}), 404

    name = data.get('name', trainer['name'])
    role = data.get('role', trainer['role'])
    experience = data.get('experience', trainer['experience'])
    specialization = data.get('specialization', trainer['specialization'])

    conn.execute('''
        UPDATE trainers SET name = ?, role = ?, experience = ?, specialization = ?
        WHERE id = ?
    ''', (name, role, experience, specialization, trainer_id))
    conn.commit()
    conn.close()

    updated = {"id": trainer_id, "name": name, "role": role, "experience": experience, "specialization": specialization}
    return jsonify({"success": True, "method": "PUT", "message": f"Trainer '{name}' updated successfully!", "trainer": updated})

@app.route('/api/trainers/<int:trainer_id>', methods=['DELETE'])
def delete_trainer(trainer_id):
    conn = get_db_connection()
    trainer = conn.execute("SELECT * FROM trainers WHERE id = ?", (trainer_id,)).fetchone()
    if not trainer:
        conn.close()
        return jsonify({"success": False, "message": "Trainer not found!"}), 404

    name = trainer['name']
    conn.execute("DELETE FROM trainers WHERE id = ?", (trainer_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "method": "DELETE", "message": f"Trainer '{name}' removed successfully!"})


# ==============================================================================
# 3. USER MANAGEMENT & AUTH ENDPOINTS (SQLite DB Persisted)
# ==============================================================================

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute("SELECT id, name, email, course, dob, gender, created_at FROM users").fetchall()
    conn.close()
    return jsonify({"success": True, "method": "GET", "users": [dict(u) for u in users]})

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

    conn = get_db_connection()
    existing = conn.execute("SELECT id FROM users WHERE LOWER(email) = LOWER(?)", (email,)).fetchone()
    if existing:
        conn.close()
        return jsonify({"success": False, "message": "Email already registered!"}), 400

    user_name = name or "Student"
    user_course = course or "Python FullStack"

    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (name, email, password, course, dob, gender)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_name, email, password, user_course, dob, gender))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "method": "POST",
        "message": f"Registration successful for {user_name}!",
        "user": {
            "id": new_id,
            "name": user_name,
            "email": email,
            "course": user_course,
            "dob": dob,
            "gender": gender
        }
    }), 201

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json(silent=True) or request.form.to_dict()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required!"}), 400

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (email,)).fetchone()
    conn.close()

    if not user:
        return jsonify({"success": False, "message": "User not found! Please register first."}), 404

    if user['password'] != password:
        return jsonify({"success": False, "message": "Invalid password!"}), 401

    is_admin = (user['email'].lower() == 'admin@11')
    return jsonify({
        "success": True,
        "method": "POST",
        "message": f"Welcome back, {user['name']}!",
        "user": {
            "id": user['id'],
            "name": user['name'],
            "email": user['email'],
            "course": user['course'],
            "dob": user['dob'] or '',
            "gender": user['gender'] or '',
            "role": "admin" if is_admin else "student"
        }
    })

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json(silent=True) or request.form.to_dict()
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        conn.close()
        return jsonify({"success": False, "message": "User not found!"}), 404

    name = data.get('name', user['name'])
    course = data.get('course', user['course'])
    password = data.get('password', user['password'])
    dob = data.get('dob', user['dob'])

    conn.execute('''
        UPDATE users SET name = ?, course = ?, password = ?, dob = ?
        WHERE id = ?
    ''', (name, course, password, dob, user_id))
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "method": "PUT",
        "message": f"Profile updated for {name}!",
        "user": {"id": user_id, "name": name, "email": user['email'], "course": course, "dob": dob}
    })

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        conn.close()
        return jsonify({"success": False, "message": "User not found!"}), 404

    user_name = user['name']
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "method": "DELETE", "message": f"User account for '{user_name}' deleted successfully!"})


# ==============================================================================
# 4. CONTACT & INQUIRIES ENDPOINTS
# ==============================================================================

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    conn = get_db_connection()
    contacts = conn.execute("SELECT * FROM contacts").fetchall()
    conn.close()
    return jsonify({"success": True, "method": "GET", "contacts": [dict(c) for c in contacts]})

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    data = request.get_json(silent=True) or request.form.to_dict()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not name or not email or not message:
        return jsonify({"success": False, "message": "Name, Email, and Message are required!"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO contacts (name, email, message, status)
        VALUES (?, ?, ?, 'Pending')
    ''', (name, email, message))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()

    new_contact = {"id": new_id, "name": name, "email": email, "message": message, "status": "Pending"}
    return jsonify({"success": True, "method": "POST", "message": "Inquiry submitted successfully!", "contact": new_contact}), 201

@app.route('/api/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    data = request.get_json(silent=True) or request.form.to_dict()
    conn = get_db_connection()
    contact = conn.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,)).fetchone()
    if not contact:
        conn.close()
        return jsonify({"success": False, "message": "Inquiry not found!"}), 404

    status = data.get('status', contact['status'])
    message = data.get('message', contact['message'])

    conn.execute('''
        UPDATE contacts SET status = ?, message = ? WHERE id = ?
    ''', (status, message, contact_id))
    conn.commit()
    conn.close()

    updated = {"id": contact_id, "name": contact['name'], "email": contact['email'], "message": message, "status": status}
    return jsonify({"success": True, "method": "PUT", "message": f"Inquiry ID {contact_id} updated!", "contact": updated})

@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    conn = get_db_connection()
    contact = conn.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,)).fetchone()
    if not contact:
        conn.close()
        return jsonify({"success": False, "message": "Inquiry not found!"}), 404

    conn.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "method": "DELETE", "message": f"Inquiry ID {contact_id} deleted successfully!"})


# ==============================================================================
# 5. GENERAL SYSTEM STATS ENDPOINT
# ==============================================================================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db_connection()
    students_cnt = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    courses_cnt = conn.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
    trainers_cnt = conn.execute("SELECT COUNT(*) FROM trainers").fetchone()[0]
    inquiries_cnt = conn.execute("SELECT COUNT(*) FROM contacts").fetchone()[0]
    conn.close()

    return jsonify({
        "success": True,
        "method": "GET",
        "stats": {
            "students_enrolled": students_cnt,
            "courses_offered": courses_cnt,
            "expert_trainers": trainers_cnt,
            "active_inquiries": inquiries_cnt
        }
    })

if __name__ == '__main__':
    print("Starting NRIIT Learning Management Flask Server with SQLite DB...")
    app.run(debug=True, port=5000)
