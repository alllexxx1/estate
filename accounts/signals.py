from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from .models import Profile


@receiver(post_save, sender=Profile)
def log_profile_created(sender: Signal, instance: Profile, **kwargs) -> None:
    instance.user.username = instance.user.username.upper()
    instance.user.save()
    print(f'Created Profile for user {instance.user.username}')
