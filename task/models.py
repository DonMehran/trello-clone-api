import os

from django.db import models

import uuid

from django.utils.deconstruct import deconstructible

TASK_STATUS = (
    ('IP', 'In Progress'),
    ('C', 'Completed'),
)


@deconstructible
class GenerateTaskImagePath(object):
    def __init__(self):
        pass

    def __call__(self, instance, filename: str):
        ext = filename.split('.')[-1]
        path = f'media/tasks/{instance.task.id}/attachments/'
        name = f'{instance.id}.{ext}'
        # return path + name
        return os.path.join(path, name)


task_image_path = GenerateTaskImagePath()


class TaskListModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_on = models.DateTimeField(null=True, blank=True)
    house = models.ForeignKey('house.HouseModel', on_delete=models.CASCADE, related_name='lists')
    created_by = models.ForeignKey(
        "user.ProfileModel", related_name="list_created_by", null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=TASK_STATUS, default='IP')

    def __str__(self):
        return f'{self.id} | {self.title}'

    class Meta:
        verbose_name = "Task List"


class TaskModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_on = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        "user.ProfileModel", related_name="created_by", null=True, blank=True, on_delete=models.SET_NULL)
    completed_by = models.ForeignKey(
        "user.ProfileModel", related_name="completed_by", null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=TASK_STATUS, default='IP')
    task_list = models.ForeignKey(TaskListModel, related_name='tasks', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} | {self.title}'

    class Meta:
        verbose_name = "Task"


class AttachmentModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.FileField(upload_to=task_image_path)
    task = models.ForeignKey(TaskModel, related_name='attachments', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} | {self.task}'

    class Meta:
        verbose_name = "Attachment"
