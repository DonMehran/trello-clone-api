from django.utils import timezone
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

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

    def get_view_name(self):
        return "Tasks_List List"


class TaskViewsSet(viewsets.ModelViewSet):
    permission_classes = [IsAllowedToEditTaskElseNone]
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = super(TaskViewsSet, self).get_queryset()
        user = self.request.user.profile
        return queryset.filter(task_list__house=user.house)

    def get_object(self):
        # Attempt to retrieve the object without filtering by house
        try:
            obj = TaskModel.objects.get(pk=self.kwargs['pk'])
        except TaskModel.DoesNotExist:
            raise NotFound(detail="No TaskListModel matches the given query.")

        # Check if the user has permission to access the object
        self.check_object_permissions(self.request, obj)

        return obj

    def get_view_name(self):
        return "Tasks List"

    @action(detail=True, methods=['patch'])
    def update_task_status(self, request, pk=None):
        try:
            task = self.get_object()
            profile = request.user.profile
            status = request.data.get('status', None)
            if status == 'IP':
                if task.status == 'C':
                    task.status = 'IP'
                    task.completed_by = None
                    task.completed_on = None
                else:
                    raise Exception('Task is already not completed.')
            elif status == 'C':
                if task.status == 'IP':
                    task.status = 'C'
                    task.completed_by = profile
                    task.completed_on = timezone.now()
                else:
                    raise Exception('Task is already completed.')
            else:
                raise Exception('Invalid status value.')
            task.save()
            serializer = TaskSerializer(instance=task, context={'request': request})
            return Response(serializer.data, status=HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)


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

    def get_object(self):
        # Attempt to retrieve the object without filtering by house
        try:
            obj = AttachmentModel.objects.get(pk=self.kwargs['pk'])
        except AttachmentModel.DoesNotExist:
            raise NotFound(detail="No TaskListModel matches the given query.")

        # Check if the user has permission to access the object
        self.check_object_permissions(self.request, obj)

        return obj
