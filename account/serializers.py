from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from account.models import User, Profile
from utils.decrypt_password import decrypt_password


class UserCreateSerializer(UserCreateSerializer):
    password = serializers.CharField(write_only=True)
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields=('id', 'email', 'first_name', 'last_name', 'password')

    def validate_password(self, value):
        # decrypt the encrypted password before validating it
        try:
            print('validate')
            decrypted_password = decrypt_password(value)
            print('decrypting successful')
            print(decrypted_password)
            return decrypted_password
        except ValueError:
            raise serializers.ValidationError("Invalid password encryption.")    


class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.ReadOnlyField(source='user.email')  
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    is_email_verified = serializers.ReadOnlyField(source="user.is_email_verified")

    class Meta:
        model = Profile
        fields = ['email', 'first_name', 'last_name', 'is_email_verified', 'mobile_number', 'instagram', 'github', 'linkedin', 'school_name', 'college_name']
