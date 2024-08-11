from rest_framework import routers
from .views import TaskListViewSet, TaskViewsSet, AttachmentViewSet


app_name = 'task'
router = routers.DefaultRouter()
router.register('tasklists', TaskListViewSet)
router.register('tasks', TaskViewsSet)
router.register('attachment', AttachmentViewSet)