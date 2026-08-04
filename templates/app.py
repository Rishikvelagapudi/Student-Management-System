import os
from flask import Flask, render_template, send_from_directory, request, jsonify

# Base directory configuration
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Template folder is current directory, static assets are in parent directory
app = Flask(__name__, template_folder=current_dir, static_folder=parent_dir)

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

# --- Static Asset Handlers ---

@app.route('/css/static/<path:filename>')
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(parent_dir, 'css', 'static'), filename)

@app.route('/js/static/<path:filename>')
@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(parent_dir, 'js', 'static'), filename)

@app.route('/image/static/<path:filename>')
@app.route('/image/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(parent_dir, 'image', 'static'), filename)

@app.route('/images/static/<path:filename>')
@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(os.path.join(parent_dir, 'images', 'static'), filename)

# --- REST API Endpoints ---

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

if __name__ == '__main__':
    print("Starting NRIIT Learning Management Flask Server from templates/...")
    app.run(debug=True, port=5000)
