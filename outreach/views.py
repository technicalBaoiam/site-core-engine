from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Contact, StudentEnrollment
from .serializers import ContactSerializer, EnrollmentSerializer
from utils.send_email import send_enrollment_email  # Assume this is your email utility
from utils.google_sheets_data import save_enrollment_data, save_contact_info
from datetime import datetime

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
        
        # Save the enrollment instance
        enrollment = serializer.save()
        # google sgeets send data
        save_enrollment_data(enrollment)
        # Send email notification after successful enrollment creation
        self.send_enrollment_email(enrollment)

        # Custom response
        return Response({
            "message": "Enrollment successfully created.",
            "enrollment_id": enrollment.id
        }, status=status.HTTP_201_CREATED)

    def send_enrollment_email(self, enrollment):
        # Implement your email sending logic here
        email_context = {
            'student_name': enrollment.student_full_name,
            'course': enrollment.course,
            'email': enrollment.student_email,
            'phone': enrollment.student_phone,
            'enrollment_type': enrollment.enrollment_type,
            'enrollment_time': enrollment.enrollment_time,
            'current_year': datetime.now().year, 

        }
        # Call your utility function to send the email
        send_enrollment_email("Enrollment Confirmation", enrollment.student_email, "enrollment_sent.html", email_context)

        # Log or print confirmation
        print(f"Enrollment email sent to {enrollment.student_full_name} regarding course: {enrollment.course}.")
