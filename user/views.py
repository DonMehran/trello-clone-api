from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializers, ProfileSerializer
from .permissions import IsOwnerOrGetAndPostOnly, IsProfileOwnerOrReadOnly
from rest_framework.response import Response
from .models import ProfileModel
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrGetAndPostOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializers

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     print(serializer.validated_data, 'view')
    #     serializer.update(instance, serializer.validated_data)
    #     return Response(serializer.data)

class ProfileViewSet(RetrieveModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsProfileOwnerOrReadOnly]
    queryset = ProfileModel.objects.all()
    serializer_class = ProfileSerializer