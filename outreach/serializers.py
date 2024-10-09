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

class ContactUsSerializer(serializers.Serializer):

    full_name = serializers.CharField(max_length=200, required=True)
    email = serializers.EmailField(required=True)  
    phone = serializers.CharField(max_length=10, required=True) 
    enquiry_type = serializers.ChoiceField(
        choices=[
            ('general', 'General'),
            ('feedback', 'Feedback'),
            ('support', 'Support')
        ],
        required=True  
    )
    message = serializers.CharField(required=True) 
    # newsletter_subscribed = serializers.BooleanField(required=False,default=False)


    def validate_full_name(self, value):
        # split the full_name to extract first and last names
        names = value.split()
        # Ensure both first name and last name are present
        if len(names) < 2:
            raise serializers.ValidationError("Please provide both first name and last name.")
        
        first_name, last_name = names[0], names[1]
        
        # ensure first name and last name are at least 3 characters long
        if len(first_name) < 3 or len(last_name) < 3:
            raise serializers.ValidationError("First name and last name must be at least 3 characters long.")

        # ensure names do not contain digits
        for part in names:
            if not part.isalpha():
                raise serializers.ValidationError("Full name must only contain alphabetic characters.")
        
        return value

    def validate_phone(self, value):
        if value and (len(value) != 10 or not value.isdigit()):
            raise serializers.ValidationError("Phone number must be exactly 10 digits.")
        return value

class NewsletterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    newsletter = serializers.BooleanField(default=True)  
