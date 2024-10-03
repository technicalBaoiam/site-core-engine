# outreach/models.py

from django.db import models
from django.utils import timezone
from course.models import Course 

class Contact(models.Model):

    CONTACT_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('agency', 'Agency'),
        ('institution', 'Institution'),
        ('organisation', 'Organisation')
    ]
    
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    institute = models.CharField(max_length=200, verbose_name="Institute")
    designation = models.CharField(max_length=100, blank=True, verbose_name="Designation (if agency)")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=15, blank=True, verbose_name="Phone")
    contact_type = models.CharField(max_length=50, choices=CONTACT_TYPE_CHOICES, verbose_name="Type")
    message = models.TextField(blank=True, verbose_name="Message")
    timestamp = models.DateTimeField(auto_now_add=True)  


    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.institute}"


class StudentEnrollment(models.Model):
    STUDENT_TYPE_CHOICES = [
        ('unspecified', 'Unspecified'),
        ('demo', 'Demo'),
        ('full', 'Full Course'),
    ]
    
    student_full_name = models.CharField(max_length=100)
    student_email = models.EmailField(max_length=254)
    student_phone = models.CharField(max_length=15)
    course = models.CharField(max_length=100)
    enrollment_type = models.CharField(max_length=20, choices=STUDENT_TYPE_CHOICES, default='unspecified')
    enrollment_time = models.DateTimeField(auto_now_add=True)  


    def __str__(self):
        return f"{self.student_full_name} ({self.enrollment_type})"

