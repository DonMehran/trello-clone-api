from django.db import models
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
import os
# Create your models here.


@deconstructible
class GenerateProfileImagePath(object):
    def __ini__(self):
        pass

    def __call__(self, instance, filename: str):
        ext = filename.split('.')[-1]
        path = f'media/account/{instance.user.id}/images/'
        name = f'profile_image.{ext}'
        return path + name

user_profile_image_path = GenerateProfileImagePath()

class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to=user_profile_image_path, blank=True, null=True)
