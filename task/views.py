from rest_framework import viewsets, mixins
from rest_framework.exceptions import PermissionDenied, NotFound

from .models import TaskListModel, TaskModel, AttachmentModel
from .permissions import IsAllowedToEditTaskListElseNone, IsAllowedToEditTaskElseNone, IsAllowedToEditAttachmentElseNone
from .serializers import TaskListSerializer, TaskSerializer, AttachmentSerializer


class TaskListViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = [IsAllowedToEditTaskListElseNone]
    queryset = TaskListModel.objects.all()
    serializer_class = TaskListSerializer

    def get_queryset(self):
        queryset = super(TaskListViewSet, self).get_queryset()
        user_profile = self.request.user.profile
        return queryset.filter(house=user_profile.house)

    def get_object(self):
        # Attempt to retrieve the object without filtering by house
        try:
            obj = TaskListModel.objects.get(pk=self.kwargs['pk'])
        except TaskListModel.DoesNotExist:
            raise NotFound(detail="No TaskListModel matches the given query.")

        # Check if the user has permission to access the object
        self.check_object_permissions(self.request, obj)

        return obj


class TaskViewsSet(viewsets.ModelViewSet):
    permission_classes = [IsAllowedToEditTaskElseNone]
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = super(TaskViewsSet, self).get_queryset()
        user = self.request.user.profile
        return queryset.filter(task_list__house=user.house)


class AttachmentViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = [IsAllowedToEditAttachmentElseNone]
    queryset = AttachmentModel.objects.all()
    serializer_class = AttachmentSerializer

    def get_queryset(self):
        queryset = super(AttachmentViewSet, self).get_queryset()
        user = self.request.user.profile
        return queryset.filter(created_by=user)
