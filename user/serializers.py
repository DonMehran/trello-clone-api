from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'first_name', 
                  'last_name', 'password',]

        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'read_only': True}
        }
    
    def validate(self, data):
        data['password'] = make_password(data['password'])
        return data
        
    