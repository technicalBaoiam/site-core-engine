from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, permissions, status
from .models import Profile, User
from .serializers import ProfileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime


class EmailVerificationView(APIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    def post(self, request):
        print(request.user,'request user')
        return self.send_verification_email(request.user)

    def send_verification_email(self, user):
        # Generate the verification URL

        verification_url = self.get_verification_url(user)

        context = {
            'name': user.first_name,
            'verification_url': verification_url,
            'current_year': datetime.now().year,  
            }
        
        # Render the HTML template for the email
        html_message = render_to_string('account/activation_email.html', context)
        
        try:
            send_mail(
                'Email Verification',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                html_message=html_message 
            )
            return Response({"detail": "Verification email sent."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_verification_url(self, user):
        print(user.pk,'pk user')
        uid = urlsafe_base64_encode(force_bytes(user.pk))  # Keep it as is
        token = PasswordResetTokenGenerator().make_token(user)
        return f"{settings.DOMAIN}/verify-email/{uid}/{token}/"


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uid, token):
        try:
            # Decode the uid
            user_id = force_str(urlsafe_base64_decode(uid))
            print(user_id, 'user id verification')
            user = User.objects.get(id=user_id)
            print(user.email, 'user')
            if PasswordResetTokenGenerator().check_token(user, token):
                user.is_email_verified = True
                user.save()
                return Response({"detail": "Email verified successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            return Response({"detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        print('printing get object')
        return self.request.user.profile
