# outreach/urls.py

from django.urls import path, include
from .views import ContactCreateView, EnrollmentCreateView

urlpatterns = [
    path('contact/', ContactCreateView.as_view(), name='contact-create'),
    path('enrollment-query-save/', EnrollmentCreateView.as_view(), name='enrollment-query'),
]