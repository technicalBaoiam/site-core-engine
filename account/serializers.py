from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from account.models import User, Profile

class UserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields=('id', 'email', 'first_name', 'last_name')


class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.ReadOnlyField(source='user.email')  
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    is_email_verified = serializers.ReadOnlyField(source="user.is_email_verified")

    class Meta:
        model = Profile
        fields = ['email', 'first_name', 'last_name', 'is_email_verified', 'mobile_number', 'instagram', 'github', 'linkedin', 'school_name', 'college_name']
