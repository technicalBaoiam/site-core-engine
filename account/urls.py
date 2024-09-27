from django.urls import path, include
from .views import EmailVerificationView, VerifyEmailView, ProfileUpdateView

urlpatterns = [
  
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path("auth/", include("djoser.social.urls")),

    # email verification
    path('auth/send_verification/', EmailVerificationView.as_view(), name='send_verification'),
    path('auth/verify_email/<uid>/<token>/', VerifyEmailView.as_view(), name='verify_email'),
    
    path('profile/', ProfileUpdateView.as_view(), name='profile-update'),
    
]
