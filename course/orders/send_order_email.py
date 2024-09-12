from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

 
def send_order_confirmation_email(user, order):
        subject = 'Enrollment Successfully'
        message = render_to_string('order_confirmation.html', {
            'user': user,
            'order': order,
        })
        email = EmailMessage(
            subject,
            message,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email],
        )
        email.content_subtype = "html" 
        email.send()

def send_demo_session_email(user, order):
    subject = 'Your Demo Session is Confirmed'
    message = render_to_string('demo_session_email.html', {
        'user': user,
        'order': order,
    })
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
    email.content_subtype = 'html'  # Important for sending HTML email
    email.send(fail_silently=False)