from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import TaskModel, AttachmentModel, TaskListModel, TASK_STATUS


@receiver(post_save, sender=TaskModel)
def update_house_points(sender, instance, **kwargs):
    house = instance.task_list.house
    if instance.status == 'C':
        house.points += 10
    elif instance.status == 'IP':
        if house.points >= 10:
            house.points -= 10
        else:
            house.points = 0

    house.save()


@receiver(post_save, sender=TaskModel)
def update_task_list(sender, instance, **kwargs):
    task_list = instance.task_list
    is_complete = True
    for task in task_list.tasks.all():
        if task.status != 'C':
            is_complete = False
            break

    task_list.status = 'C' if is_complete else 'IP'
    task_list.save()

