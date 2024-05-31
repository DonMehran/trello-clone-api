from rest_framework import serializers
from .models import HouseModel

class HouserSerializer(serializers.ModelSerializer):
    member_count = serializers.IntegerField(read_only=True)
    members = serializers.HyperlinkedRelatedField(read_only=True, many=True,
                                                  view_name='profilemodel-detail')
    manager = serializers.HyperlinkedRelatedField(read_only=True,
                                                  view_name='profilemodel-detail')
    class Meta:
        model = HouseModel
        fields = ['url', 'id', 'image', 'name', 'created_on',
                  'manager', 'desc', 'points', 'completed_tasks_count',
                  'not_completed_tasks_count', 'members', 'member_count']
        read_only_fields = ['id', 'created_on', 'points', 'completed_tasks_count',
                            'not_completed_tasks_count']

    # def create(self, validated_data):
    #     house = HouseModel.objects.create(**validated_data)
    #     return house