# outreach/serializers.py

from rest_framework import serializers
from .models import Contact

from rest_framework import serializers
from outreach.models import StudentEnrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for enrollments."""

    class Meta:
        model = StudentEnrollment
        fields = '__all__'
        # fields = ['id', 'student_full_name', 'email', 'phone_number', 'course', 'enrollment_type', 'enrollment_time']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

