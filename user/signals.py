from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import ProfileModel

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(user=instance)

@receiver(pre_save, sender=User)
def set_user(sender, instance, **kwargs):
    if not instance.username:
        username = f'{instance.first_name}_{instance.last_name}'
        counter = 1
        while User.objects.filter(username=username):
            username = f'{instance.first_name}_{instance.last_name}_{counter}'.lower()
            counter += 1
        instance.username = username
