import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Course, Trainer, Contact

def get_request_data(request):
    if request.body:
        try:
            return json.loads(request.body.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
    if request.POST:
        return request.POST.dict()
    return {}

# ==============================================================================
# PAGE VIEWS
# ==============================================================================

def home(request):
    return render(request, 'sms_app/home.html')

def students_page(request):
    return render(request, 'sms_app/students.html')

def about(request):
    return render(request, 'sms_app/about.html')

def courses_page(request):
    return render(request, 'sms_app/courses.html')

def trainers_page(request):
    return render(request, 'sms_app/trainers.html')

def register_page(request):
    return render(request, 'sms_app/register.html')

def login_page(request):
    return render(request, 'sms_app/login.html')

def admin_page(request):
    return render(request, 'sms_app/admin.html')

def contact_page(request):
    return render(request, 'sms_app/contact.html')


# ==============================================================================
# 1. COURSES ENDPOINTS
# ==============================================================================

@csrf_exempt
def courses_api(request):
    if request.method == 'GET':
        courses = list(Course.objects.values('id', 'title', 'duration', 'mode', 'topics', 'trainer'))
        return JsonResponse({"success": True, "method": "GET", "courses": courses})

    elif request.method == 'POST':
        data = get_request_data(request)
        title = data.get('title')
        duration = data.get('duration', '3 Months')
        mode = data.get('mode', 'Offline')
        topics = data.get('topics', 'Basics & Advanced')
        trainer = data.get('trainer', 'Faculty')

        if not title:
            return JsonResponse({"success": False, "message": "Course title is required!"}, status=400)

        course = Course.objects.create(
            title=title, duration=duration, mode=mode, topics=topics, trainer=trainer
        )
        new_course = {
            "id": course.id, "title": course.title, "duration": course.duration,
            "mode": course.mode, "topics": course.topics, "trainer": course.trainer
        }
        return JsonResponse({"success": True, "method": "POST", "message": f"Course '{title}' added successfully!", "course": new_course}, status=201)

    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

@csrf_exempt
def course_detail_api(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({"success": False, "message": "Course not found!"}, status=404)

    if request.method == 'PUT':
        data = get_request_data(request)
        course.title = data.get('title', course.title)
        course.duration = data.get('duration', course.duration)
        course.mode = data.get('mode', course.mode)
        course.topics = data.get('topics', course.topics)
        course.trainer = data.get('trainer', course.trainer)
        course.save()

        updated = {
            "id": course.id, "title": course.title, "duration": course.duration,
            "mode": course.mode, "topics": course.topics, "trainer": course.trainer
        }
        return JsonResponse({"success": True, "method": "PUT", "message": f"Course '{course.title}' updated successfully!", "course": updated})

    elif request.method == 'DELETE':
        title = course.title
        course.delete()
        return JsonResponse({"success": True, "method": "DELETE", "message": f"Course ID {course_id} deleted successfully!"})

    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)


# ==============================================================================
# 2. TRAINERS ENDPOINTS
# ==============================================================================

@csrf_exempt
def trainers_api(request):
    if request.method == 'GET':
        trainers = list(Trainer.objects.values('id', 'name', 'role', 'experience', 'specialization'))
        return JsonResponse({"success": True, "method": "GET", "trainers": trainers})

    elif request.method == 'POST':
        data = get_request_data(request)
        name = data.get('name')
        role = data.get('role', 'Instructor')
        experience = data.get('experience', '3+ years')
        specialization = data.get('specialization', 'FullStack')

        if not name:
            return JsonResponse({"success": False, "message": "Trainer name is required!"}, status=400)

        trainer = Trainer.objects.create(
            name=name, role=role, experience=experience, specialization=specialization
        )
        new_trainer = {
            "id": trainer.id, "name": trainer.name, "role": trainer.role,
            "experience": trainer.experience, "specialization": trainer.specialization
        }
        return JsonResponse({"success": True, "method": "POST", "message": f"Trainer '{name}' added successfully!", "trainer": new_trainer}, status=201)

    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

@csrf_exempt
def trainer_detail_api(request, trainer_id):
    try:
        trainer = Trainer.objects.get(id=trainer_id)
    except Trainer.DoesNotExist:
        return JsonResponse({"success": False, "message": "Trainer not found!"}, status=404)

    if request.method == 'PUT':
        data = get_request_data(request)
        trainer.name = data.get('name', trainer.name)
        trainer.role = data.get('role', trainer.role)
        trainer.experience = data.get('experience', trainer.experience)
        trainer.specialization = data.get('specialization', trainer.specialization)
        trainer.save()

        updated = {
            "id": trainer.id, "name": trainer.name, "role": trainer.role,
            "experience": trainer.experience, "specialization": trainer.specialization
        }
        return JsonResponse({"success": True, "method": "PUT", "message": f"Trainer '{trainer.name}' updated successfully!", "trainer": updated})

    elif request.method == 'DELETE':
        name = trainer.name
        trainer.delete()
        return JsonResponse({"success": True, "method": "DELETE", "message": f"Trainer '{name}' removed successfully!"})

    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)


# ==============================================================================
# 3. USER MANAGEMENT & AUTH ENDPOINTS
# ==============================================================================

@csrf_exempt
def users_api(request):
    if request.method == 'GET':
        users_qs = User.objects.all().values('id', 'name', 'email', 'course', 'dob', 'gender', 'created_at')
        users_list = []
        for u in users_qs:
            u['created_at'] = str(u['created_at']) if u['created_at'] else ''
            users_list.append(u)
        return JsonResponse({"success": True, "method": "GET", "users": users_list})

    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

@csrf_exempt
def api_register(request):
    if request.method != 'POST':
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    data = get_request_data(request)
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    course = data.get('course')
    dob = data.get('dob', '')
    gender = data.get('gender', 'Male')

    if not email or not password:
        return JsonResponse({"success": False, "message": "Email and password are required!"}, status=400)

    if User.objects.filter(email__iexact=email).exists():
        return JsonResponse({"success": False, "message": "Email already registered!"}, status=400)

    user_name = name or "Student"
    user_course = course or "Python FullStack"

    user = User.objects.create(
        name=user_name, email=email, password=password, course=user_course, dob=dob, gender=gender
    )

    return JsonResponse({
        "success": True,
        "method": "POST",
        "message": f"Registration successful for {user_name}!",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "course": user.course,
            "dob": user.dob,
            "gender": user.gender
        }
    }, status=201)

@csrf_exempt
def api_login(request):
    if request.method != 'POST':
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    data = get_request_data(request)
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return JsonResponse({"success": False, "message": "Email and password are required!"}, status=400)

    user = User.objects.filter(email__iexact=email).first()
    if not user:
        return JsonResponse({"success": False, "message": "User not found! Please register first."}, status=404)

    if user.password != password:
        return JsonResponse({"success": False, "message": "Invalid password!"}, status=401)

    is_admin = (user.email.lower() == 'admin@11')
    return JsonResponse({
        "success": True,
        "method": "POST",
        "message": f"Welcome back, {user.name}!",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "course": user.course,
            "dob": user.dob or '',
            "gender": user.gender or '',
            "role": "admin" if is_admin else "student"
        }
    })

@csrf_exempt
def user_detail_api(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "message": "User not found!"}, status=404)

    if request.method == 'PUT':
        data = get_request_data(request)
        user.name = data.get('name', user.name)
        user.course = data.get('course', user.course)
        user.password = data.get('password', user.password)
        user.dob = data.get('dob', user.dob)
        user.save()

        return JsonResponse({
            "success": True,
            "method": "PUT",
            "message": f"Profile updated for {user.name}!",
            "user": {"id": user.id, "name": user.name, "email": user.email, "course": user.course, "dob": user.dob}
        })

    elif request.method == 'DELETE':
        user_name = user.name
        user.delete()
        return JsonResponse({"success": True, "method": "DELETE", "message": f"User account for '{user_name}' deleted successfully!"})

    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)


# ==============================================================================
# 4. CONTACT & INQUIRIES ENDPOINTS
# ==============================================================================

@csrf_exempt
def contacts_api(request):
    if request.method == 'GET':
        contacts = list(Contact.objects.values('id', 'name', 'email', 'message', 'status'))
        return JsonResponse({"success": True, "method": "GET", "contacts": contacts})

    elif request.method == 'POST':
        data = get_request_data(request)
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        if not name or not email or not message:
            return JsonResponse({"success": False, "message": "Name, Email, and Message are required!"}, status=400)

        contact = Contact.objects.create(
            name=name, email=email, message=message, status='Pending'
        )
        new_contact = {
            "id": contact.id, "name": contact.name, "email": contact.email,
            "message": contact.message, "status": contact.status
        }
        return JsonResponse({"success": True, "method": "POST", "message": "Inquiry submitted successfully!", "contact": new_contact}, status=201)

    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

@csrf_exempt
def contact_detail_api(request, contact_id):
    try:
        contact = Contact.objects.get(id=contact_id)
    except Contact.DoesNotExist:
        return JsonResponse({"success": False, "message": "Inquiry not found!"}, status=404)

    if request.method == 'PUT':
        data = get_request_data(request)
        contact.status = data.get('status', contact.status)
        contact.message = data.get('message', contact.message)
        contact.save()

        updated = {
            "id": contact.id, "name": contact.name, "email": contact.email,
            "message": contact.message, "status": contact.status
        }
        return JsonResponse({"success": True, "method": "PUT", "message": f"Inquiry ID {contact_id} updated!", "contact": updated})

    elif request.method == 'DELETE':
        contact.delete()
        return JsonResponse({"success": True, "method": "DELETE", "message": f"Inquiry ID {contact_id} deleted successfully!"})

    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)


# ==============================================================================
# 5. GENERAL SYSTEM STATS ENDPOINT
# ==============================================================================

def get_stats(request):
    students_cnt = User.objects.count()
    courses_cnt = Course.objects.count()
    trainers_cnt = Trainer.objects.count()
    inquiries_cnt = Contact.objects.count()

    return JsonResponse({
        "success": True,
        "method": "GET",
        "stats": {
            "students_enrolled": students_cnt,
            "courses_offered": courses_cnt,
            "expert_trainers": trainers_cnt,
            "active_inquiries": inquiries_cnt
        }
    })
