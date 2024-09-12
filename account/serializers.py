from djoser.serializers import UserCreateSerializer
from account.models import User

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields=('id', 'email', 'first_name', 'last_name', 'is_active', 'is_admin')