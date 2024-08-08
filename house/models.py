from django.db import models
import os
import uuid
from django.utils.deconstruct import deconstructible


@deconstructible
class GenerateHouseImagePath(object):
    
    def __init__(self):
        pass
    
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        path = f'media/house/{instance.id}/images'
        name = f'main.{ext}'
        return os.path.join(path, name)

house_image_path = GenerateHouseImagePath()


class HouseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    image = models.FileField(upload_to=house_image_path, blank=True, null=True)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True, blank=True, null=True)
    desc = models.TextField()
    # related name will give access to the profile model like this [user.]profile.house_manager
    manager = models.OneToOneField('user.profilemodel', on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name='house_manager')
    points = models.IntegerField(default=0)
    completed_tasks_count = models.IntegerField(default=0)
    not_completed_tasks_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} | {self.id}'
    
    class Meta:
        ordering = ['-created_on']