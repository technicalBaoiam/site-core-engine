from django.urls import path, include
from .views import EmailVerificationView, VerifyEmailView, ProfileUpdateView, CustomTokenCreateView, CustomUserCreateView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    
    # custom urls login/signup 
    path('auth/jwt/create/', CustomTokenCreateView.as_view(), name='custom_token_create'),
    path('auth/users/', CustomUserCreateView.as_view(), name = "custom_user_create"),

    # djoser and jwt urls
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # email verification
    path('auth/send_verification/', EmailVerificationView.as_view(), name='send_verification'),
    path('auth/verify_email/<uid>/<token>/', VerifyEmailView.as_view(), name='verify_email'),
    
    # profile
    path('profile/', ProfileUpdateView.as_view(), name='profile-update'),

    
]
