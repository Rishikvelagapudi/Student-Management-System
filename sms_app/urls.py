from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve
from . import views

urlpatterns = [
    # Page routes (Login is default first page)
    path('', views.login_page, name='login_first'),
    path('login', views.login_page, name='login'),
    path('login.html', views.login_page),
    path('home', views.home, name='home'),
    path('home.html', views.home),
    path('index', views.home),
    path('index.html', views.home),
    path('students', views.students_page, name='students'),
    path('students.html', views.students_page),
    path('about', views.about, name='about'),
    path('about.html', views.about),
    path('courses', views.courses_page, name='courses'),
    path('courses.html', views.courses_page),
    path('trainers', views.trainers_page, name='trainers'),
    path('trainers.html', views.trainers_page),
    path('register', views.register_page, name='register'),
    path('register.html', views.register_page),
    path('login', views.login_page, name='login'),
    path('login.html', views.login_page),
    path('admin', views.admin_page, name='admin'),
    path('admin.html', views.admin_page),
    path('contact', views.contact_page, name='contact'),
    path('contact.html', views.contact_page),

    # REST API endpoints
    path('api/courses', views.courses_api),
    path('api/courses/<int:course_id>', views.course_detail_api),
    path('api/trainers', views.trainers_api),
    path('api/trainers/<int:trainer_id>', views.trainer_detail_api),
    path('api/users', views.users_api),
    path('api/students', views.users_api),
    path('api/users/<int:user_id>', views.user_detail_api),
    path('api/register', views.api_register),
    path('api/login', views.api_login),
    path('api/contacts', views.contacts_api),
    path('api/contacts/<int:contact_id>', views.contact_detail_api),
    path('api/stats', views.get_stats),

    # Static assets serving route
    re_path(r'^(?P<path>(css|js|image|images|audio|video|static)/.*)$', serve, {'document_root': settings.BASE_DIR / 'sms_app' / 'static'}),
]
