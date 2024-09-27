from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_enrollment_email(subject, recipient_email, template_name, context):
    """
    Utility function to send an email with HTML and plain text fallback.

    :param subject: Subject of the email
    :param recipient_email: Recipient's email address
    :param template_name: The HTML template for the email body
    :param context: Context data to pass into the template
    """
    try:
        # Render the email template with context
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)  

        # Send the email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_message,  
            fail_silently=False,
        )
    except Exception as e:
        # Log or handle exceptions
        print(f"Error sending email: {str(e)}")
