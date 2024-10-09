from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Contact, StudentEnrollment
from .serializers import ContactSerializer, EnrollmentSerializer, ContactUsSerializer, NewsletterSerializer
from utils.send_email import send_enrollment_email 
from utils.google_sheets_data import save_enrollment_data, save_contact_info, save_contact_us_info
from datetime import datetime
from django.utils import timezone

class ContactCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = serializer.save()
        save_contact_info(contact)
        return Response({"message": "Submitted successfully"}, status=status.HTTP_201_CREATED)

class EnrollmentCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = StudentEnrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        enrollment = serializer.save()
        save_enrollment_data(enrollment)
        self.send_enrollment_email(enrollment)

        # Custom response
        return Response({
            "message": "Enrollment successfully created.",
            "enrollment_id": enrollment.id
        }, status=status.HTTP_201_CREATED)

    def send_enrollment_email(self, enrollment):
        email_context = {
            'student_name': enrollment.student_full_name,
            'course': enrollment.course,
            'email': enrollment.student_email,
            'phone': enrollment.student_phone,
            'enrollment_time': enrollment.enrollment_time,
            'current_year': datetime.now().year, 

        }
        send_enrollment_email("Enrollment Confirmation", enrollment.student_email, "enrollment_sent.html", email_context)

        print(f"Enrollment email sent to {enrollment.student_full_name} regarding course: {enrollment.course}.")

class ContactUsCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ContactUsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            contact_data = serializer.validated_data  
            contact_data['timestamp'] = timezone.now() 
            save_contact_us_info(contact_data)
            return Response({"message": "Contact form submitted successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsletterCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = NewsletterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        newsletter_data = serializer.validated_data 
        newsletter_data['timestamp'] = timezone.now() 
        save_contact_us_info(newsletter_data) 
        return Response(serializer.data, status=status.HTTP_201_CREATED)