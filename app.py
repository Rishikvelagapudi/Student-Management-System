import os
from flask import Flask, render_template, send_from_directory, request, jsonify

# Configure Flask app to locate templates and static assets
base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=templates_dir, static_folder=base_dir)

# --- Web Page Routes ---

@app.route('/')
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

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(base_dir, 'static'), filename)

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(base_dir, 'static', 'css'), filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(base_dir, 'static', 'js'), filename)

@app.route('/image/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(base_dir, 'static', 'image'), filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(os.path.join(base_dir, 'static', 'images'), filename)

# --- REST API Endpoints ---

# In-memory storage for demonstration backend operations
registered_users = []

@app.route('/api/courses', methods=['GET'])
def get_courses():
    courses_data = [
        {
            "id": 1,
            "title": "Python FullStack Development",
            "duration": "6 Months",
            "mode": "Offline & Online",
            "topics": ["HTML5", "CSS3", "JavaScript", "Flask", "SQL", "Git"],
            "trainer": "Mr. Sriram"
        },
        {
            "id": 2,
            "title": "Java FullStack Development",
            "duration": "6 Months",
            "mode": "Offline & Online",
            "topics": ["Core Java", "Spring Boot", "REST API", "React", "PostgreSQL"],
            "trainer": "Dr. Ramesh"
        },
        {
            "id": 3,
            "title": "Data Science & AI",
            "duration": "4 Months",
            "mode": "Online",
            "topics": ["Python", "Pandas", "NumPy", "Scikit-Learn", "Machine Learning"],
            "trainer": "Ms. Priya"
        }
    ]
    return jsonify({"success": True, "courses": courses_data})

@app.route('/api/trainers', methods=['GET'])
def get_trainers():
    trainers_data = [
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
    return jsonify({"success": True, "trainers": trainers_data})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({
        "success": True,
        "stats": {
            "students_enrolled": "1,250+",
            "courses_offered": 8,
            "expert_trainers": 12,
            "placement_rate": "95%"
        }
    })

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json(silent=True) or request.form
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    course = data.get('course')

    if not email or not password:
        return jsonify({"success": False, "message": "Email and password are required!"}), 400

    existing = next((u for u in registered_users if u['email'].lower() == email.lower()), None)
    if existing:
        return jsonify({"success": False, "message": "Email already registered!"}), 400

    user = {
        "name": name or "Student",
        "email": email,
        "password": password,
        "course": course or "Python FullStack"
    }
    registered_users.append(user)
    return jsonify({"success": True, "message": f"Registration successful for {user['name']}!", "user": {"name": user['name'], "email": user['email']}})

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json(silent=True) or request.form
    email = data.get('email')
    password = data.get('password')

    user = next((u for u in registered_users if u['email'].lower() == (email or '').lower()), None)
    if not user:
        return jsonify({"success": False, "message": "User not found!"}), 404

    if user['password'] != password:
        return jsonify({"success": False, "message": "Invalid credentials!"}), 401

    return jsonify({"success": True, "message": f"Welcome back, {user['name']}!", "user": {"name": user['name'], "email": user['email']}})

if __name__ == '__main__':
    print("Starting NRIIT Learning Management Flask Server...")
    app.run(debug=True, port=5000)
