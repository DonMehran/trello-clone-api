from rest_framework import serializers

from house.models import HouseModel
from .models import TaskListModel, TaskModel, AttachmentModel


class TaskListSerializer(serializers.ModelSerializer):
    house = serializers.HyperlinkedRelatedField(queryset=HouseModel.objects.all(), many=False,
                                                view_name='housemodel-detail')
    created_by = serializers.HyperlinkedRelatedField(read_only=True, many=False,
                                                     view_name='profilemodel-detail')

    tasks = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='taskmodel-detail')

    class Meta:
        model = TaskListModel
        fields = ['url', 'id', 'title', 'description', 'status', 'created_at', 'created_by',
                  'house', 'tasks']

        read_only_fields = ['id', 'created_at', 'status']

    def validate_house(self, value):
        request = self.context.get('request')
        if request.user.profile.house != value:
            raise serializers.ValidationError('you cant make a task list for another house')
        return value

    def create(self, validated_data):
        user = self.context.get('request').user.profile
        validated_data['created_by'] = user
        return super(TaskListSerializer, self).create(validated_data)


class TaskSerializer(serializers.ModelSerializer):
    completed_by = serializers.HyperlinkedRelatedField(read_only=True, many=False,
                                                       view_name='profilemodel-detail')

    created_by = serializers.HyperlinkedRelatedField(read_only=True, many=False,
                                                     view_name='profilemodel-detail')

    task_list = serializers.HyperlinkedRelatedField(queryset=TaskListModel.objects.all(), many=False,
                                                    view_name='tasklistmodel-detail')
    attachments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='attachmentmodel-detail')

    class Meta:
        model = TaskModel
        fields = ['url', 'id', 'title', 'description', 'status', 'created_at', 'completed_on',
                  'created_by', 'completed_by', 'task_list', 'attachments']
        read_only_fields = ['id', 'created_at', 'created_by', 'completed_on', 'completed_by']

    def validate_task_list(self, value):
        request = self.context.get('request')
        if request.user.profile.house != value.house:
            raise serializers.ValidationError('Task list does not belong to this house')
        return value

    def create(self, validated_data):
        user = self.context.get('request').user.profile
        validated_data['created_by'] = user
        return super(TaskSerializer, self).create(validated_data)


class AttachmentSerializer(serializers.ModelSerializer):
    task = serializers.HyperlinkedRelatedField(queryset=TaskModel.objects.all(), many=False,
                                               view_name='taskmodel-detail')

    created_by = serializers.HyperlinkedRelatedField(read_only=True, many=False,
                                                     view_name='profilemodel-detail')

    class Meta:
        model = AttachmentModel
        fields = ['url', 'id', 'created_at', 'data', 'task', 'created_by']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user.profile
        return super(AttachmentSerializer, self).create(validated_data)

    def validate_task(self, value):
        user = self.context.get('request').user.profile
        print(user.house, value.task_list.house)
        if user.house != value.task_list.house:
            raise serializers.ValidationError('Task does not belong to the house you are part of')
        return value

