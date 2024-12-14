from course.models import Course
from django.conf import settings 


 # may be move to .env or settings.py
ALLOWED_DOMAIN = [
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://baoiam-undertesting.vercel.app/",
    'https://baoiam.com',
    'https://www.baoiam.com',
]

def get_videos_course(course_id):
    course =  Course.objects.get(id=course_id)
    playlists = course.playlists.all()
    
    videos = []
    for playlist in playlists:
        videos.extend(playlist.videos.all())
    
    return videos

def generate_referral_link(referral_code):
    # domain = getattr(settings, 'DOMAIN', ['http://127.0.0.1:8000'])[0]  # import from settings.py or .env
    domain = ALLOWED_DOMAIN[0]
    base_url = f"{domain}/api/auth/users/"
    referral_link = f'{base_url}?referral_code={referral_code}'
    return referral_link

def share_certificate_link(certificate_id):
    # domain = getattr(settings, 'DOMAIN', ['http://127.0.0.1:8000'])[0]  # import from settings.py or .env
    domain = ALLOWED_DOMAIN[0]
    generate_link = f"{domain}/api/certificate/{certificate_id}"
    return generate_link