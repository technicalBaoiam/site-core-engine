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

    def validate_student_full_name(self, value):
        name_parts = value.split()
        
        # Check if there are at least two parts (first and last name)
        if len(name_parts) < 2:
            raise serializers.ValidationError("Full name must include at least a first name and a last name.")
        
        # ensure each part only contains alphabetic characters
        for part in name_parts:
            if not part.isalpha():
                raise serializers.ValidationError("Full name must only contain alphabetic characters.")
        
        return value

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

