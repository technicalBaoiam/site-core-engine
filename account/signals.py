from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    
    if created:
        print('signal emitted')
        try:
            Profile.objects.create(user=instance)
        except Exception as e:
            print(f"Error creating profile: {e}")