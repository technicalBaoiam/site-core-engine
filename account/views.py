from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer


# Create your views here.

class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        print('printing get object')
        return self.request.user.profile
