# outreach/urls.py

from django.urls import path, include
from .views import ContactCreateView, EnrollmentCreateView, ContactUsCreateView, NewsletterCreateAPIView

urlpatterns = [
    path('contact-gcep/', ContactCreateView.as_view(), name='contact-create'),
    path('enrollment-query-save/', EnrollmentCreateView.as_view(), name='enrollment-query'),
    path('contact-us/', ContactUsCreateView.as_view(), name='contact-us'),
    path('newsletter/', NewsletterCreateAPIView.as_view(), name='newsletter-create'),

]