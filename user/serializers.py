from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import ProfileModel


class UserSerializers(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=False)
    profile = serializers.SerializerMethodField(method_name='get_profile_serializer_str')

    def get_profile_serializer_str(self, obj):
        profile_serializer = ShowProfileInsideUser(obj.profilemodel, context={'request': self.context['request']})
        return profile_serializer.data

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'first_name', 
                  'last_name', 'password', 'old_password', 'profile']

        extra_kwargs = {
            'password': {'write_only': True}, 'username': {'read_only': True}
        }

    def __init__(self, *args, **kwargs):
        super(UserSerializers, self).__init__(*args, **kwargs)
        self.fields['password'].style = {'input_type': 'password'}
        self.fields['old_password'].style = {'input_type': 'password'}
        if self.instance:
            self.fields['password'].required = False
    
    def update(self, instance, validated_data):
        password, old_password, changed = None, None,  None
        if 'password' in validated_data:
            password = validated_data.pop('password')

        if 'old_password' in validated_data:
            old_password = validated_data.pop('old_password')
        
        if password:
            if instance.check_password(old_password):
                instance.password = password
            else:
                raise serializers.ValidationError('old password is incorrect')
        
        elif old_password and not password:
            raise serializers.ValidationError('new password is not provided')

        for attr, value in validated_data.items():
            if value != '':
                changed = True
                setattr(instance, attr, value)
        # return super(UserSerializers, self).update(instance, validated_data)

        if changed:
            instance.save()
        return instance

    def validate(self, data):
        if 'password' in data:
            data['password'] = make_password(data['password'])
        return data
        

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)
    # this is the way to access of field of a related model
    house_name = serializers.CharField(source='house.name', read_only=True)
    house_url = serializers.HyperlinkedIdentityField(read_only=True, many=False, view_name='housemodel-detail')
    class Meta:
        model = ProfileModel
        fields = ['url', 'id', 'image', 'user', 'house_name', 'house_url']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user']['user_url'] = rep['user'].pop('url')
        rep['user']['user_id'] = rep['user'].pop('id')
        rep['user'].pop('profile')
        return rep

class ShowProfileInsideUser(serializers.ModelSerializer):
    # user_url = serializers.HyperlinkedIdentityField(read_only=True, many=False, view_name='user-detail')
    profile_url = serializers.HyperlinkedIdentityField(read_only=True, many=False, view_name='profilemodel-detail')

    profile_id = serializers.IntegerField(source='id')
    class Meta:
        model = ProfileModel
        fields = ['profile_url', 'profile_id', 'image']


# UserSerializers._declared_fields['profile_serializer_str'] = ProfileSerializer(read_only=True)