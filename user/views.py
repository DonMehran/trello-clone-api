from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializers
from .permissions import IsOwnerOrGetAndPostOnly

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrGetAndPostOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializers