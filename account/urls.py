from django.urls import path, include
from .views import ProfileUpdateView

urlpatterns = [
  
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path("auth/", include("djoser.social.urls")),
    path('profile/', ProfileUpdateView.as_view(), name='profile-update'),
    
]
