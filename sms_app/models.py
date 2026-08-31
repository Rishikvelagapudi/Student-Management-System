from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    course = models.CharField(max_length=255, null=True, blank=True)
    dob = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f"{self.name} ({self.email})"

class Course(models.Model):
    title = models.CharField(max_length=255)
    duration = models.CharField(max_length=100, null=True, blank=True)
    mode = models.CharField(max_length=100, null=True, blank=True)
    topics = models.TextField(null=True, blank=True)
    trainer = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'courses'

    def __str__(self):
        return self.title

class Trainer(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, null=True, blank=True)
    experience = models.CharField(max_length=100, null=True, blank=True)
    specialization = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'trainers'

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=50, default='Pending')

    class Meta:
        db_table = 'contacts'

    def __str__(self):
        return f"Inquiry from {self.name} - {self.status}"
