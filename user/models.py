from django.db import models
from django.contrib.auth.models import User
from django.utils.deconstruct import deconstructible
import os
from house.models import HouseModel
# Create your models here.


@deconstructible
class GenerateProfileImagePath(object):
    def __init__(self):
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
    # each profile can only be in one house but each house can have many profile
    # so its a one to many -> one: house, many: profiles
    # the model that define this relationship will be the many side
    # to access all profile in a house -> house.members which is related_name
    house = models.ForeignKey('house.HouseModel', on_delete=models.SET_NULL, 
                              related_name='members', null=True, blank=True)

    def __str__(self):
        full_name = f'{self.user.username}\'s Profile | ' + \
        f'name: {self.user.first_name} {self.user.last_name}'
        return full_name
